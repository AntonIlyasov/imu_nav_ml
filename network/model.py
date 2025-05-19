import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential, Model
from keras.layers import LSTM,Dense,BatchNormalization, RNN,MaxPooling2D, ConvLSTM1D,ConvLSTM2D, Embedding, Flatten, Dropout, Conv2D, TimeDistributed
from keras.callbacks import ModelCheckpoint
import numpy as np
from tensorflow.python.keras import backend as K
import time
from generator import DatasetGenerator
file_type = {'json': 1, 'csv': 2}

create_new_dataset = True 

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def get_change(next, past):
    diff = next/past - 1
    return map_range(constrain(diff, -1, 1), -1, 1, 0, 1)

class BaseModel:
    def __init__(self) -> None:
        # tf.config.gpu_options.allow_growth = True
        # tf.config.set_visible_devices([], 'GPU')
        gpu_devices = tf.config.experimental.list_physical_devices('GPU')
        for device in gpu_devices:
            tf.config.experimental.set_memory_growth(device, enable = True)
        print("Num GPUs Available: ", len(gpu_devices))
        print('started model')

        net_hparams = {}

        if create_new_dataset:
            net_hparams["dataset_name"] = None
            colum_names = {"features"     : ["a_x", "a_y", "a_z", "m_x", "m_y", "m_z", "Vn", "Ve", "Vd", "Pn", "Pe", "Pd"],
                            "features_diff": ["h"],
                            "labels"       : ["w_x", "w_y", "w_z"]
                            }
        else:
            net_hparams["dataset_name"] = "T003_logs0_F10L6_W10_09May2025_2236"
            colum_names = {}

        # self.generator = DatasetGenerator('serial_log.json', file_type['json'])
        self.generator = DatasetGenerator('ni na chto ne vliyaet', file_type['csv'])
        self.generator.generate_dataset(net_hparams, colum_names)

        self.x_train, self.y_train, self.x_test, self.y_test = self.generator.return_set()
        print(self.x_train.shape)
        print(self.x_test.shape)
        print(self.y_train.shape)
        print(self.y_test.shape)
       
        print('sets')
        self.model = self.generate_model()
        print('generated_model')
        self.training()
    def get_model_from_file(self, path):
        self.model = keras.models.load_model(path)

    def training(self) -> None:
        # keras.utils.enable_interactive_logging()
        filepath = "imu_nav_model.keras"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        self.model.fit(self.x_train, self.y_train, validation_data=(self.x_test, self.y_test), callbacks=[keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5,patience=50, min_lr=1.0e-10)],batch_size=16, epochs=1000)
        self.model.save(filepath)
    

    def generate_model(self):
        model = Sequential()
        model.add(keras.Input(shape = (11,)))
        model.add(Dense(11, activation='sigmoid'))
        model.add(Dense(11, activation='sigmoid'))
        model.add(Dense(3, activation='sigmoid'))


        model.compile(loss="mean_squared_error", optimizer=keras.optimizers.Adam(learning_rate=0.01),metrics=["accuracy"])
        return model
    

if __name__ == "__main__":
    model = BaseModel()
    # model.training()