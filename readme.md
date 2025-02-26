Проект нейронной сети для полета по инерциальной навигации.



1. Обученная нейронная сеть находится в папке results
2. Образцы журналов находятся в папке data



Запуск:

1. roscore
2. source devel/setup.bash
3. cd imu_nav_ml/realtime_inference
4. ./run_inference.py 6 100
5. cd imu_nav_ml/realtime_inference
6. ./replay_log_csv.py 0057_5.12
7. cd imu_nav_ml/realtime_inference
8. plotjuggler-ros -n -l PlotJuggler_layout.xml