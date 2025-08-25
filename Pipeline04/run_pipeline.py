import os
from glob import glob

from scripts.ingestion import ler_novos_logs, salvar_posicao, carregar_posicao
from scripts.transformation import transformar_linhas_em_dataframe
from scripts.validation import validar_dataframe
from scripts.load import salvar_em_parquet, enviar_para_s3
from scripts.utils import setup_logger, carregar_config

def main():
    #Carregar configurações
    config = carregar_config()

    #Setup do logger
    logger = setup_logger(config["paths"]["log_file"])
    logger.info("Iniciando pipeline de processamento de logs...")

    #Definições de caminhos e parâmetros
    raw_dir = config["paths"]["raw_data_dir"]
    output_dir = config["paths"]["output_data_dir"]
    extensoes = tuple(config["ingestion"]["file_extensions"])
    recursive = config["ingestion"]["recursive"]

    #Buscar todos os arquivos de log válidos
    arquivos_log = []
    if recursive:
        for ext in extensoes:
            arquivos_log.extend(glob(os.path.join(raw_dir, "**", f"*{ext}"), recursive=True))
    else:
        for ext in extensoes:
            arquivos_log.extend(glob(os.path.join(raw_dir, f"*{ext}")))

    if not arquivos_log:
        logger.info("Nenhum arquivo de log encontrado para processar.")
        return

    #Processar cada arquivo individualmente
    for log_file in arquivos_log:
        logger.info(f"Processando arquivo: {log_file}")

        #Arquivo de posição (salvo com base no nome do arquivo original)
        nome_base = os.path.basename(log_file)
        pos_file = os.path.join(raw_dir, f".{nome_base}.pos")

        #Carregar última posição lida
        pos_anterior = carregar_posicao(pos_file)

        #Ler novas linhas do log
        linhas, nova_pos = ler_novos_logs(log_file, pos_anterior)

        if not linhas:
            logger.info(f"Nenhuma nova linha em {log_file}.")
            continue

        # Transformar linhas em DataFrame
        df_transformado = transformar_linhas_em_dataframe(linhas)
        if df_transformado.empty:
            logger.warning(f"Nenhum dado válido após transformação em {log_file}.")
            continue

        # Validar DataFrame
        df_validado = validar_dataframe(df_transformado)
        if df_validado.empty:
            logger.warning(f"Nenhum dado válido após validação em {log_file}.")
            continue

        #Salvar localmente em Parquet
        salvar_em_parquet(df_validado, output_dir)

        # Enviar para S3, se ativado
        if config["load"].get("use_s3", False):
            enviar_para_s3(output_dir)

        # Atualizar posição lida
        salvar_posicao(pos_file, nova_pos)

        logger.info(f"Processamento finalizado para: {log_file}")

    logger.info("Pipeline concluído com sucesso!")

if __name__ == "__main__":
    main()
