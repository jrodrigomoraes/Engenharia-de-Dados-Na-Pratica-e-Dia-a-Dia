from src import ingestion, validation, transformation, load, utils

def main():
    logger = utils.setup_logger()

    logger.info("Início do pipeline")

    #1. Lendo o CSV
    df = ingestion.obter_dados_da_api(url, cabecalhos)

    #2. Validação
    df_valid, df_invalid = validation.validate_data(df)

    #3. Transformação
    df_clean = transformation.transform_data(df_valid)

    #4. Persistência dos dados válidos
    load.save_to_parquet(df_clean, path)

    #5. Armazenar registros inválidos
    df_invalid.to_csv("data/rejected/registros_invalidos.csv", index=False)

    logger.info(f"Processo finalizado com {len(df_clean)} registros válidos.")

if __name__ == "__main__":
    main()
