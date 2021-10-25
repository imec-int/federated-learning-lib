import os
import numpy as np
from importlib import import_module

import examples.datahandlers as datahandlers


def get_fusion_config():
    fusion = {
        'name': 'summing',
        'path': 'examples.PHR.aggregator.fusion.summing'
    }
    return fusion


def get_local_training_config(configs_folder=None):
    local_training_handler = {
        'name': 'LocalTrainingHandler',
        'path': 'examples.PHR.party.training.local_training_handler'
    }
    return local_training_handler


def get_hyperparams(model):
    hyperparams = {
        'global': {
            'rounds': 1,
        }
    }
    current_module = globals().get('__package__')

    model_module = import_module('{}.model_{}'.format(current_module, model))
    local_params_method = getattr(model_module, 'get_hyperparams')

    local_params = local_params_method()
    hyperparams['local'] = local_params

    return hyperparams


def get_data_handler_config(party_id, dataset, folder_data, is_agg=False, model='keras'):
    # TODO ADDED 'script'
    SUPPORTED_DATASETS = ['mnist', 'adult', 'cifar10',
                          'femnist', 'custom_dataset', 'script']
    if dataset in SUPPORTED_DATASETS:
        #TODO added script for not having to alter the original datahandlers.get_datahandler_config file
        if model not in 'keras' and model not in 'script':
            dataset = dataset + "_" + model

        data = datahandlers.get_datahandler_config(
            dataset, folder_data, party_id, is_agg)
    else:
        raise Exception(
            "The dataset {} is a wrong combination for fusion/model".format(dataset))
    return data


def get_model_config(folder_configs, dataset, is_agg=False, party_id=0, model='script'):
    SUPPORTED_MODELS = ['keras', 'pytorch', 'tf', 'sklearn', 'script']

    if model not in SUPPORTED_MODELS:
        raise Exception(
            "Invalid model/script config for this fusion algorithm")

    current_module = globals().get('__package__')

    model_module = import_module('{}.model_{}'.format(current_module, model))
    method = getattr(model_module, 'get_model_config')

    return method(folder_configs, dataset, is_agg=is_agg, party_id=0)
