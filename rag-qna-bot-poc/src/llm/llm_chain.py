from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from config.settings import MODEL_NAME
from llm.prompts import chat_prompt

def build_chain(temperature=0.7, max_tokens=300):
    llm = ChatGroq(
        model=MODEL_NAME,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return chat_prompt | llm | StrOutputParser()
