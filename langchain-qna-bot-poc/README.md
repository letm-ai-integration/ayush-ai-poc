# LLM QnA Bot (LangChain + Groq + Gradio)

A simple Question & Answer chatbot built using **LangChain**, **Groq LLM**, and **Gradio UI**. This project demonstrates how prompts are processed by an LLM, how tokenization works, how text is converted into embeddings (vectors), and how model parameters like temperature and max tokens affect responses.

---

# Features

* LangChain Prompt Chaining
* Groq LLM Integration
* Gradio Chat Interface
* Token Visualization
* Embedding Visualization
* Adjustable Temperature
* Adjustable Max Tokens
* Environment Variable Configuration
* Modular Project Structure

---

# Project Structure

```text
llm-qna-bot/

├── .env
├── .gitignore
├── requirements.txt
├── README.md

├── src/
│
│   ├── config.py
│   ├── prompts.py
│   ├── llm_chain.py
│   ├── token_visualizer.py
│   ├── embedding_demo.py
│   └── ui.py
```

---

# How the Application Works

## High Level Flow

```text
User
 │
 ▼
Gradio UI
 │
 ▼
LangChain Prompt Template
 │
 ▼
ChatGroq (LLM)
 │
 ▼
Output Parser
 │
 ▼
Response
```

---

## Detailed Flow

### 1. User enters a question

Example:

```text
What is Artificial Intelligence?
```

The message is submitted through the Gradio chat interface.

---

### 2. Token Visualization

Before sending the prompt to the LLM, the text is tokenized.

Example:

```text
What
is
Artificial
Intelligence
?
```

Each token is assigned a token ID.

This helps understand how language models process text internally.

---

### 3. Embedding Generation

The question is converted into a numerical vector using a Sentence Transformer model.

Example:

```python
[0.123, -0.456, 0.789, ...]
```

Embeddings are the numerical representation of text that LLMs and vector databases work with.

The application displays:

* Embedding dimensions
* Sample vector values

---

### 4. Prompt Template

LangChain creates structured prompts using roles.

Example:

```text
System:
You are a helpful AI assistant.

User:
What is Artificial Intelligence?
```

This ensures consistent and controlled responses.

---

### 5. LangChain Chain Execution

The application uses LangChain's LCEL pipeline.

```python
prompt | llm | parser
```

Flow:

```text
PromptTemplate
      │
      ▼
ChatGroq
      │
      ▼
StrOutputParser
      │
      ▼
Final Response
```

---

### 6. Groq LLM Processing

The selected model receives:

* System Prompt
* User Question
* Temperature
* Max Tokens

The model generates a response and returns it to LangChain.

---

### 7. Response Display

The answer is displayed in:

* Chat Window
* Terminal Logs

The UI also displays:

* Model Name
* Token Count
* Token IDs
* Embedding Information

---

# Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

MODEL_NAME=llama-3.3-70b-versatile

DEFAULT_TEMPERATURE=0.7

DEFAULT_MAX_TOKENS=300
```

Example models:

```env
MODEL_NAME=llama-3.3-70b-versatile
```

```env
MODEL_NAME=llama-3.1-8b-instant
```

```env
MODEL_NAME=openai/gpt-oss-20b
```

---

# Setup Instructions

## 1. Create Virtual Environment

Windows:

```bash
python -m venv .venv
```

Linux / Mac:

```bash
python3 -m venv .venv
```

---

## 2. Activate Virtual Environment

Windows CMD:

```bash
.venv\Scripts\activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux / Mac:

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_api_key

MODEL_NAME=llama-3.3-70b-versatile
```

---

## 5. Run Application

From the project root:

```bash
python src/ui.py
```

---

## 6. Open Browser

Gradio will start locally:

```text
http://127.0.0.1:7860
```

Open the URL in your browser.

---

# Technologies Used

* Python
* LangChain
* Groq API
* Gradio
* Transformers
* Sentence Transformers
* Python Dotenv

---

# Learning Outcomes

This project demonstrates:

* LLM API Integration
* Prompt Engineering
* LangChain LCEL Pipelines
* Tokenization
* Embeddings
* Environment Variables
* Model Parameter Tuning
* Building Chat-Based AI Applications
* Modern Python Project Structure

```
```
