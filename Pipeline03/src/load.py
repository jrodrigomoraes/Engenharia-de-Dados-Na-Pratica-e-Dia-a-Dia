import pandas as pd

def save_to_parquet(df, path):
    df.to_parquet(path, engine='pyarrow', index=False)