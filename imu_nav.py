#!/usr/bin/env python3

import os
import tensorflow as tf
import training
import utils
import postprocessing
from preprocessing.create_dataset import create_dataset
from tensorflow.keras import regularizers

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0 = все логи, 2 = только ошибки

# вывод доступа видеокарты
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, enable = True)
print("Num GPUs Available: ", len(gpu_devices))

# Архитектура модели нейронной сети с использованием библы TensorFlow и Keras
model_architecture = [
    tf.keras.layers.LSTM(64, return_sequences=True, kernel_regularizer=regularizers.l2(1e-4)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.3),  # Увеличенный dropout
    tf.keras.layers.LSTM(128, return_sequences=True),  # Добавлен слой
    tf.keras.layers.LSTM(64, return_sequences=False),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(3)
]

# Гиперпараметры сети
net_hparams = {"trial_number" : 31,                              # номер эксперимента огонь
                "batch_size" : int(1 * 256),
                "learning_rate" : 0.0005,
                "window_size" : 50,
                "epochs" : 200,
                "n_features": 14
                }

colum_names = {"features"     : ["w_x", "w_y", "w_z", "a_x", "a_y", "a_z", "m_x", "m_y", "m_z", "q0", "q1", "q2", "q3"],
                "features_diff": ["h"],
                "labels"       : ["Pn", "Pe", "Pd"]}
    

# создаем папки для результатов обучения (веса, графики, история потерь)
trial_tree = utils.create_trial_tree(net_hparams["trial_number"])
print(trial_tree)

# создаем оконные наборы данных из CSV-файлов полетов
train_ds, val_dataset, signals_weights = create_dataset(net_hparams, colum_names)

# # signals_weights - (6,)

dataset_size = sum(1 for _ in train_ds)
print("dataset_size: ", dataset_size)

# batch and shuffle
train_dataset = train_ds.shuffle(buffer_size=2048).batch(net_hparams["batch_size"])
val_dataset = val_dataset.batch(net_hparams["batch_size"])

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