import json, os, subprocess, streamlit as st, pandas as pd

st.set_page_config(page_title="BroGos Survey Dashboard", layout="wide")

st.title("🎸 BroGos Concept Survey Dashboard")

# Button to run survey script
import subprocess, textwrap, streamlit as st

st.title("🎸 BroGos Concept Survey Dashboard")

if st.button("Run fresh survey (GPT)"):
    with st.spinner("Running survey agents…"):
        try:
            subprocess.run(
                [sys.executable, "survey_agents.py"],   # ← use current venv's Python
                check=True,
                capture_output=True,
                text=True
            )
            st.success("✅ Survey completed!")
        except subprocess.CalledProcessError as e:
            st.error("🚫 Survey failed. Traceback below:")
            st.code(textwrap.shorten(e.stderr or e.stdout, width=6000))


# Load results
if os.path.exists("survey_output.json"):
    with open("survey_output.json") as f:
        raw = json.load(f)
    df = pd.json_normalize(raw)

    st.subheader("Raw Persona Results")
    st.dataframe(df, use_container_width=True)

    # Select metric to visualize
    metric_cols = [c for c in df.columns if c not in ("persona", "concept", "comment")]
    metric = st.selectbox("Choose metric for bar chart:", metric_cols, index=0)

    st.subheader(f"Average {metric} by Concept")
    st.bar_chart(df.groupby("concept")[metric].mean())
else:
    st.info("No survey_output.json found. Click the button above to run the survey.")
