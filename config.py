import os
### GTFS section ######
FILE: str = 'feed.zip'
GTFS_URL: str = 'http://portal.gpt.adc.spb.ru/Portal/transport/internalapi/gtfs/'
GTFS_CATALOG: str = 'feeds'
PAT_ROUTES = os.path.join(GTFS_CATALOG, 'pat_routes.csv')

# Через сколько дней обновлять фиды
UP_TO_DAYS = 2

# ID перевозчика Пассажиравтотранс
PAT_ID = 362

### SQL section ######
TRANSACTIONS_CATALOG = os.path.join(os.getcwd(), 'Transactions')


### Out Result section
OUT_REPORTS = os.path.join(os.getcwd(), 'OutReports')