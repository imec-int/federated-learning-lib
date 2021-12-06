#!/bin/bash

# assumes running from repo root

#conda activate ibm-federated-learning

# python -m ibmfl.aggregator.aggregator "examples/configs/PHR/script/config_aggregator.yml"

# arguments to add:
# 1) scripts to execute: gender, sofa or fl

case "$1" in
    "gender")
        echo starting gender setup
        python -m ibmfl.aggregator.aggregator "examples/configs/PHR/script/gender_config_aggregator.yml"
        exit 1;;
    "sofa")
        echo starting sofa setup
        python -m ibmfl.aggregator.aggregator "examples/PHR/configs/sofa_config_aggregator.yml"
        exit 1;;
    "fl")
        echo starting federated learning setup
        python -m ibmfl.aggregator.aggregator "examples/configs/PHR/script/fl_config_aggregator.yml"
        exit 1;;
    "")
        echo not enough arguments
        exit 1;;
esac
