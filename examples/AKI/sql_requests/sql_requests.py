from pathlib import Path
import pandas as pd


class sql_requests():
    def __init__(self, sqlpath, connection, cursor):
        self.sqlpath = sqlpath
        self.connection = connection
        self.cursor = cursor
        self.sql_request = {
            'weight_file': Path(self.sqlpath / 'weight.sql'),
            'uo_file': Path(self.sqlpath / 'urineoutput.sql'),
            'count_icu_stays': Path(self.sqlpath / 'counticustays.sql'),
        }

    def execute_sql(self, filename):
        '''
        we execute a query and directly place it in a pandas dataframe
        '''
        sql_file = open(filename)
        sql_as_string = sql_file.read()
        respons = pd.read_sql(sql_as_string, self.connection)
        # self.cursor.execute(sql_as_string)
        # respons = self.cursor.fetchall()
        return respons

    def count_icustays(self):
        return self.execute_sql(self.sql_request['count_icu_stays'])
