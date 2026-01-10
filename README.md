# 🌌 NASA Daily Email Bot (PazaBot)

[![PazaBot NASA Daily Sender](https://github.com/pazaborgs/nasa_daily_mail/actions/workflows/nasa_daily_mail.yml/badge.svg)](https://github.com/pazaborgs/nasa_daily_mail/actions/workflows/nasa_daily_mail.yml)

Bot automatizado em Python que consome a API da NASA (APOD) e envia e-mails diários com imagens do espaço e descrições traduzidas. Embora feito para astronomia, a arquitetura serve de base para qualquer bot de notificações via API.

## 🎯 Objetivo
Projeto desenvolvido para automatizar o envio de um "Bom dia" personalizado via e-mail, integrando APIs externas e templates HTML.

> *Nota: Esse projeto nasceu como um presente para minha namorada, que adora astronomia. O bot envia uma mensagem carinhosa junto com a descoberta cósmica do dia.* 💙

## 🛠 Tecnologias Utilizadas
- **Python 3.9+**
- **GitHub Actions:** Orquestração e execução diária automática (CI/CD/Cron).
- **NASA APOD API:** Obtenção de dados astronômicos (imagem e explicação).
- **Google Gemini API:** Geração de poemas (Haikus) românticos baseados no contexto da imagem.
- **Deep Translator:** Tradução dinâmica do conteúdo (EN -> PT-BR).
- **Jinja2:** Renderização de templates HTML (separação entre lógica e design).
- **SMTPLib:** Envio de e-mails autenticados via Gmail.

## 🚀 Como funciona
1. O script é acionado diariamente às 07:00 (BRT) via **GitHub Actions**.
2. O código faz uma requisição à API da NASA.
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

---
Feito com 🐍 e 💙 por [Patrick Regis](https://www.linkedin.com/in/patrickrgsanjos)