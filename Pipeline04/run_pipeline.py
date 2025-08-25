import os
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
    processed_dir = config["paths"]["processed_data_dir"]
    output_dir = config["paths"]["output_data_dir"]
    extensoes = tuple(config["ingestion"]["file_extensions"])
    recursive = config["ingestion"]["recursive"]

    #Caminho para o arquivo de log principal (por enquanto assumimos 1 arquivo de log)
    log_file = os.path.join(raw_dir, "pipeline.log")
    pos_file = os.path.join(raw_dir, ".pos")  # Arquivo de controle da posição de leitura

    #Carregar última posição lida
    pos_anterior = carregar_posicao(pos_file)

    #Ler novas linhas de log
    linhas, nova_pos = ler_novos_logs(log_file, pos_anterior)

    if not linhas:
        logger.info("Nenhuma nova linha para processar. Encerrando.")
        return

    #Transformar linhas em DataFrame
    df_transformado = transformar_linhas_em_dataframe(linhas)
    if df_transformado.empty:
        logger.warning("Nenhum dado válido após transformação. Encerrando.")
        return

    #Validar DataFrame
    df_validado = validar_dataframe(df_transformado)
    if df_validado.empty:
        logger.warning("Nenhum dado válido após validação. Encerrando.")
        return

    #Salvar localmente em formato Parquet particionado
    salvar_em_parquet(df_validado, output_dir)

    #Enviar para S3, se ativado
    if config["load"].get("use_s3", False):
        enviar_para_s3(output_dir)

    #Atualizar posição de leitura
    salvar_posicao(pos_file, nova_pos)

    logger.info("Pipeline concluído com sucesso!")

if __name__ == "__main__":
    main()
