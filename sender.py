import requests
from config import BOT_TOKEN, CHAT_ID

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # 🔥 Telegram limit fix (max ~4096 chars)
    if len(msg) > 4000:
        msg = msg[:4000] + "\n\n...Read more in link"

    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, data=data, timeout=10)

        # 🔥 Error handling
        if response.status_code != 200:
            print("❌ Telegram API Error:", response.text)
        else:
            print("✅ Message sent successfully")

    except Exception as e:
        print("❌ Network Error:", e)