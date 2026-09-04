from functools import lru_cache

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


@lru_cache(maxsize=1)
def get_openai_model():
    """Return the shared chat model, creating it on first use."""
    return init_chat_model("gpt-5-nano")
