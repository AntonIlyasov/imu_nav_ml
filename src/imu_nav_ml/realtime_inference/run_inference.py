#!/usr/bin/env python

print("importing libraries ...")

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # отключаем все сообщения логирования от TensorFlow
import datetime
import time
import timeit
import queue
import csv
import sys
import numpy as np
import tensorflow as tf

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped, TwistStamped
from sensor_msgs.msg import Imu, MagneticField
from mavros_msgs.msg import Altitude
from imu_nav_ml.msg import ListOfLists, PythonList, ImuNavPrediction, PosVel

# использует окно признаков для 1 предсказания
# и публикует лист с предсказанием [Pn, Pe, Pd, Vn, Ve, Vd]
# публикует и выводит время 1 предсказания
def make_prediction(data):

    if rospy.get_param("/imu_nav/enable_inference"):

        # если это первое предсказание, установим начальные состояния на состояния ekf
        if make_prediction.pos_nn is None:   
            make_prediction.pos_nn = np.copy(ekf_position)
            print("**********************************")       
            print("*        first prediction        *")
            print("*  ", make_prediction.pos_nn, "  *")
            print("**********************************")    
        
        # если мы хотим сбросить прогнозы nn до ekf (когда GPS восстановился)
        if rospy.get_param("/imu_nav/reset_nn"):   
            make_prediction.pos_nn = np.copy(ekf_position)
            print("**********************************")       
            print("*        reset predictions       *")
            print("*  ", make_prediction.pos_nn, "  *")
            print("**********************************")
            rospy.set_param("/imu_nav/reset_nn", False)   

        # время вывода записи
        inference_start_time = timeit.default_timer()

        # преобразуем опубликованную структуру ListOfLists в список списков Python (двумерный список)
        window_list = [e.row for e in data.matrix]
        
        # преобразуем 2D-список в np.array
        window_arr = np.array(window_list, dtype=np.float32)
        
        # изменим его форму, чтобы он был совместим с сетевым вводом (размер пакета, временные шаги, n_features)
        window_arr = np.resize(window_arr, (1,window_size,10))
        
        # предсказываем метки (изменения положения в NED) и аккумулируем их в положении
        delta_position = model.predict(window_arr, batch_size=1).reshape((3,))
        make_prediction.pos_nn += delta_position

        dt = 0.2
        vel_nn = delta_position / dt

        if SAVE_PREDICTIONS:
            # сохраним прогнозы для сравнения    
            predictions_row = list(vel_nn) + list(make_prediction.pos_nn)
            with open(predictions_file, 'a') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(predictions_row)

        # вычислим ошибки в предсказаниях NN
        nn_position_error = np.linalg.norm(make_prediction.pos_nn - ekf_position)
        nn_velocity_error = np.linalg.norm(vel_nn - ekf_velocity)

        # Публикуем положение и скорость NED EKF
        ned_ekf = PosVel()
        ned_ekf.header.stamp = rospy.Time.now()
        ned_ekf.header.frame_id = "fcu"
        ned_ekf.position.x = ekf_position[0]
        ned_ekf.position.y = ekf_position[1]
        ned_ekf.position.z = ekf_position[2]
        ned_ekf.velocity.x = ekf_velocity[0]
        ned_ekf.velocity.y = ekf_velocity[1]
        ned_ekf.velocity.z = ekf_velocity[2]

        # Публикуем положение, скорость, ошибки NN
        one_prediction = ImuNavPrediction()
        one_prediction.header.stamp = rospy.Time.now()
        one_prediction.header.frame_id = "fcu"
        one_prediction.position.x = make_prediction.pos_nn[0]
        one_prediction.position.y = make_prediction.pos_nn[1]
        one_prediction.position.z = make_prediction.pos_nn[2]
        one_prediction.velocity.x = vel_nn[0]
        one_prediction.velocity.y = vel_nn[1]
        one_prediction.velocity.z = vel_nn[2]
        one_prediction.position_error_3d = nn_position_error
        one_prediction.velocity_error_3d = nn_velocity_error

        # время одного предсказания
        inference_time = timeit.default_timer() - inference_start_time
        one_prediction.inference_time = inference_time

        # публикуем предсказания и EKF
        nn_predictions_pub.publish(one_prediction)
        ned_ekf_pub.publish(ned_ekf)
        
        print("\ninference_time : ", inference_time)

def window_maintainer(time_float):


    # if any sensor haven't sent measurements, return
    if counters["imu"] == 0 or counters["mag"] == 0 or counters["alt"] == 0:
        return

    # if this is the first altitude averaging, use zero, or else apply differencing
    if features["h_0"] is None:
        features["h_0"] = features["h"] / counters["alt"]
        altitude_difference = 0.0
    else:
        features["h"] = features["h"] / counters["alt"]
        altitude_difference = features["h"] - features["h_0"]
        features["h_0"] = features["h"]
        

    # construct a features vector by averaging every sensor measurement
    # Note that Magnetic field is received in Teslas, but saved in the logs in Gauss (on which the NN was trained),
    # so it must be multiplied by 10000 to convert it to gauss
    # also the y & z body axes in mavros are defined in the opposite directions to those saved in logs
    # so we must negate them (Forward-Left-Up -> Forward-Right-Down)
    features_row = [features["w_x"] / counters["imu"],     - features["w_y"] / counters["imu"],     - features["w_z"] / counters["imu"], 
                    features["a_x"] / counters["imu"],     - features["a_y"] / counters["imu"],     - features["a_z"] / counters["imu"], 
                    features["m_x"]/counters["mag"]*10000, - features["m_y"]/counters["mag"]*10000, - features["m_z"]/counters["mag"]*10000, 
                    altitude_difference
                    ]

    if SAVE_FEATURES:
        # save the features to compare them to those obtained from the ulg file (for debugging)
        with open(features_labels_file, 'a') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(features_row + list(ekf_velocity) + list(ekf_position))
    
    # add this features vector to the window queue
    window.put(features_row)

    print("________________________________")
    print("window size: ", window.qsize(), "counters:", counters)

    # reset the counters and the running sums of sensor measurements (start new averaging interval)
    for key in features.keys():
        if key != "h_0":
            features[key] = 0.0

    for key in counters.keys():
        counters[key] = 0
    
    # if we have enough window to perform one prediction
    if window.qsize() > window_size:
        # remove the oldest time step from the window queue
        window.get()
        # convert the queue to a suitable format for publishing, defined in the msg format
        window_arr = [PythonList(e) for e in window.queue]
        # Publish the window as a ListOfLists struct
        features_window_pub.publish(window_arr)

# добавляем новые измерения датчиков
def sensors_callback(data, sensor_name):
    if sensor_name == "imu":
        features["w_x"] += data.angular_velocity.x
        features["w_y"] += data.angular_velocity.y
        features["w_z"] += data.angular_velocity.z
        features["a_x"] += data.linear_acceleration.x
        features["a_y"] += data.linear_acceleration.y
        features["a_z"] += data.linear_acceleration.z
        counters["imu"] += 1
    
    elif sensor_name == "mag":
        features["m_x"] += data.magnetic_field.x
        features["m_y"] += data.magnetic_field.y
        features["m_z"] += data.magnetic_field.z
        counters["mag"] += 1
    
    elif sensor_name == "alt":
        # altimeter is notorious for sending NaN every now and then
        if np.isnan(data.amsl):
            features["h"] += features["h"]
        else:
            features["h"] += data.amsl
        
        counters["alt"] += 1
    
    elif sensor_name == "ekf_position":
        # ROS uses ENU frame while px4 ulg uses NED, so switch x & y and negate z
        ekf_position[0] = data.pose.position.y
        ekf_position[1] = data.pose.position.x
        ekf_position[2] = -data.pose.position.z
    
    elif sensor_name == "ekf_velocity":
        ekf_velocity[0] = data.twist.linear.y
        ekf_velocity[1] = data.twist.linear.x
        ekf_velocity[2] = -data.twist.linear.z

def sensors_listener():
    """
    a rospy node that subscribes to sensor measurements and spins to keep
    the code running
    """
    print("initializing sensors_listener node")

    rospy.init_node('sensors_listener')
    
    # subscribe to sensors' topics, a subscriber is initialized by (topic, msg_type, callback_fn)
    _ = rospy.Subscriber('mavros/imu/data', Imu, sensors_callback, "imu", queue_size=100)
    _ = rospy.Subscriber('mavros/imu/mag', MagneticField, sensors_callback, "mag", queue_size=100)
    _ = rospy.Subscriber('mavros/altitude', Altitude, sensors_callback, "alt", queue_size=100)

    # subscribe to window maintainer and nn_predictor
    _ = rospy.Subscriber('imu_nav/sensors_ts', Float64, window_maintainer, queue_size=15)
    _ = rospy.Subscriber('imu_nav/features_window', ListOfLists, make_prediction, queue_size=15)
    
    # subscribe to EKF local position and velocity, used to calculate error
    # and to align initial states
    _ = rospy.Subscriber('mavros/local_position/pose', PoseStamped, sensors_callback, "ekf_position", queue_size=100)
    _ = rospy.Subscriber('mavros/local_position/velocity_local', TwistStamped, sensors_callback, "ekf_velocity", queue_size=100)

    print("you can start publishing mavros sensor messages now")

    # call the window maintaner at a fixed rate of 5 Hz
    window_maintainer_rate = 5
    rate = rospy.Rate(window_maintainer_rate)
    while not rospy.is_shutdown():
        windowing_invoker_pub.publish(time.time())
        rate.sleep()

    rospy.spin()

if __name__=='__main__':

    """
    Code entry, initialize the features and counters, create a queue to hold the
    features windw, load the NN keras model, create publishers for the Network
    inputs and outputs
    """
    
    # read script call arguments
    trial_number = sys.argv[1]
    window_size = int(sys.argv[2])

    # change the working directory to this script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # This produces a csv file similar to that obtained from a saved ulg file (for comparison)
    SAVE_FEATURES = True
    # This saves the realtime predictions to compare to the predictions made offline from logs 
    SAVE_PREDICTIONS = True

    # dictionaries "features" & "counters", np arrays "ekf_position" & "ekf_velocity"
    # and queue "window" are all global variables, and are better replaced by class data
    # members by rewriting this script as a class

    # initial values for the running sums and counters (used to average sensor data)
    features = {"w_x" : 0.0, "w_y" : 0.0, "w_z" : 0.0,
                "a_x" : 0.0, "a_y" : 0.0, "a_z" : 0.0,
                "m_x" : 0.0, "m_y" : 0.0, "m_z" : 0.0,
                "h_0" : None,  "h" : 0.0
                }
    
    counters = {"imu" : 0, "mag" : 0, "alt" : 0}

    ekf_position = np.zeros((3,))
    ekf_velocity = np.zeros((3,))

    # create a queue to hold the features vectors as a fixed size window
    window = queue.Queue(maxsize=window_size + 2)

    # load the pretrained Tensorflow SavedModel to make predictions
    print("loading Tensorflow model ...")
    trial_folder = os.path.join(os.path.pardir, "results", "trial_" + str(trial_number).zfill(3))
    tf_model_path = os.path.join(trial_folder, "tf_saved_model") 
    model = tf.keras.models.load_model(tf_model_path)

    # create a static variable to hold the states, predictions are delta states
    # and should be accumulated to the states vector
    make_prediction.pos_nn = None

    # a ros parameter to programmatically enable/disable inference
    rospy.set_param("/imu_nav/enable_inference", True)
    # a ros parameter to programmatically reset NN predictions to ekf
    rospy.set_param("/imu_nav/reset_nn", False)   
  
    # a publisher to invoke the window_maintainer callback
    windowing_invoker_pub = rospy.Publisher('imu_nav/sensors_ts', Float64, queue_size=15)
    # a publisher to invoke the NN inference callback
    features_window_pub = rospy.Publisher('imu_nav/features_window', ListOfLists, queue_size=15)
    # a publisher to publish the NN predictions
    nn_predictions_pub = rospy.Publisher('imu_nav/nn_predictions', ImuNavPrediction, queue_size=15)
    # a publisher for the NED EKF states to compare to the NN
    ned_ekf_pub = rospy.Publisher('imu_nav/ned_ekf', PosVel, queue_size=15)

    # create directory to save realtime features, labels, and predictions
    realtime_out_folder = os.path.join(trial_folder, "realtime_inference")
    if not os.path.isdir(realtime_out_folder) :
        os.makedirs(realtime_out_folder)
    
    # files creation timestamp to their names
    files_creation_time = "_" + datetime.datetime.now().strftime("%d%b%Y") + \
                          "_" + datetime.datetime.now().strftime("%H%M")

    features_labels_file = os.path.join(realtime_out_folder, "realtime_features_labels" + files_creation_time + ".csv")
    predictions_file = os.path.join(realtime_out_folder, "realtime_predictions" + files_creation_time + ".csv")

    with open(features_labels_file, 'w') as f:
        csv_header = "w_x,w_y,w_z,a_x,a_y,a_z,m_x,m_y,m_z,h,Vn,Ve,Vd,Pn,Pe,Pd\n"
        f.write(csv_header)
    with open(predictions_file, 'w') as f:
        csv_header = "Vn,Ve,Vd,Pn,Pe,Pd\n"
        f.write(csv_header)

    # start the node
    sensors_listener()
