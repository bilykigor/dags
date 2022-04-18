
import airflow
from airflow.models import DAG

# from airflow.hooks.mysql_hook import MySqlHook
# from airflow.operators.mysql_operator import MySqlOperator
# from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
# from airflow.operators.docker_operator import DockerOperator
# from airflow.providers.http.sensors.http import HttpSensor

from newsfeed.parsers.news_yandex import get_news_yandex
from newsfeed.parsers.vmo24 import get_news_vmo24
from newsfeed.bot import send_news
import logging



args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),       # this in combination with catchup=False ensures the DAG being triggered from the current date onwards along the set interval
    'provide_context': True,                            # this is set to True as we want to pass variables on from one task to another
}

with DAG(
    dag_id='newsfeed',
    default_args=args,
	schedule_interval='@hourly',       # set interval
	catchup=False,                    # indicate whether or not Airflow should do any runs for intervals between the start_date and the current date that haven't been run thus far
) as dag:
    send_news = PythonOperator(
    task_id='send_news',
    python_callable=send_news,   
    trigger_rule='all_done',  
    #provide_context=True, 
    #do_xcom_push=True,     
    dag=dag,)
    
    regions=['belgorod','bryansk',
        'vladimir',
        'voronezh',
        'ivanovo',
        'Kaluga',
        'kostroma',
        'kursk',
        'lipetsk',
        'moscow',
        'Orel',
        'ryazan',
        'smolensk',
        'tambov',
        'tver',
        'tula',
        'saint_petersburg',
        'syktyvkar',
        'arhangelsk',
        'nenets_autonomous_okrug',
        'vologda',
        'saint-petersburg_and_leningrad_oblast',
        'murmansk',
        'pskov',
        'Republic_of_Ingushetia',
        'Nalchik',
        'krasnodar',
        'stavropol',
        'astrahan',
        'volgograd',
        'rostov-na-donu',
        'kazan',
        'yoshkar-ola'
    ]    
    
    get_news_yandex = PythonOperator(
    task_id=f'get_news_yandex',
    op_args=[regions],
    python_callable=get_news_yandex,  
    retries=2,
    retry_delay=60 * 20,        # 20 minutes  
    dag=dag,)
    
    get_news_yandex>>send_news
    
    get_news_vmo24 = PythonOperator(
    task_id='get_news_vmo24',
    python_callable=get_news_vmo24,           
    dag=dag,)
    
    get_news_vmo24>> send_news  

