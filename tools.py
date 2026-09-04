import logging
from functools import lru_cache

from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

# configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()


@lru_cache(maxsize=1)
def get_tavily_client() -> TavilyClient:
    """Return the shared Tavily client, creating it on first use."""
    return TavilyClient()


@tool
def search_web(topic: str) -> str:
    """Search the web for a given topic and return the results."""
    logging.info(f"Searching the web for topic: {topic}")
    response = get_tavily_client().search(topic, max_results=5, include_answer=True)

    blocks = []
    if response.get("answer"):
        blocks.append(f"Resumo: {response['answer']}")
    for item in response.get("results", []):
        blocks.append(f"{item['title']}\n{item['url']}\n{item['content']}")

    return "\n\n".join(blocks) or "Nenhum resultado encontrado."
