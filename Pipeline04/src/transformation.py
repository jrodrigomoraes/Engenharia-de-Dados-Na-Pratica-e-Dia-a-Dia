import re
import pandas as pd
from datetime import datetime
from scripts.utils import logger

LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - '
    r'(?P<level>[A-Z]+) - '
    r'(?P<service>[a-z\-]+) - '
    r'(?P<message>.*?) - '
    r'user_id=(?P<user_id>\d+)? - '
    r'host=(?P<host>[\w\-\.]+)$'
)
    
def transformar_linhas_em_dataframe(linhas: list[str]) -> pd.DataFrame:
    """
    Transforma uma lista de linhas de log em um Dataframe estruturado
    """
    
    registros = []
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        
        match = LOG_PATTERN.match(linha)
        if match:
            dados = match.groupdict() #Por isso nomeamos os grupos na regex
            try:
                dados['timestamp'] = pd.to_datetime(dados['timestamp']) #Converte a string em um objeto Timestamp
                registros.append(dados)
            except Exception as e:
                logger.warning(f'Erro ao converter timestamp: {dados['timestamp']} - {e}')
                
        else:
            logger.warning(f'Linha fora do padrão e ignorada: {linha}')
        
    if not registros:
        logger.info('Nenhuma linha válida encontrada.')
        return pd.Dataframe() #dataframe vazio é retornado
        
    df = pd.DataFrame(registros)
    
    #Criando coluna de Particionamento
    df['data_particao'] = df['timestamp'].dt.strftime('%Y-%m-%d')
    
    logger.info(f'{len(df)} registros estruturados com sucesso.')
    
    return df