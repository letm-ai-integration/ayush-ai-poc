import gradio as gr

from config import MODEL_NAME

from llm_chain import build_chain
from token_visualizer import visualize_tokens
from embedding_demo import get_embedding_info


def respond(
    message,
    history,
    model_name,
    temperature,
    max_tokens
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

    # --------------------
    # TOKENS
    # --------------------

    token_info = visualize_tokens(message)

    print("\nTOKEN VISUALIZATION")
    print("=" * 80)
    print(token_info)

    # --------------------
    # EMBEDDINGS
    # --------------------

    embedding_info = get_embedding_info(message)

    print("\nEMBEDDING INFO")
    print("=" * 80)
    print(embedding_info)

    # --------------------
    # LLM
    # --------------------

    chain = build_chain(
        temperature=temperature,
        max_tokens=max_tokens
    )

    result = chain.invoke(
        {
            "question": message
        }
    )

    response = (
        result["answer"]
        if isinstance(result, dict)
        and "answer" in result
        else str(result)
    )

    print("\nLLM RESPONSE")
    print("=" * 80)
    print(response)

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

    stats = {
        "Model": model_name,
        "Temperature": temperature,
        "Max Tokens": max_tokens,
        "Input Token Count": token_info["count"],
        "Embedding Dimensions": embedding_info["dimensions"]
    }

    return (
        "",
        history,
        token_info,
        embedding_info,
        stats
    )


with gr.Blocks(
    title="LangChain QnA Bot"
) as demo:

    gr.Markdown(
        """
        # 🤖 LangChain QnA Bot

        LangChain + Groq + Token Visualization + Embeddings
        """
    )

    # ====================================
    # SETTINGS SECTION
    # ====================================

    with gr.Row():

        model_name = gr.Textbox(
            value=MODEL_NAME,
            label="Model",
            interactive=False
        )

        temperature = gr.Slider(
            minimum=0,
            maximum=1,
            value=0.7,
            step=0.1,
            label="Temperature"
        )

        max_tokens = gr.Slider(
            minimum=50,
            maximum=2000,
            value=300,
            step=50,
            label="Max Tokens"
        )

    # ====================================
    # CHAT
    # ====================================

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

    # ====================================
    # MODEL / TOKEN STATS
    # ====================================

    with gr.Accordion(
        "📊 Request Statistics",
        open=False
    ):
        stats_output = gr.JSON()

    # ====================================
    # TOKENS
    # ====================================

    with gr.Accordion(
        "🔤 Token Visualization",
        open=False
    ):
        token_output = gr.JSON()

    # ====================================
    # EMBEDDINGS
    # ====================================

    with gr.Accordion(
        "🧠 Embedding Visualization",
        open=False
    ):
        embedding_output = gr.JSON()

    send_btn.click(
        respond,
        inputs=[
            msg,
            chatbot,
            model_name,
            temperature,
            max_tokens
        ],
        outputs=[
            msg,
            chatbot,
            token_output,
            embedding_output,
            stats_output
        ]
    )

    msg.submit(
        respond,
        inputs=[
            msg,
            chatbot,
            model_name,
            temperature,
            max_tokens
        ],
        outputs=[
            msg,
            chatbot,
            token_output,
            embedding_output,
            stats_output
        ]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860
    )