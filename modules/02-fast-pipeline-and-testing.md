# Module 02: Fast Verification Pipeline & Sub-Second Testing

Verify every code change with real execution while keeping feedback loops near-instant and terminal output ultra-compact.

## 1. Command Cache First (Zero Guessing Turns)

Before running any tool, check the **Cached Fast Commands** block at the top of `.ai-memory/CODEBASE_MAP.md`. Never waste turns guessing between `npm`, `pnpm`, `bun`, `pytest`, `uv`, or `go test`. If missing, detect once from root manifests and save to `CODEBASE_MAP.md`.

## 2. Three-Tier Verification Pyramid (Fastest-First, Fail-Fast)

Never run a full test suite or full production build after a 5-line edit unless required. Escalate only when needed:

| Tier | Target Time | Checks to Run | When to Trigger |
| :--- | :--- | :--- | :--- |
| **Tier 0 (Static)** | `< 2s` | Incremental typecheck & lint on changed files only (`tsc --noEmit --incremental`, `ruff check <file>`, `eslint <file>`, `go vet ./<pkg>`). | After **every** code edit. |
| **Tier 1 (Delta Test)** | `2 – 10s` | Affected tests ONLY + mandatory **Fail-Fast** flags (`vitest run <file> --bail 1`, `jest --findRelatedTests <file> --bail`, `pytest -x -q -k <target>`, `go test ./<pkg> -failfast`). | After every completed function, feature, or bugfix. |
| **Tier 2 (Full Pipeline)** | `15 – 45s` | Full build, integration/regression suite, or E2E using build cache (`turbo`, `nx`, incremental cache) where available. | On milestones, pre-commit, shared-core refactors, or `/test full`. |

## 3. Smart Test Skipping (Zero Redundancy)

- If an edit ONLY touches documentation (`.md`), code comments, or static copy without altering executable logic or config -> skip Tier 1 and Tier 2 automatically (`Verified: Docs-only skip`).

## 4. Silent-Pass, Loud-Fail Filter (Protect Context Window)

Verbose passing logs waste tokens and slow down inference:
- Always attach minimal output flags when supported (`--silent`, `-q`, `--reporter=dot`, `--tb=short`, `--no-color`).
- **On PASS**: Summarize in 1 line: `[PASS] 14 tests (0.9s)` — never paste full passing logs.
- **On FAIL**: Extract ONLY the failing test name, exact error/assertion diff, and top 15 stack trace lines (strip framework boilerplate).

## 5. Anti-Hang & Non-Interactive Lock + Timeout Watchdog

Terminal hangs destroy speed. Prevent every interactive stall:
- **Mandatory Non-Interactive Flags**: Always run with `CI=true` and non-watching flags (`--run`, `--watchAll=false`, `--yes`, `--no-interactive`, `-y`). Never run bare `vitest`, `jest`, or `npm run dev` in foreground.
- **Hard Timeout Watchdog**:
  - Tier 0 & Tier 1: max `15s` (`tier0_timeout_sec` / `tier1_timeout_sec`).
  - Tier 2: max `60s` (`tier2_timeout_sec`).
  - If a command exceeds its watchdog limit, kill the process immediately, diagnose the hang (open handle, missing env, watch mode), and never leave zombie processes running.

## 6. Anti-Cheat Test Gate & 3-Strike Circuit Breaker

- **Anti-Cheat Test Gate**: NEVER delete, skip (`.skip`), weaken assertions, or hardcode return values to make a failing test pass. Fix the code logic (or only update a test if the user explicitly changed the specification).
- **Bounded Self-Heal + 3-Strike Root-Cause Pause**:
  - Failure #1: Read exact failing line -> apply minimal targeted fix -> re-run.
  - Failure #2 (same error persists): **STOP blind guessing.** Enter **Root-Cause Pause** (`modules/09-forensic-debugger.md`):
    1. Write 3 concrete hypotheses for the real root cause.
    2. Run 1 minimal diagnostic check to isolate the true cause.
    3. Apply the verified 3rd fix.
  - Failure #3 (`max_self_heal_retries: 3`): **STOP** and escalate cleanly:
    - `Blocker`: exact error + `file:line`
    - `Tried`: 1-line summary of attempts
    - `Root Cause`: most likely cause
    - `Need From User`: 1 concrete decision or missing env/credential

## 7. No Proof, No Done

- Report `Verified: PASS` ONLY for commands executed **after the final edit**.
- If `HAS_SHELL=false` (chat-only engine): run an explicit **3-Edge-Case Dry-Run Trace** (empty/null input, wrong type/malformed data, boundary/timeout limit), state `Verified: Dry-Run only (no shell)`, and provide 1 exact local command.
