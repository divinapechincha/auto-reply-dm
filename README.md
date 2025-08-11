Divina Pechincha - Bot de Respostas Automáticas Instagram
Este projeto é um aplicativo Flask que integra o webhook do Instagram para receber comentários em Reels e responder automaticamente via Direct Message (DM) com links de afiliados armazenados em uma planilha Google Sheets.

Funcionalidades
Verificação do webhook do Instagram (GET /webhook)

Recebimento de notificações de comentários (POST /webhook)

Envio automático de mensagens via DM com link personalizado conforme comentário

Integração com Google Sheets para buscar os links afiliados

Estrutura do Projeto
graphql
Copiar
Editar
DEVELOPER/
├── app.py                   # Código principal Flask
├── requirements.txt         # Dependências Python
├── credentials.json         # Credenciais Google API (não subir no GitHub)
├── .gitignore               # Arquivos a ignorar no git
├── README.md                # Este arquivo
Requisitos
Python 3.8 ou superior

Conta Google com API Sheets habilitada e arquivo credentials.json

Token longo do Facebook para Instagram API

Configuração do webhook do Instagram com URL pública (ngrok ou servidor)

Como rodar localmente
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Coloque seu arquivo credentials.json na pasta raiz.

Defina as variáveis no app.py:

ACCESS_TOKEN

VERIFY_TOKEN

IG_USER_ID

GOOGLE_API_CREDENTIALS_FILE

Rode o app:

bash
Copiar
Editar
python app.py
Use ngrok para expor seu servidor local e configurar o webhook no Facebook Developer.

Implantação
Para implantar em serviços como Render ou Heroku, use o requirements.txt e configure o comando de start para:

bash
Copiar
Editar
gunicorn app:app
Segurança
Nunca compartilhe seu token do Facebook, nem o arquivo credentials.json publicamente.

Use .gitignore para evitar subir arquivos sensíveis no repositório.

Contato
Para dúvidas ou sugestões, contate [seu email ou contato].