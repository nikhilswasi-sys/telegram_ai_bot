import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

# 🔥 STOP WORDS (faltu links hatane ke liye)
STOP_WORDS = [
    "login", "signup", "register", "contact", "about",
    "privacy", "terms", "facebook", "twitter", "instagram",
    "youtube", "whatsapp", "telegram", "advertisement"
]

def is_valid_title(title):
    title_lower = title.lower()

    # ❌ Short title remove
    if len(title) < 20:
        return False

    # ❌ Stop words filter
    for word in STOP_WORDS:
        if word in title_lower:
            return False

    return True


def scrape(url):
    results = []
    seen = set()  # 🔥 duplicate remove

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # 🔥 Sirf article/news wale links uthao
        for a in soup.find_all("a", href=True):

            title = a.get_text(strip=True)
            link = a["href"]

            if not title or not link:
                continue

            # 🔥 filter lagao
            if not is_valid_title(title):
                continue

            # 🔗 Relative link fix
            if not link.startswith("http"):
                link = url.rstrip("/") + "/" + link.lstrip("/")

            # 🔥 duplicate remove
            if link in seen:
                continue
            seen.add(link)

            results.append((title, link))

    except Exception as e:
        print("Scrape error:", e)

    return results