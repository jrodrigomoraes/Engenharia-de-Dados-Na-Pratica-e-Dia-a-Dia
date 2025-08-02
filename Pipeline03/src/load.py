import pandas as pd
import boto3
import yaml
from utils import setup_logger

#Inicializa o logger
logger = setup_logger()

#Carregar configurações do arquivo YAML
with open('settings.yaml', 'r') as file:
    settings = yaml.safe_load(file)

S3_BUCKET_NAME = settings['s3']['bucket_name']
S3_PATH = settings['s3']['processed_data_path']

def upload_to_s3(file_path, s3_path):
    """Envia o arquivo para o S3."""
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, S3_BUCKET_NAME, s3_path)
        logger.info(f"Arquivo {file_path} enviado para S3 em {s3_path}.")
    except Exception as e:
        logger.error(f"Erro ao enviar o arquivo para o S3: {e}")
        raise

def save_parquet_to_s3(df, s3_path):
    """Salva os dados no S3 como Parquet particionado."""
    local_file_path = '/tmp/processed.parquet'  # Caminho temporário para salvar o arquivo

    try:
        # Salvando como Parquet particionado
        df.to_parquet(local_file_path, partition_cols=['ano_mes'], engine='pyarrow', index=False)
        logger.info(f"Arquivo Parquet particionado gerado em: {local_file_path}")

        # Enviar para o S3
        upload_to_s3(local_file_path, s3_path)
    except Exception as e:
        logger.error(f"Erro ao salvar os dados no S3: {e}")
        raise
