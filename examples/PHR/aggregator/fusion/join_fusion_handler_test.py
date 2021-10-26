from ibmfl.model.model_update import ModelUpdate

from join_fusion_handler import JoinFusionHandler

class TestProtocolHandler:
    def get_registered_parties(self):
        return ['Bruges', 'Ghent', 'Antwerp', 'Leuven', 'Hasselt']

    def query_parties(self, payload, lst_parties, perc_quorum=1.,
                      msg_type=None,
                      collect_metrics=False, metrics_party={},
                      fusion_state=None, return_responding_parties=False):
        return [ModelUpdate(**{p: {'foo': 'bar'}}) for p in self.get_registered_parties()]


jfh = JoinFusionHandler({}, TestProtocolHandler(), None, None)

jfh.start_global_training()

print(jfh.get_global_model())
