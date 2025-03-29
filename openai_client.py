import openai
import os
import streamlit as st
from dotenv import load_dotenv

# Load from .env (locally) or Streamlit secrets (cloud)
load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# Create OpenAI client for v1.x SDK
client = openai.OpenAI(api_key=api_key)

def get_ai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if your account supports it
        messages=[
            {"role": "system", "content": "You are a project planning assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
