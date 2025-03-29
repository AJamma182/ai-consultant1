import openai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
client = openai.OpenAI(api_key=api_key)

def get_ai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # <- this line is the key fix
        messages=[
            {"role": "system", "content": "You are a project planning assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content