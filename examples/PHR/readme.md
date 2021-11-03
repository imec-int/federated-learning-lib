# Setup

## General

Four VM's were created: one for the aggregator and three for the hospitals. They were put in the Azure resource group `phr-icufair` and communicate over the resource group's virtual network (using internal IP addresses). To setup:
 1. login via SSH: `ssh -i <path to private key file> azureuser@<public IP address>`
     - private keys can be found in 1Password: look for "icu" in the EDiT/Developers vault
     - public IP address can be found in the Azure Portal
 2. `git pull https://github.com/imec-int/federated-learning-lib`
 3. `cd federated-learning-lib`
 4. `. scripts/setup.sh` will install conda, the environment and all necessary python packages

There are also two database servers in play:
 - `edit-ph-eicu` with the databases `hospital1`, `hospital2` and `hospital3` each containing (a subset of) the eICU database. These are read by the hospital VM's when "training the model"
 - `central-dbs` with the database `aggregator` that is written to by the aggregator VM when "saving the model"

### aggregator

To complete the setup for the aggregator, one has to add the file `federated-learning-lib/examples/PHR/aggregator/.env` according to the template file at the same location. The database password can be found in 1Password (attention: choose the right database!). Notice the config file `federated-learning-lib/examples/configs/PHR/script/config_aggregator.yml` was already prepared and contains the private IP address of the `aggregator` VM as well as the settings for connection with the `central-dbs` database server.

To launch, simply run `. scripts/launch-aggregator.sh` from the repo root.

### hospitalN

To complete the setup for the aggregator, one has to add the file `federated-learning-lib/examples/PHR/party/.env` according to the template file at the same location. The database password can be found in 1Password (attention: choose the right database!). Notice the config files `federated-learning-lib/examples/configs/PHR/script/config_hospital*.yml` were already prepared and contain the private IP address of the `hospital*` VM as well as the settings for connection with the `edit-ph-eicu` database server.

To launch, simply run `. scripts/launch-hospitalN.sh X` with `X` being `1`, `2` or `3` from the repo root.