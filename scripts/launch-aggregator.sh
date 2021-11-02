#!/bin/bash

cd federated-learning-lib

conda activate ibm-federated-learning 

python -m ibmfl.aggregator.aggregator examples/configs/PHR/script/config_agg.yml