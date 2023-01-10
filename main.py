from os import path
import time
import config
import datetime as dt
import gtfs_download as gtfs
import F2_parsing as f2
import transaction_count as tc
import sql_get_data as sql

start = time.time()

# Обновление фидов
gtfs.feeds_update()

# Чтение отчета Ф2-(Перевозчик).xls, получение короткого названия маршрута и списка ТС
gtfs.create_directory(config.ASUGPT_DIR)
route_short_name = f2.f2_parsing()[0]

# Получение ID СЭКОП по короткому названию маршрута
sekop_id = gtfs.get_sekop_id_by_route_name(route_short_name)
print(f'Получен ID СЭКОП {sekop_id} для маршрута №{route_short_name}')

# Вызвать функцию создания директории для файлов транзакций
gtfs.create_directory(config.TRANSACTIONS_CATALOG)

# и выполнить запрос в базу для создания файлов по id маршрута

# Временные границы для запроса в БД
now = dt.datetime.now().date()
start_date = now.strftime('%Y-%m-01')
end_date = now.strftime('%Y-%m-%d')

# Тут должна быть функция получения номера таблицы с транзакциями по номеру маршрута (нужно создать такую таблицу)
# Пока временная заглушка
if sekop_id == 18067:
    park = '7'
elif sekop_id == 15333:
    park = '3'

query = f"SELECT `CARRIER_BOARD_NUM`, `TRANSACT_DATE_TIME` " \
        f"FROM `park_{park}` WHERE date (`TRANSACT_DATE_TIME`) "\
        f"BETWEEN '{start_date}' AND '{end_date}' AND `ID_ROUTE`='{sekop_id}'"

print(f'Выполняется запрос в базу Парка № {park}... '
      f'Это займет некоторое время. Подождите.')

df = sql.get_df_from_sql(query)

print('Ответ от базы данных получен')

# Сохранение ответа базы данных для маршрута в текущем месяце
file_name = f'park_{park}.csv'
file_name = path.join(config.TRANSACTIONS_CATALOG, file_name)
df.to_csv(file_name, sep=';')

print(f'Результат запроса в базу данных для маршрута {route_short_name} сохранен в файл {file_name}')

gtfs.create_directory(config.OUT_REPORTS)

# Вызов функции подсчета транзакций из модуля transaction_count
tc.transaction_count(df)

end = round(time.time() - start, 2)

if end > 60:
    minutes = int(end // 60)
    seconds = end % 60
    print(f'\nВремя выполнения {minutes} мин. {seconds} сек.')
else:
    print(f'\nВремя выполнения {end} сек.')
