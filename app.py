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

# Chat input
prompt = st.chat_input("📝 Describe your business project...")

if prompt:
    full_prompt = f"""
You are a project planning assistant.

Return the project plan in exactly this format:
```
Phase: Discovery, Start: April 1, 2025, End: April 10, 2025
Phase: Build, Start: April 11, 2025, End: May 20, 2025
```

⚠️ Do not include any commentary, intro, or explanation. Just output the list in the format above.

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
        st.subheader("📊 Project Timeline")
        st.write("🧾 GPT Response:")
        st.text(ai_reply)

        st.write("🧪 Parsed Plan DataFrame:")
        st.dataframe(st.session_state.plan_df)

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
    st.subheader("📌 GPT-Generated Project Phases")
    if not st.session_state.plan_df.empty:
        for _, row in st.session_state.plan_df.iterrows():
            st.markdown(f"**{row['Phase']}**: {row['Start'].date()} → {row['End'].date()}")
    else:
        st.info("Start chatting to see your project summary here.")
