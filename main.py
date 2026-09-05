import logging
from prompts import WEDDING_PLANNER_AGENT_PROMPT, USER_PROMPT_FOR_MAIN_AGENT
from models import get_openai_model
from agents import delegate_to_subagent1, delegate_to_subagent2
from langchain.messages import HumanMessage
from langchain.agents import create_agent

# configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# asking user for their requeriments for their wedding
logging.info("Asking user for their wedding requirements...")
user_requirements = input("Please provide your requirements for your wedding: ")

# updating the system prompt
update_system_prompt = WEDDING_PLANNER_AGENT_PROMPT.format(requirements=user_requirements)

# creating the main agent
logging.info("Creating the main agent...")
main_wedding_planner_agent = create_agent(
    model=get_openai_model(),
    tools=[delegate_to_subagent1, delegate_to_subagent2],
    name="Wedding_Planner",
    system_prompt=update_system_prompt,
)

# invoking the main agent with the user prompt
logging.info("Invoking the main agent with the user prompt...")
response_main_agent = main_wedding_planner_agent.invoke(
    {"messages": [HumanMessage(content=USER_PROMPT_FOR_MAIN_AGENT)]}
)

# printing the final response from the main agent
logging.info("Final response from the main agent:")
print(response_main_agent["messages"][-1].content)
