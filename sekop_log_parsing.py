
import numpy as np
import re

def nmea_to_degrees(nmea_array):
    '''
    Перевод строковых значений NMEA в градусы
    :param nmea_array:
    :return: ndarray.astype(float)
    '''
    nmea_array = np.array(nmea_array).astype(float)
    int_degrees = (nmea_array / 100).astype(int)
    nmea_minutes = nmea_array / 100 - int_degrees
    float_degrees = nmea_minutes * 100 / 60

    out = int_degrees + float_degrees
    print(out)
    return out


with open('SEKOP_LOGS/log_geo.csv', 'r') as file:
    s = file.read().splitlines()
    # print(s)

    # track = []
    # формирование трека в виде списка списков
    # for row in s:
    #     # Парсим из строки лога с координатами текстовые значение координат в формате NMEA.
    #     nmea_string = row[row.find(',A,') + 3: row.find(',E,')].replace(',', '').split('N')


    nmea_track = []
    for row in s:
        # Парсим из строки лога с координатами текстовые значение координат в формате NMEA.
        nmea_string = re.findall(r'\d+\.\d+', row)
        if nmea_string:             # Пустые строки не берем
            # print(nmea_string)
            track.append(nmea_string)
    # print(track)


track = nmea_to_degrees(track)[:, 1:3]
# print(track)

track2list = track.tolist()


# Перевод в градусы см. в XFleetAPI.geo_zone.nmea_to_degrees