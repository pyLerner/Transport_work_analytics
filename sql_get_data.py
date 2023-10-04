import config
from sqlalchemy import create_engine
from typing import Tuple
# import pymysql
import pandas as pd


def get_df_from_sql(query, db=config.SEKOP_DB_NAME):

    """
    Возвращает pandas DataFrame по запросу query на языке SQL
    :return: DataFrame object
    """
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

    print(url)
    sql_df = pd.read_sql(query, con=engine)
    # print(sql_df)
    return sql_df.convert_dtypes()


def get_sekop_id_by_route_id(
        query,
        db=config.FEEDS_DB_NAME
):

    """
    Возвращает pandas DataFrame по запросу query на языке SQL
    :return: DataFrame object
    """

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


def get_route_id_by_route_name(
        route_name,
        db=config.FEEDS_DB_NAME
):

    query = f"SELECT `route_id` FROM `pat_routes` WHERE `route_short_name` = {route_name}"

    sql_df = get_df_from_sql(
        query,
        db=db
    )

    out = sql_df.loc[0]['route_id'].astype(int)
    # print(out)
    return out

def get_sekop_id_by_route_name(
        route_name,
        db=config.FEEDS_DB_NAME
):

    query = f"SELECT `route_sekop_id` FROM `pat_routes` WHERE `route_short_name` = {route_name}"

    sql_df = get_df_from_sql(
        query,
        db=db
    )

    # out = sql_df.loc[0]['route_sekop_id'].astype(int)
    out = sql_df.loc[0]['route_sekop_id']  # out: str

    # print('out', type(out))
    return out


def get_route_stops(
        route_stops: Tuple[str, ],
        db=config.FEEDS_DB_NAME
):
    """
    Возвращает таблицу остановок с названиями и координатами по заданному списку id
    """

    query = f"SELECT `stop_id`, `stop_name`, `stop_lat`, `stop_lon`" \
            f"FROM stops s WHERE s.stop_id IN {route_stops} " \
            f"ORDER BY FIELD(s.stop_id, {str(route_stops)[1:-1]})"

    sql_df = get_df_from_sql(query, db)
    print(sql_df)
    return sql_df


if __name__ == "__main__":
    # query = "SELECT `route_id` FROM `pat_routes` WHERE route_short_name = 22"
    # query = "SELECT `route_id` FROM `pat_routes` WHERE route_short_name = 22"
    stops = ('3267', '3354', '2910', '17998', '28966', '28967', '18004', '35056',
             '35604', '35053', '23318', '23414', '33293', '4403', '21079', '18506')

    result = get_route_stops(stops)
    print(result)

    # route_id = get_route_id_by_route_name(
    #     '22',
    #     db=config.FEEDS_DB_NAME
    # )
    #
    # sekop_id = get_sekop_id_by_route_name(
    #     '22',
    #     db=config.FEEDS_DB_NAME
    # )
    #
    # print(route_id, sekop_id)
    #
