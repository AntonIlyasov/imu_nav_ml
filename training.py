#!/usr/bin/env python3


import os
import time
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.callbacks import TensorBoard
sns.set(rc={'figure.figsize':(18, 5)})

print("tensorflow version = ", tf.__version__)

from utils import retrieve_latest_weights

from tensorflow.python.keras import backend as K
from tensorflow.python.ops import math_ops
from tensorflow.python.framework import ops
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.keras.regularizers import l1
from livelossplot import PlotLosses
from livelossplot.tf_keras import PlotLossesCallback
from livelossplot import PlotLosses
import matplotlib.pyplot as plt
import datetime
from livelossplot import PlotLosses
import matplotlib.pyplot as plt
from livelossplot import PlotLossesKeras

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from keras.callbacks import Callback

class CustomPlotCallback(Callback):
    def __init__(self):
        super().__init__()
        self.losses = {'loss': [], 'val_loss': [], 'mae': [], 'val_mae': []}
        
        # Создаем фигуру и оси один раз
        self.fig, self.axs = plt.subplots(2, 1, figsize=(10, 8))
        plt.ion()  # Включаем интерактивный режим
        plt.show()

    def on_epoch_end(self, epoch, logs=None):
        # Сохраняем значения потерь и MAE
        self.losses['loss'].append(logs.get('loss'))
        self.losses['val_loss'].append(logs.get('val_loss'))
        self.losses['mae'].append(logs.get('mae'))
        self.losses['val_mae'].append(logs.get('val_mae'))

        # Обновляем график
        self.update_plot()

    def update_plot(self):
        # Обновляем данные графиков
        self.axs[0].clear()  # Очищаем ось для потерь
        self.axs[0].plot(self.losses['loss'], label='loss', color='blue')
        self.axs[0].plot(self.losses['val_loss'], label='val_loss', color='orange')
        self.axs[0].set_title('Training and Validation Loss')
        self.axs[0].set_ylabel('Loss')
        self.axs[0].legend()
        self.axs[0].grid(True)

        self.axs[1].clear()  # Очищаем ось для MAE
        self.axs[1].plot(self.losses['mae'], label='mae', color='green')
        self.axs[1].plot(self.losses['val_mae'], label='val_mae', color='red')
        self.axs[1].set_title('Training and Validation MAE')
        self.axs[1].set_ylabel('Mean Absolute Error')
        self.axs[1].legend()
        self.axs[1].grid(True)

        plt.xlabel('Epochs')
        plt.tight_layout()  # Для улучшения размещения графиков
        plt.pause(0.001)  # Обновляем график


# предотвратим захват всей графической памяти tf
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

def print_metrics(history):
    # pass
    df = pd.DataFrame(history.history)

    f, axes = plt.subplots(1, 2)

    ax = sns.lineplot(data=df[['loss', 'val_loss']], ax=axes[0])
    ax.set_ylim(0)

    ax = sns.lineplot(data=df[['mae', 'val_mae']], ax=axes[1])
    ax.set_ylim(0, 1)
    plt.show()

# обучение NN
def start_training(session_data, model_architecture, train_ds, val_ds, signals_weights_tensor, trial_tree):

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    epochs = session_data["epochs"]

    weights_folder = trial_tree["weights_folder"]
    history_csv_file = trial_tree["history_csv_file"]

    # обратные вызовы планирования скорости обучения
    def scheduler(epoch):
        if epoch < 50:
            return session_data["learning_rate"]
        elif epoch < 100:
            return 0.5 * session_data["learning_rate"]
        else:
            return 0.25 * session_data["learning_rate"]

    lr_callback = tf.keras.callbacks.LearningRateScheduler(scheduler)

    # logging callback
    csv_logger = tf.keras.callbacks.CSVLogger(history_csv_file, append=True)

    # weights checkpoint callback
    checkpoint_filepath = weights_folder + '/ep.{epoch:04d}-loss{loss:.4f}-val_loss{val_loss:.4f}.hdf5'
    model_ckpoint = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath, period=5)

    # custom_callback = CustomPlotCallback()

    # callbacks=[csv_logger, model_ckpoint, tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10),
    #            tf.keras.callbacks.EarlyStopping(patience=20, monitor='val_loss', restore_best_weights=True)]

    callbacks=[csv_logger, model_ckpoint, lr_callback]

    # Пользовательская функция потерь
    # взвешенная средняя абсолютная ошибка
    def weighted_MAE(y_true, y_pred):
        y_pred = tf.convert_to_tensor(y_pred)
        y_true = tf.cast(y_true, y_pred.dtype)
        weights = tf.cast(signals_weights_tensor, y_pred.dtype)
        return tf.reduce_mean(weights * tf.abs(y_pred - y_true), axis=-1)

    start_train_time = time.time()


    with tf.device("/GPU:0"):  
        singeleton_model = tf.keras.models.Sequential(model_architecture)
        optimizer = tf.keras.optimizers.Adam(lr=session_data["learning_rate"])
        singeleton_model.compile(loss=weighted_MAE, optimizer=optimizer, metrics=["mae"])
        singeleton_model.build(input_shape=(session_data["batch_size"], \
                                            session_data["window_size"], session_data["n_features"]))
        
        try:
            history = singeleton_model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=callbacks)
        except KeyboardInterrupt:
            print("Обучение прервано, сохраняем модель")
            end_train_time = time.time()
            session_data["training_time_hr"] = (end_train_time - start_train_time) / 3600
            return singeleton_model


    end_train_time = time.time()
    session_data["training_time_hr"] = (end_train_time - start_train_time) / 3600

    return singeleton_model

if __name__ == '__main__':
    start_training()
