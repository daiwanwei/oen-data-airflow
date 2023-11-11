import logging
from datetime import datetime, timedelta
from airflow.decorators import task
from airflow.models.dag import dag
from airflow.utils.dates import days_ago

from open_data.defi.tasks.debank import get_user_balances_task_logic, parse_user_balances_task_logic, \
    load_asset_balances_to_db_task
from open_data.utils.common import gen_ts_filename, get_execution_date

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'retries': 0
}


@dag(schedule_interval='3 * * * *', default_args=default_args)
def debank_user_balances_dag():
    prefix = 'debank_user_balances'
    dir_path = './tmp_files'

    @task()
    def get_user_balances_task() -> list[str]:
        # time_point = datetime.now()
        # if abs(time_point.minute - 3) <= 1:
        #     time_point = time_point.replace(minute=0, second=0, microsecond=0)
        # else:
        #     return []
        time_point = datetime.now()
        logging.info(f'execution date is {time_point}')
        file_paths = get_user_balances_task_logic(time_point, dir_path)
        return file_paths

    @task()
    def parse_user_balances_task(file_paths: list[str]) -> str:
        csv_file = gen_ts_filename(f'./tmp_files/{prefix}_user_balances_data.csv')
        parse_user_balances_task_logic(csv_file, file_paths)
        print(f'parse_user_balances_task : {csv_file}')
        return csv_file

    @task()
    def load_user_balances_task(csv_file: str):
        print(f'load_user_balances_task : {csv_file}')
        load_asset_balances_to_db_task(csv_file)

    load_user_balances_task(parse_user_balances_task(get_user_balances_task()))


debank_user_balances_dag = debank_user_balances_dag()
