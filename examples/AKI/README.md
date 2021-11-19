# AKI model

In this temp folder we'll write the functions to extract the AKI parameters and then train the model. This is not yet implemented in a federated way from start

## origin

We'll be basing ourselves on prior research, performed by imec ExaScience. They created an ML model for an Aki-predictor, based on the MIMIC-III database.

[Exascience Aki-predictor](https://github.com/ExaScience/Aki-Predictor/)

The AKI predictor should predict the Stage in which a person finds him/herselves towards Acute Kidney Injury.

## approach

We'll be using the eICU database, which is a larger dataset. 

First step is to have the necessary data captured from the entire eICU dB, train a model and compare it with the results gathered from the MIMIC-III approach. (the central approach)

Then we'll see for using the same approach, yet have the different hospitals in the eICU dB spread out over multiple storage locations. Thus, we'll have to use a federated approach in order to train the model and hopefully get similar results. (the federated approach)

## the Central approach

### Query the eICU dB

Save the responses in a dataframe.

### preprocessing of data

1. cleaning
2. converting to one unit per category whenever possible
3. scaling

### create the model

### divide the resulted dataframe

in a training and testing set

### train the model

Do we need to make use of the GPU enabled clusters of IDLab?

### evaluate the model

fingers crossed

## the federated approach

the same but spread?
