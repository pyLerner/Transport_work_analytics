"""
Программа парсит  из log БО СЭКОП данные в формате NMEA 0183.
Переводит данные в формат для отображения на карте и строит интерактивную карту в HTML
Входные данные - запакованный лог БО СЭКОП.
Результат выполнения - страница HTML с треком
"""
import io

import numpy as np
import pandas as pd
import folium
import datetime
from io import BytesIO


def extract_nmea_from_log(
        log,
        start_time: str = None,
        end_time: str = None
):

    """
    Принимает log.csv.tar.gz без предварительной распаковки.
    Возвращает numpy массив с данными NMEA. Тип данных float.
    Матрица состоит из 5 столбцов: время, широта, долгота, скорость, путевой угол в формате NMEA 0183
    :param log: лог файл СЭКОП
    :param start_time, stop_time: границы временного интервала в ФОРМАТЕ YYYY-mm-dd HH:MM
    :return: numpy.array.dtype(float)
    """

    # log = BytesIO(log)
    geo = pd.read_csv(log, sep=';', header=None, on_bad_lines='skip')
    geo = geo[geo[4] == ' geo '][[0, 1, 5]]  # Оставили только строки с NMEA, столбцы с датой, временем, NMEA

    """
    Оставлены столбцы 0 - дата, 1 - время записи строки в логе. Может пригодиться для анализа 
    точного время
    """

    # Зачищаем ячейки столбца Дата от всех символов, кроме 0-9, '-'
    geo[0].replace(r'[^\d-]', '', regex=True, inplace=True)

    # Зачищаем ячейки столбца Время от всех символов, кроме 0-9, ':'
    geo[1].replace(r'[^\d:]', '', regex=True, inplace=True)

    # Объединяем  столбцы 0 и 1 и в datetime YYYY-mm-dd HH:MM:SS
    geo[0] = pd.to_datetime(geo[0] + " " + geo[1])

    # Если граница не указана, то она принимает крайнее значение:
    if not start_time:
        start_time = geo[0].iloc[0]
    if not end_time:
        end_time = geo[0].iloc[-1]
    else:
        end_time += ":59"     # В период включается вся минута до последней секунды

    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)

    # Отбор строк за период
    geo = geo[(geo[0] >= start_time) & (geo[0] < end_time)]

    # Список чисел с плавающей точкой из строки в столбце 5
    geo_list = geo[5].str.findall(r'\d+\.\d+').to_list()

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


def draw_dot_track_to_map(
        my_map,
        track_time,
        track2list,
        radius=3,
        fill=True,
        fill_color='red',
        color='red',
        tail_label_color='blue'
):
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
    for coordination, times in zip(
            [track2list[0], track2list[-1]],
            [track_time[0], track_time[-1]]
    ):
        folium.Marker(
            location=coordination,
            icon=folium.Icon(color=tail_label_color),

            tooltip=folium.Tooltip(
                times,  # В идеале сюда подавать строку, но datetime тоже работает
                sticky=False,
                permanent=True
            )

        ).add_to(my_map)

    # Трек точками
    for times, coordinate in zip(
            track_time,
            track2list
    ):

        folium.CircleMarker(
            location=coordinate,
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
        folium.Marker(
            location=coordination,
            icon=folium.Icon(color=color)
        ).add_to(my_map)

    # Трасса маршрута
    folium.PolyLine(
        track,
        tooltip=folium.Tooltip(
            tooltip_text,
            sticky=False,  # не прилипает к курсору
            permanent=True  # отображается всегда
            #          style='background-color:grey'
        )
    ).add_to(my_map)

def log2html(
        log_file,
        map_name='map.html',
        start: str = None,
        stop: str = None
):
    # Пример работы на реальных файлах:

    # log_file = 'SEKOP_LOGS/20230218015411-logs.csv.tar.gz'
    # log_file = 'SEKOP_LOGS/019_20220408.csv'
    # log_file = 'SEKO P_LOGS/204_20230218.csv'
    # log_file = 'SEKOP_LOGS/019_20220408.csv'
    # log_file = 'SEKOP_LOGS/020_20220408.csv'

    # Получение массива данных  NMEA из лога ЗА ПЕРИОД ВРЕМЕНИ
    # start = '2022-04-08 14:30'
    # stop = '2022-04-08 14:52'
    # start = ''
    # stop = ''

    # log_file = BytesIO(log_file)

    print(log_file)

    nmea_track = extract_nmea_from_log(log_file, start, stop)

    # print(start)
    # print(stop)

    # Преобразование  времени в datetime
    track_time = track_time_to_datetime(nmea_track[:, 0])

    # Пересчитываем координаты в десятичные градусы
    track = nmea_coordinates_to_degrees(nmea_track[:, 1:3])

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
    # file = 'map.html'
    my_map.save(map_name)

    return map_name


if __name__ == "__main__":

    # Проверка работы api
    import requests

    # Отправляем лог на сервер
    file = {'file': io.open('SEKOP_LOGS/019_20220408.csv', encoding='utf-8')}

    req = requests.post(
        'http://localhost:5000/upload',
        files=file
    )

    print(req.json())

    # Вторым запросом строим трек в файле map.html по заданному временному интервалу
    log_id = req.json()['id']

    track = requests.get(
        'http://localhost:5000/track',
        params={'id': log_id,
                'start_time': '2022-04-08 13:20',
                'end_time': '2022-04-08 14:26'
                }
    )

    map_file = track.text
    print(map_file)

    file_name = log_id + '.html'
    print(file_name)