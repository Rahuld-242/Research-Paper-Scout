from ai_research_scout.arxiv_client import ArxivClient
from requests.exceptions import (
    HTTPError,
    ConnectionError,
    Timeout,
    RequestException
)

from xml.etree.ElementTree import ParseError

try: 
    client = ArxivClient()
    
    results = client.search_papers("all:retrieval")
    papers = client.parse_papers(results.text)
    if papers:
        print(f"Total papers: {len(papers)}")
        print(papers[0])
    else:
        print("No research papers found")
    
except HTTPError as e:
    print(f"HTTP error: {e}")

except Timeout as e:
    print(f"Request timed out: {e}")

except ConnectionError as e:
    print(f"Connection failed: {e}")

except RequestException as e:
    print(f"Unexpected request error: {e}")
    
except ParseError as e:
    print(f"XML parsing failed: {e}")