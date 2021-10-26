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

envPath = "./examples/PHR/.env"

class PostgreSqlDataHandler(DataHandler):
    """
    Data handler for PostgreSQL database access.
    """

    def __init__(self, data_config=None, channels_first=False):
        super().__init__()

        self.host = data_config['host']
        self.port = data_config['port']
        self.database = data_config['database']

    def get_data(self):
        """
        Gets pre-process mnist training and testing data.

        :return: the training and testing data.
        :rtype: `tuple`
        """
        dbUser = dotenv.get_key(envPath, "DB_USER")
        dbPw = dotenv.get_key(envPath, "DB_PASSWORD")

        conn = psycopg2.connect(host=self.host, port=self.port, database=self.database,
                                user=dbUser, password=dbPw,
                                sslmode='require')
        
        cur = conn.cursor()
        cur.execute('SELECT gender, COUNT(*) FROM eicu_crd.patient GROUP BY gender')
        dict = {self.database: {gender: nb for (gender, nb) in cur.fetchall()}}
        conn.close()

        return dict, None