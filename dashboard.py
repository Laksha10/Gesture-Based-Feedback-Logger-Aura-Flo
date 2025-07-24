import streamlit as st
import sqlite3
import pandas as pd
import time
import os

st.set_page_config(layout="wide", page_title="AuraFlo Feedback Tracker")

st.markdown("## 🧘 AuraFlo Mid-Session Feedback Tracker")

col1, col2 = st.columns([1.2, 1])

# === Left Panel: Video ===
with col1:
    st.markdown("### 🎥 Tutorial Video")
    if os.path.exists("sample_video.mp4"):
        st.video("sample_video.mp4")
    else:
        st.warning("⚠️ Tutorial video not found. Please add `'sample_video.mp4'`.")

# === Right Panel: Feedback Log ===
with col2:
    st.markdown("### 📝 Feedback Log")

    refresh = st.toggle("🔄 Auto-refresh every", value=True, key="autorefresh")
    refresh_rate = st.slider("", min_value=5, max_value=30, value=10)

    def load_feedback():
        conn = sqlite3.connect("feedback_logs.db")
        df = pd.read_sql_query("SELECT * FROM feedback ORDER BY id DESC", conn)
        conn.close()
        return df

    placeholder = st.empty()

    def display_feedback():
        df = load_feedback()
        if not df.empty:
            df['sentiment'] = df['sentiment'].apply(
                lambda x: "❗ pain-related" if x == 'pain-related' else x
            )
            styled_df = df.style.apply(
                lambda row: ['background-color: #ffcccc' if 'pain' in str(row.sentiment) else '' for _ in row],
                axis=1
            )
            placeholder.dataframe(styled_df, use_container_width=True)
        else:
            placeholder.info("No feedback logged yet.")

    # First render
    display_feedback()

    # Periodic refresh
    if refresh:
        while True:
            time.sleep(refresh_rate)
            display_feedback()
            st.rerun()

