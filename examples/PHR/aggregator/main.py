import logging
import os
import re
import sys

from dotenv import load_dotenv
from ibmfl.aggregator.aggregator import Aggregator
from ibmfl.aggregator.states import States

load_dotenv()

config_dict = {
    "connection": {
        "info": {
            "ip": os.getenv('AGGREGATOR_ADDR', '0.0.0.0'),
            "port": os.getenv('AGGREGATOR_PORT', 5000),
            "tls_config": {
                "enable": False,
            }
        },
        "name": "FlaskConnection",
        "path": "ibmfl.connection.flask_connection",
        "sync": False,
    },
    "data": {
        "info": {
            "host": "central-dbs.postgres.database.azure.com",
            "port": "5432",
            "database": "aggregator"
        },
        "name": "PostgreSqlDataHandler",
        "path": "examples.PHR.data."+os.environ['CASE']+"_postgresql_data_handler",
    },
    "fusion": {
        "name": "ConcatFusionHandler",
        "path": "examples.PHR.aggregator.fusion."+os.environ['CASE']+"_concat_fusion_handler",
    },
    "hyperparams": {
        "global": {
            "num_parties": 2,
            "rounds": 1,
        },
        "local": {
            "training": {
                "epochs": 1,
            },
        },
    },
    "protocol_handler": {
        "name": "ProtoHandler",
        "path": "ibmfl.aggregator.protohandler.proto_handler",
    },
}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)-6s %(name)s :: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    """Entry point for the application. Configuration is done using environment variables (.env file is automatically loaded):
    - AGGREGATOR_ADDR: The address to bind on/listen to, default 0.0.0.0 .
    - AGGREGATOR_PORT: The port to bind on/listen to, default 5000 .
    - CASE:            The case to simulate, e.g. "sofa", required.
    - DB_USER:         The username to connect to the database with, required.
    - DB_PASSWORD:     The password to connect to the database with, required.
    """
    
    agg = Aggregator(config_dict=config_dict)

    agg.start()

    # Indefinite loop to accept user commands to execute
    while 1:
        msg = sys.stdin.readline()
        # TODO: move it to Aggregator
        if re.match('STOP', msg):
            agg.proto_handler.state = States.STOP
            logging.info("State: " + str(agg.proto_handler.state))
            agg.stop()
            break

        elif re.match('TRAIN', msg):
            agg.proto_handler.state = States.TRAIN
            logging.info("State: " + str(agg.proto_handler.state))
            success = agg.start_training()
            if not success:
                agg.stop()
                break

        elif re.match('SAVE', msg):
            agg.proto_handler.state = States.SAVE
            logging.info("State: " + str(agg.proto_handler.state))
            agg.save_model()

        elif re.match('EVAL', msg):
            agg.proto_handler.state = States.EVAL
            logging.info("State: " + str(agg.proto_handler.state))
            agg.eval_model()

        elif re.match('SYNC', msg):
            agg.proto_handler.state = States.SYNC
            logging.info("State: " + str(agg.proto_handler.state))
            agg.model_synch()

    exit()
