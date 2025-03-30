import streamlit as st
from openai_client import get_ai_response
from planner import parse_response_to_plan
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("AI Project Planner 🧠")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.plan_df = pd.DataFrame()

# Chat prompt input
prompt = st.chat_input("📝 Describe your business project...")

if prompt:
    full_prompt = f"""You are a project planning assistant.

Ask the user for a project start date first. Once they provide it, generate a high-level project plan using a markdown table with columns: Phase | Start | End.

After the plan, inform the user: 
"You can edit the plan manually in the table, or ask me to modify any part of it for you."

Format your output as:
1. A markdown table (columns: Phase | Start | End)
2. A friendly reminder that the plan is editable or modifiable

Example:

| Phase                | Start         | End           |
|----------------------|---------------|---------------|
| Planning             | April 1, 2025 | April 10, 2025|
| Design and Research  | April 11, 2025| April 25, 2025|

You can edit the plan manually in the table, or ask me to modify any part of it for you.

Project Description: {prompt}
"""

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
        st.subheader("✏️ Edit Project Plan")
        edited_df = st.data_editor(
            st.session_state.plan_df,
            column_config={
                "Phase": "Phase Name",
                "Start": st.column_config.DateColumn("Start Date"),
                "End": st.column_config.DateColumn("End Date")
            },
            num_rows="dynamic",
            use_container_width=True
        )
        st.session_state.plan_df = edited_df

        df = edited_df.copy()
        df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
        df["End"] = pd.to_datetime(df["End"], errors="coerce")

        st.subheader("📊 Project Timeline")
        try:
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
        except Exception as e:
            st.error(f"❌ Failed to render timeline: {e}")

with summary_col:
    st.subheader("📌 Project Summary")
    if not st.session_state.plan_df.empty:
        for _, row in st.session_state.plan_df.iterrows():
            st.markdown(f"**{row['Phase']}**: {row['Start'].date()} → {row['End'].date()}")
    else:
        st.info("Start chatting to see your project summary here.")
