#!/bin/bash

# assumes running from repo root

conda activate ibm-federated-learning 

# arguments to add: 
# 1) number of hospital
# 2) scripts to execute: gender, sofa or fl

case "$2" in 
    "gender")
        echo starting gender setup
        python -m ibmfl.party.party "examples/configs/PHR/script/gender_config_hospital$1.yml"
        exit 1;;
    "sofa")
        echo starting sofa setup
        python -m ibmfl.party.party "examples/configs/PHR/script/sofa_config_hospital$1.yml"
        exit 1;;
    "fl")
        echo starting federated learning setup
        python -m ibmfl.party.party "examples/configs/PHR/script/fl_config_hospital$1.yml"
        exit 1;;
    "") 
        echo not enough arguments
        exit 1;;
esac