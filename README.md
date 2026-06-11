Passport Readiness AI Crew (CrewAI + Groq)

This project is an AI-powered Passport Eligibility & Fee Calculator system built using CrewAI + Groq LLM + Python.

It simulates a real-world government passport processing workflow using multiple AI agents:

Policy validation
Fee calculation
Document checklist generation
Local fallback report (always works even if AI fails)
🚀 Features

✔ Multi-agent AI system using CrewAI
✔ Groq LLM integration (fast inference)
✔ Policy-based passport eligibility rules
✔ Automatic fee calculation from structured database
✔ Dynamic document checklist generation
✔ Built-in fallback system (works without AI)
✔ JSON-based configuration system

🧠 AI Agents Used
1. Policy Guardian 🛂
Checks passport eligibility
Validates requested validity rules
2. Fee Calculator 💰
Computes passport fees
Uses structured government fee database
3. Document Specialist 📄
Generates required document checklist
Based on age and profession
📂 Project Structure
project/
│── app.py
│── passport_db.json
│── .env
│── README.md
⚙️ Installation
1. Clone the project
git clone https://github.com/your-repo/passport-ai-crew.git
cd passport-ai-crew
2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install dependencies
pip install crewai python-dotenv
🔑 Environment Setup

Create a .env file:

GROQ_API_KEY=your_groq_api_key_here

👉 Get API key from:
https://console.groq.com/

▶️ How to Run
python app.py
📊 Sample Output
================ CREW RESULT ================

(Agent-based AI output here if successful)

================ LOCAL REPORT ================

| Item | Result |
|------|--------|
| Validity | 10 Years |
| Delivery | Express |
| Total Fee | 10350 BDT |
| Required ID | NID |
| Documents | NID Card, Application Summary, Payment Slip |
| Policy Status | No Issues |
📦 passport_db.json (Structure)
fees_2026:
  48_pages:
    5_years:
      regular: 4025
      express: 6325
      super_express: 8625

Includes:

Fee matrix
Required documents
Government rules
🧩 Business Logic
Passport Policy Rule
Age < 18 → 5 years validity + Birth Registration
Age > 65 → 5 years validity + NID
Else → 10 years validity + NID
🛡️ Fallback System

Even if AI fails:

System still calculates fees
Still generates document checklist
Still shows full report

✔ This makes the system production-safe

⚠️ Common Issues
1. Invalid model error

Use:

groq/llama-3.1-8b-instant
2. API error

Check:

.env file exists
API key is valid
3. CrewAI error

Upgrade:

pip install --upgrade crewai
📈 Future Improvements
Add FastAPI backend
Add UI dashboard (React)
Add database storage (PostgreSQL)
Add real government rules API
Multi-language support (EN/BN)