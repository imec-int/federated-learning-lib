import logging
import numpy as np

from ibmfl.model.model_update import ModelUpdate
from ibmfl.aggregator.fusion.fusion_handler import FusionHandler
from ibmfl.evidencia.util.hashing import hash_model_update

logger = logging.getLogger(__name__)


class JoinFusionHandler(FusionHandler):
    """
    A simple FusionHandler that collects data from the parties in a single dict.
    """

    def __init__(self, hyperparams,
                 protocol_handler,
                 data_handler=None,
                 fl_model=None,
                 **kwargs):
        super().__init__(hyperparams,
                         protocol_handler,
                         data_handler,
                         fl_model,
                         **kwargs)
        self.name = "Iterative-Weight-Average"
        self.params_global = hyperparams.get('global') or {}
        self.params_local = hyperparams.get('local') or None

        self.global_accuracy = -1
        self.termination_accuracy = self.params_global.get(
            'termination_accuracy')
        
        self.dict = {}

    def start_global_training(self):
        """
        Starts a single round global federated learning training process.
        """
        payload = {'hyperparams': {'local': self.params_local},
                    'model_update': None
                    }

        # query all available parties
        lst_replies = self.query_all_parties(payload)

        # log to Evidentia
        if self.evidencia:
            updates_hashes = []
            for update in lst_replies:
                updates_hashes.append(hash_model_update(update))
                self.evidencia.add_claim("received_model_update_hashes",
                                        "{}, '{}'".format(self.curr_round + 1,
                                        str(updates_hashes).replace('\'', '"')))
        
        for dict in lst_replies:
            for key, value in dict.items():
                self.dict[key] = value

    def get_global_model(self):
        """
        Returns last model_update

        :return: model_update
        :rtype: `ModelUpdate`
        """
        return ModelUpdate(**self.dict)

    def get_current_metrics(self):
        """Returns metrics pertaining to current state of fusion handler

        :return: metrics
        :rtype: `dict`
        """
        fh_metrics = {}
        fh_metrics['rounds'] = 1
        fh_metrics['curr_round'] = 0
        fh_metrics['acc'] = self.global_accuracy
        #fh_metrics['model_update'] = self.model_update
        return fh_metrics