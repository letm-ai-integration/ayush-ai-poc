from vectorstore.vector_store import load_vector_store
from llm.llm_chain import build_chain


def ask_rag(
    question,
    temperature,
    max_tokens,
    k
):

    db = load_vector_store()

    if db is None:

        return (
            "No knowledge base found. Please process a PDF first.",
            []
        )

    docs = db.similarity_search(
        question,
        k=k
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    chain = build_chain(
        temperature=temperature,
        max_tokens=max_tokens
    )

    prompt = f"""
Answer ONLY from the provided context.

If answer is not present,
say:
'I could not find this information in the uploaded documents.'

Context:
{context}

Question:
{question}
"""

    result = chain.invoke(
        {
            "question": prompt
        }
    )

    answer = (
        result["answer"]
        if isinstance(result, dict)
        and "answer" in result
        else str(result)
    )

    return (
        answer,
        docs
    )