import requests
import json

def fetch_data_from_api(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  #Retorna os dados em formato JSON
    else:
        raise Exception(f"Erro ao acessar API: {response.status_code}")