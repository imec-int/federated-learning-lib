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

        """
        Starts an iterative global federated learning training process.
        """
        # self.curr_round = 0

        # # log to Evidentia
        # if self.evidencia:
        #     self.evidencia.add_claim("sent_global_model",
        #                             "{}, '\"{}\"'".format(self.curr_round + 1,
        #                             hash_model_update(model_update)))

        payload = {'hyperparams': {'local': self.params_local},
                   'test': "test-message"
                   }
        #     logger.info('Model update' + str(model_update))

        # query all available parties
        lst_replies = self.query_all_parties(payload)
        logging.info(lst_replies)
        # # log to Evidentia
        # if self.evidencia:
        #     updates_hashes = []
        #     for update in lst_replies:
        #         updates_hashes.append(hash_model_update(update))
        #         self.evidencia.add_claim("received_model_update_hashes",
        #                                 "{}, '{}'".format(self.curr_round + 1,
        #                                 str(updates_hashes).replace('\'', '"')))

        # self.update_weights(lst_replies)

        # # Update model if we are maintaining one
        # if self.fl_model is not None:
        #     self.fl_model.update_model(
        #         ModelUpdate(weights=self.current_model_weights))

        # self.curr_round += 1
        # self.save_current_state()

    def get_global_model(self):
        logging.info("I don't want a model, I just need a friend")


if __name__ == '__main__':
    """
    Main function can be used to create an application out
    of our Party class which could be interactive
    """
    logging.info('hello cold cold world')
