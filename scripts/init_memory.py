#!/usr/bin/env python3
"""
Zero-token repository scanner & memory bootstrapper for Skill Agent.
Builds `.ai-memory/CODEBASE_MAP.md` (with key exports, pinned major versions,
and cached fast commands), plus `CURRENT_STATE.md`, `RULES_LOCK.md`,
`MISTAKES.md`, and append-only `TRACK_RECORD.md` in under 1 second.

Usage:
    python scripts/init_memory.py [target_repo_dir] [--force] [--refresh-map] [--prune]
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

IGNORE_DIRS = {
    ".git", ".ai-memory", ".agent", ".agents", ".claude", ".cursor", ".opencode",
    ".windsurf", ".roo", ".gemini", "node_modules", "dist", "build", ".next",
    ".nuxt", ".svelte-kit", "out", "coverage", "__pycache__", ".venv", "venv",
    "env", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".idea", ".vscode",
    "vendor", "target", ".turbo", ".cache", "tmp", "logs", "_tmp_skill",
}

IGNORE_EXTS = {
    ".lock", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".mp3", ".pdf", ".zip",
    ".tar", ".gz", ".pyc", ".pyo", ".map", ".min.js", ".min.css", ".wasm",
}

IGNORE_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
    "poetry.lock", "Cargo.lock", "composer.lock", ".DS_Store", "Thumbs.db",
    ".clinerules", ".roorules", ".cursorrules", ".windsurfrules", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "copilot-instructions.md",
}

WEB_FRONTEND_DEPS = {
    "react", "next", "vue", "nuxt", "svelte", "astro", "vite",
    "tailwindcss", "@angular/core", "solid-js", "remix",
}

KEY_JS_DEPS = [
    "next", "react", "vue", "nuxt", "svelte", "astro", "vite",
    "tailwindcss", "typescript", "express", "fastify", "hono", "prisma", "drizzle-orm",
]

WEB_EXTS = {".html", ".css", ".scss", ".tsx", ".jsx", ".vue", ".svelte", ".astro"}
BACKEND_EXTS = {".py", ".go", ".rs", ".java", ".php", ".rb", ".cs", ".cpp", ".c", ".mq5", ".mq4", ".sh"}

MAX_FILES_IN_MAP = 140
MAX_FILE_BYTES_FOR_SYMBOLS = 120_000
MAX_SYMBOLS_PER_FILE = 5

SYMBOL_PATTERNS = {
    ".py": re.compile(r"^(?:async\s+def|def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE),
    ".ts": re.compile(r"^export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const|interface|type)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE),
    ".tsx": re.compile(r"^export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const|interface|type)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE),
    ".js": re.compile(r"^(?:export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const)|function)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE),
    ".jsx": re.compile(r"^(?:export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const)|function)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE),
    ".go": re.compile(r"^func\s+(?:\([^)]*\)\s*)?([A-Z][A-Za-z0-9_]*)|^type\s+([A-Z][A-Za-z0-9_]*)", re.MULTILINE),
    ".rs": re.compile(r"^pub\s+(?:async\s+)?(?:fn|struct|enum|trait)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE),
    ".php": re.compile(r"^(?:final\s+|abstract\s+)?class\s+([A-Za-z_][A-Za-z0-9_]*)|^\s*public\s+function\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE),
}


def extract_symbols(full_path: Path) -> list[str]:
    ext = full_path.suffix.lower()
    pattern = SYMBOL_PATTERNS.get(ext)
    if not pattern:
        return []
    try:
        if full_path.stat().st_size > MAX_FILE_BYTES_FOR_SYMBOLS:
            return []
        text = full_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    found = []
    seen = set()
    for match in pattern.finditer(text):
        sym = next((g for g in match.groups() if g), None)
        if sym and not sym.startswith("_") and sym not in seen:
            seen.add(sym)
            found.append(sym)
            if len(found) >= MAX_SYMBOLS_PER_FILE:
                break
    return found


def guess_role(rel_path: Path) -> str:
    name = rel_path.name.lower()
    parts = [p.lower() for p in rel_path.parts]
    ext = rel_path.suffix.lower()

    if name in ("package.json", "pyproject.toml", "requirements.txt", "cargo.toml", "go.mod", "composer.json"):
        return "Project manifest"
    if name in ("tsconfig.json", "vite.config.ts", "vite.config.js", "next.config.ts", "next.config.mjs", "next.config.js", "tailwind.config.js", "tailwind.config.ts"):
        return "Build/framework config"
    if name.startswith("readme"):
        return "Documentation"
    if name in ("dockerfile", "docker-compose.yml", "docker-compose.yaml"):
        return "Container config"
    if "test" in name or "spec" in name or any(p in ("tests", "test", "__tests__") for p in parts):
        return "Automated tests"
    if any(p in ("components", "ui") for p in parts):
        return "UI component"
    if any(p in ("pages", "app", "routes", "views") for p in parts):
        return "Route/page"
    if any(p in ("api", "controllers", "handlers", "services") for p in parts):
        return "Service/endpoint"
    if any(p in ("hooks", "composables") for p in parts):
        return "State/hook"
    if any(p in ("utils", "lib", "helpers") for p in parts):
        return "Utility"
    if any(p in ("styles", "css") for p in parts) or ext in (".css", ".scss"):
        return "Stylesheet"
    if any(p in ("models", "schemas", "types", "db", "prisma") for p in parts):
        return "Schema/types"
    if ext == ".html":
        return "HTML entry"
    if ext in (".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".php", ".rb", ".cpp", ".c", ".cs", ".mq5"):
        return "Source module"
    if ext in (".yml", ".yaml", ".json", ".toml", ".env.example"):
        return "Config"
    return "Project file"


def scan_repo(root: Path) -> list[Path]:
    collected = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_DIRS and not d.startswith("."))
        for fname in sorted(filenames):
            if fname in IGNORE_FILES or fname.startswith(".env"):
                continue
            if any(fname.endswith(ext) for ext in IGNORE_EXTS):
                continue
            full = Path(dirpath) / fname
            collected.append(full.relative_to(root))
            if len(collected) >= MAX_FILES_IN_MAP:
                return collected
    return collected


def detect_package_manager(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "bun.lockb").exists() or (root / "bun.lock").exists():
        return "bun"
    if (root / "yarn.lock").exists():
        return "yarn"
    return "npm"


def clean_major(raw_ver: str) -> str:
    m = re.search(r"(\d+)", str(raw_ver))
    return m.group(1) if m else str(raw_ver).strip()


def detect_profile_and_commands(root: Path, files: list[Path]) -> tuple[str, list[str], dict[str, str]]:
    if not files:
        return "new-project (greenfield)", ["Empty/New repo"], {
            "tier0": "TBD after scaffold",
            "tier1": "TBD after scaffold",
            "tier2": "TBD after scaffold",
        }

    pinned: list[str] = []
    has_web = False
    has_backend = False
    cmds = {"tier0": "", "tier1": "", "tier2": ""}

    pkg_file = root / "package.json"
    if pkg_file.exists():
        pm = detect_package_manager(root)
        run = f"{pm} run" if pm == "npm" else pm
        try:
            pkg = json.loads(pkg_file.read_text(encoding="utf-8", errors="ignore"))
            deps = {}
            deps.update(pkg.get("dependencies", {}))
            deps.update(pkg.get("devDependencies", {}))
            scripts = pkg.get("scripts", {})

            if set(deps.keys()) & WEB_FRONTEND_DEPS:
                has_web = True
            elif deps:
                has_backend = True

            for dep in KEY_JS_DEPS:
                if dep in deps:
                    pinned.append(f"{dep}@{clean_major(deps[dep])}.x")

            t0_parts = []
            if "typecheck" in scripts:
                t0_parts.append(f"CI=true {run} typecheck")
            elif "typescript" in deps:
                t0_parts.append("npx tsc --noEmit --incremental")
            if "lint" in scripts:
                t0_parts.append(f"CI=true {run} lint")
            if t0_parts:
                cmds["tier0"] = " && ".join(t0_parts)

            if "vitest" in deps:
                cmds["tier1"] = "CI=true npx vitest run <target> --bail 1 --silent"
            elif "jest" in deps:
                cmds["tier1"] = "CI=true npx jest --findRelatedTests <target> --bail --watchAll=false --silent"
            elif "test" in scripts:
                cmds["tier1"] = f"CI=true {run} test"

            if "build" in scripts:
                cmds["tier2"] = f"CI=true {run} build"
        except Exception:
            pinned.append("node")

    pyproject = root / "pyproject.toml"
    req_txt = root / "requirements.txt"
    if pyproject.exists() or req_txt.exists():
        has_backend = True
        pinned.append("python")
        if not cmds["tier0"]:
            cmds["tier0"] = "ruff check <file> || python -m py_compile <file>"
        if not cmds["tier1"]:
            cmds["tier1"] = "pytest -x -q --tb=short -k <target>"
        if not cmds["tier2"]:
            cmds["tier2"] = "pytest -q --tb=short"

    go_mod = root / "go.mod"
    if go_mod.exists():
        has_backend = True
        go_text = go_mod.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^go\s+([0-9.]+)", go_text, re.MULTILINE)
        pinned.append(f"go@{m.group(1)}" if m else "go")
        if not cmds["tier0"]:
            cmds["tier0"] = "go vet ./..."
        if not cmds["tier1"]:
            cmds["tier1"] = "go test ./<pkg> -failfast"
        if not cmds["tier2"]:
            cmds["tier2"] = "go test ./... && go build ./..."

    if (root / "Cargo.toml").exists():
        has_backend = True
        pinned.append("rust")
        if not cmds["tier0"]:
            cmds["tier0"] = "cargo check --quiet"
        if not cmds["tier1"]:
            cmds["tier1"] = "cargo test <target> -- --nocapture"
        if not cmds["tier2"]:
            cmds["tier2"] = "cargo test && cargo build"

    if (root / "composer.json").exists():
        has_backend = True
        pinned.append("php")

    exts = {f.suffix.lower() for f in files}
    if exts & WEB_EXTS:
        has_web = True
    if exts & BACKEND_EXTS:
        has_backend = True

    if has_web and has_backend:
        mode = "fullstack"
    elif has_web:
        mode = "web"
    elif has_backend:
        mode = "non-web"
    else:
        mode = "auto"

    for k in ("tier0", "tier1", "tier2"):
        if not cmds[k]:
            cmds[k] = "Detect on first run"

    return mode, (pinned or ["General project"]), cmds


def write_if_needed(path: Path, content: str, force: bool) -> str:
    existed = path.exists()
    if existed and not force:
        return "SKIPPED (exists)"
    path.write_text(content, encoding="utf-8")
    return "UPDATED" if existed else "CREATED"




def prune_memory(mem_dir: Path) -> list[str]:
    """Compact CURRENT_STATE.md (>30 lines) and deduplicate MISTAKES.md without ever touching TRACK_RECORD.md."""
    notes = []
    state_path = mem_dir / "CURRENT_STATE.md"
    if state_path.exists():
        lines = state_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if len(lines) > 30:
            # Keep header + active task block + last 3 recent change bullets
            kept = []
            recent_bullets = []
            in_recent = False
            for ln in lines:
                if ln.startswith("## Recent Changes"):
                    in_recent = True
                    kept.append(ln)
                    continue
                if ln.startswith("## ") and in_recent:
                    in_recent = False
                    kept.extend(recent_bullets[-3:])
                    kept.append("")
                if in_recent:
                    if ln.strip().startswith("- "):
                        recent_bullets.append(ln)
                else:
                    kept.append(ln)
            if in_recent:
                kept.extend(recent_bullets[-3:])
            state_path.write_text("\n".join(kept[:30]) + "\n", encoding="utf-8")
            notes.append(f"CURRENT_STATE.md pruned ({len(lines)} -> {min(len(kept), 30)} lines)")

    mistakes_path = mem_dir / "MISTAKES.md"
    if mistakes_path.exists():
        lines = mistakes_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        seen = set()
        deduped = []
        removed = 0
        for ln in lines:
            key = ln.strip().lower()
            if ln.strip().startswith("- "):
                if key in seen:
                    removed += 1
                    continue
                seen.add(key)
            deduped.append(ln)
        if removed:
            mistakes_path.write_text("\n".join(deduped) + "\n", encoding="utf-8")
            notes.append(f"MISTAKES.md deduplicated (-{removed} duplicate lines)")
    return notes

def main():
    args = sys.argv[1:]
    force = "--force" in args
    refresh_map = "--refresh-map" in args
    do_prune = "--prune" in args
    positional = [a for a in args if not a.startswith("--")]
    repo_root = Path(positional[0]).resolve() if positional else Path.cwd().resolve()

    mem_dir = repo_root / ".ai-memory"
    mem_dir.mkdir(parents=True, exist_ok=True)

    scanned = scan_repo(repo_root)
    detected_mode, pinned_versions, fast_cmds = detect_profile_and_commands(repo_root, scanned)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    map_lines = [
        "# Codebase Map",
        "",
        f"> Bootstrapped on {now_str} via `scripts/init_memory.py` (0 AI tokens). Read FIRST (Pass 1).",
        "> Format: `path/to/file` - Role | Key exports/symbols",
        "",
        "## Project Profile",
        "",
        f"- **Detected Mode**: `{detected_mode}`",
        f"- **Pinned Major Versions**: {', '.join(pinned_versions)}",
        "",
        "## Cached Fast Commands",
        "",
        f"- **Tier 0 (Static <2s)**: `{fast_cmds['tier0']}`",
        f"- **Tier 1 (Delta Test 2-10s)**: `{fast_cmds['tier1']}`",
        f"- **Tier 2 (Full Pipeline)**: `{fast_cmds['tier2']}`",
        "",
        "## Indexed Files",
        "",
    ]

    if scanned:
        for rel in scanned:
            posix = rel.as_posix()
            role = guess_role(rel)
            syms = extract_symbols(repo_root / rel)
            if syms:
                map_lines.append(f"- `{posix}` - {role} | `{', '.join(syms)}`")
            else:
                map_lines.append(f"- `{posix}` - {role}")
    else:
        map_lines.append("<!-- New project detected. Agent updates rows incrementally on first edit. -->")

    map_content = "\n".join(map_lines) + "\n"

    current_state_content = (
        "# Current State & Session Handoff\n\n"
        "> Rolling snapshot (keep <=30 lines). Always read on cold-start boot and model/agent switches.\n\n"
        "## Active Task State\n\n"
        "- **Status**: `IDLE`\n"
        "- **Detected Engine**: `auto`\n"
        "- **Active Model & Thinking**: `unset`\n"
        "- **Task Tier**: `none`\n"
        "- **Recommended Model & Thinking**: `none`\n"
        "- **Goal**: \n"
        "- **Key Decisions / Constraints**: \n"
        "- **Target Files**: \n"
        "- **Done Criteria**: \n\n"
        "## Recent Changes (Last 3 Only)\n\n"
        f"- [{now_str}] Initialized `.ai-memory/` ({len(scanned)} files indexed, mode: `{detected_mode}`).\n\n"
        "## Next Logical Step\n\n"
        "<!-- Optional 1-line handoff note -->\n"
    )

    rules_content = (
        "# Rules Lock (Hard Invariants)\n\n"
        "> Standing user rules, locked model roster, and codebase invariants. NEVER violate during coding or idea elevation.\n\n"
        "## Locked Model Inventory\n\n"
        "<!-- Populated once via first-run onboarding (screenshot or text) or /models -->\n"
        "- **Environment**: `universal`\n"
        "- **Light Tier**: `unset` *(Thinking: unset)*\n"
        "- **Balanced Tier**: `unset` *(Thinking: unset)*\n"
        "- **Heavy Tier**: `unset` *(Thinking: unset)*\n"
        "- **All Available Models**: `unset`\n\n"
        "## Stack & Conventions\n\n"
        f"- Detected project mode: `{detected_mode}` ({', '.join(pinned_versions)}).\n"
        "- Follow existing folder structure, formatting, and naming conventions in this repo.\n"
        "- Obey installed major dependency versions listed in `CODEBASE_MAP.md`.\n"
        "- Do not add new third-party dependencies without clear justification or user approval.\n\n"
        "## User Rules\n\n"
        "<!-- Add permanent project rules here -->\n"
    )

    mistakes_content = (
        "# Mistakes & Learned Rules\n\n"
        "> Self-learning permanent rules captured from user corrections and resolved regressions.\n"
        "> Keep concise (1 line per rule) and always read on boot so mistakes never repeat.\n\n"
        "<!-- Agent appends learned rules here automatically -->\n"
    )

    track_record_path = mem_dir / "TRACK_RECORD.md"
    if not track_record_path.exists():
        track_content = (
            "# Track Record (Strict Append-Only History)\n\n"
            "> PERMANENT APPEND-ONLY LOG.\n"
            "> HARD RULE: NEVER delete, edit, or truncate previous entries. Always append new entries at the BOTTOM.\n"
            "> Do NOT load this entire file on routine prompts — read `CURRENT_STATE.md` instead.\n"
            "> Format: `- [YYYY-MM-DD HH:MM] | files | what changed | why | Verify: STATUS`\n\n"
            f"- [{now_str}] | `.ai-memory/*` | Initialized living memory ({len(scanned)} files, mode: {detected_mode}) | Repo bootstrap | Verify: PASS\n"
        )
        track_record_path.write_text(track_content, encoding="utf-8")
        s_track = "CREATED"
    else:
        with track_record_path.open("a", encoding="utf-8") as fh:
            if refresh_map or force:
                fh.write(f"- [{now_str}] | `.ai-memory/CODEBASE_MAP.md` | Refreshed repo map ({len(scanned)} files, mode: {detected_mode}) | Map sync | Verify: PASS\n")
                s_track = "APPENDED (preserved history)"
            else:
                s_track = "PRESERVED (append-only)"

    s_map = write_if_needed(mem_dir / "CODEBASE_MAP.md", map_content, force or refresh_map)
    s_state = write_if_needed(mem_dir / "CURRENT_STATE.md", current_state_content, force)
    s_rules = write_if_needed(mem_dir / "RULES_LOCK.md", rules_content, force)
    s_mistakes = write_if_needed(mem_dir / "MISTAKES.md", mistakes_content, force)

    print(f"[skill-agent] Memory ready at: {mem_dir}")
    print(f"  - Detected Mode    : {detected_mode} ({', '.join(pinned_versions)})")
    print(f"  - CODEBASE_MAP.md  : {s_map} ({len(scanned)} files indexed)")
    print(f"  - CURRENT_STATE.md : {s_state}")
    print(f"  - RULES_LOCK.md    : {s_rules}")
    print(f"  - MISTAKES.md      : {s_mistakes}")
    print(f"  - TRACK_RECORD.md  : {s_track}")
    if do_prune:
        prune_notes = prune_memory(mem_dir)
        for note in (prune_notes or ["Memory already compact (TRACK_RECORD.md untouched)"]):
            print(f"  - Prune            : {note}")


if __name__ == "__main__":
    main()
