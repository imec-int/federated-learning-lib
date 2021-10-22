import os 



def get_hyperparams():
    local_params = {
        'training': {
            'epochs': 1
        }
    }
    
    return local_params

def get_model_config(folder_configs, dataset, is_agg=False, party_id=0):

    if is_agg:
        return None

    if dataset == 'mnist':
        return get_mnist_model_config(folder_configs)

    elif dataset == 'cifar10':
        return get_cifar10_model_config(folder_configs)

    elif dataset == 'femnist':
        return get_femnist_model_config(folder_configs)

    elif dataset == 'custom_dataset':
        print('Using the same model as with MNIST, provide model file to replace if needed.')
        return get_mnist_model_config(folder_configs)
    else:
        raise Exception(
            "The dataset {} is a wrong combination for fusion/model".format(dataset))


def get_mnist_model_config(folder_configs):

    if not os.path.exists(folder_configs):
        os.makedirs(folder_configs)

    # Save model
    fname = os.path.join(folder_configs, 'compiled_keras.h5')

    K.clear_session()
    # Generate model spec:
    spec = {
        'model_name': 'HelloWorld',
        'model_definition': fname
    }

    model = {
        'name': 'HelloWorld',
        'path': 'examples.PHR.HelloWorld',
        'spec': spec
    }

    return model


def get_cifar10_model_config(folder_configs):

    num_classes = 10
    img_rows, img_cols = 32, 32
    if K.image_data_format() == 'channels_first':
        input_shape = (3, img_rows, img_cols)
    else:
        input_shape = (img_rows, img_cols, 3)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy'])
    if not os.path.exists(folder_configs):
        os.makedirs(folder_configs)

    # Save model
    fname = os.path.join(folder_configs, 'compiled_cifar10_keras.h5')
    model.save(fname)

    K.clear_session()
    # Generate model spec:
    spec = {
        'model_name': 'keras-cnn-cifar10',
        'model_definition': fname
    }

    model = {
        'name': 'KerasFLModel',
        'path': 'ibmfl.model.keras_fl_model',
        'spec': spec
    }

    return model

def get_femnist_model_config(folder_configs):

    num_classes = 62
    img_rows, img_cols = 28, 28
    if K.image_data_format() == 'channels_first':
        input_shape = (1, img_rows, img_cols)
    else:
        input_shape = (img_rows, img_cols, 1)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(5, 5),
                     activation='relu', padding='same',
                     input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=2))

    model.add(Conv2D(64, (5, 5), activation='relu', padding='same',))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=2))
    model.add(Flatten())
    model.add(Dense(2048, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.SGD(),
                  metrics=['accuracy'])
    if not os.path.exists(folder_configs):
        os.makedirs(folder_configs)

    # Save model
    fname = os.path.join(folder_configs, 'compiled_femnist_keras.h5')
    model.save(fname)

    K.clear_session()
    # Generate model spec:
    spec = {
        'model_name': 'keras-cnn',
        'model_definition': fname
    }

    model = {
        'name': 'KerasFLModel',
        'path': 'ibmfl.model.keras_fl_model',
        'spec': spec
    }

    return model
