#!/bin/bash

# assumes running from repo root

conda activate ibm-federated-learning 

python -m ibmfl.aggregator.aggregator "examples/configs/PHR/script/config_aggregator.yml"