import pandas as pd
from google.transit import gtfs_realtime_pb2
import requests
import os

os.chdir('./feed')

urlBase = 'https://portal.gpt.adc.spb.ru/Portal/transport/internalapi/gtfs/realtime/'
vehicleRequest = 'vehicle'
vehiclTrip = 'vehicletrips?vehicleIDs='
stopForecast = 'stopforecast?stopID='

# response = requests.get(urlBase + vehicleRequest)
# transportType = input('Введи тип ТС (bus, tram, trolley) через запятую: ')
routeShortName = input('Введи номер маршрута: ')
route = pd.read_csv('all_operators_routes.csv', usecols=['route_id', 'route_short_name', 'transport_type'])

# На случай разных типов ТС:
# route = route[(route.route_short_name == routeShortName) & (route.transport_type == transportType)]

route = route[(route.route_short_name == routeShortName) & (route.transport_type == 'bus')]
idx = route.index                               #Строим индекс строк(и)

# На случай разных типов ТС нужно нужно включить в цикл строки ниже
# for i in idx:

routeID = route.at[idx[0], 'route_id']          #Получаем скаляр столбца route_id по индексу строки
response = requests.get('https://portal.gpt.adc.spb.ru/Portal/\
transport/internalapi/gtfs/realtime/vehicle?routeIDs=' + str(routeID))

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
print(feed.entity)
for entity in feed.entity:
    result = f'ТС {entity.vehicle.vehicle.label}, скорость {int(entity.vehicle.position.speed)}'
    print(result)


# for entity in feed.entity:
#     if entity.HasField('trip_update'):
#         print(entity.trip_update)3
