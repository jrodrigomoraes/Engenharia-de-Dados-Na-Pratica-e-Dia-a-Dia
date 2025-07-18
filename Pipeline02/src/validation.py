import re

def validate_data(df):
    #Definindo expressões regulares para validação das categorias email, telefone e website
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    phone_regex = r'^\+?[0-9]{10,15}$'  # Ex: +5511999999999 ou 11999999999
    website_regex = r'^https?:\/\/[\w\-\.]+\.\w+.*$'

    #Criando Máscaras de validação
    valid_email = df['email'].str.match(email_regex, na=False)
    valid_phone = df['telefone'].str.match(phone_regex, na=False)
    valid_website = df['website'].str.match(website_regex, na=False)

    #Validação combinada: todos os campos devem estar válidos
    valid_mask = valid_email & valid_phone & valid_website

    #Separando válidos e inválidos
    df_valid = df[valid_mask]
    df_invalid = df[~valid_mask]

    return df_valid, df_invalid