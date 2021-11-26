from dotenv import load_dotenv
import os
import re
import sys

from ibmfl.party.status_type import StatusType
from ibmfl.party.party import Party

load_dotenv()

config_dict = {
    "aggregator": {
        "ip": os.getenv('AGGREGATOR_ADDR', '127.0.0.1'),
        "port": os.getenv('AGGREGATOR_PORT', 5000), 
    },
    "connection": {
        "info": {
            "ip": os.getenv('PARTY_ADDR', '0.0.0.0'),
            "port": os.getenv('PARTY_PORT', 8085),
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
            "host": "edit-ph-eicu.postgres.database.azure.com",
            "port": "5432",
            "database": "hospital_" + os.environ['HOSP_ID'],
        },
        "name": "PostgreSqlDataHandler",
        "path": "examples.PHR.data."+os.environ['CASE']+"_postgresql_data_handler",
    },
    "local_training": {
        "name": "LocalTrainingHandler",
        "path": "examples.PHR.party.training.local_training_handler",
    },
    "model": {
        "name": "NoopFLModel",
        "path": "examples.PHR.model.noop_fl_model",
        "spec": {
            "model_name": "NoopFLModel",
        },
    },
    "privacy": {
        "metrics": True,
    },
    "protocol_handler": {
        "name": "PartyProtocolHandler",
        "path": "ibmfl.party.party_protocol_handler",
    },
}

if __name__ == '__main__':
    """Entry point for the application. Configuration is done using environment variables (.env file is automatically loaded):
    - AGGREGATOR_ADDR: The address of the aggregator to register with, default 127.0.0.1 .
    - AGGREGATOR_PORT: The port to connect to the aggregator, default 5000 .
    - PARTY_ADDR:      The address to bind on/listen to, default 0.0.0.0 .
    - PARTY_PORT:      The port to bind on/listen to, default 8085 .
    - HOSP_ID:         The id of the hospital to simulate, required.
    - CASE:            The case to simulate, e.g. "sofa", required.
    - DB_USER:         The username to connect to the database with, required.
    - DB_PASSWORD:     The password to connect to the database with, required.
    """
    
    p = Party(config_dict=config_dict)

    p.start()
    p.register_party()

    # Indefinite loop to accept user commands to execute
    while 1:
        msg = sys.stdin.readline()

        if re.match('STOP', msg):
            p.connection.stop()
            break

        if re.match('EVAL', msg):
            p.evaluate_model()

        if re.match('SAVE', msg):
            commands = msg.split(" ")
            filename = commands[1] if len(commands) > 1 else None
            p.save_model(filename)

        if p.proto_handler.status == StatusType.STOPPING:
            p.stop()
            break
    exit()
