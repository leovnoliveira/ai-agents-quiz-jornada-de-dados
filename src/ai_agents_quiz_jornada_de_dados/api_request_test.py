from fastapi import FastAPI, HTTPException
import sqlite3
from llama_cpp import Llama

# Carregar o modelo LLaMA 2 localmente
llama_model = Llama(model_path= r"C:\Users\Leonardo\jornada\Projeto\ai-agents-quiz-jornada-de-dados\.venv\Scripts\Llama-2-7B-Chat-GGUF")

app = FastAPI()

# Criar banco de dados SQLite para armazenar respostas dos usuários
conn = sqlite3.connect("quiz_respostas.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS respostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    experiencia TEXT,
    area TEXT,
    recomendacao TEXT
)
""")
conn.commit()

# Função para classificar usuário e recomendar roadmap
def gerar_recomendacao(respostas):
    prompt = f"""
    Um usuário respondeu a um quiz para saber qual roadmap ele deve seguir na Jornada de Dados.
    
    Respostas do usuário:
    {respostas}

    Baseado nessas respostas, determine:
    - O nível do usuário (Júnior, Pleno ou Sênior)
    - A área de atuação mais adequada (Analista de Dados, Engenheiro de Dados, Cientista de Dados)
    - O roadmap de aprendizado mais adequado da Jornada de Dados.
    
    Responda no formato:
    "Nível: [nível]; Área: [área]; Roadmap recomendado: [roadmap]"
    """

    resposta = llama_model(prompt)
    return resposta['choices'][0]['text'].strip()

@app.post("/quiz")
async def processar_quiz(usuario: str, experiencia: str, area: str):
    respostas = f"Experiência: {experiencia}, Área: {area}"
    recomendacao = gerar_recomendacao(respostas)

    cursor.execute("INSERT INTO respostas (usuario, experiencia, area, recomendacao) VALUES (?, ?, ?, ?)",
                   (usuario, experiencia, area, recomendacao))
    conn.commit()

    return {"usuario": usuario, "recomendacao": recomendacao}


