import time
from datetime import datetime, timedelta
from config import WEBSITES
from scraper import scrape
from database import generate_id, is_sent, save
from sender import send
from utils import detect_category

# 🔥 KEYWORDS FILTER
KEYWORDS = {
    "high": ["vacancy", "result", "admit card", "apply", "exam date", "official", "notification"],
    "medium": ["update", "news", "announcement"]
}

def is_important(title):
    title_lower = title.lower()

    for word in KEYWORDS["high"]:
        if word in title_lower:
            return True

    for word in KEYWORDS["medium"]:
        if word in title_lower:
            return True

    return False


# 🔥 SIMPLE SUMMARY (FREE METHOD)
def make_summary(title):
    words = title.split()
    short = " ".join(words[:12])  # first 10-12 words
    return f"• {short}..."


def format_msg(title, link, site, category):
    summary = make_summary(title)

    return f"""
🔥 <b>Latest Important Update</b>

📰 <b>{title}</b>

📌 Summary:
{summary}

📂 Category: <b>{category}</b>
🌐 Source: {site}
🔗 <a href="{link}">Open Link</a>

━━━━━━━━━━━━━━━
🤖 Ultra Pro Bot
"""


def run():
    print("Checking...")

    for site in WEBSITES:
        data = scrape(site["url"])

        for title, link in data[:20]:

            # ❌ Skip if not important
            if not is_important(title):
                continue

            post_id = generate_id(title, link)

            # ❌ Skip duplicate
            if is_sent(post_id):
                continue

            category = detect_category(title)

            msg = format_msg(title, link, site["name"], category)

            try:
                send(msg)
                save(post_id)
                print("Sent:", title[:50])

            except Exception as e:
                print("Send error:", e)

    print("Done\n")


while True:
    try:
        run()
        time.sleep(300)  # 5 min

    except Exception as e:
        print("Crash prevented:", e)
        time.sleep(60)