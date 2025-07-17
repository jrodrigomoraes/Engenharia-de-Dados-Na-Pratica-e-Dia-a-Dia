def validate_data(df):
    df_valid = df.dropna()  #Remove registros com valores ausentes
    df_valid = df_valid[df_valid['idade'].apply(lambda x: isinstance(x, (int, float)) and 0 <= x <= 120)] #Valida idade nesse intervalo
    df_invalid = df[~df.index.isin(df_valid.index)] #Registros inválidos
    
    return df_valid, df_invalid
