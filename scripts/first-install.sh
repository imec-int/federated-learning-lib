#!/bin/bash

# Install conda
curl https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh -o install_conda.sh
bash install_conda.sh -b

echo "source ~/miniconda3/etc/profile.d/conda.sh" >> ~/.bash_profile
source /home/azureuser/.bash_profile

# Clone federated learning repository
git clone https://github.com/imec-int/federated-learning-lib.git

conda create -n ibm-federated-learning python=3.6 tensorflow=1.15 -y
conda activate ibm-federated-learning

pip install torch==1.4.0 --no-cache-dir # this avoids out of memory issue during install of this package
pip install http://github.com/IBM/pycloudmessenger/archive/v0.7.1.tar.gz # had to do this to avoid missing modules error
pip install psycopg2

cd federated-learning-lib
pip install federated-learning-lib/federated_learning_lib-1.0.6-py3-none-any.whl