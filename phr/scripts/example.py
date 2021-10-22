from phr.party.training.scriptapi.scriptapi.py import ScriptApi

class ExampleScript:

    def __init__(self,api:ScriptApi) -> None:
        self.api = api

    def run(self) -> Any:
        cur = self.api.get_postgresql_connection().cursor()
        cur.execute('SELECT gender, COUNT(*) FROM eicu_crd.patient GROUP BY gender')
        return cur.fetchall()
        #TODO caller must close the connection

if __name__ == '__main__':
    api = ScriptApi("hospital1")
    s = ExampleScript(api)
    rows = s.run()
    for row in rows:
        print(row[0]+":\t"+str(row[1]))
    api.close_postgresql_connection()