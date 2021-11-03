#!/bin/bash

# assumes running from repo root

conda activate ibm-federated-learning 

python -m ibmfl.party.party "examples/configs/PHR/script/config_hospital$1.yml"