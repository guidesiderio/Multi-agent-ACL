from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

openai_chat_model = init_chat_model("gpt-5-nano")
