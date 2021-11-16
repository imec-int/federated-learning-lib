from dotenv import load_dotenv
import dotenv
import psycopg2
import logging

import numpy as np
import pandas as pd

import multiprocessing as mp
from multiprocessing.pool import ThreadPool

from ibmfl.data.data_handler import DataHandler
from ibmfl.util.datasets import load_mnist

logger = logging.getLogger(__name__)

# TODO place at entry point of application
load_dotenv()

def get_value_or_0(rows, patientId):
    for (patId, value) in rows:
        if patId == patientId:
            return value
    return 0

class PostgreSqlDataHandler(DataHandler):
    """
    Data handler for PostgreSQL database access.
    """

    def __init__(self, data_config=None, channels_first=False):
        super().__init__()

        self.host = data_config['host']
        self.port = data_config['port']
        self.database = data_config['database']
        self.envPath = data_config['envPath']

    def get_respiratory_scores(self, cur):
        '''
        Function calculating the respiratory components of SOFA scores.
        Returns: array of tuples like (patientId, sofaScore)
        PaO2/FiO2 [mmHg (kPa)] 	SOFA score
        ≥ 400 (53.3) ->	0
        < 400 (53.3) ->	+1
        < 300 (40) 	 -> +2
        < 200 (26.7) and mechanically ventilated ->	+3
        < 100 (13.3) and mechanically ventilated ->	+4 
        #TODO is formula correct?
        #TODO do we need mechanically ventilated?
        '''
        def to_sofa(ratio):
            if ratio < 100: return 4
            if ratio < 200: return 3
            if ratio < 300: return 2
            if ratio < 400: return 1
            return 0

        sql = """SELECT patientunitstayid, pao2 / (fio2/100) as ratio
                 FROM eicu_crd.apacheapsvar
                 WHERE pao2 > 0 AND fio2 > 0;"""
        cur.execute(sql)
        return [(patientId, to_sofa(ratio)) for (patientId, ratio) in cur.fetchall()]

    def get_nervous_system_scores(self, cur):
        '''
        Function calculating the nervous system components of SOFA scores.
        Returns: array of tuples like (patientId, sofaScore)
        '''
        sql = """SELECT patientunitstayid, eyes + verbal + motor as gcs
            FROM eicu_crd.apacheapsvar
            WHERE eyes > 0 AND verbal > 0 AND motor > 0;
            """    
        cur.execute(sql)
        def to_sofa(gcs):
            if gcs < 6: return 4
            if gcs < 10: return 3
            if gcs < 13: return 2
            if gcs < 15: return 1
            return 0
        return [(patientId, to_sofa(gcs)) for (patientId, gcs) in cur.fetchall()]

    def get_cardiovascular_system_scores(self, conn):
        '''
        Function calculating the cardiovascular system components of SOFA scores.
        Returns: array of tuples like (patientId, sofaScore)
        '''

        pool = ThreadPool(mp.cpu_count())

        mapSql = """SELECT patientunitstayid, MIN((systemicsystolic + 2 * systemicdiastolic)/3) AS map
                    FROM eicu_crd.vitalperiodic
                    WHERE systemicsystolic BETWEEN 50 AND 250
                      AND systemicdiastolic BETWEEN 25 AND 225
                    GROUP BY patientunitstayid
                    ORDER BY patientunitstayid"""
        mapResults = pool.apply_async(self.run_query, args=(conn, mapSql))

        def drug_query(drugname:str, conv_factor:str, max_rate:str):
            """Function to produce a drug query.
            conv_factor is the factor to multiply the drugrate with to get to µg/kg/min.
            max_rate is the outlier cutoff in the unit of the rows.
            The queries return two columns: patientunitstayid and (converted) drugrate"""
            return """SELECT patientunitstayid, MAX(drugrate::FLOAT * """+conv_factor+""") AS drugrate
                      FROM eicu_crd.infusiondrug
                      WHERE drugrate ~ E'^[\\\\d\\\\.]+$'
                        AND drugname = '"""+drugname+"""'
                        AND drugrate::FLOAT < """+max_rate+"""
                      GROUP BY patientunitstayid
                      ORDER BY patientunitstayid"""

        dopamineResults = [
            pool.apply_async(self.run_query, args=(conn, drug_query('Dopamine (mcg/kg/min)', '1', '100'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Dopamine (ml/hr)', '0.140', '500'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Dopamine ()', '0.105', '500'))),
        ]

        dobutamineResults = [
            pool.apply_async(self.run_query, args=(conn, drug_query('Dobutamine (mcg/kg/min)', '1', '100'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Dobutamine (ml/hr)', '0.066', '1000'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Dobutamine ()', '0.054', '1000'))),
        ]
        
        epinephrineResults = [
            pool.apply_async(self.run_query, args=(conn, drug_query('Epinephrine (mcg/kg/min)', '1', '10'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Epinephrine (ml/hr)', '0.00448', '500'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Epinephrine (mcg/min)', '0.03809', '75'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Epinephrine ()', '0.00291', '600'))),
        ]
        
        norepinephrineResults = [
            pool.apply_async(self.run_query, args=(conn, drug_query('Norepinephrine (mcg/kg/min)', '1', '2'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Norepinephrine (ml/hr)', '0.0037', '600'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Norepinephrine (mcg/min)', '0.018626', '150'))),
            pool.apply_async(self.run_query, args=(conn, drug_query('Norepinephrine ()', '0.002218', '700'))),
        ]

        def merge_drug_results(results):
            merged = []
            for rows in [result.get() for result in results]:
                for row in rows:
                    (patId, rate) = row
                    found = False
                    for idx, (patId2, rate2) in enumerate(merged):
                        if patId2 == patId:
                            found = True
                            if rate > rate2:
                                merged[idx] = row
                            break
                    if not found:
                        merged.append(row)
            return merged

        mapRows = mapResults.get()
        dopamineRows = merge_drug_results(dopamineResults)
        dobutamineRows = merge_drug_results(dobutamineResults)
        epinephrineRows = merge_drug_results(epinephrineResults)
        norepinephrineRows = merge_drug_results(norepinephrineResults)

        pool.close()

        def calculate_sofa_score(mapr, dopamineRate, dobutamineRate, epinephrineRate, norepinephrineRate):
            if dopamineRate > 15 or epinephrineRate > 0.1 or norepinephrineRate > 0.1:
                return 4
            if dopamineRate > 5 or epinephrineRate > 0 or norepinephrineRate > 0:
                return 3
            if dopamineRate > 0 or dobutamineRate > 0:
                return 2
            if mapr < 70:
                return 1
            return 0

        allPatientIds = [patId for (patId, _) in mapRows]
        for drugRows in [dopamineRows, dobutamineRows, epinephrineRows, norepinephrineRows]:
            for (patId, _) in drugRows:
                if not patId in allPatientIds:
                    allPatientIds.append(patId)

        print("nb map's: " + str(len(mapRows)))
        print("nb dopamines: " + str(len(dopamineRows)))
        print("nb dobutamines: " + str(len(dobutamineRows)))
        print("nb ephinephrines: " + str(len(epinephrineRows)))
        print("nb norepinephrines: " + str(len(norepinephrineRows)))
        print("nb patients: " + str(len(allPatientIds)))

        return [(patId, calculate_sofa_score(
                get_value_or_0(mapRows, patId),
                get_value_or_0(dopamineRows, patId),
                get_value_or_0(dobutamineRows, patId),
                get_value_or_0(epinephrineRows, patId),
                get_value_or_0(norepinephrineRows, patId),
            )) for patId in allPatientIds]

    def get_liver_scores(self, cur):
        '''
        Function calculating the liver components of SOFA scores.
        Returns: array of tuples like (patientId, sofaScore)
        '''
        def to_sofa(concentration):
            if concentration > 12: return 4
            if concentration > 6: return 3
            if concentration > 2: return 2
            if concentration > 1.2: return 1
            return 0
        sql = """SELECT patientunitstayid, MAX(bilirubin)
                 FROM eicu_crd.apacheapsvar
                 WHERE bilirubin > 0
                 GROUP BY patientunitstayid;"""
        cur.execute(sql)
        return [(patientId, to_sofa(bilirubin)) for (patientId, bilirubin) in cur.fetchall()]

    def get_coagulation_scores(self, cur):
        '''
        Function calculating the coagulation components of SOFA scores.
        Returns: array of tuples like (patientId, sofaScore)
        '''
        def to_sofa(count):
            if count < 20: return 4
            if count < 50: return 3
            if count < 100: return 2
            if count < 150: return 1
            return 0
        sql = """SELECT patientunitstayid, MIN(labresult)
                 FROM eicu_crd.lab
                 WHERE labname = 'platelet x 1000'
                   AND labresult > 0
                 GROUP BY patientunitstayid;"""
        cur.execute(sql)
        return [(patientId, to_sofa(count)) for (patientId, count) in cur.fetchall()]

    def get_kidneys_scores(self, cur):
        '''
        Function calculating the kidney components of SOFA scores.
        Returns: array of tuples like (patientId, sofaScore)
        '''
        def to_sofa(count):
            if count > 5: return 4
            if count > 3.5: return 3
            if count > 2: return 2
            if count > 1.2: return 1
            return 0
        sql = """SELECT patientunitstayid, MAX(creatinine)
                 FROM eicu_crd.apacheapsvar
                 WHERE creatinine > 0
                 GROUP BY patientunitstayid;"""
        cur.execute(sql)
        return [(patientId, to_sofa(count)) for (patientId, count) in cur.fetchall()]

    def calc_patient_scores(self, *args):
        '''
        Merges the component scores in args (assumed to be arrays of tuples like (patientId, score)). Scores missing
        from components for patients are assumed 0: parameters indicating higher values would probably have
        been measured for clinical purposes, so missing parameters and thus missing scores usually mean nothing extraordinary
        is reported and thus 0 is a good assumed value.
        Returns the average and standard deviation. 
        '''
        allPatientIds = []
        for componentscores in args:
            for (patId, _) in componentscores:
                if not patId in allPatientIds:
                    allPatientIds.append(patId)

        patientScores = []
        for patId in allPatientIds:
            patScore = 0
            for componentscores in args:
                patScore += get_value_or_0(componentscores, patId)
            patientScores.append(patScore)

        return patientScores

    def get_data(self):
        """
        Executes query and calculates the sofa score based on it.

        :return: A list with one dict like {'sourceDatabase': '...', 'sofaAvg': ..., 'sofaStd': ...} (train data) and None (test data).
        """
        conn = self.connect()

        cur = conn.cursor()

        # TODO are we allowed (depends on dB) to query in parallel?
        resp_scores = self.get_respiratory_scores(cur)
        ns_scores = self.get_nervous_system_scores(cur)
        cs_scores = self.get_cardiovascular_system_scores(conn)
        liver_scores = self.get_liver_scores(cur)
        coag_scores = self.get_coagulation_scores(cur)
        kidney_scores = self.get_kidneys_scores(cur)

        conn.close()

        patientScores = self.calc_patient_scores(resp_scores, ns_scores, cs_scores, liver_scores, coag_scores, kidney_scores)
        
        #np.savetxt("patient_scores.csv", patientScores, delimiter=",")

        return [{'sourceDatabase': self.database,
                 'sofaAvg': np.average(patientScores),
                 'sofaStd': np.std(patientScores)}], None

    def save_data(self, statement: str, rows):
        """Inserts the given rows (tuples) of data with the given INSERT statement.

        This is usually not the job of a DataHandler, but it already has all the setup for database connections and is passed to the
        FusionHander for other uses, so it was easier this way. Used aggregator side.
        """
        conn = self.connect()

        cur = conn.cursor()
        cur.executemany(statement, rows)
        conn.commit()

        conn.close()

    def connect(self):
        dbUser = dotenv.get_key(self.envPath, "DB_USER")
        dbPw = dotenv.get_key(self.envPath, "DB_PASSWORD")

        return psycopg2.connect(host=self.host, port=self.port, database=self.database,
                                user=dbUser, password=dbPw,
                                sslmode='require')
    
    def run_query(self,conn,sql:str):
        print("\nrunning query:        " + sql)
        with conn.cursor() as cur:
            cur.execute(sql)
            tuples = cur.fetchall()
            return tuples