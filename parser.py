import re

def _clean(text):
    return re.sub(r"[^a-zA-Z0-9\s']", " ", text).lower().strip()

def _find_suspect(text, case):
    text = text.lower()

    for s in case["suspects"]:
        name = s["name"].lower()
        first = name.split()[0]

        if name in text or first in text:
            return s["name"]

    return None


def parse_command(user_input, case=None, active_suspect=None):
    text = _clean(user_input)

    # ── SIMPLE COMMANDS ──
    if text in ["help"]:
        return {"action": "help"}

    if text in ["leave", "exit", "back"]:
        return {"action": "leave"}

    # ── ACCUSE ──
    if "accuse" in text:
        target = _find_suspect(text, case)
        return {"action": "accuse", "target": target}

    # ── INSPECT ──
    if any(word in text for word in ["inspect", "check", "look"]):
        return {"action": "inspect", "target": text}

    # ── INTERROGATE ──
    if any(word in text for word in ["interrogate", "talk", "ask"]):
        target = _find_suspect(text, case)

        return {
            "action": "interrogate",
            "target": target,
            "question": user_input,
            "pressure": False,
        }

    # ── DEFAULT BEHAVIOR ──
    if active_suspect:
        return {
            "action": "interrogate",
            "target": active_suspect,
            "question": user_input,
            "pressure": False,
        }

    return {"action": "unknown"}