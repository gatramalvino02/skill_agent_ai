# Module 09: Forensic Debugger & Root-Cause Protocol

Loaded for bug investigations, runtime crashes, flaky tests, regressions, and 3-Strike Root-Cause Pauses.

## 1. Reproduce & Isolate First (Never Patch Blindly)

1. **Exact Failure Capture**: Read the exact error message, failing assertion, and first project-owned frame in the stack trace (ignore deep framework internals unless proven relevant).
2. **Minimal Reproduction**: Isolate the smallest input, state, or single Tier 1 test command that triggers the bug deterministically.
3. **Backward Trace & Binary Isolation**: Follow the corrupted value backward from crash line to divergence point; for regressions across many changes, bisect (`git diff` / midpoint check) to pinpoint the exact breaking layer.

## 2. 3-Strike Root-Cause Pause (Mandatory After 2 Consecutive Failures)

If the same error fails twice:
1. **STOP patching immediately.**
2. State **3 distinct hypotheses** (e.g., stale state/cache, dependency version mismatch, race condition, env/path mismatch, wrong assumption at caller).
3. Run **1 minimal diagnostic check** to prove which hypothesis is true.
4. Apply the minimal verified fix, strip any diagnostic logs, and re-run Tier 1 verification.

## 3. Regression Lock & Learning

- Add or run a targeted regression test covering the exact bug input so it cannot silently return.
- Append 1 crisp permanent rule to `.ai-memory/MISTAKES.md` if the bug revealed a recurring project quirk.
