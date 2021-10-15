#!/usr/bin/env python3
import logging
from ibmfl.aggregator.fusion.fusion_handler import FusionHandler

logger = logging.getLogger(__name__)


class HelloWorld(FusionHandler):
    def __init__(self, hyperparams,
                 protocol_handler,
                 data_handler,):
        super().__init__(hyperparams,
                         protocol_handler,
                         data_handler)
        logging.info('initiation of a cold cold world')
        self.name = "helloworld script"
        self.params_global = hyperparams.get('global') or {}
        self.params_local = hyperparams.get('local') or None

        self.rounds = self.params_global.get('rounds') or 1
        self.curr_round = 0
        self.global_accuracy = -1
        self.termination_accuracy = self.params_global.get(
            'termination_accuracy')

    def execute_script(self):
        logging.info('hello cold cold world and mr. me')

    def start_global_training(self):
        self.execute_script()

    def get_global_model(self):
        logging.info("I don't want a model, I just need a friend")


if __name__ == '__main__':
    """
    Main function can be used to create an application out
    of our Party class which could be interactive
    """
    logging.info('hello cold cold world')
