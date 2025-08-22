import logging

def setup_logger():
    logger = logging.getLogger('pipeline_logger')
    logger.setLevel(logging.INFO)
    
    #Criando o handler para log no arquivo
    file_handler = logging.FileHandler('logs/pipeline.log')
    file_handler.setLevel(logging.INFO)
    
    #Criando o formatador para formatar as mensagens
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    #Adicionando o handler ao logger
    logger.addHandler(file_handler)
    
    return logger
