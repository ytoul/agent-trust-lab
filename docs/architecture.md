# Agent Trust Lab — Expense Processing Agent

## 1. Business Objective

Automate employee expense reimbursement using an AI agent.

The agent interprets expense information, consults company
policies, evaluates reimbursement eligibility, and can
request simulated payments.

All employees, receipts, amounts and payments are fictional.

## 2. System Components

1. FastAPI — accepts expense requests.
2. Pydantic — validates input structure.
3. SQLite — stores expenses and simulated payments.
4. Policy engine — evaluates category spending limits.
5. AI agent — interprets information and selects tools.
6. Policy retrieval tool — provides expense policy content.
7. Expense lookup tool — retrieves stored expenses.
8. Payment tool — records simulated payment transactions.

Components 5–7 are planned and not yet implemented.

## 3. Assets

- Employee expense records
- Company expense policies
- Employee identifiers
- Reimbursement eligibility decisions
- Payment authorization decisions
- Simulated payment ledger
- Agent instructions and tool permissions
- API credentials (when introduced)

## 4. Trust Boundaries

TB1: Employee input -> FastAPI application

TB2: Untrusted receipt and policy content -> AI agent context

TB3: AI agent -> Application tools

TB4: Payment tool -> SQLite payment ledger

TB5: Authenticated identity -> Employee expense records

TB2, TB3, and TB5 will be implemented and examined
in later stages.

## 5. Intended Business Rules

- Expenses must satisfy company reimbursement policies.
- Policy eligibility does not constitute payment approval.
- Payments require independent authorization.
- An expense must not be paid more than once.
- Employees should access only authorized expense records.
- Payment actions must be traceable to an authorized decision.

## 6. Known Intentional Weaknesses

VULN-001: Payment authorization is not independently
enforced by the simulated payment service.

VULN-002: Expense endpoints currently lack authentication
and object-level authorization.

VULN-003: The payment service relies on a previously
stored eligibility decision without revalidating it.

Additional AI-specific weaknesses will be documented
when the agent and retrieval components are implemented.

## 7. Lab Safety Boundaries

- Local development only.
- Bind the server to 127.0.0.1.
- Use synthetic employee and expense data.
- Never connect real payment providers.
- Never use production credentials.
- Keep intentional vulnerabilities isolated to this lab.

## 8. Current Implementation Status

Implemented:
- Expense input validation
- Expense API endpoints
- Deterministic policy evaluation
- SQLite expense storage
- Simulated payments
- Duplicate payment database constraint

Not yet implemented:
- LLM integration
- Agent tool orchestration
- Policy document retrieval
- Identity and approval workflows
- Agent-specific attack demonstrations
- Hardened security controls
