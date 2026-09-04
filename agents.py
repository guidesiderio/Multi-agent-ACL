import logging
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from models import openai_model
from tools import search_web


# configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# create subagents
logging.info("Initializing Subagent 1...")
subagent1 = create_agent(model=openai_model, tools=[search_web], name="Subagent 1")
logging.info("Initializing Subagent 2...")
subagent2 = create_agent(model=openai_model, tools=[search_web], name="Subagent 2")


@tool
def delegate_to_subagent1(query: str) -> str:
    """Delegate the query to Subagent 1 and return its response."""
    logging.info(f"Delegating query to Subagent 1: {query}")
    response = subagent1.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content


@tool
def delegate_to_subagent2(query: str) -> str:
    """Delegate the query to Subagent 2 and return its response."""
    logging.info(f"Delegating query to Subagent 2: {query}")
    response = subagent2.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
