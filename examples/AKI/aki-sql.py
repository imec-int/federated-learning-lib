import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import dotenv
from sql_requests import *
'''
In this file we'll create all hooks to extract the necessary AKI model parameters from the connected database
'''
load_dotenv()


class PostgreSqlDataHandler():
    """
    Data handler for PostgreSQL database access.
    """

    def __init__(self, data_config=None, channels_first=False):
        super().__init__()

        self.host = data_config['host']
        self.port = data_config['port']
        self.database = data_config['database']
        self.envPath = data_config['envPath']

    def get_data(self, sql_request):
        """
        Executes query to fetch training data (party side).

        :return: the training and testing data.
        :rtype: `tuple`
        """
        cur = self.open_connection()

        cur.execute(sql_request)
        data = cur.fetchall()
        self.close_connection()
        return data

    def open_connection(self):
        conn = self.connect()
        cur = conn.cursor()
        # construct an engine connection string
        engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
            user=dotenv.get_key(self.envPath, "DB_USER"),
            password=dotenv.get_key(self.envPath, "DB_PASSWORD"),
            host=self.host,
            port=self.port,
            database=self.database,
        )

        # create sqlalchemy engine
        engine = create_engine(engine_string)#, echo=True)
        return cur, engine

    def close_connection(self):
        self.conn.close()

    def connect(self):
        dbUser = dotenv.get_key(self.envPath, "DB_USER")
        dbPw = dotenv.get_key(self.envPath, "DB_PASSWORD")

        return psycopg2.connect(host=self.host, port=self.port, database=self.database,
                                user=dbUser, password=dbPw,
                                sslmode='require')


    def test_postgres(self):
        cursor, engine = self.open_connection()
        cursor.execute("""
    SELECT
        *
    FROM
    pg_catalog.pg_tables
    WHERE
    schemaname != 'pg_catalog'
    AND schemaname != 'information_schema';
        """)

        tables = cursor.fetchall()

        print("List of tables:")
        for table in tables:
            print(table)

        # read a table from database into pandas dataframe
        for table in tables:
            tn = table[1]
            print("Table {}".format(tn))

            df = pd.read_sql_table(tn, con=engine, schema = "eicu_crd")

            print("Head of extracted pandas DF:")
            print(df.head())


if __name__ == "__main__":
    data_config = {
        "host": "edit-ph-eicu.postgres.database.azure.com",
        "port": 5432,
        "database": "hospital1",
        "envPath": "./examples/PHR/party/.env"
    }
    psql = PostgreSqlDataHandler(data_config=data_config)

    # psql.test_postgres()
    cur, engine = psql.open_connection()
    urine_output(cur)
    # kidigo_stages(cur)

