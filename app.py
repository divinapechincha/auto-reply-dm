from flask import Flask, request
import requests
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

# Configurações via variáveis de ambiente
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')          # Token de página com permissões Instagram
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')          # Token para validar webhook
IG_USER_ID = os.getenv('IG_USER_ID')              # ID da conta comercial Instagram
SPREADSHEET_ID = os.getenv('SHEET_ID')           # ID da planilha do Google Sheets
SHEET_NAME = os.getenv('SHEET_NAME') or 'Links'  # Nome da aba

# JSON das credenciais do Google como string (Render)
GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS')

def carregar_links_da_planilha():
    """Carrega os links da planilha do Google Sheets"""
    if GOOGLE_CREDENTIALS_JSON:
        creds_info = json.loads(GOOGLE_CREDENTIALS_JSON)
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
    else:
        # fallback para arquivo local
        GOOGLE_API_CREDENTIALS_FILE = 'credentials.json'
        creds = Credentials.from_service_account_file(
            GOOGLE_API_CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()
    values = result.get('values', [])

    links_por_reel = {}
    for row in values:
        if len(row) >= 2:
            media_id = row[0].strip()
            link = row[1].strip()
            links_por_reel[media_id] = link
    return links_por_reel

def enviar_dm(user_id, mensagem):
    """Envia DM para usuário via Instagram Graph API"""
    url = f"https://graph.facebook.com/v15.0/{IG_USER_ID}/messages"
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": user_id},
        "message": {"text": mensagem}
    }
    params = {"access_token": ACCESS_TOKEN}
    response = requests.post(url, json=data, params=params, headers=headers)
    print("Resposta DM:", response.json())

@app.route('/webhook', methods=['GET'])
def verify():
    """Verifica o webhook"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return 'Token inválido', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """Recebe eventos do Instagram"""
    data = request.json
    print("Recebido webhook:", json.dumps(data, indent=2))  # Debug

    links_por_reel = carregar_links_da_planilha()

    try:
        entry = data['entry'][0]
        change = entry['changes'][0]
        value = change['value']

        # Pega o user_id do comentário
        user_id = value['from']['id']

        # Pega o texto do comentário
        texto = value.get('text', '').lower()

        # Pega o media_id correto (qualquer chave que não seja 'from' ou 'text')
        media_id = next((k for k in value.keys() if k not in ['from', 'text']), None)

        if texto and "quero" in texto and media_id and media_id in links_por_reel:
            link = links_por_reel[media_id]
            mensagem = f"Aqui está o link do produto que você pediu: {link}"
            enviar_dm(user_id, mensagem)
        else:
            print("Comentário não reconhecido ou link não disponível")

    except Exception as e:
        print("Erro ao processar webhook:", e)

    return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
