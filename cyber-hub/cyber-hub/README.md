# 🤖 Cyber Hub — Multi-Agent Simulation Platform

A living platform where AI agents collaborate like a real tech company.

---

## Tech Stack

| Layer      | Technology                         | Why                                   |
|------------|------------------------------------|---------------------------------------|
| Backend    | Python + FastAPI                   | Fast async API                        |
| AI Agents  | LangChain + LangGraph              | Agent orchestration + workflow graphs |
| LLM        | Groq API (Llama3 — FREE)           | Fast, free inference                  |
| Task Queue | Celery                             | Run agent tasks in background         |
| Database   | PostgreSQL                         | Persistent storage                    |
| Cache      | Redis                              | Celery broker + fast reads            |
| Frontend   | React + Vite + Tailwind            | Fast, modern UI                       |
| Container  | Docker + Docker Compose            | One-command setup                     |

---

## Setup (Step by Step)

### 1. Get a Free Groq API Key
1. Go to https://console.groq.com
2. Sign up (free)
3. Create an API key
4. Copy it

### 2. Add Your API Key
Edit the `.env` file in the root folder:
```
GROQ_API_KEY=your_actual_key_here
```

### 3. Install Docker
If you don't have Docker:
- Download Docker Desktop from https://www.docker.com/products/docker-desktop
- Install and start it

### 4. Run Everything
```bash
docker compose up --build
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- FastAPI backend on http://localhost:8000
- Celery worker (background agent runner)
- React frontend on http://localhost:3000

### 5. Open the App
Go to http://localhost:3000

---

## How It Works

```
User submits topic
      ↓
FastAPI creates research session in PostgreSQL
      ↓
Celery task starts in background
      ↓
LangGraph runs the research pipeline:
  Node 1: Research Major plans the work
  Node 2: Requests agents from Agent Hub
  Node 3: Each agent researches its area
  Node 4: Synthesizer combines all results
      ↓
Result saved to PostgreSQL
      ↓
Frontend polls and shows result
```

---

## Project Structure

```
cyber-hub/
├── backend/
│   └── app/
│       ├── agents/
│       │   ├── hub/            ← Agent Hub (spawns agents)
│       │   └── research/       ← Research Area (LangGraph pipeline)
│       ├── api/routes/         ← API endpoints
│       ├── core/               ← DB + config
│       ├── models/             ← Database tables
│       ├── schemas/            ← Request/Response shapes
│       └── tasks/              ← Celery background tasks
├── frontend/
│   └── src/
│       ├── components/         ← UI components
│       ├── pages/              ← Full page views
│       ├── services/           ← API calls
│       └── store/              ← Global state (Zustand)
└── docker-compose.yml
```

---

## API Docs
Once running, visit http://localhost:8000/docs for interactive API documentation.

---

## What's Next (Future Expansions)
- [ ] Developer Area with its own Major + agents
- [ ] Tester Area
- [ ] WebSocket for real-time agent thought streaming
- [ ] Agent-to-agent direct communication
- [ ] Agent memory across sessions
