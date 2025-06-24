import os
import pandas as pd
import numpy as np
from scipy import interpolate

# Пути к папкам
input_dir = "../data/combined_csvs/trimmed"
output_dir = "../data/combined_csvs/interpolated_30hz"

# Создаем папку для результатов, если её нет
os.makedirs(output_dir, exist_ok=True)

# Колонки для интерполяции (все кроме времени, если оно есть)
columns = ["w_x", "w_y", "w_z", "a_x", "a_y", "a_z", 
           "m_x", "m_y", "m_z", "h", "T", 
           "q0", "q1", "q2", "q3", 
           "Vn", "Ve", "Vd", "Pn", "Pe", "Pd"]

# Проход по всем файлам в папке trimmed
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Чтение данных
        df = pd.read_csv(input_path, sep='\t' if '\t' in open(input_path).readline() else ',')
        
        # Проверка, что данные не пустые
        if len(df) < 2:
            print(f"Файл {filename} слишком короткий для интерполяции. Пропускаем.")
            continue
        
        # Создание временной оси (5 Гц → 30 Гц)
        t_original = np.linspace(0, len(df) / 5, len(df))  # Время в секундах для 5 Гц
        t_new = np.linspace(0, len(df) / 5, 6 * len(df))   # Новая временная сетка (30 Гц)
        
        # Интерполяция данных
        df_interpolated = pd.DataFrame()
        for col in columns:
            if col in df.columns:
                # Кубическая интерполяция для плавности
                f = interpolate.interp1d(
                    t_original, 
                    df[col], 
                    kind='cubic', 
                    fill_value="extrapolate"
                )
                df_interpolated[col] = f(t_new)
            else:
                print(f"Колонка {col} отсутствует в файле {filename}")
        
        # Сохранение результата
        df_interpolated.to_csv(output_path, index=False, sep=',')
        print(f"Обработан файл {filename} → {output_path}")

print("Интерполяция завершена!")
