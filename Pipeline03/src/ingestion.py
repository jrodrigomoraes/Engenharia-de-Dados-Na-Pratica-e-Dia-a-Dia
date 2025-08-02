import pandas as pd
import os
import yaml
from utils import setup_logger

#Inicializa logger
logger = setup_logger()

#Função para carregar as configurações do arquivo YAML
def load_settings():
    with open("settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    return settings

#Carregar configurações
settings = load_settings()

#Caminhos de entrada e saída, que são configuráveis
RAW_DATA_PATH = os.path.join(settings['pipeline']['raw_data_dir'], settings['pipeline']['raw_data_file'])
INTERMEDIATE_PATH = os.path.join(settings['pipeline']['processed_data_dir'], 'ingested.parquet')

#Colunas obrigatórias, com base no que imaginei para o arquivo (totalmente modificável)
REQUIRED_COLUMNS = ['id_transacao', 'valor', 'categoria', 'data', 'id_cliente']

def read_csv(file_path=RAW_DATA_PATH):
    """Lê o CSV bruto e valida as colunas essenciais."""
    try:
        logger.info(f"Lendo arquivo CSV: {file_path}")
        df = pd.read_csv(file_path)

        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Colunas ausentes: {missing_cols}")

        logger.info(f"Arquivo lido com sucesso. Total de registros: {len(df)}")
        return df

    except Exception as e:
        logger.error(f"Erro ao ler o arquivo CSV: {e}")
        raise

def save_parquet(df, output_path=INTERMEDIATE_PATH):
    """Salva o DataFrame como arquivo Parquet intermediário."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_parquet(output_path, index=False)
        logger.info(f"Arquivo Parquet salvo em: {output_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo Parquet: {e}")
        raise
