rag-qna-bot/
│
├── src/
│   │
│   ├── config/
│   │   └── settings.py              ← config.py
│   │
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   └── chunker.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── vectorstore/
│   │   └── vector_store.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── llm/
│   │   ├── llm_chain.py
│   │   └── prompts.py
│   │
│   ├── pipelines/
│   │   └── rag_chain.py
│   │
│   ├── ui/
│   │   └── ui.py
│   │
│   ├── evaluation/
│   │   └── (future: ragas.py, evaluator.py)
│   │
│   ├── utils/
│   │   └── token_visualizer.py
│   │
│   ├── main.py
│   │
│   └── __init__.py
│
├── scripts/
│   └── embedding_demo.py
│
├── data/
│   └── (store PDFs here)
│
├── vectorstore/
│   └── (Chroma/FAISS persisted database)
│
├── tests/
│
├── notebooks/
│
├── requirements.txt
├── .env
└── README.md