# TODO maybe provide authentication mechanism (so the party can check access to data resources for the script)

from lib.ibmfl.model.model_update import ModelUpdate
from phr.party.training.scriptapi import ScriptApi


class EIcuMaleFemaleScript:

    def __init__(self,api:ScriptApi):
        self.api = api

    def run(self) -> ModelUpdate:
        cur = self.api.get_postgresql_connection().cursor()
        cur.execute('SELECT gender, COUNT(*) FROM eicu_crd.patient GROUP BY gender')
        return cur.fetchall()