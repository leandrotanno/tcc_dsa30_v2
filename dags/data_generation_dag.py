# dags/data_generation_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.data.gerador_dados import (gerar_produtos, gerar_clientes, 
                                  gerar_campanhas, gerar_vendas, 
                                  gerar_navegacao)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'generate_ecommerce_data',
    default_args=default_args,
    description='Gera dados sintéticos do e-commerce',
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    task_produtos = PythonOperator(
        task_id='gerar_produtos',
        python_callable=gerar_produtos
    )
    
    task_clientes = PythonOperator(
        task_id='gerar_clientes',
        python_callable=gerar_clientes
    )
    
    task_campanhas = PythonOperator(
        task_id='gerar_campanhas',
        python_callable=gerar_campanhas
    )
    
    task_vendas = PythonOperator(
        task_id='gerar_vendas',
        python_callable=gerar_vendas
    )
    
    task_navegacao = PythonOperator(
        task_id='gerar_navegacao',
        python_callable=gerar_navegacao
    )
    
    # Define o fluxo
    task_produtos >> task_clientes >> task_campanhas >> task_vendas >> task_navegacao