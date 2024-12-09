'''
Criado por Thales "D13UX" Greco "Boss"

Instalar o flask: 
pip install flask

Solicitar o token do Telegram e colocar em TOKEN
Instalar e rodar o NGROK e alterar o WEBHOOK_URL com NGROK

Rodar o bot:
python telegram_bot_modelo.py
'''

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

#VARS e TOKENS
TOKEN = "<SEU TOKEN DO TELEGRAM AQUI>"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_URL = f"https://<SEU URL NGROK AQUI>/webhook/{TOKEN}"

#FUNCOES UTEIS
def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

#Criar endpoint do webhook
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text.lower() == "/start":
            send_message(chat_id, "Bem-Vindo! Use /produtos para ver os produtos disponiveis!")
        elif text.lower() == "/produtos":
            send_message(chat_id, "Produtos disponíveis:\n1. VIP Gold - R$50\n2. VIP Silver - R$40\n3. VIP Bronze - R$35\n\nDigite o número do produto para mais informações.")
        elif text.lower() == "1":
            send_message(chat_id, "VIP Gold - R$50\nDescrição: 50 CCs FULL.\nDigite 'comprar 1' para adquirir.")
        elif text.lower() == "2":
            send_message(chat_id, "VIP Silver - R$40\nDescrição: 25 CCs FULL.\nDigite 'comprar 2' para adquirir.")
        elif text.lower() == "3":
            send_message(chat_id, "VIP Bronze - R$35\nDescrição: 15 CCs FULL.\nDigite 'comprar 3' para adquirir.")
        elif text.lower().startswith("comprar"):
            send_message(chat_id, f"Obrigado por sua compra! Seu pedido foi registrado: {text}.")
        else:
            send_message(chat_id, "Comando Invalido!")

    return jsonify({
        "status": "ok"
    })

# Endpoint para configurar o webhook no telegram
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    response = requests.get(f"{TELEGRAM_API_URL}/setWebhook?url={WEBHOOK_URL}")
    return jsonify(response.json())

@app.route("/get_webhook", methods=["GET"])
def get_webhook():
    response = requests.get(f"{TELEGRAM_API_URL}/getWebhookInfo")
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
