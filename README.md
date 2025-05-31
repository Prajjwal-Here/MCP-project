
# MCP Pokémon Interface

The **MCP Pokémon Interface** is a full-stack natural language interface for exploring Pokémon data. Built with a Flask backend and a React frontend, it enables users to get Pokémon info, compare stats, analyze types, generate strategies, and build teams using conversational input.

---

## 🔧 System Setup and Deployment

### Backend Setup

**Requirements**:
- Python 3.9+
- pip

**Steps**:
```bash
cd mcp_server
pip install -r requirements.txt
python app.py
```

This starts the Flask API on `http://localhost:5000`.

### Frontend Setup

**Requirements**:
- Node.js
- npm

**Steps**:
```bash
cd frontend
npm install
npm run dev
```

This runs the React frontend on `http://localhost:5173`.

---

## 🗂 Backend Structure Overview

```
mcp_server/
│
├── api/                  # Module endpoints
│   ├── compare.py        # Pokémon comparison
│   ├── pokemon.py        # Pokémon info
│   ├── strategy.py       # Strategy suggestions
│   ├── team.py           # Team builder
│   ├── type_info.py      # Type matchups
│   └── __init__.py
│
├── services/             # NLP and data fetching
│   ├── parser.py         # Parses natural language
│   ├── fetcher.py        # Fetches data from APIs
│   └── __init__.py
│
├── app.py                # App factory setup
├── config.py             # App settings
├── run.py                # Launch script
├── requirements.txt      # Python dependencies
└── logs/                 # Optional runtime logs
```

---

## 🧠 Available Modules and Usage

The app uses a single NLP endpoint that routes queries to the correct module:

- **Pokémon Info**  
  Get basic stats and type info.  
  _Example_: `Tell me about Pikachu`

- **Type Info**  
  Check type strengths and weaknesses.  
  _Example_: `What is Grass weak against?`

- **Strategy Suggestion**  
  Suggest movesets, battle tactics.  
  _Example_: `How should I use Scizor in battle?`

- **Pokémon Comparison**  
  Compare stats, typing, and effectiveness.  
  _Example_: `Compare Gengar and Alakazam`

- **Team Builder**  
  Generate a full team from a goal.  
  _Example_: `Create a balanced team with good type coverage`

---

## 🌐 Web Interface Walkthrough

1. Open `http://localhost:5173` after starting the frontend.
2. Select a module from the dropdown:
   - Search Info
   - Type Info
   - Strategy
   - Compare
   - Team Builder
3. Enter a natural language query (e.g., `Info about Charizard`).
4. Click Submit and view the formatted response.

Each module is in a dedicated component and styled for simplicity.

---

## 🛠 How the Team Builder Works

- Accepts freeform input like:  
  _"Build me a team that counters Dragon-types"_  
- The backend parser identifies goals, roles, and types.
- The `team.py` module selects 6 synergistic Pokémon.
- Returns a human-readable explanation with team composition.

---

## 🤖 Agent Integration Guide

To integrate this system with an AI agent:

1. **Send Queries to NLP Endpoint**:
   - POST JSON with `{ "query": "your natural language question" }` to `/nlp`.

2. **Receive Structured Response**:
   - Backend routes it to the correct module.
   - Returns a readable natural language reply.

3. **Embed into Tools or Apps**:
   - Use this API as the backend logic for chatbots, Discord bots, or voice assistants.

Example:
```python
import requests

res = requests.post("http://localhost:5000/nlp", json={"query": "Compare Garchomp and Salamence"})
print(res.json())
```

---

## 🎬 Demo Instructions

1. Run the backend and frontend.
2. Visit `localhost:5173`.
3. Try natural language queries across all modules.
4. See responses formatted as paragraphs or explanations.

---

## ✅ Summary

- Modular NLP backend (`/nlp`) with 5 functional routes.
- React frontend with dynamic module switching.
- Team builder based on type synergy and role diversity.
- Designed to be embedded in tools and expanded easily.

---
