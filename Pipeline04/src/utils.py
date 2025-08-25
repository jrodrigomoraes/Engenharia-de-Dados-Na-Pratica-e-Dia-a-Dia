from loguru import logger
import os
import yaml

def setup_logger(log_path="logs/pipeline.log"):
    """
    Garante que o diretório do log exista, e aplica rotação e retenção.
    
    Parâmetros:
        log_path (str): Caminho para o arquivo de log.
    
    Retorna:
        logger (loguru.logger): Instância do logger configurado.
    """
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger.remove()
    logger.add(
        log_path,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}",
        rotation="10 MB",
        retention="7 days",
    )
    return logger

def carregar_config(caminho_config="configs/settings.yaml"):
    """
    Carrega as configurações do pipeline a partir de um arquivo YAML.
    
    Parâmetros:
        caminho_config (str): Caminho para o arquivo de configuração YAML.
    
    Retorna:
        dict: Dicionário com as configurações carregadas.
    """
    with open(caminho_config, "r") as f:
        return yaml.safe_load(f)