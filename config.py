import os
from dotenv import load_dotenv


load_dotenv()

# GTFS section ######
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

# SQL section ######
TRANSACTIONS_CATALOG: str = os.path.join(os.getcwd(), 'Transactions')
DIALECT = os.getenv('DIALECT')
DRIVER = os.getenv('DRIVER')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWD = os.getenv('SQL_PASSWD')
SQL_HOST = os.getenv('SQL_HOST')
SEKOP_DB_NAME = os.getenv('SEKOP_DB_NAME')
FEEDS_DB_NAME = os.getenv('FEEDS_DB_NAME')

# Out Result section
OUT_REPORTS: str = os.path.join(os.getcwd(), 'OutReports')


if __name__ == "__main__":
    pass
