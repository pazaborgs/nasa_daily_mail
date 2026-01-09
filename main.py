import requests
import smtplib
import ssl
from email.message import EmailMessage
from datetime import date
from deep_translator import GoogleTranslator
import os
from dotenv import load_dotenv
from jinja2 import Template


# --- Variáveis de Ambiente ---

load_dotenv()
API_KEY = os.getenv('NASA_API_KEY')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
receivers_env = os.getenv('EMAIL_RECEIVERS', '')
EMAIL_RECEIVERS = receivers_env.split(',') if receivers_env else []
APELIDO = os.getenv('APELIDO', 'Amor')
ASSINATURA = os.getenv('ASSINATURA', 'Seu Amado')

# --- Fetch API ---

print("Iniciando o processo...")
url = "https://api.nasa.gov/planetary/apod"
params = {
    'api_key': API_KEY,
    'date': date.today(),
    'hd': True
}

DEBUG_MODE = True  # Modo de depuração ativado

if not DEBUG_MODE:

    print("Consultando a NASA...")
    response = requests.get(url, params=params)
    data = response.json()

    # Verifica a resposta
    if response.status_code != 200:
        print(f"Erro na API da NASA: {response.status_code}")
        exit()

else:
    print("API fora do ar. Modo de depuração ativado: Usando dados de teste.")
    data = {
        "title": "The Starry Night (Test)",
        "explanation": "This is a test description used when the NASA API is down. It simulates the text to verify if the translator works correctly.",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/800px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
        "hdurl": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1200px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
        "copyright": "Vincent van Gogh",
        "date": "2024-01-01"
    }

# Extraindo os dados

image_url = data.get('hdurl', data.get('url'))
title_en = data.get('title', 'Sem título')
explanation_en = data.get('explanation', 'Sem descrição')
copyright_info = data.get('copyright', 'NASA Public Domain')

# --- Traduzindo os textos ---

print("Traduzindo textos...")

translator = GoogleTranslator(source='en', target='pt')
title_pt = translator.translate(title_en)
explanation_pt = translator.translate(explanation_en)

# --- Template da mensagem HTML ---

template_str = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { 
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
            background-color: #f0f8ff; /* AliceBlue */
            color: #555; 
            margin: 0;
            padding: 20px;
        }
        .paper { 
            background-color: #ffffff; 
            max-width: 600px; 
            margin: 0 auto; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(33, 150, 243, 0.15);
            border: 2px dashed #81d4fa; /* Azul Céu */
        }
        h1 { 
            color: #0277bd; /* Azul Profundo (Corrigido de rosa) */
            text-align: center; 
            font-family: 'Georgia', serif;
            font-style: italic;
            margin-bottom: 10px;
        }
        .date {
            text-align: center;
            color: #90a4ae;
            font-size: 0.9em;
            margin-bottom: 30px;
        }
        .intro {
            font-size: 1.1em;
            text-align: center;
            color: #37474f; /* Azul acinzentado escuro (Legibilidade melhorada) */
            margin-bottom: 25px;
            line-height: 1.6;
        }
        .img-box { 
            text-align: center; 
            margin: 20px 0; 
            padding: 12px;
            background-color: #e1f5fe; /* Fundo azul bem claro */
            border-radius: 8px;
        }
        img { 
            max-width: 100%; 
            border-radius: 4px; 
        }
        h3 {
            color: #039be5; /* Azul vibrante */
            border-bottom: 1px solid #b3e5fc; /* Borda azul clara (Corrigido de rosa) */
            padding-bottom: 10px;
            margin-top: 30px;
        }
        p { line-height: 1.8; }
        .footer { 
            margin-top: 40px; 
            font-size: 13px; 
            color: #78909c; /* Cinza azulado */
            text-align: center; 
            border-top: 1px solid #eceff1;
            padding-top: 20px;
        }
        .heart { color: #0288d1; } /* Coração Azul */
    </style>
</head>
<body>
    <div class="paper">
        <h1>✨ Para o meu Universo ✨</h1>
        <p class="date">{{ data_hoje }}</p>

        <p class="intro">
            Oi, {{ apelido }}! 💙<br>
            Olhei para o espaço hoje e lembrei de você!<br>
            {{ mensagem_personalizada }}
        </p>
        
        <div class="img-box">
            <img src="{{ image_url }}" alt="{{ title }}">
            <p style="font-size: 0.8em; color: #0277bd; margin-top: 8px;">
                <strong>{{ title }}</strong>
            </p>
        </div>
        
        <h3>O que estamos vendo?</h3>
        <p>{{ explanation }}</p>
        
        <div class="footer">
            Com todo o amor do mundo (e de todas as galáxias!),<br>
            <strong>Seu {{ assinatura }} <span class="heart">💙</span></strong>
            <br><br>
            <small style="font-size: 10px">Créditos da imagem: {{ copyright }}</small>
        </div>
    </div>
</body>
</html>
"""

# --- Renderizando o template com as variáveis ---

template = Template(template_str)
html_body = template.render(
    title=title_pt,
    data_hoje=date.today().strftime('%d/%m/%Y'),
    image_url=image_url,
    explanation=explanation_pt,
    copyright=copyright_info,
    apelido=APELIDO, 
    mensagem_personalizada = "O universo é infinito, mas você ainda é minha descoberta favorita!",
    assinatura=ASSINATURA
)

# --- Envio do email ---

print("Preparando email...")
msg = EmailMessage()
msg['From'] = EMAIL_SENDER
msg['To'] = ", ".join(EMAIL_RECEIVERS) 
msg['Subject'] = f'NASA APOD: {title_pt}'

msg.set_content(html_body, subtype='html')

context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())
    print("✅ E-mail enviado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao enviar e-mail: {e}")