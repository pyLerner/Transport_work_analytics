# Подсчет транзакций для всех ТС из отчета Ф2 по дням
# Для работы нужны файлы транзакций в каталоге Transactions  и отчет Ф-2_(Перевозчик).xls рядом с этим скриптом
# Выходной файл CSV сохраняется в data_out_path
#

import config
import pandas as pd
import os
import F2_parsing as f2
import datetime as dt

def create_catalog(catalog_name: str):
    '''

    :param catalog_name:
    :return:
    '''

    base_dir = os.getcwd()
    catalog_name = os.path.join(base_dir, catalog_name)
    if not os.path.exists(catalog_name):
        os.mkdir(catalog_name)
    return catalog_name                                 # Клаcть файлы транзакций в папку Transactions

def get_df_from_files(path: str):

    '''
    Возвращает Data Frame из файлов транзакций в каталоге path
    :param path:
    :return: pandas DataFrame
    '''

    total_file = pd.DataFrame(columns=['CARRIER_BOARD_NUM', 'TRANSACT_DATE_TIME'])  # Пустой DF,
    # чтобы было с чем склеивать
    # df из файлов
    for file in os.listdir(path):  # Нужна маска для файлов csv
        if file[-4:] == '.csv':
            # print(file)
            file = os.path.join(data_in_path, file)
            file_csv = pd.read_csv(file, usecols=['CARRIER_BOARD_NUM', 'TRANSACT_DATE_TIME'], sep=';')
            print(file, '\t\t\t\tпрочитан')
            total_file = pd.concat([total_file, file_csv], axis=0, ignore_index=True)
    
    print('Все файлы транзакций в каталоге прочитаны')
    return total_file # Почему-то гаражные номера стали float. Приводим к int


def transaction_count(data_frame):
    '''
    Подсчитывает транзакции по дням для списка ТС и номероа маршрута из отчета Ф-2

    :return: file *.csv
    '''
    
    data_out_path = create_catalog(config.OUT_REPORTS)              # Каталог для сохранения отчетов

    route = f2.f2_parsing()[0]  # Номер маршрута из Ф2
    print(f'Получен список ТС маршрута №{route} из отчета Ф2-(Перевозчик).xls')
    # Список ТС из отчета АСУГПТ Ф2-Перевозчик
    vehicles = f2.f2_parsing()[1]

    vehicles = pd.DataFrame(vehicles, columns=['F2_list'])
    # vehicles['F2_list'] = vehicles['F2_list'].astype(int)  #Приводим к типу int, так как без этого почему-то тип object

    total_file = pd.merge(vehicles, data_frame, left_on='F2_list', right_on='CARRIER_BOARD_NUM')  # Объединение файла транзакций со списком ТС

    total_file.TRANSACT_DATE_TIME = total_file.TRANSACT_DATE_TIME.astype(str)  # Приводим дату к строке и убираем время срезами
    
    days = [day[0:10] for day in total_file.TRANSACT_DATE_TIME]               # список дат без времени

    days_uniq = sorted(set(days))                                             # Отсортированный уникальный список дат
    days = pd.DataFrame(list(days), columns=['TR_DATE'])                      # Массив дат

    total_file = pd.concat([total_file['CARRIER_BOARD_NUM'], days], axis=1)    # склеили даты с гаражными

    days = days_uniq                                                # дальше только уникальные даты для построения столбцов с кол-вом транз-й
    tr_by_days = total_file.groupby('CARRIER_BOARD_NUM').count()    # Иниц-я. Общее количество тр-ций за месяц

    for day in days:
        tr_for_day = total_file[total_file.TR_DATE == day].\
            groupby('CARRIER_BOARD_NUM').count()                    # Группируем по гаражным номерам
        tr_by_days = pd.concat([tr_by_days, tr_for_day], axis=1)    # Добавляем справа столбик (axis=1) на дату

    tr_by_days = tr_by_days.convert_dtypes()
    names = ['Total transactions in month'] + days
    tr_by_days.columns = names                                                  # Заголовок в итоговый DF

    date = dt.datetime.now().date().strftime('%Y-%m-%d')
    file_name = f'{data_out_path}/{date}_route_{route}_tr_by_days.csv'     # Задаем имя файла номером маршрута и датой в названии файла
    tr_by_days.to_csv(file_name, sep=';')                                       # Сохраняем в файл

    print(f'\nИтоговый отчет с количесвом транзакций по дням записан в файл {file_name}')
