# AI Agent Learning

My hands-on learning journey for building AI agents with Python, LangChain, LangGraph and MCP.

**Status:** Step 1 complete (agent + MCP server working). Step 2 in progress (HR and KB servers).

---

## Goal

Build a small **Employee Helpdesk Agent** that touches the main parts of a real agent system:

- Agent building (LangChain / LangGraph)
- MCP servers (tools) and, later, an MCP gateway
- Identity (IDP) and user permissions (OBO)
- Guardrails, observability, evaluation, deployment

Example questions the agent should handle:

- "Raise an IT ticket for my laptop"
- "How many leave days does Pandula have?"
- "What is the remote work policy?"

---

## Project structure

```
ai-agent-learning/
├── README.md
└── helpdesk-agent/
    ├── .env                 # API key (never commit)
    ├── .gitignore
    ├── .venv/               # virtual environment
    ├── app/
    │   └── agent.py         # the agent (LLM + MCP client)
    ├── mcp_servers/
    │   ├── tickets.py       # IT tickets (SQLite)
    │   ├── hr.py            # leave balance / apply leave (mock data)
    │   └── kb.py            # company policy search (mock data)
    ├── data/
    │   └── helpdesk.db      # created automatically
    └── check_db.py          # helper to view tickets
```

---

## Setup

```powershell
cd helpdesk-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install langchain langchain-openai langgraph langchain-mcp-adapters mcp python-dotenv
```

Create `.env` in `helpdesk-agent/` (no quotes, no spaces around `=`):

```
OPENCODE_API_KEY=your_key_here
```

Add this to `.gitignore`:

```
.env
.venv/
data/
__pycache__/
```

Run the agent (the prompt must start with `(.venv)`):

```powershell
python app/agent.py
```

---

## What has been done so far

### 1. Environment
- Python virtual environment and the main libraries installed.
- API key stored in `.env` and loaded with `python-dotenv`.

### 2. LLM connection (OpenCode Go)
The model is called through LangChain's `ChatOpenAI`, pointed at OpenCode Go's OpenAI-compatible endpoint:

```python
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0,
    api_key=os.environ.get("OPENCODE_API_KEY"),
    base_url="https://opencode.ai/zen/go/v1",
    default_headers={
        "x-opencode-session": SESSION_ID,     # required by OpenCode Go
        "User-Agent": "helpdesk-agent/1.0",
    },
)
```

Notes:
- OpenCode Go needs the `x-opencode-session` header (otherwise `MissingSessionID` error).
- Use models on the chat completions endpoint. Some models (MiniMax, Qwen) use a different endpoint and will not work with `ChatOpenAI`.
- OpenCode Go is designed mainly for coding agents. Keep usage light, or switch to another provider later (only this block changes).

### 3. First MCP server: `tickets.py`
- Tools: `create_ticket(user, issue)` and `get_ticket(ticket_id)`.
- Tickets are stored in **SQLite** (`data/helpdesk.db`), so they survive between runs and are shared by every client.

### 4. Agent with MCP tools
- `MultiServerMCPClient` starts each server over **stdio** and loads its tools.
- `create_agent(llm, tools)` builds the tool-calling agent.
- `agent.ainvoke(...)` runs it (async, because MCP tools are async).
- Result: the agent turns plain English into a real ticket in the database.

### 5. HR and KB servers (Step 2)
- `hr.py`: `get_leave_balance`, `apply_leave` (mock data). Later used to demonstrate user permissions.
- `kb.py`: `search_policy` (mock policies). A simple stand-in for RAG.
- Having several servers lets us practise tool selection, routing, the gateway and security.

---

## Key concepts learned

| Concept | Summary |
|---|---|
| Agent | LLM + tools + loop. The model decides, your code acts. |
| Tool calling | The model only *asks* for a tool. Your code runs it. |
| Docstring | The text in `"""..."""` under a function. MCP sends it to the model as the tool description, so write it clearly. |
| Tool choice | The model picks a **tool** from names, descriptions and parameters. Each tool is linked to its server by plain code, not by the AI. |
| stdio transport | The agent starts the MCP server itself as a child process each run. No always-on server and no dashboard. |
| MCP Inspector | A separate manual testing tool with a browser UI. Not part of the agent. |
| `invoke` vs `ainvoke` | `ainvoke` is the async version. Required with MCP tools. |
| Persistent data | Never keep important data in memory. In-memory data resets every run. Use a database. |
| Validation | Real checks (such as leave limits) belong in the tool, not in the prompt. |

---

## Useful commands

```powershell
# Run the agent
python app/agent.py

# Test one MCP server manually (silent = healthy, Ctrl+C to stop)
.\.venv\Scripts\python.exe mcp_servers\tickets.py

# Test tools in a browser
npx @modelcontextprotocol/inspector .\.venv\Scripts\python.exe mcp_servers\tickets.py

# View tickets
python check_db.py
```

`check_db.py`:

```python
import sqlite3
from pathlib import Path

db = Path(__file__).resolve().parent / "data" / "helpdesk.db"
conn = sqlite3.connect(db)
for r in conn.execute("SELECT id, user, issue, status FROM tickets"):
    print(f"T-{r[0]:03d} | {r[1]} | {r[2]} | {r[3]}")
conn.close()
```

---

## Troubleshooting log (errors I hit and fixes)

| Error | Cause | Fix |
|---|---|---|
| `No module named 'langgraph.prebuild'` | Typo | Use `prebuilt`, or better `from langchain.agents import create_agent` |
| `Missing credentials` / `Key loaded: False` | `.env` not found or wrong format | Put `.env` in project root, use `OPENCODE_API_KEY=...` with no quotes |
| `MissingSessionID` (400) | OpenCode Go needs a session header | Add `x-opencode-session` and a custom `User-Agent` |
| `No module named 'mcp'` / `'dotenv'` | Wrong Python (venv not active) | Activate `.venv`, check prompt shows `(.venv)` |
| `Connection closed` (McpError) | An MCP server script crashed on start | Run each server by hand to see its real error |
| `NameError: name 'Path' is not defined` | Missing import in `tickets.py` | Add `import sqlite3` and `from pathlib import Path` |
| `NameError: name 'sys' is not defined` | Missing import in `agent.py` | Add `import sys` |
| Ticket always `T-001` | Tickets were stored in memory, new server copy each run | Store tickets in SQLite |
| `LangGraphDeprecatedSinceV10` warning | `create_react_agent` moved | Use `langchain.agents.create_agent` |
| Tool result shows `[{'type': 'text', ...}]` | Adapter returns content blocks | Join the `text` fields when printing |

Rules of thumb:
- Do not use `print()` inside stdio MCP servers (it breaks the protocol).
- Use `sys.executable` and absolute paths (`ROOT / "mcp_servers" / ...`) in the client config.
- Always check the prompt for `(.venv)` before running.

---

## Roadmap

- [x] Step 1: One MCP server + agent that calls it
- [ ] Step 2: Add HR and KB servers, test tool selection
- [ ] Step 3: Rebuild as a LangGraph graph (guard, router, specialist nodes) with memory
- [ ] Step 4: Switch MCP servers to HTTP and add an MCP gateway
- [ ] Step 5: Add Keycloak (IDP), JWT validation, role checks (OBO style)
- [ ] Step 6: Guardrails and human approval for risky actions
- [ ] Step 7: Observability with OpenTelemetry and Arize Phoenix
- [ ] Step 8: Evaluation (golden test set, run in CI)
- [ ] Step 9: Docker Compose deployment
- [ ] Bonus: A2A, CrewAI comparison, small local model (Ollama)

---

## Test questions for Step 2

1. "How many leave days does Pandula have?" (should call `get_leave_balance`)
2. "What is the remote work policy?" (should call `search_policy`)
3. "Apply 3 days leave for Erandi, and raise a ticket that his laptop is slow." (two tools in one request)
4. "Apply 10 days leave for Erandi." (the tool should refuse: not enough balance)
