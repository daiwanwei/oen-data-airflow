import logging

import pandas as pd
import psycopg2
from airflow.models import Variable


def get_db_conn_from_env():
    postgresql_dsn = Variable.get("postgresql_dsn")
    conn = psycopg2.connect(postgresql_dsn)
    return conn


def insert_to_db(conn: psycopg2.extensions.connection, csv_file: str, insert_sql: str, params: tuple):
    cursor = conn.cursor()
    df = pd.read_csv(csv_file)
    conn.autocommit = True
    try:
        for index, row in df.iterrows():
            try:
                row_data = tuple(row[x] for x in params)
                print(f'inserted {row_data}, {index}')
                cursor.execute(insert_sql, row_data)

            except psycopg2.IntegrityError as err:
                if err.pgcode == '23505':
                    logging.warning("Data already exists: {}".format(err))
                    continue
                else:
                    msg = "Something went wrong: {},data({})".format(err, row_data)
                    logging.error(msg)
                    raise err
        conn.commit()
    except Exception as err:
        conn.rollback()
        msg = "Something went wrong: {}".format(err)
        logging.error(msg)
        raise err
    finally:
        cursor.close()
        conn.close()
