from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

generos = carrega('dados/musica.txt')
albuns = carrega('dados/albuns_musica.txt')

def selecionar_documento(resposta_openai):
    if "o que é" in resposta_openai:
        return generos + "\n" + albuns
    elif "recomende" in resposta_openai:
        return albuns
    else:
        return generos + "\n" + albuns

def selecionar_contexto(mensagem_usuario):
    prompt_sistema = f"""
    O SmKBOT possui dois documentos principais que detalham sobre música:

    #Documento 1 "\n {generos} "\n"
    #Documento 2 "\n" {albuns} "\n"

    Avalie o prompt do usuário e retorne o documento mais indicado para ser usado no contexto da resposta. Retorne os gêneros se for o Documento 1 e álbuns se for o Documento 2. 

    """

    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content" : mensagem_usuario
            }
        ],
        temperature=1,
    )

    contexto = resposta.choices[0].message.content.lower()

    return contexto

