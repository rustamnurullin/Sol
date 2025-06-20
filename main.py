
import requests
import time

bot_token = "7598877636:AAGE_92uUhdgM7ARyEYKA1iN2aCLDb1gdA8"
chat_id = "486032277"

entry_price = 155.50
take_profit_offset = 1.50
stop_loss_offset = 1.00

alert_sent = {"entry": False, "tp": False, "sl": False}
current_entry = entry_price

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

        take_profit = current_entry + take_profit_offset
        stop_loss = current_entry - stop_loss_offset

        if price >= current_entry and not alert_sent["entry"]:
            send_telegram_message(f"📥 <b>Цена входа достигнута:</b> ${price}")
            alert_sent["entry"] = True

        if price >= take_profit and not alert_sent["tp"]:
            send_telegram_message(f"✅ <b>Достигнут тейк-профит:</b> ${price}")
            current_entry = price
            alert_sent = {"entry": False, "tp": False, "sl": False}

        if price <= stop_loss and not alert_sent["sl"]:
            send_telegram_message(f"🛑 <b>Сработал стоп-лосс:</b> ${price}")
            current_entry = price
            alert_sent = {"entry": False, "tp": False, "sl": False}

        time.sleep(60)

    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(60)
