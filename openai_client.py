import openai
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
client = openai.OpenAI(api_key=api_key)

def get_ai_response(prompt):
    messages = st.session_state.messages.copy()
    messages.append({"role": "user", "text": prompt})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": msg["role"], "content": msg["text"]} for msg in messages]
    )

    return response.choices[0].message.content
