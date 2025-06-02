
import requests
import time

bot_token = "7598877636:AAGE_92uUhdgM7ARyEYKA1iN2aCLDb1gdA8"
chat_id = "486032277"

# Целевые уровни
entry_price = 155.50
take_profit = 157.00
stop_loss = 154.50
alert_sent = {"entry": False, "tp": False, "sl": False}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def get_sol_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
    response = requests.get(url)
    return float(response.json()["price"])

while True:
    try:
        price = get_sol_price()
        print(f"Текущая цена SOL: {price}")

        if price >= entry_price and not alert_sent["entry"]:
            send_telegram_message(f"📥 <b>Цена входа достигнута:</b> ${price}")
            alert_sent["entry"] = True

        if price >= take_profit and not alert_sent["tp"]:
            send_telegram_message(f"✅ <b>Достигнут тейк-профит:</b> ${price}")
            alert_sent["tp"] = True

        if price <= stop_loss and not alert_sent["sl"]:
            send_telegram_message(f"🛑 <b>Сработал стоп-лосс:</b> ${price}")
            alert_sent["sl"] = True

        time.sleep(60)

    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(60)
