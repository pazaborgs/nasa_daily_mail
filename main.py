import requests
import smtplib
import ssl
from email.message import EmailMessage
from datetime import date
from deep_translator import GoogleTranslator
import os
from dotenv import load_dotenv
from jinja2 import Template
import google.generativeai as genai
import random

# --- Variáveis de Ambiente ---

load_dotenv()
API_KEY = os.getenv('NASA_API_KEY')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
receivers_env = os.getenv('EMAIL_RECEIVERS', '')
EMAIL_RECEIVERS = receivers_env.split(',') if receivers_env else []
APELIDO = os.getenv('APELIDO', 'Amor')
ASSINATURA = os.getenv('ASSINATURA', 'Seu Amado')

# --- Funções de Busca Dedicadas (NASA x Chicago Art Institute)

def get_art_data():
    '''Busca uma arte aleatória no Art Institute of Chicago'''
    print('🎨 Tentando conectar com o Art Institute of Chicago... \n')

    try:
        # Simula um navegador para conexão
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.artic.edu/',
            'Origin': 'https://www.artic.edu',
            'Connection': 'keep-alive'
        }

        random_page = random.randint(1, 100) # Escolhe uma página aleatória no site
        url = 'https://api.artic.edu/api/v1/artworks/search'
        params = {
            'query[term][is_public_domain]': 'true',
            'fields': 'id,title,artist_display,image_id,description,date_display,medium_display',
            'limit': 10,
            'page': random_page
        }
            
        session = requests.Session()
        response = session.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('data'): return None
        
        artwork = random.choice(data['data'])
        image_id = artwork.get('image_id')
        
        # Backup de imagem
        if not image_id:
            for i in data['data']:
                if i.get('image_id'):
                    artwork = i
                    image_id = i.get('image_id')
                    break
            if not image_id: return None

        image_url = f'https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg'
        
        # Limpeza da descrição da obra
        desc = artwork.get('description')
        if desc:
            desc = str(desc).replace('<p>', '').replace('</p>', '').replace('<em>', '').replace('</em>', '')
        else:
            # CORREÇÃO 1: Aspas duplas na f-string externa para não conflitar com as internas
            desc = f"Uma obra criada por {artwork.get('artist_display')} usando a técnica {artwork.get('medium_display')}, datada de {artwork.get('date_display')}."

        # Traduzindo as informações da obra
        print('Traduzindo detalhes da obra...')
        translator = GoogleTranslator(source='auto', target='pt')
        
        try:
            title_pt = translator.translate(artwork.get('title', 'Obra'))
            explanation_pt = translator.translate(desc[:4500])
        except:
            title_pt = artwork.get('title', 'Obra')
            explanation_pt = desc

        return {
            'source': 'art',
            'type': 'art',
            'title': title_pt,
            'explanation': explanation_pt,
            'image_url': image_url,
            'video_url': None,
            'copyright_info': artwork.get('artist_display', 'Artista Desconhecido'),
            'emoji': '🎨',
            'theme_color': '#880e4f',
            'bg_color': '#fce4ec',
            'intro_text': 'A NASA estava tímida hoje, mas encontrei esta obra de arte para você!'
        }
    
    except Exception as e:
        print(f'❌ Erro na API de Arte (Chicago): {e}')
        return None

def get_nasa_data(mock_data = None):
    '''Busca uma a Imagem Astronômica do Dia usando a API APOD da NASA'''

    print('🌌 Tentando conectar com a API da NASA... \n')

    if mock_data:
        print('⚠️ MODO DE TESTE ATIVADO: Usando dados simulados.\n')
        data = mock_data
    else:
        url = 'https://api.nasa.gov/planetary/apod'
        params = {
            'api_key': API_KEY,
            'date': date.today(),
            'hd': True,
            'thumbs': True
            }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f'❌ Erro na API da NASA: {e}')
            return None

    if not data:
        return None
        
    image_url = None
    video_url = None

    if data.get('media_type') == 'video':
        print('🎥 É vídeo. Pegando thumbnail.')
        image_url = data.get('thumbnail_url')
        video_url = data.get('url')
    else:
        print('📸 É imagem. \n')
        image_url = data.get('hdurl', data.get('url'))

    if not image_url:
        print('⚠️ Não foi possível obter imagem ou thumbnail.')
        return None
        
    print('Traduzindo textos...')
    translator = GoogleTranslator(source='auto', target='pt')

    title_en = data.get('title', 'Sem Título')
    explanation_en = data.get('explanation', 'Sem Descrição')

    try:
        title_pt = translator.translate(title_en)
        explanation_pt = translator.translate(explanation_en[:4500])
    except Exception as e:
        print(f'⚠️ Falha na tradução: {e}. Usando texto original.')
        title_pt = title_en
        explanation_pt = explanation_en
        
    return {
        'source': 'nasa',
        'type': 'space',
        'image_url': image_url,
        'video_url': video_url,
        'title': title_pt,
        'explanation': explanation_pt,
        'copyright_info': data.get('copyright', 'NASA Public Domain'),
        'emoji': '🌌',
        'theme_color': '#0277bd', 
        'bg_color': '#e1f5fe',
        'intro_text': 'Olhei para o espaço hoje e lembrei de você!'
    }


# --- Rodando o Código ---

if __name__ == '__main__':

    print('Inicializando o código... \n')

    # 1. Tenta Nasa
    content_data = get_nasa_data()

    # 2. Caso falhe, tenta arte
    if not content_data:
        print('⚠️ NASA indisponível. Ativando Plano B (Arte)...')
        content_data = get_art_data()

    # 3. Falha geral
    if not content_data:
        print('❌ Erro Crítico: Nenhuma fonte disponível hoje. Encerrando.')
        exit()

    # --- Gerando Mini Poema (Gemini) ---

    geminai_api_key = os.getenv('GENAI_API_KEY')
    
    # Define mensagem padrão caso Gemini falhe
    if content_data['type'] == 'space':
        mensagem_personalizada = 'O universo é infinito, mas você ainda é minha descoberta favorita!'
    else:
        mensagem_personalizada = 'O musa tão esbelta. Vitaliza minha alma'

    if geminai_api_key:
        try:
            genai.configure(api_key=geminai_api_key)
            model = genai.GenerativeModel('models/gemini-2.5-flash')

            prompt = f'''
            Aja como um poeta apaixonado pelo cosmos e pelas artes.
            Escreva um Haiku (poema de exatamente 3 versos) romântico em português, mas com estética japonesa.
            Use a seguinte explicação como inspiração:
            
            '{content_data['explanation']}'
            
            Regras:
            1. Mantenha a estrutura de 3 linhas.
            2. Seja romântico, mas conecte com o tema acima obrigatoriamente.
            3. Não inclua títulos ou explicações extras.
            '''

            response = model.generate_content(prompt)

            if response.text:
                mensagem_personalizada = response.text.strip()

        except Exception as e:
            print(f'Erro ao gerar Haiku com Gemini: {e}')
    else:
        print('Chave da API do Gemini AI não encontrada. Usando mensagem padrão.')

    # --- Template da mensagem HTML ---

    template_str = '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #fafafa; color: #555; margin: 0; padding: 20px; }
            .paper { 
                background-color: #ffffff; max-width: 600px; margin: 0 auto; padding: 40px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0, 0.1);
                border: 2px dashed {{ theme_color }};
            }
            h1 { color: {{ theme_color }}; text-align: center; font-family: 'Georgia', serif; font-style: italic; margin-bottom: 10px; }
            .date { text-align: center; color: #999; font-size: 0.9em; margin-bottom: 30px; }
            .intro { font-size: 1.1em; text-align: center; color: #444; margin-bottom: 25px; line-height: 1.6; }
            .img-box { 
                text-align: center; margin: 20px 0; padding: 15px;
                background-color: {{ bg_color }}; 
                border-radius: 8px;
            }
            img { max-width: 100%; border-radius: 4px; }
            h3 { color: {{ theme_color }}; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-top: 30px; }
            p { line-height: 1.8; }
            .footer { margin-top: 40px; font-size: 13px; color: #888; text-align: center; border-top: 1px solid #eee; padding-top: 20px; }
            .heart { color: {{ theme_color }}; }
        </style>
    </head>
    <body>
        <div class='paper'>
            <h1>{{ emoji }} Para o Meu Amor! {{ emoji }}</h1>
            <p class='date'>{{ data_hoje }}</p>

            <p class='intro'>
                Oi, {{ apelido }}! <br>
                {{ intro_text }}<br><br>
                <em>"{{ mensagem_personalizada }}"</em>
            </p>
            
            <div class='img-box'>
                {% if video_url %}
                    <a href='{{ video_url }}' target='_blank' style='text-decoration: none;'>
                    <img src='{{ image_url }}' alt='{{ title }}'>
                    <div style='margin-top: 10px; background-color: #d32f2f; color: white; display: inline-block; padding: 8px 15px; border-radius: 20px; font-size: 12px; font-weight: bold;'>
                        ▶️ Assistir Vídeo
                    </div>
                    </a>
                {% else %}
                    <img src='{{ image_url }}' alt='{{ title }}'>
                {% endif %}

                <p style='font-size: 0.9em; color: {{ theme_color }}; margin-top: 8px;'>
                    <strong>{{ title }}</strong>
                </p>
            </div>
            
            <h3>Sobre a imagem:</h3>
            <p>{{ explanation }}</p>
            
            <div class='footer'>
                Com todo amor,<br>
                <strong>Seu {{ assinatura }} <span class='heart'>❤</span></strong>
                <br><br>
                <small>Créditos: {{ copyright }}</small>
            </div>
        </div>
    </body>
    </html>
    '''

    # --- Renderizando o template com as variáveis ---

    template = Template(template_str)
    html_body = template.render(
        title = content_data['title'],
        data_hoje = date.today().strftime('%d/%m/%Y'),
        image_url = content_data['image_url'],
        video_url = content_data['video_url'],
        explanation = content_data['explanation'],
        copyright = content_data['copyright_info'],
        apelido = APELIDO, 
        mensagem_personalizada = mensagem_personalizada,
        assinatura = ASSINATURA,
        theme_color = content_data['theme_color'],
        bg_color = content_data['bg_color'],
        emoji = content_data['emoji'],
        intro_text = content_data['intro_text']
    )


    # --- Envio do email ---

    print('Preparando email...')
    msg = EmailMessage()
    msg['From'] = EMAIL_SENDER
    msg['To'] = ', '.join(EMAIL_RECEIVERS) 
    
    # CORREÇÃO 2: Aspas duplas na f-string externa
    msg['Subject'] = f"{content_data['emoji']} {APELIDO}: {content_data['title']}"

    msg.set_content(html_body, subtype='html')

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())
        print('✅ E-mail enviado com sucesso!')
    except Exception as e:
        print(f'❌ Erro ao enviar e-mail: {e}')