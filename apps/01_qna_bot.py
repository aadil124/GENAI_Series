# from dotenv import load_dotenv
# # from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq
# import streamlit as st

# load_dotenv()

# # llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")
# llm = ChatGroq(model = "qwen/qwen3-32b")

# st.title("🤖 Ask Buddy - AI QnA Bot")
# st.markdown("My QnA Bot With LangChain and Google Gemini! 🔥🔥🔥 ")

# if "messages" not in st.session_state:
#     st.session_state.messages =[]

# for message in st.session_state.messages:
#     role=message["role"]
#     content=message["content"]
#     st.chat_message(role).markdown(content)


# query=st.chat_input("Ask me anything...")
# if query:
#     st.session_state.messages.append({"role":"user","content":query})
#     st.chat_message("user").markdown(query)
#     res=llm.invoke(query)
#     st.chat_message("ai").markdown(res.content)
#     st.session_state.messages.append({"role":"ai","content":res.content})


# ================================
# 🔹 IMPORTS
# ================================
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import streamlit as st
import re

# ================================
# 🔹 LOAD ENV VARIABLES
# ================================
load_dotenv()

# ================================
# 🔹 INITIALIZE LLM (Groq - Qwen)
# ================================
# llm = ChatGroq(model="qwen/qwen3-32b")
llm = ChatGroq(model="llama-3.3-70b-versatile")

# ================================
# 🔹 STREAMLIT UI
# ================================
st.title("🤖 Ask Buddy - AI QnA Bot")
st.markdown("LangChain + Groq (Qwen 32B) 🚀")

# ================================
# 🔹 SESSION STATE (CHAT MEMORY)
# ================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================================
# 🔹 DISPLAY CHAT HISTORY
# ================================
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

# ================================
# 🔹 CLEAN RESPONSE FUNCTION (REMOVE <think>)
# ================================
def clean_response(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# ================================
# 🔹 USER INPUT
# ================================
query = st.chat_input("Ask me anything...")

if query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)

    # ================================
    # 🔹 BUILD CHAT HISTORY FOR LLM
    # ================================
    chat_history = [
        SystemMessage(
            content="You are a helpful AI assistant. Do NOT include reasoning or <think> tags. Only give final answer."
        )
    ]

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_history.append(HumanMessage(content=msg["content"]))
        else:
            chat_history.append(AIMessage(content=msg["content"]))

    # ================================
    # 🔹 LLM CALL WITH ERROR HANDLING
    # ================================
    try:
        res = llm.invoke(chat_history)
        answer = clean_response(res.content)  # 🔥 CLEAN OUTPUT HERE
    except Exception as e:
        answer = f"⚠️ Error: {str(e)}"

    # ================================
    # 🔹 DISPLAY AI RESPONSE
    # ================================
    st.chat_message("ai").markdown(answer)

    # Save AI response
    st.session_state.messages.append({"role": "ai", "content": answer})
