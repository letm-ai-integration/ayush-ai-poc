from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader
)


def load_pdf(pdf_path):

    pdf_path = Path(pdf_path)

    loader = PyPDFLoader(
        str(pdf_path)
    )

    documents = loader.load()

    for doc in documents:

        doc.metadata["source_file"] = (
            pdf_path.name
        )

    return documents