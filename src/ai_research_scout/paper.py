from datetime import date
from dataclasses import dataclass

@dataclass
class ResearchPaper:
    paper_id: str
    title: str
    authors: list[str]
    abstract: str
    published_date: date
    pdf_url: str