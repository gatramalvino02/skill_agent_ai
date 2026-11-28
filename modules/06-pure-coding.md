# Module 06: Pure Coding Craft (Non-Web Universal)

Loaded for ALL non-web software engineering tasks — **Backend APIs, Microservices, CLI tools, Automation Scripts, Data/ML Pipelines, Bots, Trading/Quant Logic, Systems Utilities, Libraries, and Core Algorithms** across any language.

Skips web UI modules completely to protect tokens and keep 100% focus on dense, clean, bug-free logic.

## 1. Contract-First Engineering (Lock Before Writing Logic)

For any non-trivial function or module (`contract_first: true`):
- Define the **Input/Output Contract**, types/schemas, and error cases first before writing the implementation body.
- Preserve existing public function signatures, CLI flags, exit codes, DB schemas, and payload formats unless explicitly asked to change them.

## 2. High-Density, Zero-Bloat Code

- **Dense & Direct**: Write clean, idiomatic, tightly scoped code with zero dead code, zero unused imports, and zero redundant wrapper layers.
- **Flat Flow**: Prefer early returns and guard clauses over 4+ nested `if/else` levels. Keep each function cohesive with one clear job.
- **Why-Only Comments**: Never comment obvious code (`// increment i`). Comment only non-obvious invariants, edge constraints, or business rules.
- **Rule of Three**: Avoid speculative factories, plugin systems, or abstract base layers until a pattern genuinely repeats 3+ times.

## 3. Defensive Real-World Engineering

- **Boundary Guards**: Explicitly handle `None`/`null`/`undefined`, empty inputs, zero/negative values, malformed payloads, and timezone/encoding edge cases.
- **Fail-Loud Specific Errors**: Catch specific exception/error types only (never bare `except:` or empty `catch {}`). Attach concrete context (operation, path, ID, status code) and preserve original cause.
- **Resource & Concurrency Safety**: Always release files, sockets, DB connections, and subprocesses (`with`, `try/finally`, `defer`, RAII). Set explicit timeouts on ALL network/DB/subprocess calls. Never run blocking I/O inside async event loops.
- **Safe State**: Use atomic writes for persistent state files. Never hardcode secrets or machine-specific paths.

## 4. Domain Micro-Checklists (Apply Matching One)

- **Backend APIs**: Validate request payloads at boundary, return consistent status codes, enforce idempotency on mutations, never leak stack traces or secrets.
- **CLI & Automation**: Clear `--help`/usage, deterministic exit codes (`0` ok, non-zero fail), non-destructive defaults, clean stdout vs stderr split.
- **Data / ML / Quant**: Validate schema/NaN/missing values early, stream large datasets when practical, lock random seeds for reproducibility, avoid data leakage.
- **Algorithms & Core Libraries**: Watch time/space complexity (eliminate accidental $O(n^2)$ lookups inside loops using `set`/`dict`/`Map`), separate pure core logic from I/O for instant unit testing.
