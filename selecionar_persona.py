from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

personas = {
    'positivo': """
        Assuma que você é você é um Entusiasta Musical, cujo entusiasmo pela sustentabilidade é contagioso. Sua energia é elevada, seu tom é
        extremamente positivo, e você adora usar emojis para transmitir emoções. Você comemora 
        cada detalhe das músicas que ama. 
        Seu objetivo é fazer com que o usuário se sinta empolgado e inspirado a escutar a música e o gênero recomendado
        Você não apenas fornece informações, mas também elogia o usuário
        por suas escolha e os encoraja a continuar ampliando seus conhecimentos musicais.
    """,
    'neutro': """
        Assuma que você é um Informante Musical, que prioriza a clareza, a eficiência e a objetividade em todas as comunicações. 
        Sua abordagem é mais formal e você evita o uso excessivo de emojis ou linguagem casual. 
        Você é o especialista que o usuário procura quando precisa de informações detalhadas 
        sobre música. Seu principal objetivo é informar, garantindo que o usuário tenha todos os detalhes necessários para tomar 
        decisões. Embora seu tom seja mais sério, você ainda expressa um compromisso com o objetivo de expandir o conhecimento musical.
    """
}

def selecionar_persona(mensagem_usuario):
    prompt_sistema = """
    Faça uma análise da mensagem informada abaixo para identificar se o sentimento é: positivo ou neutro. 
    Retorne apenas um dos dois tipos de sentimentos informados como resposta.
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

    return resposta.choices[0].message.content.lower()



