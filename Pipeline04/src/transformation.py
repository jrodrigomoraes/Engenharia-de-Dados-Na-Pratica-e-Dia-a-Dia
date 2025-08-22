import pandas as pd
import yaml
from utils import setup_logger  # Lembre-se do utils.py

#Inicializa logger
logger = setup_logger()

#Função para carregar as configurações do arquivo YAML
def load_settings():
    with open("settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    return settings

#Carregar configurações
settings = load_settings()

#Caminho para dados intermediários e de saída, configuráveis
INTERMEDIATE_PATH = os.path.join(settings['pipeline']['processed_data_dir'], 'ingested.parquet')
PROCESSED_PATH = os.path.join(settings['pipeline']['processed_data_dir'], 'processed.parquet')

def classifa_valor(valor):
    """Classifica o valor da transação em 'alto', 'baixo' ou 'moderado'."""
    if valor > 500:
        return 'alto'
    elif valor < 50:
        return 'baixo'
    else:
        return 'moderado'

def transform_data(df):
    """Realiza as transformações necessárias no DataFrame."""
    
    #Garantir que a coluna 'data' está no formato datetime
    try:
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        logger.info("Coluna 'data' convertida para datetime.")
    except Exception as e:
        logger.error(f"Erro ao converter a coluna 'data': {e}")
        raise

    #Remover duplicatas
    df = df.drop_duplicates()
    logger.info(f"Duplicatas removidas. Total de registros: {len(df)}")

    #Remover registros com valores nulos
    df = df.dropna()
    logger.info(f"Registros com valores nulos removidos. Total de registros: {len(df)}")

    #Garantir que os dados numéricos estejam no formato correto
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    logger.info("Coluna 'valor' convertida para numérica.")

    #Padronizar textos (categorias) usando Unicode
    df['categoria'] = df['categoria'].str.normalize('NFKD').str.encode('ASCII', errors='ignore').str.decode('ASCII')
    logger.info("Coluna 'categoria' padronizada.")

    #Criar novas colunas (ex: 'ano_mes' para particionamento)
    df['ano_mes'] = df['data'].dt.to_period('M').dt.strftime('%Y-%m')
    logger.info("Nova coluna 'ano_mes' criada.")

    #Classificar a coluna 'valor' em categorias: 'alto', 'moderado' ou 'baixo'
    df['categoria_valor'] = df['valor'].apply(classifa_valor)
    logger.info("Nova coluna 'categoria_valor' criada com a classificação do valor.")

    return df

def df_transformado(df):
    """Salva os dados transformados em formato Parquet."""
    df.to_parquet(PROCESSED_PATH, index=False)
    logger.info(f"Dados transformados salvos em: {PROCESSED_PATH}")
