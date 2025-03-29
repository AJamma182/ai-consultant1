import streamlit as st
from openai_client import get_ai_response
from planner import parse_response_to_plan
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")
st.title("AI Project Planner 🧠")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.plan_df = pd.DataFrame()

prompt = st.chat_input("Describe your project or business need...")
if prompt:
    st.session_state.messages.append({"role": "user", "text": prompt})
    ai_reply = get_ai_response(prompt)
    st.session_state.messages.append({"role": "ai", "text": ai_reply})
    st.session_state.plan_df = parse_response_to_plan(ai_reply)

left, right = st.columns([2, 1])

with left:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["text"])
    if not st.session_state.plan_df.empty:
        st.subheader("📊 Visual Timeline")
        fig = px.timeline(st.session_state.plan_df, x_start="Start", x_end="End", y="Phase")
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("📌 Project Summary")
    if not st.session_state.plan_df.empty:
        st.dataframe(st.session_state.plan_df)

st.sidebar.subheader("📅 Project Timeframe")

project_start = st.sidebar.date_input("Start Date")
project_end = st.sidebar.date_input("End Date")

if project_end < project_start:
    st.sidebar.error("End date must be after start date.")