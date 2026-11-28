#!/usr/bin/env python3
"""
Selective per-agent installer for Skill Agent (`skill-agent`).
Installs ONLY the chosen AI agent's adapter + modular skill bundle so your
project folder stays clean without unused config files.

Usage:
    python scripts/setup_skill.py [target_project_dir] --agent <name> [--force] [--sync-global] [--clean-old <slug>]

Supported --agent values:
    antigravity | claude | opencode | codex | gemini | cursor | cursor-legacy | windsurf | cline | roo | copilot | all
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_NAME = "skill-agent"
SKILL_ROOT = Path(__file__).resolve().parent.parent

SKILL_COPY_ITEMS = [
    "SKILL.md",
    "config.yaml",
    "modules",
    "templates",
    "scripts",
    "docs",
]

AGENT_ADAPTERS = {
    "antigravity": ("adapters/antigravity-rules.md", f".agent/rules/{SKILL_NAME}.md", f".agents/skills/{SKILL_NAME}"),
    "claude": ("adapters/CLAUDE.md", "CLAUDE.md", f".claude/skills/{SKILL_NAME}"),
    "opencode": ("adapters/AGENTS.md", "AGENTS.md", f".agents/skills/{SKILL_NAME}"),
    "codex": ("adapters/AGENTS.md", "AGENTS.md", f".agents/skills/{SKILL_NAME}"),
    "gemini": ("adapters/GEMINI.md", "GEMINI.md", f".agents/skills/{SKILL_NAME}"),
    "cursor": ("adapters/cursor-skill.mdc", f".cursor/rules/{SKILL_NAME}.mdc", f".agents/skills/{SKILL_NAME}"),
    "cursor-legacy": ("adapters/.cursorrules", ".cursorrules", f".agents/skills/{SKILL_NAME}"),
    "windsurf": ("adapters/.windsurfrules", ".windsurfrules", f".agents/skills/{SKILL_NAME}"),
    "cline": ("adapters/.clinerules", ".clinerules", f".agents/skills/{SKILL_NAME}"),
    "roo": ("adapters/.roorules", ".roorules", f".agents/skills/{SKILL_NAME}"),
    "copilot": ("adapters/copilot-instructions.md", ".github/copilot-instructions.md", f".agents/skills/{SKILL_NAME}"),
}


def copy_skill_bundle(target_skill_dir: Path, force: bool) -> str:
    if target_skill_dir.exists():
        if not force:
            return "SKIPPED (exists; use --force to overwrite)"
        shutil.rmtree(target_skill_dir)
    target_skill_dir.mkdir(parents=True, exist_ok=True)
    for item in SKILL_COPY_ITEMS:
        src = SKILL_ROOT / item
        dst = target_skill_dir / item
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        elif src.is_file():
            shutil.copy2(src, dst)
    return "INSTALLED"


def install_adapter(target_project: Path, src_rel: str, dst_rel: str, force: bool) -> str:
    src = SKILL_ROOT / src_rel
    dst = target_project / dst_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not force:
        return "SKIPPED (exists)"
    shutil.copy2(src, dst)
    return "INSTALLED"


def clean_old_skill(target_project: Path, old_slug: str, include_global: bool):
    home = Path.home()
    candidates = [
        target_project / ".agents" / "skills" / old_slug,
        target_project / ".claude" / "skills" / old_slug,
        target_project / ".agent" / "rules" / f"{old_slug}.md",
        target_project / ".cursor" / "rules" / f"{old_slug}.mdc",
    ]
    if include_global:
        candidates.extend([
            home / ".agents" / "skills" / old_slug,
            home / ".claude" / "skills" / old_slug,
            home / ".gemini" / "antigravity" / "skills" / old_slug,
        ])

    for path in candidates:
        if path.is_dir():
            shutil.rmtree(path)
            print(f"  - Cleaned old dir  ({path})")
        elif path.is_file():
            path.unlink()
            print(f"  - Cleaned old file ({path})")


def sync_global_dirs(selected_agents: list[str], home_override: Path | None = None):
    home = home_override if home_override else Path.home()
    targets: list[Path] = []
    shared_agents = ("antigravity", "opencode", "codex", "gemini", "cursor", "cursor-legacy", "windsurf", "cline", "roo", "copilot")
    if any(a in shared_agents for a in selected_agents):
        targets.append(home / ".agents" / "skills" / SKILL_NAME)
    if "antigravity" in selected_agents:
        ag_parent = home / ".gemini" / "antigravity"
        if ag_parent.exists():
            targets.append(ag_parent / "skills" / SKILL_NAME)
    if "claude" in selected_agents:
        targets.append(home / ".claude" / "skills" / SKILL_NAME)

    seen = set()
    for tdir in targets:
        if tdir in seen:
            continue
        seen.add(tdir)
        status = copy_skill_bundle(tdir, force=True)
        print(f"  - Global sync ({tdir}): {status}")


def main():
    parser = argparse.ArgumentParser(
        description="Install Skill Agent (`skill-agent`) for a specific AI agent (clean per-agent setup)."
    )
    parser.add_argument("target", nargs="?", default=".", help="Target project directory (default: current dir)")
    parser.add_argument(
        "--agent",
        required=True,
        choices=list(AGENT_ADAPTERS.keys()) + ["all"],
        help="Target AI coding agent (pick one: antigravity, claude, opencode, codex, gemini, cursor, windsurf, cline, roo, copilot; or 'all')",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing adapter and skill files")
    parser.add_argument("--sync-global", action="store_true", help="Sync global user skill directory for the chosen agent")
    parser.add_argument("--clean-old", default="", help="Optional old skill folder/rule slug to remove during upgrade")
    parser.add_argument("--no-memory", action="store_true", help="Skip running init_memory.py")
    args = parser.parse_args()

    target_project = Path(args.target).resolve()
    target_project.mkdir(parents=True, exist_ok=True)

    selected = list(AGENT_ADAPTERS.keys()) if args.agent == "all" else [args.agent]
    installed_skill_dirs = set()

    print(f"[{SKILL_NAME}] Installing [{args.agent}] into: {target_project}")
    if args.clean_old:
        clean_old_skill(target_project, args.clean_old.strip(), include_global=args.sync_global)

    for agent_key in selected:
        src_adapter, dst_adapter, skill_rel = AGENT_ADAPTERS[agent_key]
        if skill_rel not in installed_skill_dirs:
            status_skill = copy_skill_bundle(target_project / skill_rel, args.force)
            print(f"  - Skill bundle ({skill_rel}): {status_skill}")
            installed_skill_dirs.add(skill_rel)
        status_adapter = install_adapter(target_project, src_adapter, dst_adapter, args.force)
        print(f"  - Adapter [{agent_key}] ({dst_adapter}): {status_adapter}")

    if args.sync_global:
        sync_global_dirs(selected)

    sys.stdout.flush()
    if not args.no_memory:
        init_script = SKILL_ROOT / "scripts" / "init_memory.py"
        subprocess.run([sys.executable, str(init_script), str(target_project)], check=True)

    print(f"\n[{SKILL_NAME}] Done! Open a new chat tab (+) in your {args.agent} agent to activate `skill-agent`.")


if __name__ == "__main__":
    main()
