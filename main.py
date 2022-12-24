import time
import gtfs_download as gtfs
import F2_parsing as f2
import transaction_count as tc

start = time.time()

# Обновление фидов
gtfs.feeds_update()

# Чтение отчета Ф2-(Перевозчик).xls, получение короткого названия маршрута и списка ТС
route_short_name = f2.f2_parsing()[0]

# Получение ID маршрута по короткому названию
route_id = gtfs.route_id_by_route_name(route_short_name)
print(f'Маршрут {route_short_name} с номером ID {route_id}')

# Вызвать функцию создания директории для файлов транзакций и
# и выполнить запрос в базу для создания файлов

# Вызов функции подсчета транзакций из модуля transaction_count
tc.transaction_count()

end = time.time() - start
print('Время выполнения {:.2} сек.'.format(end))

