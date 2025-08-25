import pandas as pd
from scripts.utils import logger

#Lista de níveis válidos
niveis_validos = ['INFO', 'WARNING', 'ERROR', 'DEBUG', 'CRITICAL']

def validar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida os registros do DataFrame e remove entradas incompletas ou inválidas
    
    Campos Obrigatórios:
    timestamp, level, service, host
    """
    colunas_esperadas = ['timestamp', 'level', 'service', 'message', 'user_id', 'host', 'data_particao']
    
    if df.empty:
        logger.warning("DataFrame vazio recebido")
        return df
        
    #Validar as colunas e verificar se todas estão presentes
    
    if set(df.columns) != set(colunas_esperadas):
        logger.error(f"Colunas inválidas no DataFrame: {df.columns.tolist()}")
        logger.error(f"Esperado: {colunas_esperadas}")
        return pd.DataFrame()
        
    total = len(df)
    
    df_validado = df[
        df['timestamp'].notna() &
        df['level'].isin(niveis_validos) &
        df['service'].notna() &
        df['host'].notna()
    ]
    
    validos = len(df_validado)
    removidos = total - validos
    
    logger.info(f"Validação concluída: {validos} válidos, {removidos} removidos.")
    
    return df_validado.reset_index(drop=True)