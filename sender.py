import requests
from config import BOT_TOKEN, CHAT_ID


def send(msg, image=None):
    # 🔥 Telegram limit fix
    if len(msg) > 4000:
        msg = msg[:4000] + "\n\n...Read more in link"

    try:
        if image:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

            data = {
                "chat_id": CHAT_ID,
                "caption": msg,
                "photo": image,
                "parse_mode": "HTML"
            }

            response = requests.post(url, data=data, timeout=10)

            print("📡 Photo Response:", response.status_code, response.text)

            if response.status_code != 200:
                print("⚠️ Photo failed → fallback to text")
                send_text(msg)
            else:
                print("✅ Photo + Message sent")

        else:
            send_text(msg)

    except Exception as e:
        print("❌ Network Error (send):", e)


def send_text(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, data=data, timeout=10)

        print("📡 Text Response:", response.status_code, response.text)

        if response.status_code != 200:
            print("❌ Telegram Error:", response.text)
        else:
            print("✅ Text message sent")

    except Exception as e:
        print("❌ Network Error (text):", e)