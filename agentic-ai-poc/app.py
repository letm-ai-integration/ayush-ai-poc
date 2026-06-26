import gradio as gr

from agent import chat
from enums import AgentType

choices=[
    AgentType.HR,
    AgentType.DEVELOPER,
]

def respond(message, history, mode=AgentType.HR):
    """
    Handles a user message and returns the agent's response.
    """
    response = chat(message, mode=mode)
    return response


demo = gr.ChatInterface(
    fn=respond,
    additional_inputs=[
        gr.Dropdown(
            choices=choices,
            value=AgentType.HR,
            label="Agent"
        )
    ],
    title="🤖 Agentic AI Demo",
    description=(
        "Ask questions related to company policies or project files."
    ),
    chatbot=gr.Chatbot(height=500),
    textbox=gr.Textbox(
        placeholder="Example: How many casual leaves do employees get?",
        container=False,
        scale=7,
    )
)


if __name__ == "__main__":
    demo.launch()