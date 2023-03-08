#  Программа читает файл со строками в формате NMEA 0183 и строит трек на карте

import numpy as np
import re
import folium
import datetime

def nmea_coordinates_to_degrees(nmea_array):
    '''
    Перевод строковых значений NMEA в градусы
    :param nmea_array:
    :return: ndarray.astype(float)
    '''
    nmea_array = np.array(nmea_array).astype(float)
    int_degrees = (nmea_array / 100) // 1       # Целая часть
    nmea_minutes = (nmea_array / 100) % 1       # Мантисса
    float_degrees = nmea_minutes * 5 / 3        # Перевод из минут в десятичную дробь *100/60

    out = int_degrees + float_degrees
    # print(out)
    return out


def nmea_time_to_readable(nmea_time):
    '''
    Перевод времени NMEA в читаемый вид
    :param nmea_time: list or array
    :return:
    '''
    nmea_time = np.array(nmea_time).astype(float)
    print(nmea_time)
    hours = nmea_time // 10000                              # Часы
    minutes = nmea_time // 100 % 100                        # Минуты
    seconds = nmea_time % (hours * 10000 + minutes * 100)   # Секунды
    hours += 3                                             #  + 3 GMT
    out = datetime.time(int(hours), int(minutes), int(seconds))
    print(out)
    return out


with open('SEKOP_LOGS/log_geo.csv', 'r') as file:
    s = file.read().splitlines()
    # print(s)

    nmea_time, nmea_track = [], []
    for row in s:
        # Парсим из строки лога с координатами текстовые значение координат в формате NMEA.
        nmea_string = re.findall(r'\d+\.\d+', row)
        if nmea_string:             # Пустые строки не берем
            # print(nmea_string)

            # Рабочий, но медленный способ
            nmea_date_time = datetime.time(int(nmea_string[0][:2]) + 3,  # GMT 3
                                          int(nmea_string[0][2:4]),
                                          int(nmea_string[0][4:6]))


            nmea_time.append(nmea_date_time)  # Список значений времени datetime

            nmea_string = nmea_string[1:]
            nmea_track.append(nmea_string)      #Числовые данные: координаты, скорость, путевой угол

    # print(nmea_track)
    # print(nmea_time)


track = nmea_coordinates_to_degrees(nmea_track)[:, 0:2]     # Перевод из строкового NMEA в десятичный np.array
# print(nmea_coordinates_to_degrees(nmea_track))


# Привели к виду для загрузки в leaflet/foliant:
track2list = track.tolist()


# Инициализация карты в начальной точке трассы (АС)
map = folium.Map(location=track2list[0], zoom_start=12)


# Рисование иконок геопозиции
# for coordinates in track:
#     folium.Marker(location=coordinates, icon=folium.Icon(color='green')).add_to(map)


# Метки для НП/КП (Начало и конец трека)
for coordination in [track2list[0], track2list[-1]]:

    folium.Marker(location=coordination,
                    icon=folium.Icon(color='blue')
                  ).add_to(map)


# Трасса маршрута в полилиниях
# folium.PolyLine(track, tooltip=folium.Tooltip("3-й Парк",
#                                            sticky=False,    # не прилипает к курсору
#                                            permanent=True,  # отображается всегда
#                                     #      style='background-color:grey'
#                                               )
#                 ).add_to(map)



# Рисуем трек красными кружками:

for times, coordinate in zip(nmea_time, track2list):

    folium.CircleMarker(location=coordinate,
                        color='red',
                        radius=3,
                        tooltip=times,
                        fill=True,
                        fill_color='red').add_to(map)


# Одиночная координата
# location = track[15]
# folium.CircleMarker(location=location,
#                     color='red',
#                     radius=4,
#                     tooltip=location,
#                     fill=True,
#                     fill_color='red').add_to(map)


map.save("map2.html")

check = nmea_time_to_readable('001234.123')