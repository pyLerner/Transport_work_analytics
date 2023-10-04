import json
import os
import requests
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from sql_get_data import get_route_id_by_route_name, get_route_stops

load_dotenv()


def get_route_trace_by_route_id(route_id: int, direction: int) -> Dict:
    """
    Получаем трассу маршрута и список остановок для маршрута с заданным route_id и для заданного направления
    """
    server = os.getenv('API_SERVER')
    url = f'{server}/routes/stops'

    payload = {
        'routeIDs': route_id,
        'directions': direction
    }

    response = requests.get(url, params=payload)

    try:
        assert response.status_code == 200
        # print(response.json())
        return response.json()

    except AssertionError:
        print('Ответ не  получен')
        print(response.status_code, response.reason)

        # return response.status_code
    # Для красивого вывода:
    # result = json.dumps(result, indent=4)
    # print(result)
    # return json.loads(result)


if __name__ == "__main__":

    route = '228'
    route_id = get_route_id_by_route_name('228')
    # print(route_id)

    response = get_route_trace_by_route_id(route_id, 1)

    path = response['result'][0]['path']
    # print(path)

    # Список списков координат  из АСУ ГПТ с поменянными местами координатами
    path = [[list(p.values())[1], list(p.values())[0]] for p in path]
    # print(path)

    stop_list = response['result'][0]['stopIDs']
    stop_list = tuple(stop_list)

    stops = get_route_stops(stop_list)

    # Список координат
    stops = stops[['stop_lat', 'stop_lon']].values.tolist()
    print(stops)
