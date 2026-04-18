from config import KEYWORDS

def detect_category(title):
    title = title.lower()

    for category, words in KEYWORDS.items():
        if any(w in title for w in words):
            return category

    return "UPDATE"