from generator import DatasetGenerator
from keras.models import load_model
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')
model = load_model('imu_nav_model.keras')

generator = DatasetGenerator('serial_log.json')

generator.generate_dataset()




x = range(1000)
results_pitch = []
real_results_pitch = []
results_roll = []
real_results_roll = []
results_yaw = []
real_results_yaw = []
for i in range(1000):
    results_pitch.append(model.predict(np.array([generator.dataset["x"][i]]))[0][0])
    real_results_pitch.append(generator.dataset["y"][i][0])

plt.plot(x,results_pitch, 'b', x, real_results_pitch, 'g')
plt.show()