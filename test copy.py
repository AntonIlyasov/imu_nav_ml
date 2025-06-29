import tensorflow as tf
from tensorflow import keras
from keras.layers import LSTM,Dense,BatchNormalization, RNN,MaxPooling2D, ConvLSTM1D,ConvLSTM2D, Embedding, Flatten, Dropout, Conv2D, TimeDistributed
import numpy as np
from tensorflow.python.keras import backend as K
import time

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Activation, Dropout, LeakyReLU
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping, Callback

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
import multiprocessing as mp
import time
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0 = все логи, 2 = только ошибки


class Test:
    def __init__(self) -> None:

        window = mp.Queue(maxsize=window_size + 2)

        self.window_maintainer_p = mp.Process(target=self.window_maintainer, args=(window,))
        self.make_prediction_p = mp.Process(target=self.make_prediction, args=(window,))

        self.window_maintainer_p.start()
        self.make_prediction_p.start()

        self.window_maintainer_p.join()
        self.make_prediction_p.join()



    def window_maintainer(self, window):
        count = 0

        

        

        while(1):
            count += 1
            print("window_maintainer count: ", count)



            
            time.sleep(0.03333333333333)
        pass

    def make_prediction(self, window):

        self.model = self.load_model()
        print('success load model')

        count = 0
        while(1):
            count += 1
            print("make_prediction count: ", count)
            time.sleep(0.1)
        pass




    # def create_dataset(self):
    #     self.generator = DatasetGenerator('from_csv_log_small.json')

    #     # создаем оконные наборы данных из CSV-файлов полетов (или извлечь старые из двоичных файлов)
    #     train_ds, val_ds = self.generator.create_tensor_dataset(net_hparams)

    #     dataset_size = sum(1 for _ in train_ds)
    #     print("dataset_size: ", dataset_size)

    #     # batch and shuffle
    #     train_dataset = train_ds.shuffle(buffer_size=1000).batch(net_hparams["batch_size"])
    #     val_dataset = val_ds.shuffle(buffer_size=1000).batch(net_hparams["batch_size"])

    #     train_dataset_size = sum(1 for _ in train_dataset)
    #     print("train_dataset_size: ", type(train_dataset))

    #     return train_dataset, val_dataset
    
    def load_model(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        print("loading Tensorflow model ...")
        trial_folder = os.path.join(current_dir, "results", "trial_" + str(trial_number).zfill(3))
        keras_model_path = os.path.join(trial_folder, "keras_model") 
        print("keras_model_path: ", keras_model_path)
        model = tf.keras.models.load_model(keras_model_path)
        print("Model summary:")
        model.summary()

        return model
    

if __name__ == "__main__":

    # номер папки с моделью
    trial_number = sys.argv[1]                      # ./run_inference.py 6 100    // 6 папка trial_006

    # размер окна
    window_size = int(sys.argv[2])                  # 100



    test = Test()
    # model.training()