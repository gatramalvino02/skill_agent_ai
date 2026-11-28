# Selective per-agent installer for Skill Agent (Windows PowerShell)
# Usage: .\install.ps1 -Target "." -Agent "antigravity"

param(
    [string]$Target = ".",
    [Parameter(Mandatory=$true)]
    [ValidateSet("antigravity", "claude", "opencode", "codex", "gemini", "cursor", "cursor-legacy", "windsurf", "cline", "roo", "copilot", "all")]
    [string]$Agent,
    [string]$CleanOld = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SetupScript = Join-Path $ScriptDir "scripts\setup_skill.py"

$ArgsList = @($SetupScript, $Target, "--agent", $Agent, "--force", "--sync-global")
if ($CleanOld -ne "") {
    $ArgsList += @("--clean-old", $CleanOld)
}

python @ArgsList
