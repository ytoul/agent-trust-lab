# Agent Trust Lab

**A hands-on AI security lab for threat modeling agentic systems.**

Agent Trust Lab is a free educational project that follows the development and security testing of a fictional enterprise expense-processing AI agent.

The goal is to make AI security risks observable and reproducible, rather than simply describing them.

The project accompanies the **Agent Trust Lab** article series on Substack.

## What the lab demonstrates

- AI agent tool access and least privilege
- Read-only versus action-capable agents
- Object-level authorization weaknesses
- Indirect prompt injection through untrusted receipts
- Source-authority confusion and fabricated policy evidence
- Independent authorization and payment security
- Agent execution tracing and security testing

Not every scenario is implemented yet. The lab evolves alongside the article series.

## Current implementation

The application is built with Python, FastAPI, SQLite and the OpenAI Responses API.

Implemented application tools:

| Tool | Purpose |
|---|---|
| `get_receipt` | Retrieve a synthetic expense receipt |
| `get_expense` | Retrieve an expense record |
| `get_policy` | Retrieve company spending limits |
| `simulate_payment` | Record a simulated payment |

The read-only agent can execute the first three tools.

The simulated payment tool is blocked in the read-only configuration.

## Episode #3 — What Can This Agent Actually Do?

This episode examines the agent's tool inventory and the difference between model instructions and application-enforced permissions.

The accompanying experiments demonstrate:

1. A read-only agent cannot execute the simulated payment tool.
2. The agent may retrieve an unrelated expense record even when its final answer is correct.
3. Tool-level permissions do not replace object-level authorization.

## Security warning

**This project is intentionally vulnerable.**

It uses synthetic data and simulated payments only.

Do not connect it to production systems, real employee records, financial accounts or payment services.

Do not deploy the application publicly without implementing appropriate authentication, authorization and other security controls.

## Quick Start

### Prerequisites

- Python 3.12
- Git
- Windows PowerShell (instructions below)
- An OpenAI API key only for live AI agent experiments

This project is an intentionally vulnerable educational
application. Run it locally using synthetic data.

### 1. Clone the repository

```powershell
git clone https://github.com/ytoul/agent-trust-lab.git
cd agent-trust-lab
```

### 2. Create a virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the expense API

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open the following URLs:

- API documentation: http://127.0.0.1:8000/docs
- Health endpoint: http://127.0.0.1:8000/health

The application initializes its local SQLite database
during startup.

Press Ctrl+C to stop the server.

### 5. Run the security regression tests

In the activated virtual environment:

```powershell
python -m pytest tests/ -q
```

The current published baseline contains 17 tests.

No OpenAI API key is required for these tests.

### 6. Configure live AI agent experiments (optional)

Copy the example configuration:

```powershell
Copy-Item .env.example .env
```

Open .env and replace the placeholder with your own OpenAI API key.

The example configuration uses:

```text
OPENAI_MODEL=gpt-5.4-mini
```

Live agent experiments use the OpenAI API and may incur
API usage charges. A ChatGPT subscription does not
automatically include API credits.

Never commit your `.env` file or share API keys.

### 7. Explore Episode #3

Start with the
[Episode #3 tool permissions walkthrough](labs/03-tool-permissions/README.md).

The lab demonstrates:

- Three read tools available to the agent
- A payment tool blocked by application-level controls
- An unexpected cross-employee expense lookup
- Why tool permissions do not replace record-level authorization

You can inspect the
[recorded experiment evidence](examples/episode-03/unexpected-expense-lookup.json)
without making an OpenAI API call.

## Safety and limitations

Agent Trust Lab intentionally contains insecure behavior
for threat-modeling and security education.

- Use synthetic data only.
- Bind the development API to localhost.
- Do not connect real payment services or enterprise data.
- Do not expose the API directly to the internet.
- Do not interpret successful tests as proof of overall security.

The project is not production-ready.

## Project status

Educational prototype under active development.

The repository will evolve as new Agent Trust Lab episodes are published.

## Related writing

Agent Trust Lab on Substack:
https://yiannitouliatos.substack.com/

## License

Apache 2.0 License
