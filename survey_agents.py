import os
import json
from typing import List, Dict

# ──────────────────────────────────────────────────────────────
# Securely load OpenAI key (Streamlit Cloud or local)
# ──────────────────────────────────────────────────────────────
try:
    import streamlit as st  # Present when running inside Streamlit Cloud
    openai_key = st.secrets.get("OPENAI_API_KEY")
except ModuleNotFoundError:
    openai_key = None

if not openai_key:
    openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    raise RuntimeError(
        "OPENAI_API_KEY not found. Set it in Streamlit Secrets or as an env var."
    )

# We are pinned to openai==0.28.1 in requirements.txt
import openai
openai.api_key = openai_key

# ──────────────────────
# Persona profiles
# ──────────────────────
personas: List[Dict] = [
    # (same long persona list you provided) …
    #  ────────────────────────────────────
    {"name": "Sarah", "age": 48, "profile": "Working mom who grew up on MTV, loves nostalgic 80s pop and light humor."},
    {"name": "Linda", "age": 52, "profile": "Empty-nester, big on 80’s fashion and concert experiences."},
    {"name": "Tina", "age": 45, "profile": "Single professional, nostalgic but busy, prefers straightforward fun."},
    {"name": "Karen", "age": 50, "profile": "Suburban mom juggling soccer practice and 80s karaoke nights."},
    {"name": "Michelle", "age": 49, "profile": "Career-driven, loves retro dance moves and MP3 nostalgia."},
    {"name": "Julie", "age": 47, "profile": "Creative graphic designer, avid 80s movie buff and synthwave fan."},
    {"name": "Denise", "age": 51, "profile": "Community volunteer, attended numerous 80s concerts in college."},
    {"name": "Cynthia", "age": 46, "profile": "Tech consultant, collects vintage 80s vinyl records."},
    {"name": "Lisa", "age": 53, "profile": "High-school teacher, organizes 80s-themed fundraisers."},
    {"name": "Patricia", "age": 52, "profile": "Real-estate agent, playlists filled with 80s pop divas."},
    {"name": "Donna", "age": 54, "profile": "Health coach, loves aerobics-era 80s workout tracks."},
    {"name": "Barbara", "age": 55, "profile": "Retired librarian, hosts 80s trivia nights at the local bar."},
    {"name": "Susan", "age": 45, "profile": "Graphic novelist, draws inspiration from 80s aesthetics."},
    {"name": "Angela", "age": 44, "profile": "Entrepreneur, mixes 80s tunes into her daily workout."},
    {"name": "Rebecca", "age": 49, "profile": "Event planner, specializes in throwback 80s parties."},
    {"name": "Amanda", "age": 43, "profile": "Marketing manager, DJ for 80s nights on the weekends."},
    {"name": "Jennifer", "age": 48, "profile": "Photographer, nostalgic about 80s fashion shoots."},
    {"name": "Melissa", "age": 50, "profile": "Yoga instructor, fond of 80s synth-pop during classes."},
    {"name": "Stephanie", "age": 42, "profile": "Software engineer, grew up coding to 80s soundtracks."},
    {"name": "Kimberly", "age": 46, "profile": "Financial analyst, weekend vinyl DJ for 80s funk."},
    {"name": "Deborah", "age": 44, "profile": "Podcast host, runs a show on 80s culture and music."},
    {"name": "Christine", "age": 47, "profile": "Non-profit coordinator, organizes 80s charity dances."},
    {"name": "Heather", "age": 51, "profile": "Fitness trainer, choreographs 80s-themed workout routines."},
    {"name": "Rachel", "age": 45, "profile": "Film critic, writes about 80s cinema and soundtracks."},
    {"name": "Monica", "age": 54, "profile": "Travel blogger, captures 80s retro hotspots around the world."},
    # Younger nostalgia fans
    {"name": "Alex", "age": 22, "profile": "College student, discovered 80s music through TikTok retro challenges."},
    {"name": "Jordan", "age": 28, "profile": "Junior graphic designer, loves VHS aesthetics and synthwave."},
    {"name": "Taylor", "age": 31, "profile": "Bartender by night, streams 80s playlists for shift vibes."},
    {"name": "Morgan", "age": 36, "profile": "Fitness influencer, uses 80s workout tracks in online classes."},
    {"name": "Casey", "age": 24, "profile": "Barista, hosts 80s trivia nights at local coffee shop."},
    {"name": "Riley", "age": 27, "profile": "Startup marketer, remixes 80s hits for social campaigns."},
    {"name": "Avery", "age": 34, "profile": "Graphic novelist, inspired by retro 80s comic art."},
    {"name": "Bailey", "age": 29, "profile": "UX researcher, listens to 80s soundtracks while prototyping."},
    {"name": "Cameron", "age": 37, "profile": "Software dev, codes to 80s synth-pop beats."},
    {"name": "Drew", "age": 26, "profile": "Social-media coordinator, curates 80s nostalgia posts."},
    {"name": "Kai", "age": 33, "profile": "Photographer, uses retro 80s filters in photo edits."},
    {"name": "Sydney", "age": 30, "profile": "Graphic designer, runs an 80s-inspired merch store."},
    {"name": "Devin", "age": 35, "profile": "Barista and part-time DJ, spins 80s classics on weekends."},
]

# ──────────────────────
# 20-metric survey questions
# ──────────────────────
metric_keys = [
    "fun", "authenticity", "attendance",
    "novelty", "memorability", "emotional", "clarity",
    "recommend", "has_penis", "shareability", "media_feature",
    "podcast_interest", "persona_likeability", "merch_purchase",
    "sponsor_appeal", "catchphrase", "brand_recall",
    "market_viability", "brand_extension", "ad_click_through"
]

concepts = {
    "dad_powered": "Dad-Powered ’80s Ladies Tribute Band",
    "all_male": "All Male Tribute to the ’80s Ladies"
}

# ──────────────────────
# GPT call for one persona
# ──────────────────────
def run_survey_for_persona(persona: Dict) -> Dict:
    # Build schema block dynamically
    schema_lines = "\n".join([f"  - {k}: integer 1-5" for k in metric_keys])

    system_prompt = (
        f"You are {persona['name']}, age {persona['age']}. "
        f"{persona['profile']}\n"
        "Respond in JSON with keys for each concept "
        '("dad_powered", "all_male"), each containing:\n'
        f"{schema_lines}\n"
        "  - comment: 1-2 sentence justification."
    )

    # Build user prompt with each metric question
    user_prompt = "Please rate the following two band concepts:\n"
    for desc in concepts.values():
        user_prompt += f"\n[{desc}]\n"
        for key in metric_keys:
            q_text = key.replace('_', ' ')
            user_prompt += f"On a scale of 1–5, how would you rate {q_text}?\n"
    user_prompt += "\nRespond only with valid JSON."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # keep consistent with requirements.txt pin
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0  # deterministic for clean JSON
    )

    return json.loads(response.choices[0].message["content"].strip())

# ──────────────────────
# Run full survey
# ──────────────────────
def run_full_survey(personas: List[Dict]) -> List[Dict]:
    results = []
    for p in personas:
        try:
            ratings = run_survey_for_persona(p)
            results.append({"persona": p["name"], "ratings": ratings})
        except Exception as e:
            results.append({"persona": p["name"], "error": str(e)})
    return results

# ──────────────────────
# CLI entry-point
# ──────────────────────
if __name__ == "__main__":
    all_results = run_full_survey(personas)
    with open("survey_output.json", "w") as fp:
        json.dump(all_results, fp, indent=2)
    print(f"✅ survey_output.json written with {len(all_results)} persona entries.")
