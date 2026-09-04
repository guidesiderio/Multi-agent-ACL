import logging

from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

# configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()
tavily_client = TavilyClient()


@tool
def search_web(topic: str) -> str:
    """Search the web for a given topic and return the results."""
    logging.info(f"Searching the web for topic: {topic}")
    return tavily_client.search_web(topic)
