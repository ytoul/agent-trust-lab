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

## Project status

Educational prototype under active development.

The repository will evolve as new Agent Trust Lab episodes are published.

## Related writing

Agent Trust Lab on Substack:
https://yiannitouliatos.substack.com/

## License

A license has not yet been selected.
