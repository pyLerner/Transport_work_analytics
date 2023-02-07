import gtfs_download as gtfs
from google.transit import gtfs_realtime_pb2
import requests
import os

urlBase = 'https://portal.gpt.adc.spb.ru/Portal/transport/internalapi/gtfs/realtime/'
vehicleRequest = 'vehicle'
vehicleTrip = 'vehicletrips?vehicleIDs='
stopForecast = 'stopforecast?stopID='

routeShortName = input('Введи номер маршрута: ')

route_id = gtfs.get_route_id_by_route_name(routeShortName)

response = requests.get('https://portal.gpt.adc.spb.ru/Portal/\
transport/internalapi/gtfs/realtime/vehicle?routeIDs=' + str(route_id))

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
# print(feed.entity)
for entity in feed.entity:
    result = f'ТС {entity.vehicle.vehicle.label}, скорость {int(entity.vehicle.position.speed)}'
    print(result)


# for entity in feed.entity:
#     if entity.HasField('trip_update'):
#         print(entity.trip_update)3