import pandas as pd

def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo CSV: {e}")