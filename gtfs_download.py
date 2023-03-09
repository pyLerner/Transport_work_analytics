import requests
import zipfile
import config
import pandas as pd
import os
import datetime as dt

file = config.FILE
# GTFS_URL: str = 'http://portal.gpt.adc.spb.ru/Portal/transport/internalapi/gtfs/'
URL = config.GTFS_URL + file
catalog = config.GTFS_CATALOG

# Функция проверки актуальной версии feeds
# def up2date_check(url):

def download_feed(url, file):
    '''

    :param url:
    :param file:
    :return:
    '''
    with open(file, "wb") as f:
        file_zip = requests.get(url)
        print(f'Скачивание {url}')
        f.write(file_zip.content)
        print(f'Файл {f} скачан')
        

def unzip_feed(file, catalog):
    '''

    :param file:
    :param catalog:
    :return:
    '''
    with zipfile.ZipFile(file, 'r') as f:
        f.extractall(catalog)
        print(f'{f} распакован в {catalog}')
        return 0

def ctime_difference(file: str):
    '''
    Возвращает срок создания файла в днях
    :param file: str
    :return: int(days)
    '''
    now = dt.datetime.now().date()
    file_time = os.path.getmtime(file)
    file_time = dt.datetime.fromtimestamp(file_time).date()
    delta = (now - file_time).days
    return delta

def feeds_update():
    #Если фиды старше UP_2_DAYS дней, обновляем
    url = config.GTFS_URL + config.FILE
    if (not os.path.exists(config.FILE)) or \
        (ctime_difference(config.FILE) >= config.UP_TO_DAYS):
        print(f'Обновление справочников ОРГП ...')
        download_feed(url, config.FILE)
        unzip_feed(config.FILE, config.GTFS_CATALOG)

    else:
        print(f'Справочники ОРГП актуальные. Обновления не требуются')
        return

# download_feed(URL, file)
# unzip_feed(file, catalog)

def get_pat_routes():
    '''
    Возвращает DataFrame с номерами маршрутов ПАТ из GTFS Feeds
    :return: object pandas DataFrame
    '''
    route_id = pd.read_csv(os.path.join(config.GTFS_CATALOG, 'operator_routes.txt'))
    route = pd.read_csv(os.path.join(config.GTFS_CATALOG,'routes.txt'))
    route.drop(columns=['agency_id'], axis=1, inplace=True)
    ops = pd.read_csv(os.path.join(config.GTFS_CATALOG, 'operators.txt'))
    ops.drop(columns=['operator_address', 'operator_phone'], axis=1, inplace=True)
    pat_routes_id = route_id[route_id.operator_id == config.PAT_ID]
    # Запись маршрутов ПАТ в CSV
    pat_routes = pd.merge(pat_routes_id, route, left_on='route_id', right_on='route_id')
    pat_routes.to_csv(config.PAT_ROUTES, index=False)
    return pat_routes


def get_route_id_by_route_name(route_short_name: str):
    '''
    Возвращает номер ID маршрута по короткому названию маршрута
    :param route_short_name: str
    :return: route_id: int
    '''
    # Если нет спрвочника маршрутов ПАТ, или он старше актуального архива фидов, нужно заново создать справочник
    if (not os.path.exists(config.PAT_ROUTES)) \
        or (ctime_difference(config.PAT_ROUTES) < ctime_difference(config.FILE)):

        # print(f'Синхронизируем справочник маршрутов {config.PAT_ROUTES} со справочниками ОРГП')
        route = get_pat_routes()
    else:
        print(f'Чтение файла маршрутов {config.PAT_ROUTES}...')
        route = pd.read_csv(config.PAT_ROUTES)
        print('Ok')

    route = route[route.route_short_name == route_short_name]
    idx = route.index                               #Строим индекс строк(и)

    route_id = int(route.at[idx[0], 'route_id'])     #
    return route_id

def get_sekop_id_from_csv_by_route_name(route_short_name: str):
    '''
    Возвращает целое число - идентификатор СЭКОП по номеру (названию) маршрута
    :param route_name: str
    :return: sekop_id: int
    '''
    pat_ids_file = config.PAT_IDS
    if not os.path.exists(pat_ids_file):
        print('Справочник идентификаторов маршрута и СЭКОП не найден')
        print('Ошибка')
        return -1
    pat_ids = pd.read_csv(pat_ids_file, sep=';')
    sekop_id = pat_ids[pat_ids.route_short_name == route_short_name]
    sekop_id = sekop_id['route_sekop_id']
    sekop_id = int(sekop_id)
    return sekop_id

def get_sekop_id_from_by_route_name(route_short_name: str):
    '''
    Возвращает целое число - идентификатор СЭКОП по номеру (названию) маршрута
    :param route_name: str
    :return: sekop_id: int
    '''
    pat_ids_file = config.PAT_IDS
    if not os.path.exists(pat_ids_file):
        print('Справочник идентификаторов маршрута и СЭКОП не найден')
        print('Ошибка')
        return -1
    pat_ids = pd.read_csv(pat_ids_file, sep=';')
    sekop_id = pat_ids[pat_ids.route_short_name == route_short_name]
    sekop_id = sekop_id['route_sekop_id']
    sekop_id = int(sekop_id)
    return sekop_id


def get_route_shortname_by_routeid(route_id: int):
    '''
    Возвращает номер маршрута по route id
    :param route_id:
    :return: route_short_name: str
    '''
    if (not os.path.exists(config.PAT_ROUTES)) \
        or (ctime_difference(config.PAT_ROUTES) < ctime_difference(config.FILE)):

        # print(f'Синхронизируем справочник маршрутов {config.PAT_ROUTES} со справочниками ОРГП')
        route = get_pat_routes()
    else:
        print(f'Чтение файла маршрутов {config.PAT_ROUTES}...')
        route = pd.read_csv(config.PAT_ROUTES)
        print('Ok')

    route = route[route.route_id == route_id]
    idx = route.index                               #Строим индекс строк(и)

    route_shortname = int(route.at[idx[0], 'route_short_name'])     #
    return route_shortname


def create_directory(dir: str):
    '''
    :param dir: str - имя каталога
    :return:
    '''
    if not os.path.exists(dir):
        print(f'Создание каталога {dir}')
        os.mkdir(dir)
# get_sekop_id_by_route_name('203')
# print(type(route_id_by_route_name('228')))
