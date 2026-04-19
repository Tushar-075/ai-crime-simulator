import json
import random
import os
from functools import lru_cache
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import *

# ── LOAD ENV ─────────────────────────────
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)

MODEL = "gemini-2.5-flash"   # 


# ── SAFE CACHED CALL ─────────────────────
@lru_cache(maxsize=200)
def cached_call(prompt: str, temperature: float):
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print("Gemini Error:", e)
        return None


# ── CASE GENERATION ──────────────────────
def generate_case():
    try:
        raw = cached_call(CASE_GENERATION_PROMPT, 0.9)

        if raw:
            case = json.loads(raw)

            for s in case["suspects"]:
                s.setdefault("secret", "They are hiding something personal.")

            return case

        return _fallback_case()

    except:
        return _fallback_case()


def _fallback_case():
    suspects = [
        {"name": "Marcus Thorne", "role": "assistant", "motive": "money", "alibi": "home", "secret": "debt"},
        {"name": "Eleanor Vance", "role": "partner", "motive": "revenge", "alibi": "office", "secret": "affair"},
        {"name": "Arthur Finch", "role": "doctor", "motive": "cover up", "alibi": "clinic", "secret": "fraud"},
        {"name": "Clara Higgins", "role": "friend", "motive": "jealousy", "alibi": "party", "secret": "gambling"},
    ]

    killer = random.choice(suspects)["name"]

    clues = [
        {"description": "Fingerprint on glass", "links_to": killer},
        {"description": "Suspicious message", "links_to": killer},
        {"description": "Broken watch", "links_to": None},
        {"description": "Footprints", "links_to": None},
    ]

    return {
        "victim": {"name": "John Doe", "description": "Found dead mysteriously"},
        "setting": "Luxury apartment",
        "time_of_death": "11 PM",
        "suspects": suspects,
        "clues": clues,
        "killer": killer,
        "murder_weapon": "knife",
        "true_motive": "greed",
    }


# ── INTERROGATION ────────────────────────
def interrogate_suspect(case, name, question, history=None, pressure=False):
    suspect = next(s for s in case["suspects"] if s["name"] == name)

    # limit spam
    if history and len(history) >= 5:
        return "They repeat themselves, clearly irritated."

    system = INTERROGATION_SYSTEM.format(
        name=suspect["name"],
        role=suspect["role"],
        motive=suspect["motive"],
        alibi=suspect["alibi"],
        secret=suspect["secret"],
        is_killer=(name == case["killer"]),
        victim_name=case["victim"]["name"],
        victim_desc=case["victim"]["description"],
        setting=case["setting"],
        clues="\n".join(c["description"] for c in case["clues"]),
    )

    prompt = f"{system}\n\nDetective: {question}\n{name}:"

    result = cached_call(prompt, 0.7)

    # fallback if API fails
    if result:
        return result

    if name == case["killer"]:
        return f"{name} looks nervous. 'I already told you... I was at home.'"
    else:
        return f"{name} says calmly, 'I had nothing to do with it.'"


# ── CLUE ANALYSIS ────────────────────────
def analyze_clue(case, examined):
    for clue in case["clues"]:
        if examined.lower() in clue["description"].lower():
            if clue["links_to"]:
                return f"This clearly points toward {clue['links_to']}."
    return "Nothing significant found."


# ── SOLUTION ─────────────────────────────
def explain_solution(case, accused):
    if accused == case["killer"]:
        return f"{accused} is guilty. The clues clearly pointed to them."
    else:
        return f"Wrong. The real killer was {case['killer']}."
