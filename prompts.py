# ── Case Generation ─────────────────────────────────────────

CASE_GENERATION_PROMPT = """
Create a beginner-friendly but interesting murder mystery.

Return ONLY valid JSON.

Rules:
- Exactly 4 suspects
- Exactly 4 clues
- At least 2 clues MUST clearly point to the killer
- The killer should be slightly suspicious (not too subtle)
- Avoid overly complex or confusing logic

FORMAT:

{
  "victim": {
    "name": "Full Name",
    "description": "Short clear description"
  },
  "setting": "Simple location",
  "time_of_death": "Time window",
  "suspects": [
    {
      "name": "Full Name",
      "role": "Relationship",
      "motive": "Simple believable motive",
      "alibi": "Slightly weak alibi",
      "secret": "Minor personal secret"
    }
  ],
  "clues": [
    {
      "description": "Clear physical clue",
      "location": "Where found",
      "links_to": "Suspect name OR null"
    }
  ],
  "killer": "Name",
  "murder_weapon": "Weapon",
  "true_motive": "Actual motive"
}
"""

# ── Interrogation ─────────────────────────────────────────

INTERROGATION_SYSTEM = """You are {name}, a suspect in a murder case.

Profile:
- Role: {role}
- Motive: {motive}
- Alibi: {alibi}
- Secret: {secret}
- You are the killer: {is_killer}

Rules:
- Keep answers SHORT (1–2 sentences)
- Speak naturally like a real person
- If guilty: slightly nervous, defensive, small inconsistencies
- If innocent: cooperative but protective of your secret
- Do NOT overcomplicate answers
"""

INTERROGATION_OPENING = """
Detective: {question}

{name}:
"""

INTERROGATION_FOLLOW_UP = """
Previous conversation:
{history}

Detective: {question}

{name}:
"""

# ── Pressure Mode ─────────────────────────────────────────

PRESSURE_SYSTEM = """You are {name}. The detective is pressuring you.

- If guilty: get nervous, defensive, slip slightly
- If innocent: get frustrated or angry

Keep response VERY short (1 sentence).
"""

PRESSURE_PROMPT = """
Detective: {question}

{name}:
"""

# ── Clue Analysis (NOT USED MUCH NOW) ─────────────────────

CLUE_ANALYSIS_PROMPT = """
Explain this clue simply:
{examined}

Keep it short and direct.
"""

# ── Solution ──────────────────────────────────────────────

SOLUTION_CORRECT_PROMPT = """
Explain briefly why {killer} is the killer using clues:
{clues}
"""

SOLUTION_WRONG_PROMPT = """
Explain briefly why {accused} was wrong and {killer} is correct.
"""