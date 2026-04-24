import requests
from config import BOT_TOKEN, CHAT_ID

def send(msg, image=None):
    # 🔥 Telegram limit fix (max ~4096 chars)
    if len(msg) > 4000:
        msg = msg[:4000] + "\n\n...Read more in link"

    try:
        # ✅ अगर image mila → photo send karo
        if image:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

            data = {
                "chat_id": CHAT_ID,
                "caption": msg,
                "photo": image,
                "parse_mode": "HTML"
            }

            response = requests.post(url, data=data, timeout=10)

            # ❌ अगर photo fail → text fallback
            if response.status_code != 200:
                print("⚠️ Photo failed, sending text...", response.text)
                send_text(msg)

            else:
                print("✅ Photo + Message sent")

        else:
            # ✅ normal text
            send_text(msg)

    except Exception as e:
        print("❌ Network Error:", e)


# 🔥 fallback text function
def send_text(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    response = requests.post(url, data=data, timeout=10)

    if response.status_code != 200:
        print("❌ Telegram Error:", response.text)
    else:
        print("✅ Text message sent")