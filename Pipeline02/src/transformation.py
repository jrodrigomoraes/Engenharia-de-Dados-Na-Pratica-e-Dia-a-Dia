def transform_data(df):
    df['nome'] = df['nome'].str.title()
    return df
