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
    csvs_root_directory = os.path.join(data_directory, "combined_csvs", "trimmed")

    session_data["n_features"] = len(colum_names["features"]) + len(colum_names["features_diff"])

    # создадим два словаря для обучения и валидации
    combined_windowed_features = {}
    combined_windowed_labels = {}
    
    for set_subdir in sets_subdirs:
        csvs_directory = os.path.join(csvs_root_directory, set_subdir)

        x_list = []
        y_list = []

        for flight_file in sorted(os.listdir(csvs_directory)):
            
            # считываем данные полета
            csv_file_name = os.path.join(csvs_directory, flight_file)

            print("\n\n!!!!!!!!!csv_file_name: ", csv_file_name)

            features = pd.read_csv(csv_file_name, usecols=colum_names["features"]).to_numpy()[:-1, :] # (n, n_features)

            # Пропустить файлы с недостаточным количеством данных
            if features.shape[0] < session_data["window_size"]:
                print(f"Warning: {flight_file} has too few samples ({features.shape[0]}). Skipping.")
                continue

            print("features.shape: ", features.shape)   # (1419, 9)
            print(features[0])

            features_diff = pd.read_csv(csv_file_name, usecols=colum_names["features_diff"]).to_numpy()     # # (n, 1)
            print("features_diff.shape: ", features_diff.shape)     # (1420, 1)
            print(features_diff[:5])

            labels = pd.read_csv(csv_file_name, usecols=colum_names["labels"]).to_numpy()       # # (n, n_labels)
            print("labels.shape: ", labels.shape)       # (1420, 6)
            print(labels[0])

            features_diff = np.diff(features_diff, axis=0)              # обучаем на дельта состояниях
            labels = np.diff(labels, axis=0)                            # обучаем на дельта состояниях
            print("! features_diff.shape: ", features_diff.shape)
            print("! labels.shape: ", labels.shape)
            
            features = np.hstack((features,features_diff))          # (n, n_features)
            print("! features.shape: ", features.shape)

            windowed_features = []
            windowed_labels = []

            # добавляем окно w и метку,признаки в i -> i+w, а метка в i+w
            for i in range (labels.shape[0] - session_data["window_size"]):
                
                one_window = features[i:i+session_data["window_size"], :]   # one_window.shape:  (200, 15)
                one_label = labels[i+session_data["window_size"], :]        # one_label.shape:  (3,)
                
                windowed_features.append(one_window)
                windowed_labels.append(one_label)
        
            x_one_flight = np.array(windowed_features)              # (n_samples, 10, 10)   (1426, 10, 10)
            y_one_flight = np.array(windowed_labels)                # (n_samples, 6)        (1426, 6)

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
        print(combined_windowed_labels[set_subdir].shape[0])

        # данные перемешиваются, чтобы избежать возможных зависимостей между последовательными окнами
        shuffled_indices = np.arange(combined_windowed_features[set_subdir].shape[0])
        np.random.shuffle(shuffled_indices)
        combined_windowed_features[set_subdir] = combined_windowed_features[set_subdir][shuffled_indices]
        combined_windowed_labels[set_subdir] = combined_windowed_labels[set_subdir][shuffled_indices] 


    # при создании весов уделим внимание меньшим сигналам
    print("^_^ combined_windowed_labels[\"training\"].shape: ",combined_windowed_labels["training"].shape)
    print("^_^ combined_windowed_labels[\"validation\"].shape: ",combined_windowed_labels["validation"].shape)
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
        dt = 0.033333333
        flight_time_hr = f'{(combined_windowed_features[set_subdir].shape[0] * dt / 3600):.2f}'
        print("flight time used for", set_subdir, " : ", flight_time_hr, "hours")
        print("------------")

    # датасет
    training_dataset = tf.data.Dataset.from_tensor_slices((combined_windowed_features["training"], combined_windowed_labels["training"]))
    validation_dataset = tf.data.Dataset.from_tensor_slices((combined_windowed_features["validation"], combined_windowed_labels["validation"]))

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    return training_dataset, validation_dataset, signals_weights

if __name__ == '__main__':
    create_dataset()