import os
import pandas as pd

os.chdir('/Users/Mac/Python/feed')
routeId = pd.read_csv('operator_routes.txt')
route = pd.read_csv('routes.txt')
route.drop(columns=['agency_id'], axis=1, inplace=True)
ops = pd.read_csv('operators.txt')
ops.drop(columns=['operator_address', 'operator_phone'], axis=1, inplace=True)
patRoutesId = routeId[routeId.operator_id == 362]

# Запись маршрутов ПАТ в CSV
patRoutes = pd.merge(patRoutesId, route, left_on='route_id', right_on='route_id')
patRoutes.to_csv('pat_routes.csv', index=False)

# Запись всех маршрутов в CSV
allOperRoutes = pd.merge(routeId, route, left_on='route_id', right_on='route_id')
allOperRoutes = pd.merge(ops, allOperRoutes, left_on='operator_id', right_on='operator_id')
allOperRoutes.to_csv('all_operators_routes.csv', index=False)

# Запись всех маршрутов в Excel
allOperRoutes.to_excel('all_operators_routes.xlsx', sheet_name='Routes', index=False)
