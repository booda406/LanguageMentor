from langchain_ollama.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

AVAILABLE_MODELS = {
    "llama2": lambda: ChatOllama(
        model="llama3.1:8b-instruct-q8_0",
        max_tokens=8192,
        temperature=0.8,
    ),
    "gpt-4o-mini": lambda: ChatOpenAI(
        model_name="gpt-4o-mini",
        max_tokens=4096,
        temperature=0.7,
    ),
    "gpt-4o": lambda: ChatOpenAI(
        model_name="gpt-4o",
        max_tokens=4096,
        temperature=0.7,
    ),
    # 可以添加更多模型
}
