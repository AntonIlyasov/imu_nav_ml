#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

trials_str = sys.argv[1]
trials = [int(trial) for trial in trials_str.split(',')]

zoom = int(sys.argv[2])

legends = []
train_loss_plots = plt.subplot(211)
val_loss_plots = plt.subplot(212)

for trial in trials:

    legends.append("trial " + str(trial).zfill(3))
    
    trial_log_file = os.path.join("results", "trial_" + str(trial).zfill(3), "model_history_log.csv")
    try:
        df = pd.read_csv(trial_log_file)
    except:
        print("didn't find ", trial_log_file)
        continue
    
    df.head()
    df = df[["loss", "val_loss"]]
    train_loss = df.loss
    val_loss = df.val_loss
    
    # create epochs vector (x-axis)
    epochs = list(range(zoom, len(train_loss)))
    
    # print total epochs, minimum loss and val_loss along with their epochs
    print("trial:", trial, ", epochs:", val_loss.size, end=", ")
    print("min training loss:", f'{np.min(train_loss):.4f}', "at epoch", np.argmin(train_loss), end=", ") 
    print("min validation loss:", f'{np.min(val_loss):.4f}', "at epoch", np.argmin(val_loss),)

    train_loss_plots.plot(epochs, train_loss[zoom:])
    val_loss_plots.plot(epochs, val_loss[zoom:])
    

train_loss_plots.grid(True)
train_loss_plots.set_ylabel("Training Loss (MAE)")
train_loss_plots.legend(legends)

val_loss_plots.grid(True)
val_loss_plots.set_ylabel("Validation Loss (MAE)")
val_loss_plots.legend(legends)

plt.xlabel("epochs")
plt.savefig("losses.pdf")
plt.show()
