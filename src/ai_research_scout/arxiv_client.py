import requests

import xml.etree.ElementTree as ET

from datetime import datetime
from ai_research_scout.paper import ResearchPaper

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
        
        response.raise_for_status()
        
        return response
    
    def parse_papers(self, xml_text: str) -> list[ResearchPaper]:
        root = ET.fromstring(xml_text)
        namespaces = {
            "atom": "http://www.w3.org/2005/Atom"
        }
        entries = root.findall("atom:entry", namespaces)
        papers = []

        for entry in entries:
            id_element = entry.find("atom:id", namespaces)
            if id_element is None or not id_element.text:
                continue
            url_text = id_element.text.strip()
            if not url_text:
                continue
            paper_id = url_text.rsplit("/",1)[-1]
            if not paper_id:
                continue
            title_element = entry.find("atom:title", namespaces)
            if title_element is None:
                continue
            title_text = title_element.text
            if not title_text:
                continue
            title = title_text.strip()
            if not title:
                continue
            abstract_element = entry.find("atom:summary", namespaces)
            if abstract_element is None:
                abstract_text = ""
            else:
                abstract_text = abstract_element.text
            if not abstract_text:
                abstract_text = ""
            abstract = abstract_text.strip()
            author_entries = entry.findall("atom:author", namespaces)
            authors = []
            for author_entry in author_entries:
                author = author_entry.find("atom:name", namespaces).text.strip()
                authors.append(author)
            published_date_text = entry.find("atom:published", namespaces).text.strip()
            published_date = datetime.fromisoformat(published_date_text).date()
            link_elements = entry.findall("atom:link", namespaces)
            pdf_url = None
            for link_element in link_elements:
                if link_element.get("type") == "application/pdf":
                    pdf_url = link_element.get("href")
                    break
            research_paper = ResearchPaper(paper_id, title, authors, abstract, published_date, pdf_url)
            papers.append(research_paper)
        return papers
        
    