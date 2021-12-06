import logging

import psycopg2
from ibmfl.aggregator.fusion.fusion_handler import FusionHandler
from ibmfl.evidencia.util.hashing import hash_model_update
from ibmfl.model.model_update import ModelUpdate

logger = logging.getLogger(__name__)


class ConcatFusionHandler(FusionHandler):
    """
    A simple FusionHandler that collects data from the parties in a single list.
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
        if "info" not in kwargs:
            raise NameError("Missing database config")

        self.database_config = kwargs['info']['database']

        self.name = "ConcatFusionHandler"
        self.params_global = hyperparams.get('global') or {}
        self.params_local = hyperparams.get('local') or None

        self.global_accuracy = -1
        self.termination_accuracy = self.params_global.get(
            'termination_accuracy')

        self.data_handler = data_handler

        self.list = []

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

        for list in lst_replies:
            self.list.extend(list)

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
        # fh_metrics['model_update'] = self.model_update
        return fh_metrics

    def save_parties_models(self):
        """Will save the aggregated results instead (triggered by the SAVE command)."""
        rows = []
        for dict in self.list:
            rows.append((
                dict['sourceDatabase'],
                dict['sofaAvg'],
                dict['sofaStd']
            ))

        if not rows:
            logger.warning("Trying to save an empty list of party data")
            return

        conn = psycopg2.connect(host=self.database_config['host'],
                                port=self.database_config['port'],
                                database=self.database_config['database'],
                                user=self.database_config['user'],
                                password=self.database_config['password'],
                                sslmode=self.database_config['sslmode'])

        logger.info('Connecting')
        try:
            with conn:
                with conn.cursor() as curs:
                    curs.executemany("INSERT INTO results.sofaScores(sourceDatabase, sofaAvg, sofaStd) VALUES(%s,%s,%s)", rows)
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()
