# Module 07: Fast Web Live Runner & Visual Verification

Never deliver a website based purely on reading source files. Build, run locally with strict non-interactive timeouts, verify desktop/mobile rendering and console hygiene, and clean up immediately.

Respect `web_live_runner` in `config.yaml` and engine capabilities from `modules/00-engine-and-model-gate.md`.

## 1. Detect Stack & Reuse Cached Commands

Check `CODEBASE_MAP.md` first for cached fast commands (never scan `node_modules/`):
- **Node / Frontend (`package.json`)**: Use detected package manager (`pnpm`/`bun`/`yarn`/`npm`). Run with `CI=true`.
- **Static HTML/CSS/JS**: Serve via `python -m http.server <port>` or `npx --yes serve -l <port>`.
- **Python Web (FastAPI/Flask/Django/Streamlit)**: Launch configured local runner on a free port.

## 2. Fast Live Verification Pipeline

### Step A — Static & Build Gate (Fastest-First)
1. Run Tier 0 incremental typecheck/lint (`<15s` watchdog).
2. Run production build (e.g., `CI=true npm run build`, `<60s` watchdog) when applicable to catch bundling, SSR, CSS, or import failures.

### Step B — Isolated Background Server Boot
1. Pick a clean free port (default app port or `4173` / `5173` / `8080`).
2. Start dev/preview server in the background and poll until HTTP responds (hard timeout: `server_boot_timeout_sec`, default `15s` — never hang).

### Step C — Engine-Adaptive Inspection
- **If `HAS_BROWSER=true`** (Antigravity browser tool, Playwright MCP, IDE browser):
  1. Open local URL and verify **zero** uncaught JS errors, **zero** hydration warnings, and **zero** 404 assets in console/network.
  2. Inspect **Desktop (`1440x900`)** and **Mobile (`375x812`)**:
     - Confirm hero breathing room, typography contrast, living micro-interactions, and `<=10%` AI-slop standard (`modules/05-web-craft-anti-slop.md`).
     - Confirm zero horizontal overflow on mobile (`document.documentElement.scrollWidth <= window.innerWidth`).
     - Confirm zero clipped text, broken images, or overlapping elements.
  3. Trigger primary interactive controls (nav, tabs, forms, modals) to confirm real state transitions.
- **If `HAS_SHELL=true` and `HAS_BROWSER=false`**:
  1. Run fast `curl -fsS http://localhost:<port>` check confirming HTTP 200 and clean rendered HTML with zero error overlays/tracebacks.
  2. Run headless UI tests (`playwright`/`vitest --run`) if already installed.
  3. Inspect server stderr for runtime/SSR errors.
- **If `HAS_SHELL=false`**:
  - Perform strict manual code/responsive audit and output 1 exact local launch command.

## 3. Clean Process & Port Hygiene (Zero Zombie Servers)

- Always kill the temporary background server immediately after verification (`cleanup_background_server: true`) unless the user explicitly asked to keep the preview running.
- If left running at user request, report the exact `http://localhost:<port>` URL.
