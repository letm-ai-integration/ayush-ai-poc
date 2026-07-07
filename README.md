# rag-qna-bot-poc

## Overview
This project is a proof-of-concept for a Q&A bot using a combination of retrieval and generation. It uses a vector store to index and retrieve relevant documents, and a language model to generate responses.

## Project Structure

rag-qna-bot-poc/
.env
README.md
requirements.txt
src/
__init__.py
config/
__init__.py
settings.py
embeddings/
__init__.py
embedder.py
ingestion/
__init__.py
chunker.py
pdf_loader.py
llm/
__init__.py
llm_chain.py
prompts.py
main.py
pipelines/
__init__.py
rag_chain.py
retrieval/
__init__.py
retriever.py
ui/
__init__.py
ui.py
utils/
__init__.py
embedding_demo.py
token_visualizer.py
vectorstore/
__init__.py
vector_store.py
vectorstore/
index.faiss
index.pkl

## Technologies
sentence-transformers, langchain, gradio, transformers

## Running the Project
To run the project, simply execute `python main.py` in the project directory.