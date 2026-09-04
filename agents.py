import logging
from functools import lru_cache

from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from models import get_openai_model
from tools import get_tavily_client, search_web


# configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@lru_cache(maxsize=1)
def get_subagent1():
    """Return Subagent 1, creating it on first delegation."""
    logging.info("Initializing Subagent 1...")
    return create_agent(model=get_openai_model(), tools=[search_web], name="Subagent 1")


@lru_cache(maxsize=1)
def get_subagent2():
    """Return Subagent 2, creating it on first delegation."""
    logging.info("Initializing Subagent 2...")
    return create_agent(model=get_openai_model(), tools=[search_web], name="Subagent 2")


def reset_agent_clients() -> None:
    """Drop every cached client so the next call picks up new API keys."""
    logging.info("Resetting cached agent clients...")
    get_subagent1.cache_clear()
    get_subagent2.cache_clear()
    get_openai_model.cache_clear()
    get_tavily_client.cache_clear()


@tool
def delegate_to_subagent1(query: str) -> str:
    """Delegate the query to Subagent 1 and return its response."""
    logging.info(f"Delegating query to Subagent 1: {query}")
    response = get_subagent1().invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content


@tool
def delegate_to_subagent2(query: str) -> str:
    """Delegate the query to Subagent 2 and return its response."""
    logging.info(f"Delegating query to Subagent 2: {query}")
    response = get_subagent2().invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
