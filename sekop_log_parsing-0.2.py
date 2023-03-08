"""
Программа парсит  из log БО СЭКОП данные в формате NMEA 0183.
Переводит данные в формат для отображения на карте и строит интерактивную карту в HTML
Входные данные - запакованный лог БО СЭКОП.
Результат выполнения - страница HTML с треком
"""

import numpy as np
import pandas as pd
import folium
import datetime


def extract_nmea_from_log(log):
    """
    Принимает log.csv.tar.gz без предварительной распаковки.
    Возвращает numpy массив с данными NMEA. Тип данных float.
    Матрица состоит из 5 столбцов: время, широта, долгота, скорость, путевой угол в формате NMEA 0183
    :param log:
    :return: numpy.array.dtype(float)
    """

    geo = pd.read_csv(log, sep=';', header=None, on_bad_lines='skip')
    geo = geo[geo[4] == ' geo '][[0, 1, 5]]  # Оставили только строки с NMEA, столбцы с датой, временем, NMEA

    """
    На всякий случай оставлены столбцы 0 - дата, 1 - время записи строки в логе. Может пригодиться для анализа 
    точного время
    """

    geo_list = geo[5].str.findall(r'\d+\.\d+').to_list()  # Список  чисел с плавающей точкой из строки в столбце 5
    return np.array(geo_list).astype(float)


def nmea_coordinates_to_degrees(nmea_array):
    """
    Перевод строковых значений NMEA в градусы
    :param nmea_array:
    :return: ndarray.astype(float)
    """

    int_degrees = nmea_array // 100      # Целая часть
    nmea_minutes = (nmea_array / 100) % int_degrees      # Мантисса
    float_degrees = nmea_minutes * 5 / 3        # Перевод из минут в десятичную дробь *100/60

    out = int_degrees + float_degrees
    return out


def track_time_to_datetime(nmea_time):
    """
    Перевод времени NMEA в datetime
    :param nmea_time: numpy array [n, 1]
    :return: datetimes list
    """

    hours = nmea_time // 10000                              # Часы в UTC
    minutes = nmea_time // 100 % 100                        # Минуты
    seconds = nmea_time % (hours * 10000 + minutes * 100)   # Секунды
    hours = (hours + 3) % 24                                # GMT+3 !!!

    out = [datetime.time(int(hours[i]),
                         int(minutes[i]),
                         int(seconds[i]))
           for i in range(hours.shape[0])
           ]

    # print(out)
    return out


# log_file = 'SEKOP_LOGS/20230218015411-logs.csv.tar.gz'
# log_file = 'SEKOP_LOGS/204_20230218.csv'
log_file = 'SEKOP_LOGS/019_20220408.csv'
# log_file = 'SEKOP_LOGS/020_20220408.csv'


# Получение массива данных  NMEA из лога
nmea_track = extract_nmea_from_log(log_file)

# Преобразование  времени в datetime
track_time = track_time_to_datetime(nmea_track[:, 0])

# Пересчитываем координаты в десятичные градусы
track = nmea_coordinates_to_degrees(nmea_track)[:, 1:3]


# Приведение к виду для загрузки в leaflet/foliant:
track2list = track.tolist()

# Инициализация карты в начальной точке трассы (АС)
my_map = folium.Map(location=track2list[0], zoom_start=12)


# Рисование иконок геопозиции
# for coordinates in track:
#     folium.Marker(location=coordinates, icon=folium.Icon(color='green')).add_to(my_map)


# Метки для НП/КП (Начало и конец трека)
for coordination, times in zip([track2list[0], track2list[-1]],
                               [track_time[0], track_time[-1]]):

    folium.Marker(location=coordination,
                  icon=folium.Icon(color='blue'),
                  tooltip=folium.Tooltip(times,       # В иделе сюда подавать строку, но datetime тоже работает
                                         sticky=False,
                                         permanent=True
                                         )
                  ).add_to(my_map)


# Трасса маршрута в полилиниях
# folium.PolyLine(track, tooltip=folium.Tooltip("3-й Парк",
#                                            sticky=False,    # не прилипает к курсору
#                                            permanent=True,  # отображается всегда
#                                     #      style='background-color:grey'
#                                               )
#                 ).add_to(my_map)


# Рисуем трек красными кружками:
for times, coordinate in zip(track_time, track2list):

    folium.CircleMarker(location=coordinate,
                        color='red',
                        radius=3,
                        tooltip=times,      # Программа ожидает строку, но с datetime работает
                        fill=True,
                        fill_color='red'
                        ).add_to(my_map)


# Одиночная координата
# location = track[15]
# folium.CircleMarker(location=location,
#                     color='red',
#                     radius=4,
#                     tooltip=location,
#                     fill=True,
#                     fill_color='red').add_to(my_map)

file = 'map.html'
file = my_map.save(file)
