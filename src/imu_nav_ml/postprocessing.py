#!/usr/bin/env python3

import os, csv, json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def flight_pdf_plots(file_name, ground_truth, predictions):


    # timesteps vector
    time_length = ground_truth.shape[0]
    time_steps = np.linspace(0, time_length-1, time_length)

    # convert time from steps to minutes (5 examples are logged per second)
    dt = 0.2
    time_steps = time_steps * dt / 60

    with PdfPages(file_name) as pdf:

        signal_names = ["north velocity (m/s)", "east velocity (m/s)", "down velocity (m/s)", 
                        "north position (m)", "east position (m)", "down position (m)"]

        # loop on signals of this one flight
        for signal_number, signal_name in enumerate(signal_names):
            plt.figure()
            true_signal = ground_truth[:, signal_number]
            predicted_signal = predictions[:, signal_number]

            # plot title is the mean absolute error between the truth and predictions
            signal_MAE = np.mean(np.absolute(true_signal - predicted_signal))

            plt.plot(time_steps, true_signal) 
            plt.plot(time_steps, predicted_signal, linestyle=(0, (1, 1)))
            plt.grid(True)
            plt.ylabel(signal_name)
            plt.xlabel("time (minutes)")
            plt.title("MAE=" + '{:.3f}'.format(signal_MAE))
            plt.legend(("EKF with GPS", "Network without GPS"))   
            pdf.savefig()
            plt.close()


def evaluate_all_flights(model, train_flights_dict, val_flights_dict, trial_folder, n_extreme_flights=10):

    # loop on sets, one iteration for training and another for validation
    flights_summary = {}
    set_names = ["training","validation"]
    for flights_dict, set_name in zip([train_flights_dict, val_flights_dict], set_names):
        
        # sort flights by name (shorter flight first)
        flights_list = sorted(flights_dict.items())
        total_flights = len(flights_list) - 1

        # dictionary of (flight_name : max_pos_error) pairs, used to extract the best & worst flights
        flights_errors = {}

        # array of shape (time_steps, 3), colums are (flight_duration, max_pos_error, max_vel_error)
        set_summary = []

        for flight_number, one_flight_data in enumerate(flights_list):
            
            ##to speedup experimenting
            # if flight_number > 5:
            #     break

            flight_name = one_flight_data[0]
            print("flight " + str(flight_number) + "/" + str(total_flights) + " : " + flight_name)
            
            features = one_flight_data[1][0]
            ground_truth_diff = one_flight_data[1][1]
            predictions_diff = model.predict(features)

            # Reconstruct the original signals from differenced signals
            ground_truth_reconstructed = np.cumsum(ground_truth_diff, axis = 0)
            predictions_reconstructed = np.cumsum(predictions_diff, axis = 0)

            # reconstructed output csv file name 
            output_csv_file_nn = os.path.join(trial_folder, set_name, "reconstructed", \
                                              "nn_output_csv", flight_name + "_nn.csv")

            # differenced output csv file name 
            output_csv_file_nn_diff = os.path.join(trial_folder, set_name, "differenced", \
                                              "nn_output_csv", flight_name + "_nn.csv")
            
            # save the reconstructed predictions (ground truth already saved by create_dataset.py)
            np.savetxt(output_csv_file_nn, predictions_reconstructed, delimiter=",")

            # save the differenced predictions
            np.savetxt(output_csv_file_nn_diff, predictions_diff, delimiter=",")

            # maximum errors between prediction and ground truth
            max_velocity_error = np.max(np.linalg.norm(ground_truth_reconstructed[:,0:3] \
                                                      -predictions_reconstructed[:,0:3], axis=1))
            max_position_error = np.max(np.linalg.norm(ground_truth_reconstructed[:,3:6] \
                                                      -predictions_reconstructed[:,3:6], axis=1))

            # add error to the output file name
            pdf_name = flight_name + "_MPE_" f'{max_position_error:.2f}' + \
                                     "_MVE_" f'{max_velocity_error:.2f}' + ".pdf"

            # create a pdf for this flight differenced signals
            pdf_name_diff = os.path.join(trial_folder, set_name, "differenced", pdf_name)
            flight_pdf_plots(pdf_name_diff, ground_truth_diff, predictions_diff)

            # create a pdf for this flight reconstructed signals
            pdf_name_recon = os.path.join(trial_folder, set_name, "reconstructed", "other", pdf_name)
            flight_pdf_plots(pdf_name_recon, ground_truth_reconstructed, predictions_reconstructed)

            flights_errors[pdf_name] = max_position_error

            flight_duration = ground_truth_reconstructed.shape[0] * 0.2 / 60
            set_summary.append([int(flight_name[0:4]), flight_duration, max_position_error, max_velocity_error])
        
        flights_summary[set_name] = set_summary
        
        # sort the flights from by position error (min error first)
        sorted_flights = sorted(flights_errors.items(), key=lambda x: x[1])
        
        # move the pdfs of best & worst flights of this set to their respective folders
        old_name_base = os.path.join(trial_folder, set_name, "reconstructed", "other")
        best_name_base = os.path.join(trial_folder, set_name, "reconstructed", "best")
        worst_name_base = os.path.join(trial_folder, set_name, "reconstructed", "worst")

        for i in range(n_extreme_flights):
            pdf_name = sorted_flights[i][0]
            old_name = os.path.join(old_name_base, pdf_name)
            new_name = os.path.join(best_name_base, pdf_name)
            os.rename(old_name, new_name)
        
        for i in range(-n_extreme_flights, 0):
            pdf_name = sorted_flights[i][0]
            old_name = os.path.join(old_name_base, pdf_name)
            new_name = os.path.join(worst_name_base, pdf_name)
            os.rename(old_name, new_name)
    
    return flights_summary

def summarize_session(trial_tree, model, session_data, flights_summary):
    
    # extract number of epochs and losses from last line of history csv file
    with open(trial_tree["history_csv_file"],'r') as log_file:
	    logged_losses = log_file.readlines()

    last_epoch_log = logged_losses[-1] 
    last_log = [float(i) for i in last_epoch_log.split(",")]
    epochs = f'{last_log[0]+1:.0f}'
    training_loss = f'{last_log[1]:.4f}'
    validation_loss = f'{last_log[3]:.4f}'

    session_data.update({"epochs":epochs, "training_loss":training_loss,
    "validation_loss":validation_loss})
    
    # model object => json string => dictionary => extract layers list
    json_model = model.to_json()
    model_dict = json.loads(json_model)
    layers_list = model_dict['config']['layers']
    
    # write each layer in the list as a string
    layers_data = []
    for layer in layers_list:
        if layer['class_name'] == 'LSTM':
            layers_data.append(layer['class_name'] + '_' + str(layer['config']['units'])
             + '_' + layer['config']['activation'] + '_ra_' +  layer['config']['recurrent_activation'])
        elif layer['class_name'] == 'Dense':
            layers_data.append(layer['class_name'] + '_' + str(layer['config']['units']) \
            + '_' + layer['config']['activation'])
        else:
            layers_data.append(layer['class_name'])
    
    session_data.update({"architecture":layers_data})

    # create a csv file of the trial results
    set_names = ["training", "validation"]

    for set_name in set_names:
      
        flights_errors = np.array(flights_summary[set_name])[:,1:]

        mean_errors = np.mean(flights_errors, axis=0)
        median_errors = np.median(flights_errors, axis=0)
        max_errors = np.max(flights_errors, axis=0)
        min_errors = np.min(flights_errors, axis=0)

        session_stats = ['\n', \
                         "mean," + ','.join(map(str, mean_errors)) + '\n', 
                         "median," + ','.join(map(str, median_errors)) + '\n',
                         "max," + ','.join(map(str, max_errors)) + '\n',
                         "min," + ','.join(map(str, min_errors)) + '\n']
        
        summary_file = os.path.join(trial_tree["trial_root_folder"], set_name + "_summary.csv")
        file_header = "Flight Number, Duration (min), Max Position Error (m), Max Velocity Error (m/s)"
        np.savetxt(summary_file, flights_summary[set_name], delimiter=",", header=file_header)

        with open(summary_file,'a') as file_obj:
            for line in session_stats:
                file_obj.write(line)
        
        # update session data with the error means
        session_data[set_name + "_mean_pos_error"] = mean_errors[1]
        session_data[set_name + "_mean_vel_error"] = mean_errors[2]

    # read the header of summary.csv
    with open('summary.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        header = next(csv_reader)

    #remove unnecessary session_data items
    # session_data.pop("n_labels") 
    session_data.pop("n_features") 
    session_data.pop("initial_epoch") 
    
    # write session_data according to the header
    with open('summary.csv', 'a+', newline='') as write_obj:
        dict_writer = csv.DictWriter(write_obj, fieldnames=header)
        dict_writer.writerow(session_data)
