#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import tensorflow as tf
import datetime
import pickle
import glob

def create_dataset(session_data, colum_names):
 
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    data_directory = os.path.join(os.path.pardir, "data")
    
    # папки для training и validation
    sets_subdirs = ["training", "validation"]

    # загрузить существующий датасет
    if session_data["dataset_name"] is not None:
        print("retrieving", session_data["dataset_name"])

        datasets_directory = os.path.join(data_directory, "datasets", session_data["dataset_name"])

        # загружаем training и validation массивы
        with open(os.path.join(datasets_directory, "features_labels"), 'rb') as features_labels_file:
            npzfile = np.load(features_labels_file)
            combined_windowed_features = {"training":npzfile["features_tr"], "validation":npzfile["features_val"]}
            combined_windowed_labels = {"training":npzfile["labels_tr"], "validation":npzfile["labels_val"]}

        session_data["n_features"] = combined_windowed_features["validation"].shape[-1]
        
        with open(os.path.join(datasets_directory, "flights_dictionaries"), 'rb') as flights_dict_file:
            flights_dictionaries = pickle.load(flights_dict_file)

    # если его нет, создаем из csv-файла 
    else:

        csvs_root_directory = os.path.join(data_directory, "combined_csvs", "trimmed")
        
        # кол-во всех csv файлов в подпапках
        n_logs = len([filename for filename in glob.iglob(csvs_root_directory + '/*/*', recursive=True)])
        session_data["n_features"] = len(colum_names["features"]) + len(colum_names["features_diff"])
        n_features = str(session_data["n_features"])
        n_labels = str(len(colum_names["labels"]))
        # номер полета, кол-во признаков, меток, размер окна и время создания
        dataset_name = "T" + str(session_data["trial_number"]).zfill(3) + "_logs" + str(n_logs) + \
                       "_F" + n_features + "L" + n_labels + "_W" + str(session_data["window_size"]) + \
                       "_" + datetime.datetime.now().strftime("%d%b%Y") + \
                       "_" + datetime.datetime.now().strftime("%H%M")

        datasets_directory = os.path.join(data_directory, "datasets", dataset_name)

        if not os.path.isdir(datasets_directory):
            os.makedirs(datasets_directory)
        
        print("creating", dataset_name, "...")
        session_data["dataset_name"] = dataset_name

        # создадим два словаря для обучения и валидации
        combined_windowed_features = {}
        combined_windowed_labels = {}
        
        # подсловари - пары ключ-значение (flight_name, list of windows)
        flights_dictionaries = {"training":{}, "validation":{}}

        for set_subdir in sets_subdirs:
            csvs_directory = os.path.join(csvs_root_directory, set_subdir)

            x_list = []
            y_list = []

            for flight_file in sorted(os.listdir(csvs_directory)):
                
                # считываем данные полета
                csv_file_name = os.path.join(csvs_directory, flight_file)
                features = pd.read_csv(csv_file_name, usecols=colum_names["features"]).to_numpy()[1:,:]

                # Пропустить файлы с недостаточным количеством данных
                if features.shape[0] < session_data["window_size"]:
                    print(f"Warning: {flight_file} has too few samples ({features.shape[0]}). Skipping.")
                    continue

                # print("features.shape: ", features.shape)   # (1419, 9)

                features_diff = pd.read_csv(csv_file_name, usecols=colum_names["features_diff"]).to_numpy()
                # print("features_diff.shape: ", features_diff.shape)     # (1420, 1)

                # print(features_diff[:5])

                labels = pd.read_csv(csv_file_name, usecols=colum_names["labels"]).to_numpy()
                # print("labels.shape: ", labels.shape)       # (1420, 6)

                features_diff = np.diff(features_diff, axis=0)              # обучаем на дельта состояниях
                labels = np.diff(labels, axis=0)                            # обучаем на дельта состояниях
                # print("! features_diff.shape: ", features_diff.shape)
                # print("! labels.shape: ", labels.shape)

                # print(features_diff[:5])


                features = np.hstack((features,features_diff))
                # print("!!! features.shape: ", features.shape)
                
                windowed_features = []
                windowed_labels = []

                # print("delta = ", labels.shape[0] - session_data["window_size"])
                
                # добавляем окно w и метку,признаки в i -> i+w, а метка в i+w
                for i in range (labels.shape[0] - session_data["window_size"]):
                    
                    one_window = features[i:i+session_data["window_size"], :]
                    one_label = labels[i+session_data["window_size"], :]

                    # print("one_window.shape: ", one_window.shape)
                    # print("one_label.shape: ", one_label.shape)
                    
                    windowed_features.append(one_window)
                    windowed_labels.append(one_label)
            
                x_one_flight = np.array(windowed_features)              # (n, 10, 10)   (1426, 10, 10)
                y_one_flight = np.array(windowed_labels)                # (n, 6)        (1426, 6)
                # print("x_one_flight.shape: ", x_one_flight.shape)
                # print("y_one_flight.shape: ", y_one_flight.shape)

                flights_dictionaries[set_subdir].update({flight_file[0:-4]:(x_one_flight, y_one_flight)})
                
                x_list.append(x_one_flight)
                y_list.append(y_one_flight)
            print("len(x_list): ", len(x_list))     # (n_flights, n_samples, 10, 10)

            print("\nDebugging array shapes in x_list:")
            for i, arr in enumerate(x_list):
                print(f"Array {i}: shape={arr.shape}, ndim={arr.ndim}")

            # все окна признаков и меток объединяются в один массив для каждого подкаталога
            combined_windowed_features[set_subdir] = np.vstack(x_list)      # (n_flights*n_samples, 10, 10)
            combined_windowed_labels[set_subdir] = np.vstack(y_list)        # (n_flights*n_samples, 6)
            
            print(combined_windowed_features[set_subdir].shape[0])

            # данные перемешиваются, чтобы избежать возможных зависимостей между последовательными окнами
            shuffled_indices = np.arange(combined_windowed_features[set_subdir].shape[0])
            np.random.shuffle(shuffled_indices)
            combined_windowed_features[set_subdir] = combined_windowed_features[set_subdir][shuffled_indices]
            combined_windowed_labels[set_subdir] = combined_windowed_labels[set_subdir][shuffled_indices] 

        # сохраним датасет в файлы (features, labels)
        with open(os.path.join(datasets_directory, "features_labels"), 'wb') as features_labels_file:
            np.savez(features_labels_file, \
                     features_tr=combined_windowed_features["training"], \
                     labels_tr=combined_windowed_labels["training"], \
                     features_val=combined_windowed_features["validation"], \
                     labels_val=combined_windowed_labels["validation"])

        # словари
        with open(os.path.join(datasets_directory, "flights_dictionaries"), 'wb') as flights_dict_file:
            pickle.dump(flights_dictionaries, flights_dict_file,  protocol=pickle.HIGHEST_PROTOCOL)

        # названия столбцов
        with open(os.path.join(datasets_directory, "features_labels_names.txt"), 'w') as f:
            for key, value in colum_names.items():
                line = key + ":\n" + ','.join(map(str, value)) + "\n"
                f.write(line)
        
    # при создании весов уделим внимание меньшим сигналам
    print("^_^ combined_windowed_labels[\"training\"].shape: ",combined_windowed_labels["training"].shape)
    average_absolutes = np.mean(np.abs(combined_windowed_labels["training"]), axis = 0)

    print("average_absolutes: ", average_absolutes)
    
    signals_weights = 1 / average_absolutes
    signals_weights = signals_weights / np.min(signals_weights) # нормализуем
    print("\nsignals weights:\n", signals_weights, "\n")

    for set_subdir in sets_subdirs:
        print("shape of", set_subdir, "features", combined_windowed_features[set_subdir].shape) # (10014, 10, 10)
        print("shape of", set_subdir, "labels", combined_windowed_labels[set_subdir].shape)     # (10014, 6)
        print("----")

        # итоговое время полета
        dt = 0.2
        flight_time_hr = f'{(combined_windowed_features[set_subdir].shape[0] * dt / 3600):.2f}'
        print("flight time used for", set_subdir, " : ", flight_time_hr, "hours")
        print("------------")

        session_data_new_key = "flight_duration_" + set_subdir + "_hr"

        session_data[session_data_new_key] = flight_time_hr

    # датасет
    training_dataset = tf.data.Dataset.from_tensor_slices((combined_windowed_features["training"], combined_windowed_labels["training"]))
    validation_dataset = tf.data.Dataset.from_tensor_slices((combined_windowed_features["validation"], combined_windowed_labels["validation"]))

    return training_dataset, validation_dataset, flights_dictionaries["training"], flights_dictionaries["validation"], signals_weights

if __name__ == '__main__':
    create_dataset()