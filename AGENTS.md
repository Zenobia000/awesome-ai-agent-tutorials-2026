# AGENTS.md

## Repository Instructions for AI Agents

- **Environment**: Python 3.11+, strict PEP 8 formatting.
- **Layout**:
  - `modules/module-XX-*/` — one self-contained lab per module; do not import across modules.
  - `projects/incident-autonomous-agent/` — flagship project; infra via its `docker-compose.yml`.
  - `docs/` — theory write-ups only, no runnable code.
  - `eval_benchmarks/` — datasets and eval scripts (Ragas / G-Eval).
- **Architectural Rules**:
  - Always prefer deterministic state transitions in LangGraph over unbounded LLM loops; set `recursion_limit`.
  - All tool definitions must use Pydantic models for argument validation.
  - Implement checkpointing using `PostgresSaver` or `InMemorySaver`; never leave states in volatile variables.
  - Any retrieval pipeline must implement fallback strategies (Dense + Sparse with RRF).
- **Secrets**: read from environment (`.env`, see `.env.example`); never hardcode keys or passwords.
