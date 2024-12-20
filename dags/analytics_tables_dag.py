# dags/analytics_tables_dag.py
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'create_analytics_tables',
    default_args=default_args,
    description='Cria tabelas analíticas do e-commerce',
    schedule_interval='@daily',
    catchup=False
) as dag:

    create_vendas_diarias = PostgresOperator(
        task_id='create_vendas_diarias',
        postgres_conn_id='postgres_default',
        sql="""
        CREATE TABLE IF NOT EXISTS analytics.vendas_diarias AS
        SELECT 
            DATE(v.data_venda) as data,
            COUNT(DISTINCT v.venda_id) as num_vendas,
            SUM(v.valor_total) as receita_total,
            AVG(v.valor_total) as ticket_medio
        FROM vendas v
        GROUP BY 1;
        """
    )
    
    create_metricas_marketing = PostgresOperator(
        task_id='create_metricas_marketing',
        postgres_conn_id='postgres_default',
        sql="""
        CREATE TABLE IF NOT EXISTS analytics.metricas_marketing AS
        SELECT 
            c.plataforma,
            c.tipo_midia,
            SUM(mc.custo_total) as investimento_total,
            SUM(mc.conversoes) as total_conversoes,
            SUM(mc.valor_conversoes) as receita_total,
            ROUND(SUM(mc.valor_conversoes)::numeric / 
                  NULLIF(SUM(mc.custo_total), 0)::numeric, 2) as roas
        FROM campanhas c
        JOIN metricas_campanhas mc ON c.campanha_id = mc.campanha_id
        GROUP BY 1, 2;
        """
    )
    
    create_perfil_clientes = PostgresOperator(
        task_id='create_perfil_clientes',
        postgres_conn_id='postgres_default',
        sql="""
        CREATE TABLE IF NOT EXISTS analytics.perfil_clientes AS
        SELECT 
            c.estado_civil,
            c.faixa_renda,
            COUNT(DISTINCT v.venda_id) as total_compras,
            COUNT(DISTINCT c.cliente_id) as total_clientes,
            ROUND(AVG(v.valor_total)::numeric, 2) as ticket_medio
        FROM clientes c
        LEFT JOIN vendas v ON c.cliente_id = v.cliente_id
        GROUP BY 1, 2;
        """
    )
    
    # Define o fluxo
    create_vendas_diarias >> create_metricas_marketing >> create_perfil_clientes