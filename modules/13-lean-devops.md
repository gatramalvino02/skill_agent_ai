# Module 13: Lean DevOps, Containers & Automation

Loaded for Dockerfiles, Docker Compose, GitHub Actions/CI, deployment configs, and shell/PowerShell automation scripts.

## 1. Lean & Reproducible Containers

- Use multi-stage builds and minimal pinned base images (avoid unpinned `:latest` tags).
- Order layers for maximum build cache hit rate (copy manifests -> install deps -> copy source).
- Run containers as a non-root user and pair with a clean `.dockerignore` excluding `.git`, `node_modules`, `.env`, and caches.

## 2. Fast, Non-Interactive CI & Scripts

- Every CI workflow and automation script must be idempotent, fail-fast (`set -euo pipefail` in Bash; `$ErrorActionPreference = "Stop"` in PowerShell), and 100% non-interactive (`CI=true`, `--yes`).
- Cache dependencies in CI pipelines and separate fast lint/unit jobs from slower build/deploy stages.
- Never echo secrets in logs; mask sensitive env vars and document required variables in `.env.example`.
