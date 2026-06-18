import gradio as gr

from config.settings import MODEL_NAME
from ingestion.pdf_loader import load_pdf
from ingestion.chunker import create_chunks
from vectorstore.vector_store import (
    build_vector_store,
    clear_vector_store
)
from pipelines.rag_chain import ask_rag
from utils.token_visualizer import visualize_tokens
from utils.embedding_demo import get_embedding_info

def process_pdf(
    pdf_file,
    use_existing_db
):

    if not pdf_file:

        return "Please upload a PDF."

    logs = []

    logs.append(
        f"Loading PDF: {pdf_file.name}"
    )

    documents = load_pdf(
        pdf_file.name
    )

    logs.append(
        f"Pages Loaded: {len(documents)}"
    )

    chunks = create_chunks(
        documents
    )

    logs.append(
        f"Chunks Created: {len(chunks)}"
    )

    build_vector_store(
        chunks,
        append=use_existing_db
    )

    logs.append(
        "Vector Database Updated Successfully ✅"
    )

    return "\n".join(logs)

def clear_vector_db():

    return "Vector Database Cleared ✅"


# =====================================================
# CHAT FUNCTION
# =====================================================

def respond(
    message,
    history,
    model_name,
    temperature,
    max_tokens,
    top_k
):

    history = history or []

    print("\n" + "=" * 80)
    print("MODEL")
    print("=" * 80)
    print(model_name)

    print("\n" + "=" * 80)
    print("USER QUESTION")
    print("=" * 80)
    print(message)

    # ------------------------------------
    # TOKEN VISUALIZATION
    # ------------------------------------

    token_info = visualize_tokens(
        message
    )

    print("\nTOKEN INFO")
    print(token_info)

    # ------------------------------------
    # EMBEDDING VISUALIZATION
    # ------------------------------------

    embedding_info = get_embedding_info(
        message
    )

    print("\nEMBEDDING INFO")
    print(embedding_info)

    # ------------------------------------
    # RAG QUERY
    # ------------------------------------

    response, docs = ask_rag(
        question=message,
        temperature=temperature,
        max_tokens=max_tokens,
        k=top_k
    )

    print("\nRAG RESPONSE")
    print(response)

    # ------------------------------------
    # CHAT HISTORY
    # ------------------------------------

    history.append(
        {
            "role": "user",
            "content": message
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # ------------------------------------
    # RETRIEVED SOURCES
    # ------------------------------------

    retrieved_sources = []

    for doc in docs:

        retrieved_sources.append(
            {
                "source_file":
                    doc.metadata.get(
                        "source_file",
                        "Unknown"
                    ),

                "page":
                    doc.metadata.get(
                        "page",
                        "Unknown"
                    ),

                "content":
                    doc.page_content[:500]
            }
        )

    # ------------------------------------
    # STATS
    # ------------------------------------

    stats = {
        "Model": model_name,
        "Temperature": temperature,
        "Top K": top_k,
        "Max Tokens": max_tokens,
        "Input Token Count": token_info["count"],
        "Embedding Dimensions": embedding_info["dimensions"],
        "Retrieved Chunks": len(docs)
    }

    return (
        "",
        history,
        token_info,
        embedding_info,
        stats,
        retrieved_sources
    )

# =====================================================
# UI
# =====================================================

with gr.Blocks(
    title="LangChain RAG Bot"
) as demo:

    gr.Markdown(
        """
        # 🤖 LangChain RAG Bot

        Groq + LangChain + Tokens + Embeddings + RAG
        """
    )

    # =================================================
    # SETTINGS
    # =================================================

    with gr.Row():

        model_name = gr.Textbox(
            value=MODEL_NAME,
            label="Model",
            interactive=False
        )

        temperature = gr.Slider(
            0,
            1,
            value=0.7,
            step=0.1,
            label="Temperature"
        )

        max_tokens = gr.Slider(
            50,
            2000,
            value=300,
            step=50,
            label="Max Tokens"
        )
        top_k = gr.Slider(
            minimum=1,
            maximum=10,
            value=3,
            step=1,
            label="Top K Chunks"
        )

    # =================================================
    # KNOWLEDGE BASE SECTION
    # =================================================

    with gr.Accordion(
        "📚 Knowledge Base",
        open=True
    ):

        pdf_file = gr.File(
            label="Upload PDF",
            file_types=[".pdf"]
        )

        use_existing_db = gr.Checkbox(
            value=True,
            label="Use Existing Knowledge Base"
        )

        with gr.Row():

            process_btn = gr.Button(
                "📚 Process PDF"
            )

            clear_btn = gr.Button(
                "🗑️ Clear Vector DB"
            )

        rag_logs = gr.Textbox(
            label="RAG Pipeline Logs",
            lines=10
        )

    # =================================================
    # CHATBOT
    # =================================================

    chatbot = gr.Chatbot(
        height=500,
        label="Conversation"
    )

    msg = gr.Textbox(
        label="Question",
        placeholder="Ask anything..."
    )

    send_btn = gr.Button(
        "Send",
        variant="primary"
    )

    # =================================================
    # RETRIEVED SOURCES
    # =================================================

    with gr.Accordion(
        "📄 Retrieved Sources",
        open=False
    ):
        source_output = gr.JSON()

    # =================================================
    # STATS
    # =================================================

    with gr.Accordion(
        "📊 Request Statistics",
        open=False
    ):
        stats_output = gr.JSON()

    # =================================================
    # TOKENS
    # =================================================

    with gr.Accordion(
        "🔤 Token Visualization",
        open=False
    ):
        token_output = gr.JSON()

    # =================================================
    # EMBEDDINGS
    # =================================================

    with gr.Accordion(
        "🧠 Embedding Visualization",
        open=False
    ):
        embedding_output = gr.JSON()

    # =================================================
    # PROCESS PDF
    # =================================================

    process_btn.click(
        process_pdf,
        inputs=[
            pdf_file,
            use_existing_db
        ],
        outputs=[
            rag_logs
        ]
    )

    # =================================================
    # CLEAR DB
    # =================================================

    clear_btn.click(
        clear_vector_db,
        outputs=[
            rag_logs
        ]
    )

    # =================================================
    # SEND MESSAGE
    # =================================================

    send_btn.click(
        respond,
        inputs=[
            msg,
            chatbot,
            model_name,
            temperature,
            max_tokens,
            top_k
        ],
        outputs=[
            msg,
            chatbot,
            token_output,
            embedding_output,
            stats_output,
            source_output
        ]
    )

    msg.submit(
        respond,
        inputs=[
            msg,
            chatbot,
            model_name,
            temperature,
            max_tokens,
            top_k
        ],
        outputs=[
            msg,
            chatbot,
            token_output,
            embedding_output,
            stats_output,
            source_output
        ]
    )


if __name__ == "__main__":

    demo.launch(
        server_name="127.0.0.1",
        server_port=7860
    )