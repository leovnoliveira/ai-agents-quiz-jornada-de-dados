import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_URL = os.getenv("HUGGINGFACE_MODEL_URL")

# Verificar se a API Key foi carregada corretamente
if not API_KEY or not MODEL_URL:
    raise ValueError("Chave da API ou URL do modelo não encontradas no .env!")

# Função para enviar uma pergunta ao modelo
def query_huggingface(question: str):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"inputs": question}

    response = requests.post(MODEL_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Erro na requisição: {response.status_code}, {response.text}"

if __name__ == "__main__":
    question = "Qual roadmap de aprendizado é recomendado para um Cientista de Dados pleno?"
    resposta = query_huggingface(question)
    print(resposta)