import requests
import json

def obter_dados_da_api(url, cabecalhos):
    resposta = requests.get(url, headers=cabecalhos)
    if resposta.status_code == 200:
        return resposta.json()  #Retorna os dados em formato JSON
    else:
        raise Exception(f"Erro ao acessar API: {resposta.status_code}")
