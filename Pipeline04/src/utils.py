from loguru import logger
import os

# Diretório onde o log será armazenado
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Nome fixo para o log do pipeline
LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")

#Remove o logger padrão para evitar duplicações
logger.remove()

#Adicionar um novo logger com formato personalizado
logger.add(
    LOG_FILE,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}",
    rotation="10 MB",        # Rotaciona o log ao atingir 10 MB
    retention="7 days",      # Mantém logs antigos por 7 dias
)

__all__ = ["logger"]