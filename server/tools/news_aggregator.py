# server/tools/news_aggregator.py

import os
import requests

class NewsAggregatorTool:
    def __init__(self):
        self.api_key = os.getenv("SERP_KEY")
        if not self.api_key:
            raise EnvironmentError("SERP_KEY is not set")

    def run(self, company_name: str) -> str:
        print(f"[NewsAggregatorTool] Fetching news for: {company_name}")
        params = {
            "q": f"{company_name} latest news",
            "api_key": self.api_key,
            "engine": "google",
            "tbm": "nws",  
            "num": 5
        }

        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json()

        news_items = []
        for article in results.get("news_results", []):
            title = article.get("title")
            snippet = article.get("snippet")
            link = article.get("link")
            date = article.get("date")
            if snippet:
                news_items.append(f"{title} ({date})\n{snippet}\n[Link]({link})")

        return "\n\n".join(news_items) if news_items else "No recent news found."
