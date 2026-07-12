from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()


@dataclass(frozen=True)
class Settings:
    groq_api_key: str
    model_name: str
    langsmith_api_key: str
    langchain_project: str
    tracing_enabled: bool
    openweathermap_api_key: str


settings = Settings(
    os.getenv("GROQ_API_KEY", ""),
    os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
    os.getenv("LANGSMITH_API_KEY", ""),
    os.getenv("LANGCHAIN_PROJECT", "langgraph-poc"),
    os.getenv("LANGCHAIN_TRACING_V2", "true").lower() == "true",
    os.getenv("OPENWEATHERMAP_API_KEY", ""),
)
