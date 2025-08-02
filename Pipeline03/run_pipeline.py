import pandas as pd
from src.ingestion import read_csv, save_parquet
from src.transformation import transform_data
from src.validation import validate_data
from src.load import save_parquet_to_s3
from src.utils import setup_logger

# Inicializa o logger
logger = setup_logger()

# Caminhos
RAW_DATA_PATH = 'data/input/transactions.csv'
INTERMEDIATE_PATH = 'data/processed/ingested.parquet'
PROCESSED_PATH = 'data/processed/processed.parquet'

def run_pipeline():
    try:
        #Passo 1: Ingestão dos dados
        logger.info("Iniciando a ingestão de dados...")
        df = read_csv(RAW_DATA_PATH)  # Lê o arquivo CSV
        save_parquet(df, INTERMEDIATE_PATH)  # Salva como Parquet intermediário

        #Passo 2: Transformação dos dados
        logger.info("Iniciando a transformação dos dados...")
        df_transformed = transform_data(df)  # Aplica as transformações no DataFrame
        save_parquet(df_transformed, PROCESSED_PATH)  # Salva os dados transformados localmente

        #Passo 3: Validação dos dados
        logger.info("Validando os dados...")
        if not validate_data(df_transformed):  # Valida o DataFrame transformado
            logger.error("Falha na validação dos dados. O pipeline será interrompido.")
            return

        #Passo 4: Carregamento para o S3
        logger.info("Carregando dados para o S3...")
        save_parquet_to_s3(df_transformed, 'data/processed/transactions')  # Envia para o S3

        logger.info("Pipeline executado com sucesso!")

    except Exception as e:
        logger.error(f"Erro durante a execução do pipeline: {e}")

if __name__ == "__main__":
    run_pipeline()