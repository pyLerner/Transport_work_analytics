import os
import dotenv

### GTFS section ######
FILE: str = 'feed.zip'
GTFS_URL: str = 'http://portal.gpt.adc.spb.ru/Portal/transport/internalapi/gtfs/'
GTFS_CATALOG: str = os.path.join(os.getcwd(), 'Feeds')
PAT_ROUTES = os.path.join(GTFS_CATALOG, 'pat_routes.csv')

# Через сколько дней обновлять фиды
UP_TO_DAYS = 2

# ID перевозчика Пассажиравтотранс
PAT_ID = 362

ASUGPT_DIR: str = os.path.join(os.getcwd(), 'ASUGPT_reports')

# Справочник ID_ROUTE, ID_SEKOP
PAT_IDS: str = os.path.join(GTFS_CATALOG, 'pat_ids.csv')

### SQL section ######
TRANSACTIONS_CATALOG: str = os.path.join(os.getcwd(), 'Transactions')
DIALECT: str = 'mysql'
DRIVER: str = 'pymysql'
SQL_USER: str = 'obo'
SQL_PASSWD: str = 'hN8L36Cl'
SQL_HOST: str = '192.168.45.75'
DB_NAME: str = 'obo'


### Out Result section
OUT_REPORTS: str = os.path.join(os.getcwd(), 'OutReports')