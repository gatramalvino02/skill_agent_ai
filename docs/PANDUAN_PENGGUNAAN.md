# Panduan Penggunaan Skill Agent (`skill-agent`)

Pasang secara selektif **satu per satu sesuai AI agent yang kamu gunakan** agar folder proyek tetap bersih dan tidak penuh file konfigurasi yang tidak terpakai.

---

## 1. Pemasangan di Proyek (Pilih Satu Agent)

Buka terminal di root folder proyek kamu, lalu jalankan perintah sesuai AI agent yang kamu pakai:

**Windows (PowerShell):**

```powershell
# Antigravity
python path/ke/skill-agent/scripts/setup_skill.py . --agent antigravity --force --sync-global

# OpenCode atau Codex
python path/ke/skill-agent/scripts/setup_skill.py . --agent opencode --force --sync-global

# Claude Code
python path/ke/skill-agent/scripts/setup_skill.py . --agent claude --force --sync-global

# Cursor
python path/ke/skill-agent/scripts/setup_skill.py . --agent cursor --force --sync-global
```

**Linux / macOS:**

```bash
./install.sh . antigravity
```

> **Daftar lengkap `--agent`**: `antigravity`, `claude`, `opencode`, `codex`, `gemini`, `cursor`, `cursor-legacy`, `windsurf`, `cline`, `roo`, `copilot` *(atau `all` hanya jika memang ingin pasang semuanya sekaligus)*.
>
> **Upgrade dari nama skill lama?** Tambahkan `--clean-old <nama_folder_lama>`.

Setelah selesai, **buka Tab Chat Baru (`+`)** di AI agent tersebut agar `skill-agent` aktif.

**Untuk Web Chat (ChatGPT, Claude Web, Gemini Web, atau LLM lokal tanpa folder proyek):**
Cukup copy-paste isi `adapters/UNIVERSAL_PROMPT.md` ke Custom Instructions / System Prompt.

---

## 2. File yang Terpasang per Pilihan Agent (Bersih & Rapi)

| Pilihan `--agent` | File Adapter yang Dipasang | Folder Skill |
| :--- | :--- | :--- |
| `antigravity` | `.agent/rules/skill-agent.md` | `.agents/skills/skill-agent/` |
| `claude` | `CLAUDE.md` | `.claude/skills/skill-agent/` |
| `opencode` / `codex` | `AGENTS.md` | `.agents/skills/skill-agent/` |
| `gemini` | `GEMINI.md` | `.agents/skills/skill-agent/` |
| `cursor` | `.cursor/rules/skill-agent.mdc` | `.agents/skills/skill-agent/` |
| `cursor-legacy` | `.cursorrules` | `.agents/skills/skill-agent/` |
| `windsurf` | `.windsurfrules` | `.agents/skills/skill-agent/` |
| `cline` | `.clinerules` | `.agents/skills/skill-agent/` |
| `roo` | `.roorules` | `.agents/skills/skill-agent/` |
| `copilot` | `.github/copilot-instructions.md` | `.agents/skills/skill-agent/` |

---

## 3. Cara Pakai Sehari-hari

1. **Setup Daftar Model (Cukup Sekali)**: Saat pertama kali `skill-agent` dipanggil, kirimkan **screenshot** atau **teks daftar model + opsi thinking** (`Off` / `Low` / `Medium` / `High`) yang tersedia di aplikasi AI kamu. Daftar ini dikunci di `.ai-memory/RULES_LOCK.md` agar rekomendasi selalu akurat. *(Perbarui kapan saja dengan `/models`.)*
2. **Langsung Coding**: Ketik prompt tugasmu seperti biasa -> agent berhenti sejenak di **Pre-Flight Check** (saran Model + Thinking Effort) -> pindah model bila perlu -> balas **`gas`** atau **`lanjutkan`** -> agent langsung mengeksekusi sampai selesai, teruji, dan lolos audit mandiri.
3. **Brainstorming Dulu**: Ngobrol atau diskusi ide seperti biasa -> agent otomatis menahan diri (*read-only*, hemat token 70–85%). Begitu ide sudah klop dan kamu bilang *"oke jalanin yang ini"*, agent otomatis menampilkan **Pre-Flight Check** dulu sebelum mulai ngoding saat kamu balas **`gas`**.
4. **Super Cepat Tanpa Jeda**: Awali prompt dengan **`/fast`** atau tambahkan **`skip check`**.
5. **Pindah Agent / Model di Tengah Jalan**: Ketik **`/handoff`**, buka agent lain, lalu langsung lanjut — konteks otomatis terbaca dari `.ai-memory/CURRENT_STATE.md`.

---

## 4. Perintah Pemeliharaan Cepat

- **Segarkan peta file setelah banyak edit manual:**
  ```bash
  python .agents/skills/skill-agent/scripts/init_memory.py . --refresh-map
  ```
- **Rapikan `CURRENT_STATE.md` & deduplikasi `MISTAKES.md` (tanpa pernah menyentuh `TRACK_RECORD.md`):**
  ```bash
  python .agents/skills/skill-agent/scripts/init_memory.py . --prune
  ```
