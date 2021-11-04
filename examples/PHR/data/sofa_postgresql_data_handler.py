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

    def get_data(self):
        """
        Executes query to fetch training data (party side).

        :return: the training and testing data.
        :rtype: `tuple`
        """
        conn = self.connect()
        
        cur = conn.cursor()

        sql = """SELECT gender, substring(hospitaladmittime24, 0, 3) AS admissionHour, count(*)
FROM eicu_crd.patient
GROUP BY gender, substring(hospitaladmittime24, 0, 3)"""
        cur.execute(sql)
        data = [{'sourceDatabase': self.database, 'gender': gender, 'admissionHour': int(admissionHour), 'count': int(count)}
            for (gender, admissionHour, count) in cur.fetchall()]

        #cur.execute('SELECT gender, COUNT(*) FROM eicu_crd.patient GROUP BY gender')
        #data = {self.database: {gender: nb for (gender, nb) in cur.fetchall()}}
        
        conn.close()

        return data, None

    def save_data(self,statement:str,rows):
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
