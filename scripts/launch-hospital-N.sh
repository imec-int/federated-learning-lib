#!/bin/bash

cd federated-learning-lib

conda activate ibm-federated-learning 

python -m ibmfl.party.party examples/configs/PHR/script/config_hospitalN.yml