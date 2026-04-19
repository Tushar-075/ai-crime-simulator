import json
import random
import os
import time
from functools import lru_cache
from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv
from prompts import *

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL = "models/gemini-2.5-flash"  
@lru_cache(maxsize=200)
def cached_call(prompt: str, temperature: float):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config={"temperature": temperature},
        )
        return response.text.strip()

    except ClientError as e:
        if "429" in str(e):
            return " The suspect pauses, clearly overwhelmed... try again shortly."
        return " AI error occurred."


# ── CASE GENERATION ──────────────────────────────────

def generate_case():
    try:
        raw = cached_call(CASE_GENERATION_PROMPT, 0.9)
        case = json.loads(raw)

        for s in case["suspects"]:
            s.setdefault("secret", "They are hiding something personal.")

        return case

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


# ── INTERROGATION ───────────────────────────────────

def interrogate_suspect(case, name, question, history=None, pressure=False):
    suspect = next(s for s in case["suspects"] if s["name"] == name)

    # limit spam calls
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

    prompt = f"Detective: {question}\n{name}:"

    return cached_call(system + "\n\n" + prompt, 0.7)


# ── CLUE ANALYSIS (NO API) ───────────────────────────

def analyze_clue(case, examined):
    for clue in case["clues"]:
        if examined.lower() in clue["description"].lower():
            if clue["links_to"]:
                return f"This clearly points toward {clue['links_to']}."
    return "Nothing significant found."


# ── SOLUTION ────────────────────────────────────────

def explain_solution(case, accused):
    if accused == case["killer"]:
        return f"{accused} is guilty. The clues clearly pointed to them."
    else:
        return f"Wrong. The real killer was {case['killer']}."