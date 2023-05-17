import config
from sqlalchemy import create_engine
import pymysql
import pandas as pd

def get_df_from_sql(query, db=config.SEKOP_DB_NAME):

    '''
    Возвращает pandas DataFrame по запросу query на языке SQL
    :return: DataFrame object
    '''
    url = f'{config.DIALECT}+' \
          f'{config.DRIVER}://' \
          f'{config.SQL_USER}:' \
          f'{config.SQL_PASSWD}@' \
          f'{config.SQL_HOST}/' \
          f'{db}?charset=utf8mb4'

    engine = create_engine(url)
    connection = engine.connect()
    connection.execution_options(
        isolation_level="READ COMMITTED"
    )

    sql_df = pd.read_sql(query, con=engine)
    # print(sql_df)
    return sql_df.convert_dtypes()

def get_sekop_id_by_route_id(query, db=config.FEEDS_DB_NAME):

    '''
    Возвращает pandas DataFrame по запросу query на языке SQL
    :return: DataFrame object
    '''
    url = f'{config.DIALECT}+' \
          f'{config.DRIVER}://' \
          f'{config.SQL_USER}:' \
          f'{config.SQL_PASSWD}@' \
          f'{config.SQL_HOST}/' \
          f'{db}?charset=utf8mb4'

    engine = create_engine(url)
    connection = engine.connect()
    connection.execution_options(
        isolation_level="READ COMMITTED"
    )

    sql_df = pd.read_sql(query, con=engine)
    out = sql_df.loc[0]['route_sekop_id'].astype(int)
    # print(out)
    return out

#TODO:!!!
def get_route_id_by_route_name(route_name, db=config.FEEDS_DB_NAME):

    query = f"SELECT `route_id` FROM `pat_routes` WHERE `route_short_name` = {route_name}"
    sql_df = get_df_from_sql(query, db=config.FEEDS_DB_NAME)
    out = sql_df.loc[0]['route_id'].astype(int)
    # print(out)
    return out

def get_sekop_id_by_route_name(route_name, db=config.FEEDS_DB_NAME):

    query = f"SELECT `route_sekop_id` FROM `pat_routes` WHERE `route_short_name` = {route_name}"
    sql_df = get_df_from_sql(query, db=config.FEEDS_DB_NAME)
    out = sql_df.loc[0]['route_sekop_id'].astype(int)
    # print(out)
    return out

if __name__ == "__main__":
    # query = "SELECT `route_id` FROM `pat_routes` WHERE route_short_name = 22"
    # query = "SELECT `route_id` FROM `pat_routes` WHERE route_short_name = 22"

    route_id = get_route_id_by_route_name('22', db=config.FEEDS_DB_NAME)
    sekop_id = get_sekop_id_by_route_name('22', db=config.FEEDS_DB_NAME)

    print(route_id, sekop_id)