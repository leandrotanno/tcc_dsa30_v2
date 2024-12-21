# E-commerce Analytics Project

Projeto de análise de dados de e-commerce usando Python, Airflow e PostgreSQL para previsão de vendas e análises de marketing digital.

## Tecnologias Utilizadas
- Python 3.9
- Apache Airflow 2.7.3
- PostgreSQL
- Docker e Docker Compose
- Jupyter Lab

## Pré-requisitos
- Docker instalado
- Docker Compose instalado
- Git instalado

## Estrutura do Projeto
ecommerce_analytics/ \
├── dags/                 # Airflow DAGs \
├── notebooks/            # Jupyter notebooks \
├── plugins/              # Plugins do Airflow \
├── sql/                  # Scripts SQL \
├── src/                  # Código fonte \
├── data/                 # Dados gerados \
├── logs/                 # Logs do Airflow \
├── .env                  # Variáveis de ambiente \
└── docker-compose.yml    # Configuração dos containers

## Setup do Projeto

1. Clone o repositório:
```bash
git clone https://github.com/leandrotanno/tcc_dsa30_v2.git
cd cc_dsa30_v2
```
2. Copie o .env.example:
```bash
cp .env.example .env
```

3. Edite .env com seus dados:
```bash
DB_USER=postgres
DB_PASSWORD=postgres123
FERNET_KEY=sua_fernet_key_aqui # gerar key: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
AIRFLOW_UID=50000
```

4. Crie as pastas necessárias e ajuste as permissões:
```bash
mkdir -p ./dags ./logs ./plugins
chmod -R 777 ./dags ./logs ./plugins
```

5. Inicie os containers:
```bash
docker compose up -d
```

## Acessando as Interfaces
Após a inicialização, você pode acessar:

Jupyter Lab: http://localhost:8888 \
Apache Airflow: http://localhost:8080

Username: admin \
Password: admin


## PostgreSQL:

Host: localhost \
Port: 5432 \
Database: ecommerce \
User: (definido no .env) \
Password: (definido no .env)



## Gerando dados sintéticos
Os dados são gerados automaticamente através de DAGs no Airflow. Para executar:

Acesse o Airflow (http://localhost:8080) \
Ative as DAGs na interface:

generate_ecommerce_data.py \
load_ecommerce_data.py \
create_analytics_tables.py

## Parando o ambiente
Para parar os containers:
```bash
docker compose down
```

## Para remover volumes e começar do zero:
```bash
docker compose down -v
```

## Troubleshooting

Se encontrar problemas de permissão:
```bash
sudo chown -R $USER:$USER ./dags ./logs ./plugins
chmod -R 777 ./dags ./logs ./plugins
```
