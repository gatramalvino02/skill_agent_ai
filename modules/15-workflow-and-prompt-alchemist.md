# Module 15: Workflow Automation, Tool/MCP Design & Prompt Alchemist

Loaded when automating repetitive personal/work tasks, designing AI/MCP tool pipelines, or crafting high-precision prompts for any external model.

## 1. Workflow Automation First (Eliminate Manual Friction)

1. **Map the Bottleneck (<=5 lines)**: `Trigger -> Input -> Transform -> Output -> Failure Recovery`.
2. **Pick the Simplest Reliable Engine**:
   - Local file/data/batch tasks -> self-contained Python or shell script (standard library first).
   - Scheduled / API / webhook / AI flows -> idempotent script, cron/Task Scheduler, GitHub Actions, or lightweight workflow (n8n/Make/MCP server).
3. **Production-Safe Defaults**: Include `--dry-run` for batch mutations, deterministic exit codes, retry with backoff on network calls, structured logs, and env-based secrets.

## 2. High-Signal Prompt & Agent Skill Engineering

When crafting prompts or agent instructions for another AI tool:
- Strip generic roleplay fluff; pack dense structure: `Objective | Hard Constraints | Input Format | Exact Output Schema | Quality Bar`.
- Include concrete edge-case guards and anti-patterns so even lightweight models cannot drift into generic output.
- Keep token footprint tight so it works sharply across both small/local and frontier models.
