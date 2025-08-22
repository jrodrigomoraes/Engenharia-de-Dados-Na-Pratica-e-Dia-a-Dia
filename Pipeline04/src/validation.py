import pandas as pd
from utils import setup_logger

#Inicializa logger
logger = setup_logger()

def validate_data(df):
    """Valida a integridade e qualidade dos dados com checagens mínimas."""
    
    #Verificar colunas obrigatórias
    required_columns = ['id_transacao', 'valor', 'categoria', 'data', 'id_cliente', 'ano_mes', 'categoria_valor']
    if not all(col in df.columns for col in required_columns):
        logger.error(f"Colunas obrigatórias ausentes!")
        return False

    #Verificar valores nulos
    if df.isnull().any().any():
        logger.error("Dados nulos encontrados.")
        return False

    #Verificar valores negativos na coluna 'valor'
    if (df['valor'] < 0).any():
        logger.error("Valores negativos encontrados na coluna 'valor'.")
        return False

    #Verificar unicidade do 'id_transacao'
    if not df['id_transacao'].is_unique:
        logger.error("A coluna 'id_transacao' não é única.")
        return False

    logger.info("Validação concluída com sucesso.")
    return True
