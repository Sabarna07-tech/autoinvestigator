# server/tools/news_scanner.py

from duckduckgo_search import DDGS
from shared.config import REGION,SAFE_SEARCH, TIME_LIMIT, MAX_RESULTS
from server.tools.web_search import WebSearchTool

from .web_search import WebSearchTool

class NewsScannerTool:
    """
    A tool to scan for news articles related to lawsuits, fraud, or other risks.
    """
    def __init__(self):
        self.web_search = WebSearchTool()

    def run(self, company_name: str):
        """
        Runs a risk-focused news search for a given company.
        
        Args:
            company_name (str): The name of the company to search for.
            
        Returns:
            list: A list of search result strings, or an empty list if an error occurs.
        """
        query = f'{company_name} lawsuit fraud OR scandal OR investigation OR controversy'
        print(f"[NewsScannerTool] Searching risk-related news for {company_name}")
        try:
            # The WebSearchTool's run method now returns the results directly
            results = self.web_search.run(query)
            return results
        except Exception as e:
            # Catch the API quota error (and any other errors) gracefully
            print(f"[NewsScannerTool] An error occurred: {e}")
            print("[NewsScannerTool] This may be due to the Google Search API daily quota being exceeded.")
            # Return an empty list to prevent the calling agent from crashing
            return []
