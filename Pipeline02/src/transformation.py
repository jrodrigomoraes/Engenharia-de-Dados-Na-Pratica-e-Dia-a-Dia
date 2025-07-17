def transform(df):
    df['idade'] = df['idade'].astype(int) #Garantindo idade inteiro
    df['nome'] = df['nome'].str.title()  #Capitalizar a primeira letra do nome
    
    return df
