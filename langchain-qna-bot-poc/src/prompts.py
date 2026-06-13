from langchain_core.prompts import ChatPromptTemplate
chat_prompt=ChatPromptTemplate.from_messages([('system','You are a helpful AI assistant.'),('user','{question}')])
