# dags/data_load_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def load_csv_to_postgres(filename, table_name, **context):
    df = pd.read_csv(filename)
    conn = context['task_instance'].xcom_pull(task_ids='create_connection')
    df.to_sql(table_name, conn, if_exists='replace', index=False)

with DAG(
    'load_ecommerce_data',
    default_args=default_args,
    description='Carrega dados do e-commerce no PostgreSQL',
    schedule_interval='@daily',
    catchup=False
) as dag:

    load_produtos = PythonOperator(
        task_id='load_produtos',
        python_callable=load_csv_to_postgres,
        op_kwargs={
            'filename': 'produtos.csv',
            'table_name': 'produtos'
        }
    )
    
    load_clientes = PythonOperator(
        task_id='load_clientes',
        python_callable=load_csv_to_postgres,
        op_kwargs={
            'filename': 'clientes.csv',
            'table_name': 'clientes'
        }
    )
    
    load_vendas = PythonOperator(
        task_id='load_vendas',
        python_callable=load_csv_to_postgres,
        op_kwargs={
            'filename': 'vendas.csv',
            'table_name': 'vendas'
        }
    )
    
    # Define o fluxo
    load_produtos >> load_clientes >> load_vendas