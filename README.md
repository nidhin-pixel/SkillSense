 HEAD
# SkillSense — AI-Powered Competency Intelligence Platform
Smart India Hackathon 2026 · SIH26101 · Theme: Smart Education

Full-stack scaffold: **FastAPI backend** + **React (Vite + Tailwind) frontend**.
Implements the core loop from the idea deck: Assess → Diagnose → Personalize →
Practice/Reassess → Track → Competency Passport → Department Dashboard.

---

## 1. Backend setup (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # edit if needed (DB, Groq key, etc.)

python -m app.seed                # creates DB + demo skills + demo accounts
uvicorn app.main:app --reload     # runs on http://localhost:8000
```

Interactive API docs: http://localhost:8000/docs

**Demo accounts (created by seed.py):**
| Role    | Email                        | Password     |
|---------|-------------------------------|--------------|
| Officer | officer@skillsense.gov.in     | Officer@123  |
| Admin   | admin@skillsense.gov.in       | Admin@123    |

**Database:** SQLite by default (`skillsense.db`, zero setup). To use
PostgreSQL/MySQL for a real deployment, just change `DATABASE_URL` in `.env`
— e.g. `postgresql://user:pass@localhost:5432/skillsense`.

**AI layer (optional):** Set `GROQ_API_KEY` in `.env` to generate real
LLM-based questions (matches your team's AI layer notes — currently using
`openai/gpt-oss-120b` on Groq). Without a key, the app automatically falls
back to a rule-based question bank so every feature still works end-to-end
for demos.

## 2. Frontend setup (React + Vite)

```bash
cd frontend
npm install
cp .env.example .env              # VITE_API_BASE_URL=http://localhost:8000
npm run dev                       # runs on http://localhost:5173
```

Open http://localhost:5173 — you'll land on the login page.

## 3. How the whole thing flows

1. **Login / Register** — JWT-based auth. New officers self-register; admins
   are set via `role` in the DB (seed script creates one demo admin).
2. **Dashboard** — officer's overall competency score, strongest/weakest
   skill, skill-by-skill bars with trend, recent session history.
3. **Take assessment** — pick a skill → adaptive 5-question quiz. Answering
   correctly raises difficulty (basic → intermediate → advanced → scenario),
   answering wrong lowers it. Each question is either AI-generated (if
   `GROQ_API_KEY` set) or drawn from the fallback bank.
4. **Session scoring** — harder questions are worth more; the session score
   and estimated level (Beginner…Expert) are computed and blended into the
   officer's running **Competency Record** (60% new evidence / 40% history —
   responsive but not erased by one bad day).
5. **Competency Passport** — a living, continuously-updated profile per
   skill: level %, confidence (low/medium/high, based on how many times
   it's been assessed), trend (improving/declining/stable), and gap
   severity (none/moderate/critical, critical skills flagged specially).
6. **Admin / Department dashboard** — aggregates every officer's competency
   records by skill to show department-wide averages and critical gaps,
   for evidence-based training planning.

## 4. Project structure

```
skillsense/
├── backend/
│   ├── app/
│   │   ├── main.py            FastAPI app, CORS, router registration
│   │   ├── config.py          Settings (.env driven)
│   │   ├── database.py        SQLAlchemy engine/session
│   │   ├── models.py          User, Skill, Question, AssessmentSession/Response, CompetencyRecord
│   │   ├── schemas.py         Pydantic request/response models
│   │   ├── security.py        Password hashing + JWT
│   │   ├── deps.py            get_current_user / require_admin
│   │   ├── seed.py            Demo data
│   │   ├── ai/
│   │   │   ├── question_gen.py       LLM question generation + fallback bank
│   │   │   └── competency_engine.py  Adaptive difficulty, scoring, gap logic
│   │   └── routers/
│   │       ├── auth.py, skills.py, assessment.py, competency.py, dashboard.py
│   └── requirements.txt
└── frontend/
    └── src/
        ├── api/client.js       Axios instance with auth interceptor
        ├── context/AuthContext.jsx
        ├── components/         Sidebar, SkillBar, StatCard, ProtectedRoute
        └── pages/               Login, Register, Dashboard, Assessment, Passport, AdminDashboard
```

## 5. What to build next (natural extensions, matches the idea deck)

- Skill Knowledge Graph visualization (skills already support `parent_id` nesting)
- iGOT Karmayogi content recommendation API integration
- Spaced reassessment scheduler (competency decay detection)
- AI-generated MCQs from uploaded PDFs/docs (feed extracted text into `question_gen.py`)
- Migrate SQLite → PostgreSQL + Alembic migrations for production
=======
# SkillSense
>>>>>>> b416d9f16436732cc091c00f5fecd1f5714ec3fb
