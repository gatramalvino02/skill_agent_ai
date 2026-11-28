# Module 03: Living Memory & Append-Only Track Record (.ai-memory/)

Keep full permanent project history, locked model/thinking inventory, and instant cross-agent/cross-session continuity without letting memory files bloat the token budget.

## 1. Five-File Memory Architecture

All memory lives locally in `.ai-memory/` so any agent or model can resume seamlessly:

| File | Purpose | Read Behavior |
| :--- | :--- | :--- |
| `CURRENT_STATE.md` | Rolling snapshot (<=30 lines): active status, active engine/model/thinking, last 3 changes, pending task / brainstorming handoff. | **Always read on boot.** |
| `CODEBASE_MAP.md` | 1-line/file index + key exports + **Pinned Major Versions** + **Cached Fast Commands**. | **Always read on boot (Pass 1).** |
| `RULES_LOCK.md` | **Locked Model & Thinking Inventory**, standing user rules, stack locks, do-not-break invariants (<=80 lines). | **Always read on boot.** |
| `MISTAKES.md` | Self-learning permanent rules captured from user corrections so errors never repeat. | **Always read on boot.** |
| `TRACK_RECORD.md` | **STRICT APPEND-ONLY** permanent history. Old entries are **NEVER deleted**. | **DO NOT read by default.** Only read when auditing or debugging deep history. |

## 2. Cold-Start Boot Sequence (<1,000 Tokens)

On every new session or after switching agent/model:
1. If `.ai-memory/` exists: read `CURRENT_STATE.md`, `RULES_LOCK.md`, `MISTAKES.md`, and `CODEBASE_MAP.md` in **one parallel batch**. Never open `TRACK_RECORD.md` during normal coding.
2. If `.ai-memory/` is missing on an **existing project (Brownfield Safe)**:
   - Run `python scripts/init_memory.py .` (0 AI tokens) if shell is available, OR create the 5 files from `templates/ai-memory/` via read-only inspection without altering existing code.
3. If `.ai-memory/` is missing on a **new project (Greenfield)**:
   - Initialize `.ai-memory/` immediately once the base scaffold is created (or right after first-run model inventory onboarding).

## 3. Mandatory Post-Edit & Onboarding Update Hooks

1. **After First-Run Model Inventory Onboarding**:
   - Write the user's exact model list + supported thinking levels (`Off`/`Low`/`Medium`/`High`) into `RULES_LOCK.md` under `## Locked Model Inventory`.
2. **After Brainstorming -> Execution Transition**:
   - Compress the agreed brainstorming decisions into `CURRENT_STATE.md` (`Status: WAITING_MODEL_SWITCH`) before showing the Pre-Flight Check so zero context is lost when the user switches models.
3. **After Any Code Creation, Edit, Rename, or Deletion** (update BEFORE the final reply):
   - **`TRACK_RECORD.md` (STRICT APPEND-ONLY — AT THE BOTTOM)**:
     - **HARD RULE**: NEVER delete, overwrite, or truncate previous entries. Always **APPEND** the new 1-line record at the very **bottom**:
     ```markdown
     - [YYYY-MM-DD HH:MM] | `path/file1`, `path/file2` | What changed (<=12 words) | Why | Verify: PASS (`cmd`, Xs)
     ```
   - **`CURRENT_STATE.md` (Rolling Snapshot <=30 Lines)**:
     - Update active status (`COMPLETED` / `WAITING_MODEL_SWITCH` / `AUTONOMOUS_EXEC`), active model & thinking effort, keep only the **3 most recent changes**, and 1 optional next step.
   - **`CODEBASE_MAP.md` (Self-Healing Incremental Sync)**:
     - Update ONLY the rows for added, deleted, renamed, or export-changed files (0 re-scan cost).
   - **`MISTAKES.md` (Self-Learning Capture)**:
     - Whenever the user corrects a mistake, library choice, naming style, or preference -> immediately append 1 crisp permanent rule to `MISTAKES.md`.

## 4. Anchor Refresh & Auto-Compaction Alert

- **Anchor Refresh**: After completing a major milestone or roughly every 10 turns in a long session, silently re-read `CURRENT_STATE.md` and `MISTAKES.md` to prevent context drift.
- **Auto-Compaction Alert**: When a session grows heavy or switches to an unrelated feature, write a clean <=10-line handoff into `CURRENT_STATE.md`, ensure `TRACK_RECORD.md` is appended, and notify the user in 1 line: *"Context is heavy; state & model roster are saved in `.ai-memory/` — safe to open a new chat or switch agents."*
