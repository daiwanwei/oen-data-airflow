from datetime import datetime, timedelta
from airflow.decorators import task
from airflow.models.dag import dag
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


@dag(dag_id='test_dag', schedule_interval='0 * * * *', default_args=default_args)
def test_dag():

    @task()
    def generate_time_point_task() -> str:
        print('generate_time_point_task')
        return 'generate_time_point_task'

    generate_time_point_task()


test_dag = test_dag()
