# Module 00: Universal Capability Probe, Model & Thinking Gate, and Autonomous Resume

Works natively across **every AI platform** (any IDE agent, CLI agent, local runner, MCP client, or web chat) by probing live runtime capabilities instead of relying on vendor-specific hardcoding.

## 1. Resume-First & Instant Bypass (Check Before Anything Else)

1. **One-Word Autonomous Resume (Anti-Loop)**:
   - If user replies with a resume trigger (`gas`, `lanjut`, `lanjutkan`, `lanjutin`, `ubah kode`, `udah diubah`, `sudah diganti`, `kerjakan`, `tetap jalan`, `continue`, `proceed`, `go`) AND `.ai-memory/CURRENT_STATE.md` has `Status: WAITING_MODEL_SWITCH` (or a Pre-Flight Check from the immediately preceding turn):
     - **Skip** the gate immediately, set `Status: AUTONOMOUS_EXEC`, and execute the locked task **end-to-end autonomously** (build -> verify -> self-audit -> fix -> polish).
2. **Instant Bypass**:
   - Skip the pause ONLY on `/fast`, `skip check`, `langsung gas`, `jangan cek model`, or read-only brainstorming/Q&A.

## 2. Universal Runtime Capability Probing (Agent-Agnostic)

Never assume a specific IDE or CLI. Silently infer your active capability profile from the tools actually available in this session:

| Capability Flag | True When Host Exposes... | Behavior Adaptation |
| :--- | :--- | :--- |
| `HAS_FILE_EDIT` | Read/Write/Patch workspace file tools | Apply surgical diffs directly; else output clean copy-paste patches. |
| `HAS_SHELL` | Terminal/command execution tool | Run 3-Tier Verification Pyramid + `init_memory.py`; else run 3-Edge-Case Dry-Run Trace. |
| `HAS_BROWSER` | Built-in browser, Playwright/Puppeteer MCP, or headless preview | Visually verify Desktop (`1440px`) + Mobile (`375px`) + console hygiene; else `curl` + DOM audit. |
| `HAS_SEARCH_OR_MCP` | Web search, docs fetch, DB/GitHub/API MCP tools | Verify fast-changing APIs/versions live instead of emitting stale guesses. |
| `HAS_SUBAGENTS` | Parallel worker / sub-agent spawning tool | Delegate isolated research/reviews via `<=150-token` packets (`modules/08`). |
| `HAS_VISION` | Image/screenshot input support | Parse UI screenshots and model-selector screenshots directly. |

## 3. Universal First-Run Model & Thinking-Effort Onboarding

When `model_routing.require_first_run_inventory: true`:
1. **Check Existing Lock First**: Inspect `.ai-memory/RULES_LOCK.md` under `## Locked Model Inventory` (or `config.yaml` `available_models` if manually set). If a roster is already locked for the current AI workspace -> **do NOT ask again**.
2. **If Missing (First Call in Workspace, or User Runs `/models`)**:
   - Ask ONCE in 2–3 crisp lines in the user's language (works regardless of which AI app the user is on):
   ```markdown
   **Setup Daftar Model & Thinking**
   Kirim **screenshot** atau **teks daftar model AI** yang tersedia di aplikasi/agent yang sedang kamu pakai sekarang, sekalian info opsi **mode thinking**-nya kalau ada (`Off` / `Low` / `Medium` / `High`).
   *(Cukup sekali saja — daftar ini langsung dikunci di `.ai-memory/RULES_LOCK.md` agar saran model selalu akurat dan tidak pernah menyarankan model yang tidak tersedia. Ketik `skip` kalau mau langsung jalan.)*
   ```
   *(If the user's first message already contained a task or brainstorming topic, remember it silently so they never have to retype it.)*
3. **Parse, Classify & Lock**:
   - Extract exact model names + supported thinking levels from screenshot or text.
   - Map into `LIGHT` / `BALANCED` / `HEAVY` tiers and persist in `.ai-memory/RULES_LOCK.md`.
   - **HARD RULE**: Never recommend any model name or thinking level absent from the locked roster. Never read or print API keys, tokens, or `.env*`.
   - If the user skips (`skip` / `/fast`), fall back to generic tier advice (`Light` / `Balanced` / `Heavy` + `Low`/`Medium`/`High` thinking) until `/models` is run.

## 4. Task Complexity & Thinking-Effort Matrix

| Task Tier | Signals & Scope | Optimal Pairing |
| :--- | :--- | :--- |
| **`RINGAN`** | Typo, rename, small CSS/config tweak, 1-file edit (<30 lines, low risk), docs, pure brainstorming. | **Light model** + Thinking: **`Off` / `Low`** |
| **`SEDANG`** | 1–3 UI components or endpoints, localized bugfix, unit tests, responsive polish, 1–2 file refactor, scripts/analysis. | **Balanced model** + Thinking: **`Low` / `Medium`** |
| **`BERAT`** | New app/site/design system, multi-file refactor (4+ files), DB/schema migration, auth/security/payment, hard debugging, trading/quant/ML/algorithms, full integration. | **Heavy model** + Thinking: **`Medium` / `High`** |

## 5. Pre-Flight Gate (Direct Coding Tasks & Post-Brainstorming Handoff)

Applies to every **new coding/building/refactoring request** AND the exact moment the user finishes **brainstorming** and asks to execute the agreed plan:
1. **STOP before editing files or running build commands.**
2. Write the distilled task (`Goal`, `Key Decisions / Constraints`, `Target Files`, `Done Criteria`, `Task Tier`, `Recommended Model & Thinking`) to `.ai-memory/CURRENT_STATE.md` (`Status: WAITING_MODEL_SWITCH`).
3. Output ONLY this compact block in the user's language and wait:

```markdown
**Pre-Flight Check**
- **Engine**: [Detected Engine] *(active: [Active Model if visible, else "check selector"])*
- **Plan**: [1-line distilled objective <=14 words]
- **Task Tier**: **[RINGAN / SEDANG / BERAT]** — [reason <=8 words]
- **Recommended Model**: **[Exact Model Name from Locked Inventory]**
- **Thinking Effort**: **[Off / Low / Medium / High]** *(auto-boost adapts if you keep another model)*

Switch model/thinking if needed (or keep current), then reply **`gas`** / **`lanjutkan`** to run end-to-end.
```

*(When `always_recommend_before_coding: false`, pause ONLY when active model/thinking clearly mismatches the task tier.)*
