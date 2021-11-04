from dotenv import load_dotenv
import dotenv
import psycopg2
import logging

import numpy as np

from ibmfl.data.data_handler import DataHandler
from ibmfl.util.datasets import load_mnist

logger = logging.getLogger(__name__)

# TODO place at entry point of application
load_dotenv()


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

    def get_respiratory_data(self, cur):
        '''
        function querying the dB for respiratory entries (PaO2/FiO2).
        Returns: array of patient-ids & SOFA scores based on PaO2/FiO2
        '''
        sql = """SELECT patientunitstayid,
            pao2,
            fio2,
            pao2 / fio2 as ademhaling
            FROM eicu_crd.apacheapsvar;"""
        cur.execute(sql)
        data = [{'sourceDatabase': self.database, 'patientid': patient, 'ademhaling': ademhaling}
                for (patient, ademhaling) in cur.fetchall()]
        resp_data = data  # TODO calculate array of SOFA scores for respiratory entries
        return resp_data

    def get_nervous_system_data(self, cur):
        '''
        function querying the dB for nervous system entries (Glasgow Coma scale).
        Returns: array of patient-ids & SOFA scores based on Glasgow Coma scale
        '''
        sql = """SELECT patientunitstayid,
            eyes + verbal + motor as glasgow_coma_scale
            FROM eicu_crd.apacheapsvar;
            """
        cur.execute(sql)
        data = [{'sourceDatabase': self.database, 'patientid': patient, 'gcs': gcs}
                for (patient, gcs) in cur.fetchall()]
        ns_data = data  # TODO calculate array of SOFA scores for ns entries
        return ns_data

    def get_cardiovascular_system_data(self, cur):
        '''
        function querying the dB for cardiovascular system entries 
        Functioneren Hart/bloedsomloop: Gemiddelde bloeddruk (MAP) 
        needs: MAP, dopamine, dobutamin, epinephrine, norepinephrine
        MAP = (SBP + 2* DBP)/3 
        ==> SBP = pasystolic
        ==> DBP = padiastolic
        TODO: dopamine:  
        when lower(drugname) like '%(ml/hr)%' then round(cast(drugrate as numeric) / 3, 3) -- rate in ml/h * 1600 mcg/ml / 80 kg / 60 min, to convert in mcg/kg/min
        when lower(drugname) like '%(mcg/kg/min)%' then cast(drugrate as numeric)

        Returns: array of patient-ids & SOFA scores based on MAP and vasopressors
        '''
        sql = """SELECT v.patientunitstayid,
            (v.pasystolic + 2 * v.padiastolic) / 3 as MAP,
            i.drugname,
            i.drugrate
            FROM eicu_crd.vitalperiodic v
            FULL OUTER JOIN eicu_crd.infusiondrug i
            ON v.patientunitstayid = i.patientunitstayid
            WHERE lower(i.drugname) like '%dopamine%'
            or lower(i.drugname) like '%dobutamin%'
            or lower(i.drugname) like '%epinephrine%'
            or lower(i.drugname) like '%norepinephrine%'
            ORDER BY i.patientunitstayid;
            """
        cur.execute(sql)
        data = [{'sourceDatabase': self.database, 'patientid': patient, 'map': map, 'drug': drugname, 'drugrate': drugrate}
                for (patient, map, drugname, drugrate) in cur.fetchall()]
        vs_data = data  # TODO calculate array of SOFA scores for ns entries
        return vs_data

    def get_liver_data(self, cur):
        '''
        function querying the dB for liver entries (bilirubin).
        Returns: array of patient-ids & SOFA scores based on bilirubin
        '''
        sql = """SELECT patientunitstayid,
        bilirubin as liver
        FROM eicu_crd.apacheapsvar;
        """
        cur.execute(sql)
        data = [{'sourceDatabase': self.database, 'patientid': patient, 'liver': liver}
                for (patient, liver) in cur.fetchall()]
        liver_data = data  # TODO calculate array of SOFA scores for liver entries
        return liver_data

    def get_coagulation_data(self, cur):
        '''
        function querying the dB for Coagulation entries (platelets).
        Returns: array of patient-ids & SOFA scores based on platelets
        '''
        sql = """SELECT patientunitstayid,
        labname ,
        labresult / 1000
        FROM eicu_crd.lab
        WHERE labname like '%platelet%';
        """
        cur.execute(sql)
        data = [{'sourceDatabase': self.database, 'patientid': patient, 'labname': lab_name, 'labresult': lab_result}
                for (patient, lab_name, lab_result) in cur.fetchall()]
        # TODO calculate array of SOFA scores for coagulation entries, do we need/want labname?
        coagulation_data = data
        return coagulation_data

    def get_kidneys_data(self, cur):
        '''
        function querying the dB for kidney entries (creatinine).
        Returns: array of patient-ids & SOFA scores based on creatinine
        '''
        sql = """SELECT patientunitstayid,
            creatinine
            FROM eicu_crd.apacheapsvar;
        """
        cur.execute(sql)
        data = [{'sourceDatabase': self.database, 'patientid': patient, 'creatinine': creatinine}
                for (patient, creatinine) in cur.fetchall()]
        # TODO calculate array of SOFA scores for coagulation entries, do we need/want labname?
        kidney_data = data
        return kidney_data
    def calc_sofa(self, *args):
        '''
        in calc_sofa function we calculate the sofa score for each correspond patient id
        we return the mean, std_dev & length of the sofa score 
        '''
        #TODO
        print(args)

    def get_data(self):
        """
        Executes query and calculates the sofa score based on it.


        :return: the mean + stddev of the sofa score
        :rtype: `tuple`
        """
        conn = self.connect()

        cur = conn.cursor()
        # TODO are we allowed (depends on dB) to query in parallel?
        resp_data = self.get_respiratory_data(cur)
        ns_data = self.get_nervous_system_data(cur)
        cs_data = self.get_cardiovascular_system_data(cur)
        liver_data = self.get_liver_data(cur)
        coag_data = self.get_coagulation_data(cur)
        kidney_data = self.get_kidneys_data(cur)
        data = self.calc_sofa(resp_data, ns_data, cs_data, liver_data, coag_data, kidney_data)
        conn.close()

        return data, None

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
