
import airflow
from airflow.models import DAG

# from airflow.hooks.mysql_hook import MySqlHook
# from airflow.operators.mysql_operator import MySqlOperator
# from airflow.operators.bash_operator import BashOperator
# from airflow.operators.python_operator import PythonOperator
# from airflow.operators.docker_operator import DockerOperator
# from airflow.providers.http.sensors.http import HttpSensor

from newsfeed.parsers.grab_news_belgorod import *
from newsfeed.parsers.vmo24 import *


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),       # this in combination with catchup=False ensures the DAG being triggered from the current date onwards along the set interval
    'provide_context': True,                            # this is set to True as we want to pass variables on from one task to another
}

with DAG(
    dag_id='newsfeed',
    default_args=args,
	schedule_interval='@daily',       # set interval
	catchup=False,                    # indicate whether or not Airflow should do any runs for intervals between the start_date and the current date that haven't been run thus far
) as dag:
    get_news_belgorod = PythonOperator(
    task_id='get_news_belgorod',
    python_callable=get_news_belgorod,           
    dag=dag,)
    
    get_news_vmo24 = PythonOperator(
    task_id='get_news_vmo24',
    python_callable=get_news_vmo24,           
    dag=dag,)

    get_news_belgorod>>get_news_vmo24     

# creating_table = MySqlOperator(
#         task_id='creating_tables',
#         mysql_conn_id='local_db',
#         sql = r"""
#         create TABLE if not exists users (
#             user_id integer primary key AUTO_INCREMENT,
#             firstname text not null,
#             lastname text not null,
#             username text not null,
#             password text not null    
#         );
#         """,
#         dag=dag,
#     )
    
# t1 = BashOperator(
# task_id='print_current_date',
# bash_command='date',
# dag=dag
# )

# t2 = DockerOperator(
# task_id='docker_command',
# image='centos:latest',
# api_version='auto',
# auto_remove=True,
# command="/bin/sleep 30",
# docker_url="tcp://docker-proxy:2375",#"unix://var/run/docker.sock",
# network_mode="bridge",
# dag=dag
# )

# is_api_available = HttpSensor(
#         task_id='is_api_available',
#         http_conn_id='user_api',
#         endpoint='api/',
#         dag=dag,
#     )


