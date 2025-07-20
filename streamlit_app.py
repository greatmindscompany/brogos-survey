`KeyError: 'concept'` means the DataFrame you built has **no `concept` column** (your JSON rows look like
`{"persona": "...", "ratings": {"dad_powered": {...}, "all_male": {...}}}`).

Below is a **drop-in replacement** for **your entire `streamlit_app.py`** that:

* Imports `sys` (fixes the previous `NameError`).
* Launches `survey_agents.py` with the correct interpreter.
* Flattens the nested JSON into rows with a real **`concept`** column, so `df.groupby("concept")` works.
* Shows errors in the UI if the subprocess crashes.

```python
import sys
import subprocess
import textwrap
import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="BroGos Survey Dashboard", layout="wide")
st.title("🎸 BroGos Concept Survey Dashboard")

# ──────────────────────────
# Helper: run the survey script
# ──────────────────────────
def run_survey_script():
    """
    Launch survey_agents.py with the SAME python interpreter
    the Streamlit app is using (so all packages are available).
    """
    return subprocess.run(
        [sys.executable, "survey_agents.py"],
        check=True,
        capture_output=True,
        text=True
    )

# ──────────────────────────
# UI: button to run survey
# ──────────────────────────
if st.button("🔄 Run fresh survey (GPT)"):
    with st.spinner("Running survey agents… this may take a few minutes ⏳"):
        try:
            result = run_survey_script()
            st.success("✅ Survey completed!")
            # Optionally show stdout for debugging
            # st.code(result.stdout)
        except subprocess.CalledProcessError as e:
            st.error("🚫 Survey script crashed. Traceback below:")
            st.code(textwrap.shorten(e.stderr or e.stdout, width=6000))

# ──────────────────────────
# Load survey_output.json if present
# ──────────────────────────
if os.path.exists("survey_output.json"):
    with open("survey_output.json") as f:
        raw = json.load(f)

    # Flatten nested structure into rows with a 'concept' col
    rows = []
    metrics_keys = [
        "fun", "authenticity", "attendance", "novelty", "memorability",
        "emotional", "clarity", "recommend", "value", "shareability",
        "media_feature", "podcast_interest", "persona_likeability",
        "merch_purchase", "sponsor_appeal", "catchphrase", "brand_recall",
        "market_viability", "brand_extension", "ad_click_through"
    ]

    for rec in raw:
        persona = rec.get("persona")
        ratings_block = rec.get("ratings", {})  # might be missing if error
        for concept, ratings in ratings_block.items():
            row = {"persona": persona, "concept": concept}
            for key in metrics_keys:
                row[key] = ratings.get(key)
            rows.append(row)

    df = pd.DataFrame(rows)
    if df.empty:
        st.warning("survey_output.json loaded, but no rows were parsed. Check JSON structure.")
    else:
        # Show raw data
        st.subheader("Raw Persona Ratings")
        st.dataframe(df, use_container_width=True)

        # Let user pick metric
        metric = st.selectbox("Choose metric for bar chart:", metrics_keys, index=0)
        st.subheader(f"Average **{metric}** by Concept")
        st.bar_chart(df.groupby("concept")[metric].mean())
else:
    st.info("No survey_output.json found. Click the button above to run the survey.")