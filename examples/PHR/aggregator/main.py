import logging
import os
import re
import sys

from dotenv import load_dotenv
from ibmfl.aggregator.aggregator import Aggregator
from ibmfl.aggregator.states import States

load_dotenv()

rabbit_mq_connection = {
    "info": {
        'credentials': {
            "broker_host": os.getenv('RABBITMQ_HOST', '0.0.0.0'),
            "broker_vhost": "/",
            "broker_port": os.getenv('RABBITMQ_PORT', 5672),
        },
        'user': 'guest',
        'password': 'guest',
        'role': 'aggregator',
        "task_name": 'sample',
        "tls_config": {
            "enable": False,
        }
    },
    "name": "RabbitMQConnection",
    "path": "ibmfl.connection.rabbitmq_connection",
    "sync": True,
}

flask_connection = {
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
}

config_dict = {
    "connection": flask_connection,
    "fusion": {
        "name": "ConcatFusionHandler",
        "path": os.getenv('FUSION_HANDLER_PATH',
                          "examples.PHR.aggregator.fusion." + os.environ['CASE'] + "_concat_fusion_handler"),
        "info": {
            "database": {
                "host": os.getenv('DB_HOST', "central-dbs.postgres.database.azure.com"),
                "port": os.getenv('DB_PORT', "5432"),
                "database": os.getenv('DB_DATABASE_NAME', "postgres"),
                "user": os.getenv('DB_USER', "postgres"),
                "password": os.getenv('DB_PASSWORD', "postgres"),
                'sslmode': os.getenv('DB_SSL_MODE', 'require')
            }
        }

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
