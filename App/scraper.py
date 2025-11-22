from newspaper import Article
from urllib.parse import urlparse

def scrape_url(url: str) -> dict:
    try:
        article = Article(url)
        article.download()
        article.parse()

        domain = urlparse(url).netloc

        return {
            "success": True,
            "url": url,
            "domain": domain,
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "publish_date": article.publish_date,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
