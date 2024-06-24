from flask import Flask, render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_persona import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4"

app = Flask(__name__)
app.secret_key = 'chatbot'

context = carrega("dados/musica.txt")

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    personalidade = personas[selecionar_persona(prompt)]

    while True:
        try:
            prompt_do_sistema = f"""
            Você é um chatbot de música que informa os usuários sobre metal e shoegaze. 
            Você não deve responder perguntas que não pertençam aos dados informados!
            Você deve gerar respostas utilizando o contexto abaixo.
            Você deve adotar a persona abaixo
            #Contexto
            {context}

            #Persona
            {personalidade}
            """
            response = client.chat.completions.create(
                messages=[
                        {
                                "role": "system",
                                "content": prompt_do_sistema
                        },
                        {
                                "role": "user",
                                "content": prompt
                        }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model = model)
            return response
        except Exception as erro:
                repeticao += 1
                if repeticao >= maximo_tentativas:
                        return "Erro no GPT: %s" % erro
                print('Erro de comunicação com OpenAI:', erro)
                sleep(1)


@app.route("/chat", methods = ['POST'])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    texto_resposta = resposta.choices[0].message.content
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)