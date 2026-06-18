import os
import shutil

from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

VECTOR_DB_PATH = "vectorstore"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def build_vector_store(
    chunks,
    append=True
):
    """
    Creates or updates FAISS vector database.

    append=True
        Existing vectors are loaded and
        new chunks are added.

    append=False
        Creates a brand-new database.
    """

    # -----------------------------------
    # Existing DB Found
    # -----------------------------------

    if (
        append
        and os.path.exists(VECTOR_DB_PATH)
    ):

        print(
            "\nLoading existing vector database..."
        )

        db = FAISS.load_local(
            VECTOR_DB_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )

        print(
            f"Adding {len(chunks)} new chunks..."
        )

        db.add_documents(
            chunks
        )

    # -----------------------------------
    # Create New DB
    # -----------------------------------

    else:

        print(
            "\nCreating new vector database..."
        )

        db = FAISS.from_documents(
            chunks,
            embedding_model
        )

    db.save_local(
        VECTOR_DB_PATH
    )

    print(
        "Vector database saved."
    )

    return db


def load_vector_store():
    """
    Loads existing vector database.
    """

    if not os.path.exists(
        VECTOR_DB_PATH
    ):
        return None

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )


def clear_vector_store():
    """
    Deletes the vector database.
    """

    if os.path.exists(
        VECTOR_DB_PATH
    ):

        shutil.rmtree(
            VECTOR_DB_PATH
        )

        return (
            "Knowledge Base Cleared Successfully ✅"
        )

    return (
        "No Knowledge Base Found"
    )


def vector_store_exists():

    return os.path.exists(
        VECTOR_DB_PATH
    )


def get_vector_db_stats():
    """
    Returns vector DB statistics.
    """

    if not vector_store_exists():

        return {
            "status": "Not Created"
        }

    db = load_vector_store()

    total_chunks = len(
        db.index_to_docstore_id
    )

    return {
        "status": "Ready",
        "total_chunks": total_chunks,
        "embedding_model":
        "all-MiniLM-L6-v2"
    }