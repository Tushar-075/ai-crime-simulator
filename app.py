import streamlit as st
from game_engine import generate_case, interrogate_suspect, analyze_clue, explain_solution
from parser import parse_command

st.set_page_config(page_title="AI Crime Simulator", layout="wide")

# ── INIT ─────────────────────────────────────────────

def init():
    if "case" not in st.session_state:
        st.session_state.case = generate_case()

    defaults = {
        "history": [],
        "score": 100,
        "suspect_history": {},
        "interrogated": [],
        "active_suspect": None,
        "game_over": False,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()
case = st.session_state.case

# ── LOG ─────────────────────────────────────────────

def log(user, bot, t="default"):
    st.session_state.history.append({"user": user, "bot": bot, "type": t})


# ── SIDEBAR ─────────────────────────────────────────

with st.sidebar:
    st.header("🗂 Case")

    st.write(f"**Victim:** {case['victim']['name']}")
    st.write(case["victim"]["description"])

    st.divider()

    st.subheader("📍 Scene")
    st.write(case["setting"])
    st.write(case["time_of_death"])

    st.divider()

    st.subheader("🔍 Clues")
    for clue in case["clues"]:
        st.write(f"- {clue['description']}")

    st.divider()

    st.subheader("💯 Score")
    st.write(st.session_state.score)

    # 🔥 HINT BUTTON
    if st.button("💡 Hint"):
        killer = case["killer"]
        hint = f"Focus on clues related to {killer.split()[0]}..."
        st.session_state.score -= 3
        log("Hint used", hint, "system")

    if st.button("🔄 New Case"):
        st.session_state.clear()
        st.rerun()


# ── HEADER ─────────────────────────────────────────

st.title("🕵️ AI Crime Simulator")

# ── SUSPECTS ───────────────────────────────────────

st.subheader("Suspects")

cols = st.columns(len(case["suspects"]))

for i, s in enumerate(case["suspects"]):
    name = s["name"]

    with cols[i]:
        st.write(f"**{name}**")
        st.write(s["role"])

        if st.button("Interrogate", key=f"int_{i}"):
            st.session_state.active_suspect = name

        if st.button("Accuse", key=f"acc_{i}"):
            explanation = explain_solution(case, name)
            st.session_state.game_over = True

            if name == case["killer"]:
                st.success("✅ Correct!")
                st.session_state.score += 20
            else:
                st.error(f"❌ Wrong! Killer was {case['killer']}")
                st.session_state.score -= 10

            st.write(explanation)


st.divider()

# ── INTERACTION ─────────────────────────────────────

active = st.session_state.active_suspect

if not st.session_state.game_over:

    if active:
        st.subheader(f"🎤 Interrogating {active}")

        # 🔥 SUGGESTED QUESTIONS
        st.markdown("💬 Suggested questions:")
        st.markdown("- Where were you?")
        st.markdown("- Do you know the victim?")
        st.markdown("- Can anyone confirm your alibi?")

    user_input = st.text_input("Enter command")

    if user_input:
        cmd = parse_command(user_input, case, active)

        # ── INTERROGATE ──
        if cmd["action"] == "interrogate":
            target = cmd.get("target") or active

            if target:
                history = st.session_state.suspect_history.get(target, [])

                response = interrogate_suspect(
                    case,
                    target,
                    cmd["question"],
                    history
                )

                st.session_state.score -= 1

                if target not in st.session_state.suspect_history:
                    st.session_state.suspect_history[target] = []

                st.session_state.suspect_history[target].append(
                    (cmd["question"], response)
                )

                log(cmd["question"], f"{target}: {response}", "suspect")

        # ── INSPECT ──
        elif cmd["action"] == "inspect":
            result = analyze_clue(case, cmd["target"])
            st.session_state.score -= 1
            log(user_input, result, "inspect")

        # ── ACCUSE ──
        elif cmd["action"] == "accuse":
            target = cmd.get("target")

            if target:
                explanation = explain_solution(case, target)

                if target == case["killer"]:
                    st.success("✅ Correct!")
                    st.session_state.score += 20
                else:
                    st.error(f"❌ Wrong! Killer was {case['killer']}")
                    st.session_state.score -= 10

                log(user_input, explanation, "system")
                st.session_state.game_over = True

        elif cmd["action"] == "leave":
            st.session_state.active_suspect = None

        elif cmd["action"] == "help":
            st.info("Try: interrogate, inspect, accuse, or just ask questions")

        else:
            st.warning("Unknown command")


# ── LOG ─────────────────────────────────────────────

st.divider()
st.subheader("📜 Investigation Log")

for entry in reversed(st.session_state.history):
    st.write(f"> {entry['user']}")
    st.write(entry["bot"])
    st.write("---")