# AGENTS.md

## Repository Instructions for AI Agents

- **Environment**: Python 3.11+, strict PEP 8 formatting.
- **Layout**:
  - `modules/module-XX-*/` — numbered notebooks per module; modules never import each other, only `course_utils/`.
  - `course_utils/` — shared model client (`chat`, `stream`, `embed`); keep it small.
  - `projects/incident-autonomous-agent/` — flagship project; infra via its `docker-compose.yml`.
  - `docs/` — theory write-ups only, no runnable code.
  - `eval_benchmarks/` — datasets and eval scripts (Ragas / G-Eval).
- **Architectural Rules**:
  - Write operations go through a fixed LangGraph flow (approve → execute → verify); agent loops always set `recursion_limit`.
  - All tool definitions must use Pydantic models for argument validation.
  - Implement checkpointing using `PostgresSaver` or `InMemorySaver`; never leave states in volatile variables.
  - Any retrieval pipeline must implement fallback strategies (Dense + Sparse with RRF).
- **Teaching style**: build the minimal version by hand first (numpy, a while loop), then swap in the library. One idea per notebook; print every intermediate result. No ops tooling (Kubernetes, Triton, vLLM clusters, DeepSpeed).
- **Secrets**: read from environment (`.env`, see `.env.example`); never hardcode keys or passwords.
