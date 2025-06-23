Проект нейронной сети для полета по инерциальной навигации.
(рабочий)


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



Обучение:
1. скачиваем датасеты ./logs_downloader.py в папку ulg_files
2. конвертируем в csv ./ulog2csv.py в папке flight_csvs
3. объединяем CSV-файлы каждого журнала в один CSV-файл в папке combined_csvs
4. уберем дубликаты и плохие графики ./manual_trimmer.py, результат занесем в папку trimmed в папке combined_csvs
5. разделим датасет на training и validation (85% : 15%) - создаст две папки training и validation в папке trimmed и перенесет туда файлы с предыдущего шага
5. теперь можно проводить обучение сети с помощью ./imu_nav.py - сохраненная модель с весами будет в results/trial_NExp
