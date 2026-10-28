"""Tests for the HTTP and Atom XML parsing methods in ArxivClient.

These tests do not access the internet. They exercise the implementation as it
currently exists, without imposing a policy for missing paper metadata yet.
"""

from datetime import date
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET

import pytest
from requests import Response
from requests.exceptions import ConnectionError, HTTPError, Timeout

from ai_research_scout.arxiv_client import ArxivClient
from ai_research_scout.paper import ResearchPaper


SAMPLE_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>https://arxiv.org/abs/2610.05750v1</id>
    <title>  Beyond Semantic Similarity  </title>
    <summary>  An evaluation of retrieval approaches.  </summary>
    <published>2026-10-05T14:20:00Z</published>
    <author><name>First Author</name></author>
    <author><name>Second Author</name></author>
    <link href="https://arxiv.org/abs/2610.05750v1" type="text/html" rel="alternate" />
    <link href="https://arxiv.org/pdf/2610.05750v1" type="application/pdf" rel="related" />
    <link href="https://example.org/doi/123" type="text/html" rel="related" />
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2504.05181v2</id>
    <title>Another Retrieval Study</title>
    <summary>Comparing methods for retrieving papers.</summary>
    <published>2025-04-07T15:27:37Z</published>
    <author><name>Third Author</name></author>
    <link href="https://arxiv.org/pdf/2504.05181v2" type="application/pdf" rel="related" />
  </entry>
</feed>
"""


def test_parse_papers_creates_dataclass_objects_with_metadata():
    papers = ArxivClient().parse_papers(SAMPLE_XML)

    assert len(papers) == 2
    assert all(isinstance(paper, ResearchPaper) for paper in papers)

    first = papers[0]
    assert first.paper_id == "2610.05750v1"
    assert first.title == "Beyond Semantic Similarity"
    assert first.authors == ["First Author", "Second Author"]
    assert first.abstract == "An evaluation of retrieval approaches."
    assert first.published_date == date(2026, 10, 5)
    assert first.pdf_url == "https://arxiv.org/pdf/2610.05750v1"

    second = papers[1]
    assert second.paper_id == "2504.05181v2"
    assert second.authors == ["Third Author"]
    assert second.published_date == date(2025, 4, 7)
    assert second.pdf_url == "https://arxiv.org/pdf/2504.05181v2"


def test_parse_papers_returns_empty_list_for_empty_feed():
    empty_xml = '<feed xmlns="http://www.w3.org/2005/Atom"></feed>'

    assert ArxivClient().parse_papers(empty_xml) == []


def test_parse_papers_rejects_malformed_xml():
    with pytest.raises(ET.ParseError):
        ArxivClient().parse_papers("<feed><entry></feed>")


def test_search_papers_passes_parameters_checks_status_and_returns_response():
    response = Mock(spec=Response)

    with patch("ai_research_scout.arxiv_client.requests.get", return_value=response) as mock_get:
        actual = ArxivClient().search_papers("all:retrieval", max_results=3)

    mock_get.assert_called_once_with(
        ArxivClient.BASE_URL,
        params={"search_query": "all:retrieval", "start": 0, "max_results": 3},
        timeout=15,
    )
    response.raise_for_status.assert_called_once_with()
    assert actual is response


@pytest.mark.parametrize("status_code", [404, 429, 500])
def test_search_papers_propagates_http_errors(status_code):
    response = Response()
    response.status_code = status_code
    response.url = "https://export.arxiv.org/api/query"

    with patch("ai_research_scout.arxiv_client.requests.get", return_value=response):
        with pytest.raises(HTTPError) as caught:
            ArxivClient().search_papers("all:retrieval")

    assert caught.value.response is response


@pytest.mark.parametrize("failure", [ConnectionError("Network unavailable"), Timeout("Request timed out")])
def test_search_papers_propagates_connection_and_timeout_errors(failure):
    with patch("ai_research_scout.arxiv_client.requests.get", side_effect=failure):
        with pytest.raises(type(failure)):
            ArxivClient().search_papers("all:retrieval")
