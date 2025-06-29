import numpy as np
import time
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
import multiprocessing as mp
import time
import os
import timeit
import datetime
import csv
import tensorflow as tf
from multiprocessing import Manager

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0 = все логи, 2 = только ошибки


def ensure_dir(file_path):
    """Создает директорию, если она не существует"""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_to_csv(csv_path, data_dict, column_order):
    """Записывает данные в CSV файл"""
    # Проверяем, существует ли файл
    file_exists = os.path.isfile(csv_path)
    
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_order)
        
        # Если файл новый - записываем заголовки
        if not file_exists:
            writer.writeheader()
        
        # Записываем данные
        writer.writerow(data_dict)

class Test:
    def __init__(self) -> None:

        manager = Manager()

        window = mp.Queue(maxsize=window_size + 2)
        labels_l = manager.list([None])

        window_count = mp.Value('i', 0)

        self.window_maintainer_p = mp.Process(target=self.window_maintainer, args=(window,window_count,labels_l))
        self.make_prediction_p = mp.Process(target=self.make_prediction, args=(window,window_count,labels_l))

        self.window_maintainer_p.start()
        self.make_prediction_p.start()

        self.window_maintainer_p.join()
        self.make_prediction_p.join()



    def window_maintainer(self, window, window_count, labels_l):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_directory = os.path.join(current_dir, "data")
        csvs_directory = os.path.join(data_directory, "combined_csvs", "trimmed", "validation")
        csv_file_name = os.path.join(csvs_directory, flight_file + ".csv")

        print("!!! journal csv_file_name: ", csv_file_name)
        
        i = 1
        while(1):

            features = pd.read_csv(csv_file_name, usecols=colum_names["features"]).to_numpy()[i:i+1, :] # (n, n_features)
            
            features_diff_prev = pd.read_csv(csv_file_name, usecols=colum_names["features_diff"]).to_numpy()[i-1:i, :]
            features_diff_next = pd.read_csv(csv_file_name, usecols=colum_names["features_diff"]).to_numpy()[i:i+1, :]
            features_diff = features_diff_next - features_diff_prev
            
            features = np.hstack((features,features_diff))          # (n, n_features)
            # print(features)

            labels = pd.read_csv(csv_file_name, usecols=colum_names["labels"]).to_numpy()[i:i+1, :]       # # (1, n_labels)
            # print(labels)

            window.put(features)
            print("window.qsize(): ", window.qsize())

            # если у нас достаточно окна для одного предсказания
            if window.qsize() > window_size:
                # удаляем самый старый элемент очереди
                window.get()
                print(window.qsize())

                labels_l[0] = labels
                print("window_maintainer labels: ", labels)

                with window_count.get_lock():
                    window_count.value += 1
                    print("window_maintainer window_count.value: ", window_count.value)

            time.sleep(0.033333)
            i+=1
        pass

    def make_prediction(self, window, window_count, labels_l):

        run_inference_csv = os.path.join("tests", "trial_" + str(trial_number).zfill(3), flight_file,
                                         "run_inference_result.csv")
        
        colum_names = {"top_view" : ["ekf_x", "ekf_y", "ekf_z", "nn_x", "nn_y", "nn_z"],
                       "errors"   : ["pose_error_3d", "d_nn_x", "d_nn_y", "d_nn_z"]}
        
        ekf_position = np.zeros((3,))

        self.model = self.load_model()
        print('success load model')

        window_count_prev = 0
        window_count_cur = 0

        pos_nn = None

        while(1):
            with window_count.get_lock():
                window_count_cur = window_count.value

            if (window_count_prev == window_count_cur):
                continue

            window_count_prev = window_count_cur
            print("make_prediction window_count_cur: ", window_count_cur)

            print("\n\n[ START PREDICT ]")

            inference_start_time = timeit.default_timer()

            labels = labels_l[0]
            print("make_prediction labels: ", labels)

            # Копируем значения из labels в ekf_position
            ekf_position[:] = labels[0, :]  # или ekf_position[:] = labels[0]
            print("make_prediction ekf_position: ", ekf_position)  # [20.11839097 -0.92444029 -8.28785124]

            # Собираем все данные из очереди в список
            window_data = []
            while not window.empty():
                window_data.append(window.get())

            # возвращаем словарь на место
            for item in window_data:
                window.put(item)

            # Преобразуем список в numpy array
            window_arr = np.array(window_data)

            # Добавляем оси для временных шагов и размера пакета
            window_arr = window_arr.reshape(1, window_arr.shape[0], window_arr.shape[2])

            delta_position = self.model.predict(window_arr, batch_size=1).reshape((3,))
            print("delta_position: ", delta_position)

            print("\n\n[ END PREDICT ]")

            if pos_nn is None:
                pos_nn = np.copy(ekf_position)
                print("**********************************")       
                print("*        first prediction        *")
                print("*          ", pos_nn, "          *")
                print("**********************************")

            else:
                pos_nn += delta_position

            nn_position_error = np.linalg.norm(pos_nn - ekf_position)

            # Подготовка данных для записи в CSV
            data_to_log = {
                'timestamp': datetime.datetime.now().isoformat(),
                'ekf_x': ekf_position[0],
                'ekf_y': ekf_position[1],
                'ekf_z': ekf_position[2],
                'nn_x': pos_nn[0],
                'nn_y': pos_nn[1],
                'nn_z': pos_nn[2],
                'd_nn_x': delta_position[0],
                'd_nn_y': delta_position[1],
                'd_nn_z': delta_position[2],


                'pose_error_3d': nn_position_error,
            }

            # Определяем порядок столбцов на основе colum_names
            column_order = ['timestamp']  # добавляем временную метку
            for category in colum_names.values():
                column_order.extend(category)

            # Убеждаемся, что директория существует
            ensure_dir(run_inference_csv)
            write_to_csv(run_inference_csv, data_to_log, column_order)

            time.sleep(0.001)
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

        # Получение количества features
        first_lstm_layer = model.layers[0]
        input_shape = first_lstm_layer.input_shape  # Получаем входную форму
        num_features = input_shape[2]  # Третий элемент - количество features

        print(f"Количество входных features: {num_features}")

        return model
    

if __name__ == "__main__":

    # номер папки с моделью
    trial_number = sys.argv[1]                      # ./run_inference.py 6 100    // 6 папка trial_006

    
    # размер окна
    window_size = int(sys.argv[2])                  # 100

    # файл полета
    flight_file = str(sys.argv[3])

    num_features = 0

    colum_names = {"features"     : ["w_x", "w_y", "w_z", "a_x", "a_y", "a_z", "m_x", "m_y", "m_z", "q0", "q1", "q2", "q3"],
                    "features_diff": ["h"],
                    "labels"       : ["Pn", "Pe", "Pd"]}

    test = Test()
    # model.training()