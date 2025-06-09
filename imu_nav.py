#!/usr/bin/env python3

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Только ошибки
import tensorflow as tf
import training
import utils
import postprocessing
from preprocessing.create_dataset import create_dataset

# Параметры сеанса
session_mode = ["Fresh", "Resume", "Evaluate", "Override"]
mode_id = 0
gpu_name = ["/GPU:0", "/GPU:1", None]
gpu_id = 0
create_new_dataset = True 

# Архитектура модели нейронной сети с использованием библы TensorFlow и Keras
# модель состоит из двух LSTM слоев и одного полносвязного слоя
model_architecture = [
    tf.keras.layers.LSTM(20, return_sequences=True), #200       Первый LSTM слой (Long Short-Term Memory) с 20 нейронами
                                                                # Этот слой будет обрабатывать последовательные данные.
    tf.keras.layers.Dropout(0.2),
    # tf.keras.layers.LSTM(200, return_sequences=True),         # доп LSTM слой с 200 нейронами
    # tf.keras.layers.LSTM(200, return_sequences=True),         # доп LSTM слой с 200 нейронами
    tf.keras.layers.LSTM(20, return_sequences=False), #200S     LSTM слой с 20 нейронами
    tf.keras.layers.Dropout(0.2),
                                                                # слой должен возвращать только последний выходной вектор
    tf.keras.layers.Dense(6)                                    # полносвязный слой с 6 нейронами
    ]

# Гиперпараметры сети
net_hparams = {"trial_number" : 7,                              # номер эксперимента
                "session_mode" : session_mode[mode_id],
                "gpu_name" : gpu_name[gpu_id],
                "batch_size" : int(1 * 1024),
                "learning_rate" : 0.001,
                "window_size" : 100,
                "epochs" : 1000,
                "initial_epoch" : 0
                }

# создаем папки для результатов обучения (веса, графики, история потерь)
trial_tree = utils.create_trial_tree(net_hparams["trial_number"], net_hparams["session_mode"])
print(trial_tree)


if create_new_dataset:
    net_hparams["dataset_name"] = None
    colum_names = {"features"     : ["w_x", "w_y", "w_z", "a_x", "a_y", "a_z", "m_x", "m_y", "m_z"],
                    "features_diff": ["h"],
                    "labels"       : ["Vn", "Ve", "Vd", "Pn", "Pe", "Pd"]}
else:
    net_hparams["dataset_name"] = "T003_logs0_F10L6_W10_09May2025_2236"
    colum_names = {}
    
# создаем оконные наборы данных из CSV-файлов полетов (или извлечь старые из двоичных файлов)
train_ds, val_dataset, train_flights_dict, val_flights_dict, signals_weights = create_dataset(net_hparams, colum_names)

# signals_weights - (6,)

dataset_size = sum(1 for _ in train_ds)
print("dataset_size: ", dataset_size)

# batch and shuffle
train_dataset = train_ds.shuffle(buffer_size=1000).batch(net_hparams["batch_size"])
val_dataset = val_dataset.shuffle(buffer_size=1000).batch(net_hparams["batch_size"])

train_dataset_size = sum(1 for _ in train_dataset)
print("train_dataset_size: ", type(train_dataset))

# преобразуем веса сигналов в тензор, который будет использоваться функцией потерь
signals_weights_tensor = tf.constant(signals_weights, dtype=tf.float32)
print(signals_weights_tensor)

# начинаем обучение
model = training.start_training(net_hparams, model_architecture, train_dataset, val_dataset, \
                                signals_weights_tensor, trial_tree)

# сохраняем модель keras
keras_model_path = trial_tree["trial_root_folder"] + "/keras_model"
model.save(keras_model_path, include_optimizer=False)
print("успешное сохранение в формате tf SavedModel")

# сохраняем модель в формате tf SavedModel
tf_model_path = trial_tree["trial_root_folder"] + "/tf_saved_model"
tf.saved_model.save(model, tf_model_path)

print("успешное сохранение в формате tf SavedModel")