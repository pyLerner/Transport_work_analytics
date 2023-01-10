import config
from sqlalchemy import create_engine
import pymysql
import pandas as pd

def get_df_from_sql(query: str):

    '''
    Возвращает pandas DataFrame по запросу query на языке SQL
    :return: DataFrame object
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
