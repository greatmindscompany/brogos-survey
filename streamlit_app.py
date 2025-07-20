import sys
import subprocess
import textwrap
import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="BroGos Survey Dashboard", layout="wide")
st.title("🎸 BroGos Concept Survey Dashboard")

# Input: custom slogans
slogan1 = st.text_input("Concept A Slogan", placeholder="Dad-Powered ’80s Ladies Tribute Band")
slogan2 = st.text_input("Concept B Slogan", placeholder="All Male Tribute to the ’80s Ladies")

# Helper: run the survey script
def run_survey_script(concept1: str, concept2: str):
    cmd = [sys.executable, "survey_agents.py"]
    if concept1:
        cmd += ["--concept1", concept1]
    if concept2:
        cmd += ["--concept2", concept2]
    return subprocess.run(cmd, check=True, capture_output=True, text=True)

# Button to run survey
if st.button("🔄 Run fresh survey (GPT)"):
    with st.spinner("Running survey agents… this may take a few minutes ⏳"):
        try:
            run_survey_script(slogan1, slogan2)
            st.success("✅ Survey completed!")
        except subprocess.CalledProcessError as e:
            st.error("🚫 Survey script crashed. Traceback below:")
            st.code(textwrap.shorten(e.stderr or e.stdout, width=6000))

# Load and display results
if os.path.exists("survey_output.json"):
    with open("survey_output.json") as f:
        raw = json.load(f)

    rows = []
    for rec in raw:
        persona = rec.get("persona")
        ratings = rec.get("ratings", {})
        for concept, metrics in ratings.items():
            row = {"persona": persona, "concept": concept}
            row.update(metrics)
            rows.append(row)

    df = pd.DataFrame(rows)
    if df.empty or "concept" not in df.columns:
        st.warning("No survey results parsed. Check JSON structure.")
    else:
        st.subheader("Raw Persona Ratings")
        st.dataframe(df, use_container_width=True)
        metric_cols = [c for c in df.columns if c not in ["persona", "concept"]]
        metric = st.selectbox("Choose metric for bar chart:", metric_cols, index=0)
        st.subheader(f"Average **{metric}** by Concept")
        st.bar_chart(df.groupby("concept")[metric].mean())
else:
    st.info("No survey_output.json found. Click the button above to run the survey.")