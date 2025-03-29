import streamlit as st
from openai_client import get_ai_response
from planner import parse_response_to_plan
import plotly.express as px
import pandas as pd
from datetime import date, timedelta

st.set_page_config(layout="wide")
st.title("AI Project Planner 🧠")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.plan_df = pd.DataFrame()

# Date input section in sidebar
st.sidebar.subheader("📅 Project Timeframe")
project_start = st.sidebar.date_input("Start Date", date.today())
project_end = st.sidebar.date_input("End Date", date.today() + timedelta(days=30))

if project_end < project_start:
    st.sidebar.error("End date must be after start date.")
else:
    # Chat prompt input
    prompt = st.chat_input("📝 Describe your business project...")

    if prompt:
        full_prompt = f"""Project Goal: {prompt}
Start Date: {project_start}
End Date: {project_end}

Please generate a project plan broken down into logical phases. For each phase, provide a name, start date, and end date, all within this range."""
        st.session_state.messages.append({"role": "user", "text": prompt})
        ai_reply = get_ai_response(full_prompt)
        st.session_state.messages.append({"role": "ai", "text": ai_reply})
        st.session_state.plan_df = parse_response_to_plan(ai_reply)

# Layout
chat_col, summary_col = st.columns([2.5, 1])

with chat_col:
    for msg in st.session_state.messages:
        role = msg.get("role", "user")
        text = msg.get("text", "")
        with st.chat_message(role):
            st.markdown(text)

    if not st.session_state.plan_df.empty:
        st.subheader("📊 Project Timeline (from AI)")
        df = st.session_state.plan_df
        fig = px.timeline(
            df,
            x_start="Start",
            x_end="End",
            y="Phase",
            color="Phase",
            hover_name="Phase"
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

with summary_col:
    st.subheader("📌 Project Summary")
    if not st.session_state.plan_df.empty:
        st.markdown(f"**Project Phases:** {len(st.session_state.plan_df)}")
        st.dataframe(st.session_state.plan_df)
    else:
        st.info("Start chatting to see your project summary here.")
