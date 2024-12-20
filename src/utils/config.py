from dotenv import load_dotenv
import os
import configparser

def load_db_config():
    load_dotenv()
    
    # Primeiro tenta ler do .env
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    
    # Se não encontrar no .env, tenta ler do database.ini
    if not all(db_config.values()):
        config = configparser.ConfigParser()
        config.read('config/database.ini')
        db_config = dict(config['postgresql'])
    
    return db_config