from src.ai_agents_quiz_jornada_de_dados.api_request_test import gerar_recomendacao
import gradio as gr

def quiz_interface(usuario, experiencia, area):
    recomendacao = gerar_recomendacao(f"Experiência: {experiencia}, Área: {area}")
    return f"Recomendação para {usuario}: {recomendacao}"

gr.Interface(
    quiz_interface,
    inputs=["text", "dropdown", "dropdown"],
    outputs="text",
    title="AI Quiz - Roadmap de Dados",
    description="Responda ao quiz para receber a recomendação ideal na Jornada de Dados.",
    examples=[
        ["Leonardo", "Pleno", "Engenheiro de Dados"],
        ["Ana", "Júnior", "Analista de Dados"]
    ]
).launch()
