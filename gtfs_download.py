import requests
import zipfile
import gtfs_config

File = gtfs_config.file
# GTFS_URL: str = 'http://portal.gpt.adc.spb.ru/Portal/transport/internalapi/gtfs/'
URL = gtfs_config.GTFS_URL + File
Catalog = gtfs_config.GTFS_CATALOG

# Функция проверки актуальной версии feeds
# def up2date_check(url):

def download_feed(url, file):
    with open(file, "wb") as f:
        file_zip = requests.get(url)
        f.write(file_zip.content)
        print('Downloaded')
        return 0


def unzip_feed(file, catalog):
    with zipfile.ZipFile(file, 'r') as f:
        f.extractall(catalog)
        print('UnZipped')
        return 0

#
# download_feed(URL, File)
# unzip_feed(File, Catalog)

