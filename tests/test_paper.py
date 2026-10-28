"""Smoke tests for the existing ResearchPaper dataclass."""

from datetime import date

from ai_research_scout.paper import ResearchPaper


def test_research_paper_stores_all_six_fields():
    paper = ResearchPaper(
        paper_id="2610.05750v1",
        title="Beyond Semantic Similarity",
        authors=["First Author", "Second Author"],
        abstract="An evaluation of retrieval approaches.",
        published_date=date(2026, 10, 5),
        pdf_url="https://arxiv.org/pdf/2610.05750v1",
    )

    assert paper.paper_id == "2610.05750v1"
    assert paper.title == "Beyond Semantic Similarity"
    assert paper.authors == ["First Author", "Second Author"]
    assert paper.abstract == "An evaluation of retrieval approaches."
    assert paper.published_date == date(2026, 10, 5)
    assert paper.pdf_url == "https://arxiv.org/pdf/2610.05750v1"
