import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class NewsRetriever:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
        self.headers = {"User-Agent": "NewsSummarizer/1.0"}
        self.last_request = None

    def fetch_articles(self, query, language="en", page_size=5):
        try:
            if self.last_request and (datetime.now() - self.last_request).seconds < 1:
                time.sleep(1)  # Rate limiting
            
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            params = {
                "q": query,
                "language": language,
                "pageSize": page_size,
                "apiKey": self.api_key,
                "from": from_date,
                "sortBy": "publishedAt"
            }
            
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            self.last_request = datetime.now()
            articles = response.json().get("articles", [])
            
            return [{
                "title": a.get("title", "No title"),
                "content": a.get("content", ""),
                "url": a.get("url", "#"),
                "publishedAt": a.get("publishedAt", ""),
                "source": a.get("source", {}).get("name", "Unknown")
            } for a in articles if a.get("content")]
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {str(e)}")
            return []