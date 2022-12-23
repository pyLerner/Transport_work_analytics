# Получение уникальных гаражных номеров из отчета Ф2-Перевозчик
import pandas as pd
import os

def f2_parsing():
    '''
    Возвращает кортеж из номера маршрута и списка уникальных номеров ТС из отчета Ф2-Перевозчик
    :return:
    '''
    f2_file = os.path.join(os.getcwd(), 'Ф-2_(Перевозчик).xls')
    if not os.path.exists(f2_file):
        print('Ф-2_(Перевозчик).xls не найден')
        print('Сохраните его в каталоге со скритпом transacion_count.py')

    f2 = pd.read_excel(f2_file)
    route = f2.iloc[6]['Unnamed: 2']
    f2 = f2.drop(index=range(15))
    f2 = f2.drop(f2.columns[[0]], axis=1)
    f2.columns = ['TC', 'time_out', 'start_point_depart', 'end_point_arrive', 'end_point_depart',
                  'start_point_arrive', 'time_back']
    TC_list = []

    for TC in list(f2.TC.unique()):
        TC = str(TC)
        if len(TC) < 9 and TC[:4].isdigit():
            TC = TC[:4]
            # f.write(TC + '\n')
            TC_list.append(TC)

    return route, TC_list

# print(f2_parsing())