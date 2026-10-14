import requests

class ArxivClient:
    BASE_URL = "https://export.arxiv.org/api/query"
    
    def search_papers(self, query: str, max_results: int = 5):
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results
        }
        
        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=15
        )
        
        return response
        
    