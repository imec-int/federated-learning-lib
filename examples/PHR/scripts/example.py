from lib.ibmfl.model.model_update import ModelUpdate
from phr.party.training.scriptapi import ScriptApi

class ExampleScript:

    def __init__(self,api:ScriptApi) -> None:
        self.api = api

    def run(self):
        cur = self.api.get_postgresql_connection().cursor()
        cur.execute('SELECT gender, COUNT(*) FROM eicu_crd.patient GROUP BY gender')
        dict = {gender: nb for (gender, nb) in cur.fetchall()}
        return ModelUpdate(**{'hospital1':dict}) #TODO get hospital from environment somehow (via ScriptApi)

if __name__ == '__main__':
    api = ScriptApi()
    s = ExampleScript(api)
    dict = s.run()
    print(dict)
    api.close_postgresql_connection()