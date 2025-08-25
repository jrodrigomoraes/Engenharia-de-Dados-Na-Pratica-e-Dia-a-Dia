import os
import pandas as pd
import boto3
from datetime import datetime
from scripts.utils import logger
from dotenv import load_dotenv

#Carregar variáveis de ambiente para acessar o S3
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
REGIAO = os.getenv("AWS_REGION", "us-east-1")


def salvar_em_parquet(df: pd.DataFrame, diretorio_saida: str):
    """
    Salva os dados em formato Parquet particionado por ano/mês/dia.
    """
    for data, grupo in df.groupby("data_particao"):
        try:
            ano, mes, dia = data.split("-")
        except ValueError:
            logger.error(f"Data de partição inválida: {data}")
            continue

        caminho_particionado = os.path.join(
            diretorio_saida,
            f"ano={ano}",
            f"mes={mes}",
            f"dia={dia}",
        )

        os.makedirs(caminho_particionado, exist_ok=True)

        nome_arquivo = f"logs_{data}.parquet"
        caminho_arquivo = os.path.join(caminho_particionado, nome_arquivo)

        grupo.drop(columns=["data_particao"]).to_parquet(
            caminho_arquivo,
            index=False,
            engine="pyarrow",
        )

        logger.info(f"Arquivo salvo em: {caminho_arquivo}")


def enviar_para_s3(diretorio_saida: str):
    """
    Envia os arquivos Parquet salvos localmente para um bucket S3.
    """
    if not BUCKET_NAME:
        logger.warning("Bucket S3 não definido. Upload ignorado.")
        return

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGIAO,
    )

    for root, _, files in os.walk(diretorio_saida):
        for file in files:
            if file.endswith(".parquet"):
                caminho_local = os.path.join(root, file)
                caminho_s3 = os.path.relpath(caminho_local, diretorio_saida)

                try:
                    s3_client.upload_file(
                        Filename=caminho_local,
                        Bucket=BUCKET_NAME,
                        Key=caminho_s3,
                    )
                    logger.info(f"Arquivo enviado ao S3: {caminho_s3}")
                except Exception as e:
                    logger.error(f"Erro ao enviar {file} para o S3: {e}")
