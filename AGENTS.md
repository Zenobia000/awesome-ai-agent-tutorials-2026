# AGENTS.md

## Repository Instructions for AI Agents

- **Environment**: Python 3.11+, strict PEP 8 formatting.
- **Layout**:
  - `modules/module-XX-*/` — numbered notebooks per module; modules never import each other, only `course_utils/`.
  - `infra/` — service deployment guides and `compose.yml` (profiles m1–m7); no course code.
  - `course_utils/` — shared model client (`chat`, `stream`, `embed`); keep it small.
  - `projects/incident-autonomous-agent/` — flagship project; infra via its `docker-compose.yml`.
  - `docs/` — theory write-ups only, no runnable code.
  - `eval_benchmarks/` — datasets and eval scripts (Ragas / G-Eval).
- **Architectural Rules**:
  - Write operations go through a fixed LangGraph flow (approve → execute → verify); agent loops always set `recursion_limit`.
  - All tool definitions must use Pydantic models for argument validation.
  - Implement checkpointing using `PostgresSaver` or `InMemorySaver`; never leave states in volatile variables.
  - Any retrieval pipeline must implement fallback strategies (Dense + Sparse with RRF).
- **Teaching style**: each module starts with `00_concepts.md` (principles in prose and diagrams); notebooks use mainstream libraries from the first cell and print their intermediate results instead of re-implementing internals. Only exception: hand-written ReAct and function-calling loops in module 5. One idea per notebook. No ops tooling (Kubernetes, Triton, vLLM clusters, DeepSpeed).
- **Secrets**: read from environment (`.env`, see `.env.example`); never hardcode keys or passwords.
