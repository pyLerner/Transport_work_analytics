from os import path
import time
import config
import datetime as dt
import gtfs_download as gtfs
import F2_parsing as f2
import pandas as pd
import transaction_count as tc
import sql_get_data as sql


start = time.time()

# Обновление фидов
# gtfs.feeds_update()

# Чтение отчета Ф2-(Перевозчик).xls, получение короткого названия маршрута и списка ТС
gtfs.create_directory(config.ASUGPT_DIR)
route_short_name = f2.f2_parsing()[0]

# Получение ID СЭКОП по короткому названию маршрута

# query = f"SELECT `route_sekop_id` " \
#         f"FROM `pat_routes` " \
#         f"WHERE `route_short_name` = '{route_short_name}'"

sekop_id = sql.get_sekop_id_by_route_name(route_short_name)

# sekop_id = gtfs.get_sekop_id_by_route_name(route_short_name)
print(f'Получен ID СЭКОП {sekop_id} для маршрута №{route_short_name}')

# Вызвать функцию создания директории для файлов транзакций
gtfs.create_directory(config.TRANSACTIONS_CATALOG)

# и выполнить запрос в базу для создания файлов по id маршрута

# Временные границы для запроса в БД
now = dt.datetime.now().date()
start_date = now.strftime('%Y-%m-01')
end_date = now.strftime('%Y-%m-%d')

# Получение номера парка для определения номера таблицы базы    
parks = f2.get_park_number()
df = pd.DataFrame()

for park in parks:

    query = f"SELECT `CARRIER_BOARD_NUM`, `TRANSACT_DATE_TIME` " \
            f"FROM `park_{park}` WHERE date (`TRANSACT_DATE_TIME`) "\
            f"BETWEEN '{start_date}' AND '{end_date}' AND `ID_ROUTE`='{sekop_id}'"

    print(f'Выполняется запрос в базу Парка № {park}... '
          f'Это займет некоторое время. Подождите.')

    df_park = sql.get_df_from_sql(query)

    print('Ответ от базы данных получен')

    # Сохранение ответа базы данных для маршрута в текущем месяце
    file_name = f'park_{park}.csv'

    file_name = path.join(
        config.TRANSACTIONS_CATALOG,
        file_name
    )

    df_park.to_csv(file_name, sep=';')

    print(f'Результат запроса в базу данных для маршрута {route_short_name} сохранен в файл {file_name}')

    df = pd.concat([df, df_park], axis=0)
    
gtfs.create_directory(config.OUT_REPORTS)

# Вызов функции подсчета транзакций из модуля transaction_count
tc.transaction_count(df)

end = round(time.time() - start, 2)

if end > 60:
    minutes = int(end // 60)
    seconds = round(end % 60, 2)
    print(f'\nВремя выполнения {minutes} мин. {seconds} сек.')
else:
    print(f'\nВремя выполнения {end} сек.')
