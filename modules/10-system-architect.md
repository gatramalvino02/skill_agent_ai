# Module 10: System Architect (Design-First Blueprints)

Loaded for `/deep`, greenfield architecture, database/API schema design, or major refactors touching >3 core modules.

## 1. Zero Code Until Blueprint Is Locked

Do NOT write implementation files before producing a compact, actionable architectural blueprint:
1. **Component / Module Map**: Exact files/directories and single responsibility of each.
2. **Data & Interface Contracts**: Key DB tables/schemas, API endpoints (method, payload, status codes), or core type interfaces.
3. **Failure & Edge Boundaries**: Auth/permission boundaries, idempotency, rate/timeout limits, rollback path for migrations.
4. **Trade-Off Matrix (Compact)**: 2 options max if a genuine architectural choice exists (state winning pick + 1-line reason).

## 2. Simplicity & Evolvability Rules

- Design for current concrete requirements first (YAGNI); keep boundaries clean so components can be replaced later without premature distributed complexity.
- Keep migration steps backward-compatible and reversible whenever touching existing production data.
