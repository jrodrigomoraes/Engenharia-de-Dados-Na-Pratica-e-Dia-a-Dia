import os
from scripts.utils import logger

def ler_novos_logs(caminho_log: str, posicao_anterior: int = 0) -> (list[str], int):
    """
    Lê apenas as novas linhas adicionadas a um arquivo de log desde a última posição
    
    :param caminho_log: Caminho para o arquivo de log
    :param posicao_anterior: Posição anterior do ponteiro no arquivo
    :return: Lista as novas linhas e nova posição
    
    """
    
    if not os.path.exists(caminho_log):
        logger.warning(f'Arquivo de log não encontrado: {caminho_log}')
        return [], posicao_anterior
        
    novas_linhas = []
    with open(caminho_log, 'r', encoding='utf-8') as f:
        f.seek(posicao_anterior)
        novas_linhas = f.readlines()
        nova_posicao = f.tell()
        
    logger.info(f'Lidas {len(novas_linhas)} novas linhas do log.')
    return novas_linhas, nova_posicao
    
#Funções para salvar e carregar posição respectivamente, são funções auxiliares
#No arquivo run_pipeline.py, fica bem claro o papel delas
def salvar_posicao(caminho_pos: str, posicao: int):
    with open(caminho_pos, 'w') as f:
        f.write(str(posicao))
        
def carregar_posicao(caminho_pos: str) -> int:
    if os.path.exists(caminho_pos):
        with open(caminho_pos, 'r') as f:
            return int(f.read())
    return 0