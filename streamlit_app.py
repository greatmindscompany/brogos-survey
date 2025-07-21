import sys
import subprocess
import textwrap
import json
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="BroGos Concept Survey Dashboard", layout="wide")
st.title("🎸 BroGos Concept Survey Dashboard")

# ──────────────────────────
# User inputs for custom slogans
# ──────────────────────────
DEFAULT1 = "Dad-Powered ’80s Ladies Tribute Band"
DEFAULT2 = "All Male Tribute to the ’80s Ladies"

slogan1 = st.text_input("Phrase for 'dad_powered' concept:", value=DEFAULT1)
slogan2 = st.text_input("Phrase for 'all_male' concept:", value=DEFAULT2)

custom_input_detected = slogan1.strip() != DEFAULT1 or slogan2.strip() != DEFAULT2
concept_labels = {
    "custom1": slogan1.strip(),
    "custom2": slogan2.strip()
} if custom_input_detected else {
    "dad_powered": DEFAULT1,
    "all_male": DEFAULT2
}

# ──────────────────────────
# Helper: run the survey script with env overrides
# ──────────────────────────
def run_survey_script(s1: str, s2: str):
    env = os.environ.copy()
    if custom_input_detected:
        env["PHRASE_CUSTOM1"] = s1
        env["PHRASE_CUSTOM2"] = s2
    else:
        env["PHRASE_DAD_POWERED"] = s1
        env["PHRASE_ALL_MALE"] = s2
    return subprocess.run(
        [sys.executable, "survey_agents.py"],
        check=True,
        capture_output=True,
        text=True,
        env=env
    )

# ──────────────────────────
# UI: button to run survey
# ──────────────────────────
if st.button("🔄 Run fresh survey (GPT)"):
    with st.spinner("Running survey agents… this may take a few minutes ⏳"):
        try:
            result = run_survey_script(slogan1, slogan2)
            st.success("✅ Survey completed!")
        except subprocess.CalledProcessError as e:
            st.error("🚫 Survey script crashed. Traceback below:")
            st.code(textwrap.shorten(e.stderr or e.stdout, width=6000))

# ──────────────────────────
# Load survey_output.json if present
# ──────────────────────────
if os.path.exists("survey_output.json"):
    with open("survey_output.json") as f:
        raw = json.load(f)

    rows = []
    metrics_keys = [
        "fun", "authenticity", "attendance", "novelty", "memorability",
        "emotional", "clarity", "recommend", "has_penis", "shareability",
        "media_feature", "podcast_interest", "persona_likeability",
        "merch_purchase", "sponsor_appeal", "catchphrase", "brand_recall",
        "market_viability", "guitar_shredding", "ad_click_through"
    ]

    for rec in raw:
        persona = rec.get("persona")
        ratings_block = rec.get("ratings", {})
        concept_order = rec.get("concept_order")
        if not concept_order:
            st.warning(f"⚠️ Warning: concept_order missing for persona {persona}. Fallback order used.")
            concept_order = list(concept_labels.keys())
        for concept_key in concept_order:
            ratings = ratings_block.get(concept_key, {})
            label = concept_labels.get(concept_key, concept_key)
            row = {"persona": persona, "concept": label}
                for key in metrics_keys:
                    row[key] = ratings.get(key)
                rows.append(row)

    df = pd.DataFrame(rows)
    if df.empty:
        st.warning("survey_output.json loaded, but no rows were parsed. Check JSON structure.")
    else:
        st.subheader("Raw Persona Ratings")
        st.dataframe(df, use_container_width=True)

        metric = st.selectbox("Choose metric for bar chart:", metrics_keys, index=0)
        st.subheader(f"Average **{metric}** by Concept")

        grouped = df.groupby("concept")[metric].mean()

        fig, ax = plt.subplots()
        grouped.plot(kind='bar', ax=ax)
        ax.set_ylabel(f"Average {metric}")
        ax.set_xlabel("Concept")
        ax.set_xticklabels(grouped.index, rotation=0)  # <-- horizontal labels
        st.pyplot(fig)
else:
    st.info("No survey_output.json found. Click the button above to run the survey.")
