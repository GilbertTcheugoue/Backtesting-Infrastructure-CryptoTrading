from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


with DAG(
    dag_id="backt_example",
    description="A simple DAG that prints 'Hello World' to the logs",
    start_date=datetime(2024, 6, 21),
    schedule_interval="@daily",
    catchup=False,
    tags=["atest"],
) as dag:
    def print_hello():
        print("Hello World")

    print_task = PythonOperator(
        task_id="print_hello",
        python_callable=print_hello
    )