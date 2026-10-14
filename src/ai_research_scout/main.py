from ai_research_scout.arxiv_client import ArxivClient

client = ArxivClient()
results = client.search_papers("all:retrieval")
print(results.text)
