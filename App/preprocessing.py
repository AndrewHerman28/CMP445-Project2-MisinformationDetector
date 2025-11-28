# preprocessing.py
import re
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are downloaded
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))

if stop_words:
    print("Stop words loaded successfully.")
else:
    print("Stop words could not be loaded.")


def clean_text(article_text):
    # Ensure text is a string
    if not isinstance(article_text, str):
        article_text = ""

    print(f"Cleaning {article_text}...")
    # Remove emoticons
    emoticons = re.findall(r"(?::|;|=)(?:-)?(?:\)|\(|D|P)", article_text)

    # Remove punctuation
    final_text = (re.sub(r"[\W]+", ' ', article_text.lower()) + ' '.join(emoticons))

    # Remove stopwords
    tokens = final_text.split()
    tokens = [w for w in tokens if w not in stop_words]
    return " ".join(tokens)


def preprocess_article(result):
    title = clean_text(result["title"])
    text = clean_text(result["text"])

    print(f"Title: {title}")
    print(f"Text: {text}")
