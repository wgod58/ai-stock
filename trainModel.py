from keras import optimizers
from keras.layers import Activation, Conv2D, Dense, Flatten

# from keras.utils import np_utils
from keras.models import Sequential
from sklearn.metrics import confusion_matrix

# customized utilities
# from utils import util_processor as pro
from utils import util_process as pro

# import numpy as np


def get_model(params):
    model = Sequential()

    # Conv1
    model.add(
        Conv2D(16, (2, 2), input_shape=(10, 10, 4), padding="same", strides=(1, 1))
    )
    model.add(Activation("sigmoid"))

    # Conv2
    model.add(Conv2D(16, (2, 2), padding="same", strides=(1, 1)))
    model.add(Activation("sigmoid"))

    # FC
    model.add(Flatten())
    model.add(Dense(128, activation="relu"))

    model.add(Dense(params["classes"]))
    model.add(Activation("softmax"))
    model.summary()

    return model


def train_model(params, data):
    model = get_model(params)
    model.compile(
        loss="categorical_crossentropy",
        optimizer=params["optimizer"],
        metrics=["accuracy"],
    )
    hist = model.fit(
        x=data["train_gaf"],
        y=data["train_label_arr"],
        validation_data=(data["val_gaf"], data["val_label_arr"]),
        batch_size=params["batch_size"],
        epochs=params["epochs"],
        verbose=2,
    )

    return (model, hist)


def print_result(data, model):
    # get train & test pred-labels
    train_pred = model.predict(data["train_gaf"])
    test_pred = model.predict(data["test_gaf"])
    # get train & test true-labels
    train_label = data["train_label"][:, 0]
    test_label = data["test_label"][:, 0]
    # train & test confusion matrix
    train_result_cm = confusion_matrix(train_label, train_pred, labels=range(9))
    test_result_cm = confusion_matrix(test_label, test_pred, labels=range(9))

    print(train_result_cm, "\n", test_result_cm)


PARAMS = {}
PARAMS["pkl_name"] = "./data/label8_eurusd_10bar_1500_500_val200_gaf_culr.pkl"
PARAMS["model_name"] = "./model/cnn_model_01.keras"
PARAMS["classes"] = 9
PARAMS["learning_rate"] = 0.01
PARAMS["epochs"] = 50
PARAMS["batch_size"] = 64
PARAMS["optimizer"] = optimizers.SGD(learning_rate=PARAMS["learning_rate"])

# ---------------------------------------------------------

import pandas as pd

# Load the CSV file into a DataFrame
# df = pd.read_csv("./data/BTCUSDT_1h_train_pattern.csv")

# print(df.head())  # Print the
# load data & keras model
data = pro.load_pkl(PARAMS["pkl_name"])

print(data)  # Print the

# train cnn model
model, hist = train_model(PARAMS, data)
model.save(PARAMS["model_name"])

# train & test result
print_result(data, model)
