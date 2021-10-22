"""
Licensed Materials - Property of IBM
Restricted Materials of IBM
20190891
© Copyright IBM Corp. 2021 All Rights Reserved.
"""
import logging

from ibmfl.exceptions import LocalTrainingException, \
    ModelUpdateException
from ibmfl.evidencia.util.hashing import hash_np_array, \
    hash_model_update
import numpy as np

logger = logging.getLogger(__name__)


class LocalTrainingHandler():

    def __init__(self, fl_model, data_handler, hyperparams=None, evidencia=None, **kwargs):
        """
        Initialize LocalTrainingHandler with fl_model, data_handler

        :param fl_model: model to be trained
        :type fl_model: `model.FLModel`
        :param data_handler: data handler that will be used to obtain data
        :type data_handler: `DataHandler`
        :param hyperparams: Hyperparameters used for training.
        :type hyperparams: `dict`
        :param evidencia: evidencia to use
        :type evidencia: `evidencia.EvidenceRecorder`
        :param kwargs: Additional arguments to initialize a local training \
        handler, e.g., a crypto library object to help with encryption and \
        decryption.
        :type kwargs: `dict`
        :return None
        """
        self.fl_model = fl_model
        self.data_handler = data_handler
        self.hyperparams = hyperparams
        self.evidencia = evidencia

        self.metrics_recorder = None
        self.n_completed_trains = 0
        self.n_completed_evals = 0

    def train(self, fit_params=None):
        """
        Train function is "wrongly" used to execute a script 

        :param fit_params: (optional) Query instruction from aggregator
        :type fit_params: `dict`
        :return: ModelUpdate
        :rtype: `ModelUpdate`
        """

        if self.evidencia:
            self.evidencia.add_claim("executing script", "helloworld")
        self.fl_model.execute()
        update = self.fl_model.fetch_results()
        

        if self.evidencia:
            self.evidencia.add_claim("sentresults", "results")

        return update
