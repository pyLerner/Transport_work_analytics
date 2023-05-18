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

    np.seterr(invalid='ignore')         # Обход деления на ноль
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


def draw_dot_track_to_map(my_map,
                          track_time,
                          track2list,
                          radius=3,
                          fill=True,
                          fill_color='red',
                          color='red',
                          tail_label_color='blue'):
    """
    Отрисовка трека на карте точками.
    :param my_map: folium Map
    :param track_time: Список дат в строковом формате. Список дат в формате datetime также возможен
    :param track2list: Список кортежей или список списков с координатами
    :param radius: радиус круга
    :param fill: закрашивать круг или нет
    :param fill_color: каким цветом закрашивать
    :param color: цвет круга
    :param tail_label_color: цвет метки в начальной и конечной точках
    len(trac2list) == len(track_time)
    :return: None

    ## Примеры
    # Рисование иконок геопозиции
    for coordinates in track:
        folium.Marker(location=coordinates, icon=folium.Icon(color='green')).add_to(my_map)


    # Метки для НП/КП (Начало и конец трека)
    for coordination, times in zip([track2list[0], track2list[-1]],
                                   [track_time[0], track_time[-1]]):

        folium.Marker(location=coordination,
                      icon=folium.Icon(color='blue'),
                      tooltip=folium.Tooltip(times,       # Любит строку, но с datetime тоже работает
                                             sticky=False,
                                             permanent=True
                                             )
                      ).add_to(my_map)


    # Трасса маршрута в полилиниях
    folium.PolyLine(track, tooltip=folium.Tooltip("text",
                                               sticky=False,    # не прилипает к курсору
                                               permanent=True,  # отображается всегда
                                        #      style='background-color:grey'
                                                  )
                    ).add_to(my_map)


    # Рисуем трек красными кружками:
    for times, coordinate in zip(track_time, track2list):

        folium.CircleMarker(location=coordinate,
                            color='red',
                            radius=3,
                            tooltip=times,      # Программа ожидает строку, но с datetime работает
                            fill=True,
                            fill_color='red'
                            ).add_to(my_map)


    # Одиночная координата:
    # location = tuple or list
    folium.CircleMarker(location=location,
                        color='red',
                        radius=4,
                        tooltip=location,
                        fill=True,
                        fill_color='red').add_to(my_map)

    """

    # Метки для НП/КП (Начало и конец трека)
    for coordination, times in zip([track2list[0], track2list[-1]],
                                   [track_time[0], track_time[-1]]):
        folium.Marker(location=coordination,
                      icon=folium.Icon(color=tail_label_color),
                      tooltip=folium.Tooltip(times,  # В иделе сюда подавать строку, но datetime тоже работает
                                             sticky=False,
                                             permanent=True
                                             )
                      ).add_to(my_map)

    # Трек точками
    for times, coordinate in zip(track_time, track2list):
        folium.CircleMarker(location=coordinate,
                            color=color,
                            radius=radius,
                            tooltip=times,  # Программа ожидает строку, но с datetime работает
                            fill=fill,
                            fill_color=fill_color
                            ).add_to(my_map)


def draw_polyline_trip_track(my_map,
                             track,
                             color='blue',
                             tooltip_text=None):

    """
    :param my_map:  folium Map
    :param track: список кортежей или списков с координатами
    :param color: цвет полилиний трека
    :param tooltip_text: текст в текстовой метке

    :return: None
    """

    # Метки для НП/КП
    for coordination in [track[0], track[-1]]:
        folium.Marker(location=coordination,
                      icon=folium.Icon(color=color)
                      ).add_to(my_map)

    # Трасса маршрута
    folium.PolyLine(track, tooltip=folium.Tooltip(tooltip_text,
                                                  sticky=False,  # не прилипает к курсору
                                                  permanent=True  # отображается всегда
                                                  #          style='background-color:grey'
                                                  )
                    ).add_to(my_map)


if __name__ == "__main__":
    pass

    # Пример работы на реальных файлах:

    # log_file = 'SEKOP_LOGS/20230218015411-logs.csv.tar.gz'
    # log_file = 'SEKOP_LOGS/019_20220408.csv'
    # log_file = 'SEKO P_LOGS/204_20230218.csv'
    # log_file = 'SEKOP_LOGS/019_20220408.csv'
    log_file = 'SEKOP_LOGS/020_20220408.csv'

    # Получение массива данных  NMEA из лога
    nmea_track = extract_nmea_from_log(log_file)

    # Преобразование  времени в datetime
    track_time = track_time_to_datetime(nmea_track[:, 0])

    # Пересчитываем координаты в десятичные градусы
    track = nmea_coordinates_to_degrees(nmea_track)[:, 1:3]

    # Приведение к виду для загрузки в leaflet/foliant:
    track2list = track.tolist()

    # Инициализация карты с центром в начальной точке трека
    # my_map = folium.Map(
    #     location=track2list[0],
    #     zoom_start=12
    # )

    # Среднее арифметическая координата всех точек трека
    # mean_track_dot = track.mean(axis=0).tolist()
    # Центрирование карты в точке среднеарифметического значений трека
    # my_map = folium.Map(
    #     location=mean_track_dot,
    #     zoom_start=12
    # )

    # Параметры баундингбокса
    bottom_right = [
        track.max(axis=0)[0],
        track.min(axis=0)[1]
    ]

    top_left = [
        track.min(axis=0)[0],
        track.max(axis=0)[1]
    ]

    # Центр баундингбокса
    center_dot = (np.array(bottom_right) + np.array(top_left)) / 2
    center_dot = center_dot.tolist()

    # Центрирование карты в центре баундингбокса
    my_map = folium.Map(location=center_dot)

    # Отрисовка трека точками
    draw_dot_track_to_map(my_map, track_time, track2list)

    # Трек линиями
    draw_polyline_trip_track(my_map, track2list)

    # Автомасштаб по границам баундингбокса
    my_map.fit_bounds(
        [bottom_right, top_left],
        padding=top_left  # Отступы по краям (не понятно в каких единицах)
    )

    # Генерируем HTML страницу
    file = 'map.html'
    file = my_map.save(file)
