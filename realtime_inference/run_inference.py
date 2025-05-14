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

start_time = time.time()
start_time_window_pub = time.time()
start_time_imu = time.time()
start_time_mag = time.time()
start_time_alt = time.time()
start_time_ekf_position = time.time()
start_time_ekf_velocity = time.time()

UPDATE_RATE = 5
ekf_position_is_updated = False
ekf_velocity_is_updated = False

nn_position_error = 0
nn_velocity_error = 0

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

# использует окно признаков для 1 предсказания (100 samples * 10 features)
# и публикует лист с предсказанием [Pn, Pe, Pd, Vn, Ve, Vd]
# публикует и выводит время 1 предсказания
def make_prediction(data):

    # время вывода записи
    inference_start_time = timeit.default_timer()

    global start_time
    global ekf_position_is_updated
    global ekf_velocity_is_updated
    global nn_position_error
    global nn_velocity_error

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



        # print("type(data): ", type(data))

        # преобразуем опубликованную структуру ListOfLists в список списков Python (двумерный список)
        window_list = [e.row for e in data.matrix]

        # print("type(window_list): ", type(window_list))
        
        # преобразуем 2D-список в np.array
        window_arr = np.array(window_list, dtype=np.float32)
        print("!window_arr.size: ", window_arr.size)
        
        # изменим его форму, чтобы он был совместим с сетевым вводом (размер пакета, временные шаги, n_features)
        window_arr = np.resize(window_arr, (1,window_size,10))
        print("window_arr.shape: ", window_arr.shape)
        
        # предсказываем метки (изменения положения в NED) и аккумулируем их в положении
        delta_position = model.predict(window_arr, batch_size=1).reshape((3,))
        print("delta_position.shape: ", delta_position.shape)
        make_prediction.pos_nn += delta_position

        dt = 1 / UPDATE_RATE
        vel_nn = delta_position / dt

        if SAVE_PREDICTIONS:
            # сохраним прогнозы для сравнения    
            predictions_row = list(vel_nn) + list(make_prediction.pos_nn)
            with open(predictions_file, 'a') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(predictions_row)

        if ekf_position_is_updated:
            nn_position_error = np.linalg.norm(make_prediction.pos_nn - ekf_position)
            ekf_position_is_updated = False
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if ekf_velocity_is_updated:
            nn_velocity_error = np.linalg.norm(vel_nn - ekf_velocity)
            ekf_velocity_is_updated = False
        else:
            print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")

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

        print("123 inference_time: ", inference_time)

        # публикуем предсказания и EKF  # 5 Hz
        nn_predictions_pub.publish(one_prediction)
        ned_ekf_pub.publish(ned_ekf)

        print(f"Время между замерами 666: {1/(time.time() - start_time)} Гц")
        start_time = time.time()

        run_inference_csv = os.path.join("run_inference_results", "trial_" + str(trial_number).zfill(3), "run_inference_result.csv")
        colum_names = {"top_view" : ["ekf_x", "ekf_y", "ekf_z", "nn_x", "nn_y", "nn_z"],
                       "velocity" : ["ekf_vx", "ekf_vy", "ekf_vz", "nn_vx", "nn_vy", "nn_vz"],
                       "errors"   : ["pose_error_3d", "velocity_error_3d"]}

        # Подготовка данных для записи в CSV
        data_to_log = {
            'timestamp': datetime.datetime.now().isoformat(),
            'ekf_x': ekf_position[0],
            'ekf_y': ekf_position[1],
            'ekf_z': ekf_position[2],
            'nn_x': make_prediction.pos_nn[0],
            'nn_y': make_prediction.pos_nn[1],
            'nn_z': make_prediction.pos_nn[2],
            'ekf_vx': ekf_velocity[0],
            'ekf_vy': ekf_velocity[1],
            'ekf_vz': ekf_velocity[2],
            'nn_vx': vel_nn[0],
            'nn_vy': vel_nn[1],
            'nn_vz': vel_nn[2],
            'pose_error_3d': nn_position_error,
            'velocity_error_3d': nn_velocity_error
        }

        # Определяем порядок столбцов на основе colum_names
        column_order = ['timestamp']  # добавляем временную метку
        for category in colum_names.values():
            column_order.extend(category)

        # Убеждаемся, что директория существует
        ensure_dir(run_inference_csv)

        write_to_csv(run_inference_csv, data_to_log, column_order)
        
        # print("\ninference_time : ", inference_time)

# вызывается с частотой в 5 Гц
def window_maintainer(time_float):

    global start_time
    global start_time_window_pub

    # print(f"Время между замерами: {time.time() - start_time:.4f} секунд")
    # start_time = time.time()

    # если никто не отправил новые измерения, выходим
    if counters["imu"] == 0 or counters["mag"] == 0 or counters["alt"] == 0:
        return

    # если это первое усреднение по высоте, используем нулевое значение, иначе дифферинцирование
    if features["h_0"] is None:
        features["h_0"] = features["h"] / counters["alt"]
        altitude_difference = 0.0
    else:
        features["h"] = features["h"] / counters["alt"]
        altitude_difference = features["h"] - features["h_0"]
        features["h_0"] = features["h"]
        
    # построим вектор признаков путем усреднения каждого измерения датчика
    # магнитное поле принимается в теслах, но сохраняется в журналах в гауссах (на которых обучалась NN),
    # поэтому его нужно умножить на 10000, чтобы преобразовать в гауссы
    # также оси тела y и z в mavros определены в противоположных направлениях к сохраненным в журналах
    # поэтому мы должны инвертировать их (вперед-влево-вверх -> вперед-вправо-вниз)
    features_row = [features["w_x"] / counters["imu"],     - features["w_y"] / counters["imu"],     - features["w_z"] / counters["imu"], 
                    features["a_x"] / counters["imu"],     - features["a_y"] / counters["imu"],     - features["a_z"] / counters["imu"], 
                    features["m_x"]/counters["mag"]*10000, - features["m_y"]/counters["mag"]*10000, - features["m_z"]/counters["mag"]*10000, 
                    altitude_difference
                    ]

    if SAVE_FEATURES:
        # сохраняем вектор признаков для дебага
        with open(features_labels_file, 'a') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(features_row + list(ekf_velocity) + list(ekf_position))
    
    # добавляем этот вектор признаков в окно
    window.put(features_row)

    print("________________________________")
    print("window size: ", window.qsize(), "counters:", counters)

    # print("before\n", "features:", features, "\ncounters:", counters)

    # запуск нового интервала усреднения
    for key in features.keys():
        if key != "h_0":
            features[key] = 0.0

    for key in counters.keys():
        counters[key] = 0

    # print("features:", features, "\ncounters:", counters)
    
    # если у нас достаточно окна для одного предсказания
    if window.qsize() > window_size:
        # удаляем самый старый элемент очереди
        window.get()
        # конвертируем очередь в список списков
        window_arr = [PythonList(e) for e in window.queue]
        # публикуем окно
        features_window_pub.publish(window_arr)

        # print("type(window_arr): ", type(window_arr))

        end_time_window_pub = time.time()  # Засекаем конечное время
        execution_time_window_pub = end_time_window_pub - start_time_window_pub
        start_time_window_pub = time.time()
        # print(window.qsize())
        # print(f"Время между вызовом features_window_pub.publish: {execution_time_window_pub:.4f} секунд")



# добавляем новые измерения датчиков
def sensors_callback(data, sensor_name):

    global start_time
    global ekf_position_is_updated
    global ekf_velocity_is_updated

    if sensor_name == "imu":        # 250 Hz
        features["w_x"] += data.angular_velocity.x
        features["w_y"] += data.angular_velocity.y
        features["w_z"] += data.angular_velocity.z
        features["a_x"] += data.linear_acceleration.x
        features["a_y"] += data.linear_acceleration.y
        features["a_z"] += data.linear_acceleration.z
        counters["imu"] += 1
        # print("!!!counters:", counters)
    
    elif sensor_name == "mag":      # 50 Hz
        features["m_x"] += data.magnetic_field.x
        features["m_y"] += data.magnetic_field.y
        features["m_z"] += data.magnetic_field.z
        counters["mag"] += 1
    
    elif sensor_name == "alt":      # 80 Hz
        if not np.isnan(data.amsl):
            features["h"] += data.amsl
            counters["alt"] += 1
    
    elif sensor_name == "ekf_position":         # 5 Hz
        ekf_position[0] = data.pose.position.y
        ekf_position[1] = data.pose.position.x
        ekf_position[2] = -data.pose.position.z
        ekf_position_is_updated = True
    
    elif sensor_name == "ekf_velocity":         # 5 Hz
        ekf_velocity[0] = data.twist.linear.y
        ekf_velocity[1] = data.twist.linear.x
        ekf_velocity[2] = -data.twist.linear.z
        ekf_velocity_is_updated = True

# основная функция программы
def sensors_listener():
    print("initializing sensors_listener node")

    rospy.init_node('sensors_listener')
    
    # подписчики на топики датчиков
    _ = rospy.Subscriber('mavros/imu/data', Imu, sensors_callback, "imu", queue_size=100)
    _ = rospy.Subscriber('mavros/imu/mag', MagneticField, sensors_callback, "mag", queue_size=100)
    _ = rospy.Subscriber('mavros/altitude', Altitude, sensors_callback, "alt", queue_size=100)

    # подписчики на window maintainer и nn-предсказатель
    _ = rospy.Subscriber('imu_nav/sensors_ts', Float64, window_maintainer, queue_size=15)
    _ = rospy.Subscriber('imu_nav/features_window', ListOfLists, make_prediction, queue_size=15)
    
    # подписчики для ekf навигации
    _ = rospy.Subscriber('mavros/local_position/pose', PoseStamped, sensors_callback, "ekf_position", queue_size=100)
    _ = rospy.Subscriber('mavros/local_position/velocity_local', TwistStamped, sensors_callback, "ekf_velocity", queue_size=100)

    # ожидаем показания датчиков - входы для рекуррентной сети
    print("you can start publishing mavros sensor messages now")

    # call the window maintaner at a fixed rate of UPDATE_RATE Hz
    window_maintainer_rate = UPDATE_RATE
    rate = rospy.Rate(window_maintainer_rate)
    while not rospy.is_shutdown():
        windowing_invoker_pub.publish(time.time())
        rate.sleep()

    rospy.spin()

if __name__=='__main__':
    
    # номер папки с моделью
    trial_number = sys.argv[1]                      # ./run_inference.py 6 100    // 6 папка trial_006

    # размер окна
    window_size = int(sys.argv[2])                  # 100

    # изменим текущую рабочую директорию
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # сохраняем результаты
    SAVE_FEATURES = True
    SAVE_PREDICTIONS = True

    # начальные условия 
    features = {"w_x" : 0.0, "w_y" : 0.0, "w_z" : 0.0,
                "a_x" : 0.0, "a_y" : 0.0, "a_z" : 0.0,
                "m_x" : 0.0, "m_y" : 0.0, "m_z" : 0.0,
                "h_0" : None,  "h" : 0.0
                }
    
    counters = {"imu" : 0, "mag" : 0, "alt" : 0}

    # массивы для ekf позиции и скорости
    ekf_position = np.zeros((3,))
    ekf_velocity = np.zeros((3,))

    # создаем очередь для хранения векторов признаков в виде окна фиксированного размера
    window = queue.Queue(maxsize=window_size + 2)

    # загружаем предварительно обученную сохраненную модель Tensorflow для выполнения прогнозов
    print("loading Tensorflow model ...")
    trial_folder = os.path.join(os.path.pardir, "results", "trial_" + str(trial_number).zfill(3))
    tf_model_path = os.path.join(trial_folder, "tf_saved_model") 
    model = tf.keras.models.load_model(tf_model_path)

    # переменная для хранения состояний; предсказания - дельта состояния и должны быть накоплены в векторе состояний
    make_prediction.pos_nn = None

    # вкл/выкл вывод
    rospy.set_param("/imu_nav/enable_inference", True)
    # сброс прогнозов NN
    rospy.set_param("/imu_nav/reset_nn", False)   
  
    # паблишеры
    windowing_invoker_pub = rospy.Publisher('imu_nav/sensors_ts', Float64, queue_size=15)
    features_window_pub = rospy.Publisher('imu_nav/features_window', ListOfLists, queue_size=15)
    nn_predictions_pub = rospy.Publisher('imu_nav/nn_predictions', ImuNavPrediction, queue_size=15)
    ned_ekf_pub = rospy.Publisher('imu_nav/ned_ekf', PosVel, queue_size=15)

    # создаем директорию для сохранения результатов работы модели: признаков, меток и предсказаний в реальном времени
    realtime_out_folder = os.path.join(trial_folder, "realtime_inference")
    if not os.path.isdir(realtime_out_folder) :
        os.makedirs(realtime_out_folder)
    
    # прикрепляем метку времени создания файлов к их именам
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

    # стартуем :)
    sensors_listener()
