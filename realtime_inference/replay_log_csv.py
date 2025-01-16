#!/usr/bin/env python

import os
import sys
import pandas as pd
import rospy
from geometry_msgs.msg import PoseStamped, TwistStamped
from sensor_msgs.msg import Imu, MagneticField
from mavros_msgs.msg import Altitude

def ulg_sensors_broadcaster():
    rospy.init_node('ulg_sensors_broadcaster')

    # будем публиковать с заданной частотой
    broadcasting_rate = imu_rate
    rate = rospy.Rate(broadcasting_rate)
   
    while not rospy.is_shutdown():
        for message_name, message in messages.items():
            idx = message["iterator"]
            # print(message_name, idx)
            if idx == message["length"]:
                print("published all data in the csv files, exiting")
                exit()

            if message_name == "imu":
                message["timestamp"] = message["timestamps"][idx] 
                row = message["data"][message["iterator"],:] 
                
                one_msg = Imu()
                one_msg.angular_velocity.x = row[0]
                one_msg.angular_velocity.y = -row[1]
                one_msg.angular_velocity.z = -row[2]
                one_msg.linear_acceleration.x = row[3]
                one_msg.linear_acceleration.y = -row[4]
                one_msg.linear_acceleration.z = -row[5]

                message["iterator"] += 1

                imu_pub.publish(one_msg)

            else:
                sensor_ts = message["timestamps"][idx]
                
                if sensor_ts <= messages["imu"]["timestamp"]:
                    row = message["data"][message["iterator"],:]
                    if message_name == "mag":
                        one_msg = MagneticField()
                        one_msg.magnetic_field.x = row[0] / 10000.0 # перейти от Гаусса к Тесле
                        one_msg.magnetic_field.y = -row[1] / 10000.0 # оси y и z в мавросе противоположны логам
                        one_msg.magnetic_field.z = -row[2] / 10000.0
                        mag_pub.publish(one_msg)

                    elif message_name == "baro":
                        one_msg = Altitude()
                        one_msg.amsl = row[0]
                        baro_pub.publish(one_msg)

                    elif message_name == "ekf":
                        # В ROS используется рамка ENU, а в px4 ulg - NED, поэтому меняем местами x и y и отриньте z.
                        one_msg_vel = TwistStamped()
                        one_msg_vel.twist.linear.x = row[1]
                        one_msg_vel.twist.linear.y = row[0]
                        one_msg_vel.twist.linear.z = -row[2]
                        ekf_vel_pub.publish(one_msg_vel)

                        one_msg_pos = PoseStamped()
                        one_msg_pos.pose.position.x = row[4]
                        one_msg_pos.pose.position.y = row[3]
                        one_msg_pos.pose.position.z = -row[5]
                        ekf_pos_pub.publish(one_msg_pos)

                    message["iterator"] += 1

        rate.sleep()

    rospy.spin()

if __name__=='__main__':

    log_folder = sys.argv[1]

    messages = {"ekf" : {"file" : '_estimator_status',     "cols" : ["states["+str(i)+"]" for i in range(4,10)]},

                "mag" : {"file" : '_vehicle_magnetometer', "cols" : ["magnetometer_ga["+str(i)+"]" for i in range(3)]},

                "baro": {"file" : '_vehicle_air_data',     "cols" : ["baro_alt_meter"]},

                "imu" : {"file" : '_sensor_combined',      "cols" : ["gyro_rad["+str(i)+"]" for i in range(3)] + \
                                                                    ["accelerometer_m_s2["+str(i)+"]" for i in range(3)]},
                }

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # каталог csv журнала для воспроизведения
    base_name = os.path.join(os.path.pardir, "data", "flight_csvs", log_folder, log_folder)

    for message in messages.values():
        file_name = base_name + message["file"] + "_0.csv"
        message["timestamps"] = pd.read_csv(file_name, usecols=["timestamp"]).to_numpy().squeeze()
        message["data"] = pd.read_csv(file_name, usecols=message["cols"])[message["cols"]].to_numpy()
        message["iterator"] = 0
        message["length"] = message["data"].shape[0]

    messages["imu"]["timestamp"] = 0

    # чтение csv файлов в словарь сообщений
    for message_name, message in messages.items():
        file_name = base_name + message["file"] + "_0.csv"
        message["timestamps"] = pd.read_csv(file_name, usecols=["timestamp"]).to_numpy().squeeze()
        message["data"] = pd.read_csv(file_name, usecols=message["cols"])[message["cols"]].to_numpy()
        message["iterator"] = 0
        message["length"] = message["data"].shape[0]

    # imu timestep, используется в трансляции измерений датчиков (иммитация работы в реальном времени)
    imu_dt = messages["imu"]["timestamps"][2] - messages["imu"]["timestamps"][1]
    imu_rate = 1.0 / imu_dt * 1000000 # микросекунды в секунду
    imu_rate = round(imu_rate) 
    
    log_duration_minutes = messages["imu"]["timestamps"].shape[0] / imu_rate / 60
    print("imu timestep = ", imu_dt, " microseconds, imu rate = ", imu_rate, " Hz")
    print("this log will replay for ", f'{log_duration_minutes:.2f}', " minutes")

    # паблишеры для измерений датчиков, полученных из csv
    imu_pub = rospy.Publisher('mavros/imu/data', Imu, queue_size=1)
    mag_pub = rospy.Publisher('mavros/imu/mag', MagneticField, queue_size=1)
    baro_pub = rospy.Publisher('mavros/altitude', Altitude, queue_size=1)
    ekf_pos_pub = rospy.Publisher('mavros/local_position/pose', PoseStamped, queue_size=1)
    ekf_vel_pub = rospy.Publisher('mavros/local_position/velocity_local', TwistStamped, queue_size=1)

    # стартуем :)
    print("mavros messages are now being published")
    ulg_sensors_broadcaster()
