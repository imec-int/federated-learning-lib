# PHR - ICU use cases

## Local development
### Setup

IMPORTANT: Execute all these commands in the root directory of the project:

1. Install conda, if not already installed: `curl https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh -o install_conda.sh && bash install_conda.sh -b`
2. `conda env create -f examples/PHR/environment.yml -n ibm-federated-learning-phr`
3. `conda activate ibm-federated-learning-phr`

Alternatively, when using Windows, you can run these tasks with `./scripts/setup.sh`. 

TIP: if you update the `environment.yml` file, you update the conda environment with `conda env update -f examples/PHR/environment.yml`

### Start the aggregator

We will be using docker-compose to initialize any 3rd party local infrastructure.

    docker-compose up 

will start a postgres database on port 5432.

Next, we have to configure the aggregator.
Copy `examples/PHR/aggregator/.env.template` file to `examples/PHR/aggregator/.env` and update its values.

In a terminal, start the aggregator:

    $ python -m examples.PHR.aggregator.main

### Start the parties

In another terminal, run

     $ ./scripts/launch-hospitalN.sh 1234 sofa #replace 1234 with ID of the party

or use the command

    $ python -m ibmfl.party.party "examples/PHR/configs/sofa_config_hospital73.yml"


Notice that the config file, specified in the last argument, needs to be present for this to work.
    
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

To launch, simply run `. scripts/launch-aggregator.sh` from the repo root with a startup option: `gender` or `sofa` or `fl`.

### hospitalN

To complete the setup for the aggregator, one has to add the file `federated-learning-lib/examples/PHR/party/.env` according to the template file at the same location. The database password can be found in 1Password (attention: choose the right database!). Notice the config files `federated-learning-lib/examples/configs/PHR/script/config_hospital*.yml` were already prepared and contain the private IP address of the `hospital*` VM as well as the settings for connection with the `edit-ph-eicu` database server.

To launch, simply run `. scripts/launch-hospitalN.sh X Y` with `X` being `1`, `2` or `3` from the repo root and Y the startup option: `gender` or `sofa` or `fl`.

### commands

|command|where to execute|function|
|---|---|---|
|START|all|launch inits from script, read config files|
|REGISTER|parties| registers the specific party at the aggregator, so it's a known participator|
|TRAIN|aggregator| repurposed FL TRAIN command to run the query on the parties and gather the results|
|SAVE|aggregator|inject the query results in the application dB|
