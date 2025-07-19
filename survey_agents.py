import os
import openai
from typing import List, Dict

# Ensure your OpenAI API key is set in environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define your persona profiles
personas = [
    {
        "name": "Sarah",
        "age": 48,
        "profile": "Working mom who grew up on MTV, loves nostalgic 80s pop and light humor."
    },
    {
        "name": "Linda",
        "age": 52,
        "profile": "Empty-nester, big on 80’s fashion and concert experiences."
    },
    {
        "name": "Tina",
        "age": 45,
        "profile": "Single professional, nostalgic but busy, prefers straightforward fun."
    },
    {
        "name": "Karen",
        "age": 50,
        "profile": "Suburban mom juggling soccer practice and 80s karaoke nights."
    },
    {
        "name": "Michelle",
        "age": 49,
        "profile": "Career-driven, loves retro dance moves and MP3 nostalgia."
    },
    {
        "name": "Julie",
        "age": 47,
        "profile": "Creative graphic designer, avid 80s movie buff and synthwave fan."
    },
    {
        "name": "Denise",
        "age": 51,
        "profile": "Community volunteer, attended numerous 80s concerts in college."
    },
    {
        "name": "Cynthia",
        "age": 46,
        "profile": "Tech consultant, collects vintage 80s vinyl records."
    },
    {
        "name": "Lisa",
        "age": 53,
        "profile": "High school teacher, organizes 80s-themed fundraisers."
    },
    {
        "name": "Patricia",
        "age": 52,
        "profile": "Real estate agent, playlists filled with 80s pop divas."
    },
    {
        "name": "Donna",
        "age": 54,
        "profile": "Health coach, loves aerobics-era 80s workout tracks."
    },
    {
        "name": "Barbara",
        "age": 55,
        "profile": "Retired librarian, hosts 80s trivia nights at the local bar."
    },
    {
        "name": "Susan",
        "age": 45,
        "profile": "Graphic novelist, draws inspiration from 80s aesthetics."
    },
    {
        "name": "Angela",
        "age": 44,
        "profile": "Entrepreneur, mixes 80s tunes into her daily workout."
    },
    {
        "name": "Rebecca",
        "age": 49,
        "profile": "Event planner, specializes in throwback 80s parties."
    },
    {
        "name": "Amanda",
        "age": 43,
        "profile": "Marketing manager, DJ for 80s nights on the weekends."
    },
    {
        "name": "Jennifer",
        "age": 48,
        "profile": "Photographer, nostalgic about 80s fashion shoots."
    },
    {
        "name": "Melissa",
        "age": 50,
        "profile": "Yoga instructor, fond of 80s synth-pop during classes."
    },
    {
        "name": "Stephanie",
        "age": 42,
        "profile": "Software engineer, grew up coding to 80s soundtracks."
    },
    {
        "name": "Kimberly",
        "age": 46,
        "profile": "Financial analyst, weekend vinyl DJ for 80s funk."
    },
    {
        "name": "Deborah",
        "age": 44,
        "profile": "Podcast host, runs a show on 80s culture and music."
    },
    {
        "name": "Christine",
        "age": 47,
        "profile": "Non-profit coordinator, organizes 80s charity dances."
    },
    {
        "name": "Heather",
        "age": 51,
        "profile": "Fitness trainer, choreographs 80s-themed workout routines."
    },
    {
        "name": "Rachel",
        "age": 45,
        "profile": "Film critic, writes about 80s cinema and soundtracks."
    },
    {
        "name": "Monica",
        "age": 54,
        "profile": "Travel blogger, captures 80s retro hotspots around the world."
    },
    # Younger personas (ages 18-40) ~35% of total to reflect US distribution
    {
        "name": "Alex",
        "age": 22,
        "profile": "College student, discovered 80s music through TikTok retro challenges."
    },
    {
        "name": "Jordan",
        "age": 28,
        "profile": "Junior graphic designer, loves VHS aesthetics and synthwave."
    },
    {
        "name": "Taylor",
        "age": 31,
        "profile": "Bartender by night, streams 80s playlists for shift vibes."
    },
    {
        "name": "Morgan",
        "age": 36,
        "profile": "Fitness influencer, uses 80s workout tracks in online classes."
    },
    {
        "name": "Casey",
        "age": 24,
        "profile": "Barista, hosts 80s trivia nights at local coffee shop."
    },
    {
        "name": "Riley",
        "age": 27,
        "profile": "Startup marketer, remixes 80s hits for social campaigns."
    },
    {
        "name": "Avery",
        "age": 34,
        "profile": "Graphic novelist, inspired by retro 80s comic art."
    },
    {
        "name": "Bailey",
        "age": 29,
        "profile": "UX researcher, listens to 80s soundtracks while prototyping."
    },
    {
        "name": "Cameron",
        "age": 37,
        "profile": "Software dev, codes to 80s synth-pop beats."
    },
    {
        "name": "Drew",
        "age": 26,
        "profile": "Social media coordinator, curates 80s nostalgia posts."
    },
    {
        "name": "Kai",
        "age": 33,
        "profile": "Photographer, uses retro 80s filters in photo edits."
    },
    {
        "name": "Sydney",
        "age": 30,
        "profile": "Graphic designer, runs an 80s-inspired merch store."
    },
    {
        "name": "Devin",
        "age": 35,
        "profile": "Barista and part-time DJ, spins 80s classics on weekends."
    }
]

# Define the survey questions and concepts
survey_questions = [
    {"key": "fun",                   "question": "On a scale of 1–5, how fun does this concept feel?"},
    {"key": "authenticity",          "question": "On a scale of 1–5, how authentic does this feel?"},
    {"key": "attendance",            "question": "On a scale of 1–5, how likely are you to attend a show?"},
    {"key": "novelty",               "question": "On a scale of 1–5, how fresh or unique does this concept seem?"},
    {"key": "memorability",          "question": "On a scale of 1–5, how memorable is the band’s branding?"},
    {"key": "emotional",             "question": "On a scale of 1–5, how emotionally engaging is this concept?"},
    {"key": "clarity",               "question": "On a scale of 1–5, how clear is the concept’s message at first glance?"},
    {"key": "recommend",             "question": "On a scale of 1–5, how likely would you be to recommend this band to a friend?"},
    {"key": "value",                 "question": "On a scale of 1–5, how good of a value do you think tickets would be?"},
    {"key": "shareability",          "question": "On a scale of 1–5, how likely would you be to share a video or post about this concept on social media?"},
    {"key": "media_feature",         "question": "On a scale of 1–5, how likely is this concept to be featured on a talk show or morning news segment?"},
    {"key": "podcast_interest",      "question": "On a scale of 1–5, how interested would you be in hearing a podcast or interview series about this band?"},
    {"key": "persona_likeability",   "question": "On a scale of 1–5, how likable and relatable do you find the band’s personalities?"},
    {"key": "merch_purchase",        "question": "On a scale of 1–5, how likely would you be to buy the band’s merchandise (shirts, mugs, etc.)?"},
    {"key": "sponsor_appeal",        "question": "On a scale of 1–5, how appealing is this concept for brand sponsorships or partnerships?"},
    {"key": "catchphrase",           "question": "On a scale of 1–5, how catchy is the band’s slogan or tagline?"},
    {"key": "brand_recall",          "question": "On a scale of 1–5, how well would you recall the band’s name and concept after seeing its promotion?"},
    {"key": "market_viability",      "question": "On a scale of 1–5, how likely do you think this concept would achieve sustained commercial success over the next year?"},
    {"key": "brand_extension",       "question": "On a scale of 1–5, how likely is this concept to support spin-offs (web series, live streams, etc.)?"},
    {"key": "ad_click_through",      "question": "On a scale of 1–5, how likely are you to click on an online ad promoting this band?"}
]

concepts = {
    "dad_powered": "Dad-Powered ’80s Ladies Tribute Band",
    "all_male": "All Male Tribute to the ’80s Ladies"
}

def run_survey_for_persona(persona: Dict) -> Dict:
    '''
    Runs the mini-survey for both concepts for a single persona.
    Returns structured ratings and comments.
    '''
    system_prompt = f"""
You are {persona['name']}, age {persona['age']}. {persona['profile']}
Respond in JSON with keys for each concept ("dad_powered", "all_male"), each containing:
  - fun: integer 1-5
  - authenticity: integer 1-5
  - attendance: integer 1-5
  - comment: 1-2 sentence justification.
"""
    user_prompt = "Please rate the following two band concepts:\n"
    for key, desc in concepts.items():
        user_prompt += f"\n[{desc}]\n"
        for q in survey_questions:
            user_prompt += f"{q['question']}\n"
    user_prompt += "\nRespond only with valid JSON."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message["content"]

def run_full_survey(personas: List[Dict]) -> List[Dict]:
    results = []
    for p in personas:
        result = run_survey_for_persona(p)
        results.append({"persona": p["name"], "result": result})
    return results

if __name__ == "__main__":
    import json
    survey_results = run_full_survey(personas)
    print(json.dumps(survey_results, indent=2))
