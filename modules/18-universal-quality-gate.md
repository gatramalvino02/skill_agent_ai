# Module 18: Universal Quality Gate & Adversarial Self-Audit

Loaded automatically before final delivery in autonomous mode (and on `/audit`) to guarantee consistently high output quality across coding, web UI, copy, analysis, and automation.

## 1. Universal 6-Point Definition of Done (Silent Audit Before Reply)

Check every item silently before finishing. If ANY item fails, fix it autonomously first:

1. [ ] **Exact Intent Match**: Solves the user's real goal completely—no missing pieces, no unrequested bloat.
2. [ ] **Zero Placeholders**: Zero `TODO`, `pass`, `// ... rest of code`, `Lorem Ipsum`, dead links, or mocked values where real logic was expected.
3. [ ] **Boundary & Error Resilience**: Handles null/empty inputs, invalid types, timeouts, and failure states cleanly without swallowing errors.
4. [ ] **Evidence-Backed Accuracy**: Every referenced file path, symbol, dependency version, calculation, or command is verified—zero hallucinations.
5. [ ] **Domain Craft Standard**:
   - *Web/UI*: Passes `05-web-craft-anti-slop.md` 10-Point Audit + `07-web-live-runner.md` (desktop & mobile clean).
   - *Pure Coding*: Passes `06-pure-coding.md` (dense, flat flow, clean resource cleanup) + Tier 0/1 verification.
   - *Copy / Docs / Analysis*: Passes direct human voice, zero AI clichés, verified numbers, clear recommendation.
6. [ ] **Hygiene & Memory Sync**: Zero debug leftovers, zero exposed secrets, `.ai-memory/` updated (`TRACK_RECORD.md` appended at bottom, `CURRENT_STATE.md` <=30 lines).

## 2. Adversarial 1-Question Final Check

Ask silently once: *"If a strict senior engineer or skeptical user inspected this right now, what is the first flaw they would call out?"*
- If a real flaw exists -> patch it immediately before sending the final response.
