# 🕵️ AI Crime Simulator

AI Crime Simulator is an interactive detective game powered by Google Gemini AI. Players solve a murder mystery by interrogating suspects, analyzing clues, and making logical deductions.

---

## 🎮 Features

- AI-generated murder mystery cases
- Interactive suspect interrogation
- Clue analysis system
- Score-based gameplay
- Hint system for guidance
- Fallback mode (works even if API fails)

---

## 🧠 Tech Stack

- Python
- Streamlit
- Google Gemini API

---

## ⚙️ How It Works

1. A murder case is generated using AI
2. Player interrogates suspects
3. Clues are analyzed
4. Player makes a final accusation
5. System evaluates correctness and gives result

---

## ▶️ Run Locally

1. Clone the repository:

```bash
git clone https://github.com/Tushar-075/ai-crime-simulator.git
cd ai-crime-simulator
pip install streamlit python-dotenv google-generativeai
streamlit run app.py


Create a .env file in the root folder:

GOOGLE_API_KEY=your_api_key_here
