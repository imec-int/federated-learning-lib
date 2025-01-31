"""
Licensed Materials - Property of IBM
Restricted Materials of IBM
20190891
© Copyright IBM Corp. 2021 All Rights Reserved.
"""
"""
Module to where fusion algorithms are implemented.
"""
import logging
import numpy as np

from ibmfl.aggregator.fusion.iter_avg_fusion_handler import \
    IterAvgFusionHandler
from ibmfl.exceptions import HyperparamsException

logger = logging.getLogger(__name__)


class GradientFusionHandler(IterAvgFusionHandler):
    """
    Class for gradient based aggregation and aggregated gradient descent
    """

    def __init__(self, hyperparams,
                 protocol_handler,
                 data_handler=None,
                 fl_model=None,
                 **kwargs):
        """
        Initializes an GradientFusionHandler object with provided information,
        such as protocol handler, fl_model, data_handler and hyperparams.

        :param hyperparams: Hyperparameters used for training.
        :type hyperparams: `dict`
        :param protocol_handler: Protocol handler used for handling learning \
        algorithm's request for communication.
        :type protocol_handler: `ProtoHandler`
        :param data_handler: data handler that will be used to obtain data
        :type data_handler: `DataHandler`
        :param fl_model: model to be trained
        :type fl_model: `model.FLModel`
        :param kwargs: Additional arguments to initialize a fusion handler.
        :type kwargs: `Dict`
        :return: None
        """
        super().__init__(hyperparams,
                         protocol_handler,
                         data_handler,
                         fl_model,
                         **kwargs)
        self.name = "Gradient-Avg-SGD"

        self.lr = self.params_global.get('lr') or 0.1

        if not self.current_model_weights and hyperparams.get(
                'initial_weights'):
            self.current_model_weights = hyperparams.get('initial_weights')
        elif not self.current_model_weights:
            raise HyperparamsException('Initial weights must be provided if '
                                       'no model is provided for aggregator!')

    def update_weights(self, lst_model_updates):
        """
        Update the global model's weights with the list of collected
        model_updates from parties.
        In this method, it calls self.fusion_collected_responses to average
        the gradients collected from parties, and performs a one-step
        gradient descent with learning rate as self.lr.

        :param lst_model_updates: List of model updates of type `ModelUpdate` \
        to be averaged.
        :type lst_model_updates: `lst`
        :return: None
        """
        agg_gradient = self.fusion_collected_responses(lst_model_updates,
                                                       key='gradients')
        new_weights = np.array(self.current_model_weights) - \
            self.lr*np.array(agg_gradient)
        self.current_model_weights = new_weights.tolist()
