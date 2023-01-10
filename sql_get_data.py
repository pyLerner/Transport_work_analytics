import config
from sqlalchemy import create_engine
import pymysql
import pandas as pd

def get_df_from_sql(query: str):

    '''

    :return: DataFrame oject
    '''
    url = f'{config.DIALECT}+' \
          f'{config.DRIVER}://' \
          f'{config.SQL_USER}:' \
          f'{config.SQL_PASSWD}@' \
          f'{config.SQL_HOST}/' \
          f'{config.DB_NAME}?charset=utf8mb4'

    engine = create_engine(url)
    connection = engine.connect()
    connection.execution_options(
        isolation_level="READ COMMITTED"
    )

    sql_df = pd.read_sql(query, con=engine)
    print(sql_df)
    return sql_df.convert_dtypes()

park = '3'
start_date = '2022-12-01'
end_date = '2022-12-30'
sekop_id = '15333'

# query = f"SELECT * FROM `park_3`"

# query = f"SELECT `TRANSACT_DATE_TIME`, `CARRIER_BOARD_NUM` " \
#         f"FROM `park_{3}` WHERE date (`TRANSACT_DATE_TIME`) "\
#         f"BETWEEN '{start_date}' AND '{end_date}' AND `ID_ROUTE`='{sekop_id}'"

# query = f"SELECT `TRANSACT_DATE_TIME`, `CARRIER_BOARD_NUM` " \
#         f"FROM `park_{park}` WHERE date (`TRANSACT_DATE_TIME`) "\
#         f"BETWEEN {start_date} AND {end_date} AND `ID_ROUTE`={sekop_id}"

# query = "SELECT `TRANSACT_DATE_TIME`, `CARRIER_BOARD_NUM`, `ID_ROUTE` \
# FROM `park_7` WHERE date (`TRANSACT_DATE_TIME`) BETWEEN '2022-12-01' AND '2022-12-29' AND `ID_ROUTE`=18067"

# print(query)
# df = get_df_from_sql(query)
# print(type(df))
# print(df)
# print(df.columns)
# print(df.head())
#
