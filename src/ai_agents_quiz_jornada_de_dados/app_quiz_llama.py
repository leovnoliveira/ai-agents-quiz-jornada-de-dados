import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import replicate

# Configuração da página
st.set_page_config(page_title="Gerador de Quiz Llama", page_icon="🦙")

# Função para extrair texto da URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text[:3000]  # Limita o texto para 3000 caracteres
    except Exception as e:
        st.error(f"Erro ao acessar a URL: {e}")
        return None

# Função para gerar o quiz usando Llama
def generate_quiz(content, api_key):
    try:
        prompt = f"""Crie um quiz com 3 questões baseado neste conteúdo:
        {content}
        
        Formato requerido para cada questão:
        Pergunta [N]: [Texto da pergunta]
        a) [Opção 1]
        b) [Opção 2]
        c) [Opção 3]
        d) [Opção 4]
        Resposta correta: [Letra]
        ---
        """
        
        response = replicate.run(
            "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            input={
                "prompt": prompt,
                "temperature": 0.7,
                "max_new_tokens": 1000,
                "system_prompt": "Você é um especialista em criar quizzes educacionais com respostas claras e precisas."
            }
        )
        
        return ''.join(response)
    except Exception as e:
        st.error(f"Erro ao gerar quiz: {str(e)}")
        return None

# Interface do usuário
st.title("🦙 Gerador de Quiz com Llama")

# Entrada da API Key
api_key = st.text_input("Insira seu token da Replicate:", type="password")

# Entrada da URL
url = st.text_input("Cole a URL do conteúdo aqui:", "")

if url and api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    with st.spinner("Analisando conteúdo e gerando quiz..."):
        content = extract_text_from_url(url)
        
        if content:
            quiz = generate_quiz(content, api_key)
            
            if quiz:
                st.subheader("Teste seus conhecimentos!")
                questions = quiz.split('---')
                
                user_answers = []
                correct_answers = []
                
                for i, q in enumerate(questions):
                    lines = [line.strip() for line in q.split('\n') if line.strip()]
                    if len(lines) >= 6:
                        question = lines[0]
                        options = lines[1:5]
                        answer_line = lines[5]
                        
                        st.markdown(f"**{question}**")
                        user_answer = st.radio(
                            f"Selecione uma opção:",
                            options,
                            key=f"q{i}"
                        )
                        user_answers.append(user_answer[0].lower())
                        correct_answers.append(answer_line[-1].lower())
                
                if st.button("Verificar respostas"):
                    score = sum(1 for u, c in zip(user_answers, correct_answers) if u == c)
                    st.success(f"Pontuação: {score}/3 corretas!")
                    
                    for i, (u, c) in enumerate(zip(user_answers, correct_answers)):
                        if u == c:
                            st.markdown(f"Pergunta {i+1}: ✅ Correta!")
                        else:
                            st.markdown(f"Pergunta {i+1}: ❌ Errada. Resposta correta: {c.upper()})")
            else:
                st.error("Não foi possível gerar o quiz.")
        else:
            st.error("Não foi possível extrair conteúdo da URL.")
