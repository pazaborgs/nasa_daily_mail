# 🌌 NASA & Art Daily Email Bot (PazaBot)

[![PazaBot Daily Sender](https://github.com/pazaborgs/nasa_daily_mail/actions/workflows/nasa_daily_mail.yml/badge.svg)](https://github.com/pazaborgs/nasa_daily_mail/actions/workflows/nasa_daily_mail.yml)

Bot automatizado em Python que envia doses diárias de inspiração via e-mail. Ele prioriza o cosmos (NASA), mas possui um sistema inteligente de fallback para a arte clássica (Chicago Art Institute) caso o universo esteja "fora do ar".

## 🎯 Objetivo
Projeto desenvolvido para automatizar o envio de um "Bom dia" personalizado e carinhoso via e-mail, integrando múltiplas APIs, tratamento de erros robusto e templates HTML dinâmicos.

> *Nota: Esse projeto nasceu como um presente para minha namorada. O bot envia uma mensagem romântica contextualizada junto com a descoberta cósmica ou artística do dia.* 💙🎨

## ✨ Funcionalidades Principais
* **Dual Source Strategy:** Prioriza a **NASA (APOD)**. Se a API falhar ou cair, ativa automaticamente o **Protocolo de Arte**, buscando obras impressionistas/clássicas no **Art Institute of Chicago**.
* **Poesia via AI:** O **Google Gemini** analisa a descrição técnica da imagem (seja uma galáxia distante ou uma pintura a óleo) e compõe um Haiku romântico exclusivo para aquele dia.
* **Suporte Multimídia:** Lida com imagens em HD e detecta vídeos da NASA (extraindo thumbnails e gerando links clicáveis no e-mail).
* **Design Dinâmico:** O template HTML muda de cor e estilo automaticamente (Azul/Cosmos ou Vinho/Arte) dependendo do conteúdo.
* **Tradução Automática:** Todo conteúdo técnico (inglês) é traduzido para PT-BR antes do envio.
## 🛠 Tecnologias Utilizadas
- **Python 3.9+**
- **GitHub Actions:** Orquestração e execução diária automática (CI/CD/Cron).
- **NASA APOD API:** Obtenção de dados astronômicos (imagem e explicação).
- **Art Institute of Chicago API**: Obtenção de obras de arte e metadados.
- **Google Gemini API:** Geração de poemas (Haikus) românticos baseados no contexto da imagem.
- **Deep Translator:** Tradução dinâmica do conteúdo (EN -> PT-BR).
- **Jinja2:** Renderização de templates HTML (separação entre lógica e design).
- **SMTPLib:** Envio de e-mails autenticados via Gmail.

## 🚀 Como funciona
1. O script é acionado diariamente às 07:00 (BRT) via **GitHub Actions**.
2. Tentativa inicial usando a API da NASA: Busca a imagem ou vídeo do dia.
    * *Sucesso:* Processa a imagem/thumbnail.
    * *Falha:* Inicia o fallback.
3. Tentativa secundária: Se a NASA falhar, busca uma obra de arte aleatória (com filtro de domínio público e tentativas múltiplas para garantir uma imagem válida).
3. Traduz o título e a explicação para o português.
4. Envia a explicação para o Google Gemini, que compõe um Haiku romântico contextualizado.
4. Injeta os dados em um template HTML estilizado com **Jinja2**.
5. Envia o e-mail final via servidor SMTP do Google.

## ⚙️ Configuração
Para rodar este projeto, é necessário configurar as seguintes Variáveis de Ambiente (no `.env` local ou nos **Secrets** do GitHub):

- `NASA_API_KEY`: Sua chave de API da NASA.
- `GENAI_API_KEY`: Sua chave de API do Google AI Studio (Gemini).
- `EMAIL_PASSWORD`: Senha de App do Gmail.
- `EMAIL_SENDER`: E-mail que enviará as mensagens.
- `EMAIL_RECEIVERS`: Lista de destinatários.

## 🧪 Testes
O projeto inclui um script de teste (`tests.py`) que permite validar as integrações sem enviar e-mails reais:
- Simula respostas da NASA (incluindo vídeos).
- Testa a conexão real com a API de Arte.
- Valida o sistema de fallback.

---
Feito com 🐍, 💙 e 🎨 por [Patrick Regis](https://www.linkedin.com/in/patrickrgsanjos)