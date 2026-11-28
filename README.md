# Skill Agent (`skill-agent`)

Sistem skill modular lintas-agent yang padat, super irit token, dan **dipasang selektif satu per satu sesuai AI agent yang kamu pakai** agar folder proyek tetap bersih tanpa file config yang tidak terpakai.

Mendukung **Antigravity, Claude Code, OpenCode, Codex CLI, Gemini CLI, Cursor, Windsurf, Cline, Roo Code, GitHub Copilot**, serta model lokal/web chat lewat [`adapters/UNIVERSAL_PROMPT.md`](adapters/UNIVERSAL_PROMPT.md).

> Panduan pemasangan dan penggunaan singkat: [`docs/PANDUAN_PENGGUNAAN.md`](docs/PANDUAN_PENGGUNAAN.md).

---

## Cara Pasang (Pilih Satu per Satu Sesuai Agent)

Pasang hanya agent yang benar-benar kamu gunakan di proyek tersebut:

**Windows (PowerShell):**

```powershell
# Contoh untuk Antigravity:
python scripts/setup_skill.py . --agent antigravity --force --sync-global

# Contoh untuk OpenCode / Claude Code / Cursor:
python scripts/setup_skill.py . --agent opencode --force --sync-global
python scripts/setup_skill.py . --agent claude --force --sync-global
python scripts/setup_skill.py . --agent cursor --force --sync-global
```

**Linux / macOS:**

```bash
./install.sh . antigravity
```

**Pilihan `--agent` yang tersedia:**
`antigravity` | `claude` | `opencode` | `codex` | `gemini` | `cursor` | `cursor-legacy` | `windsurf` | `cline` | `roo` | `copilot` *(atau `all` jika memang ingin pasang semuanya sekaligus)*.

**Pakai Web Chat (ChatGPT / Claude Web / Gemini Web / Local LLM)?**
Salin langsung isi [`adapters/UNIVERSAL_PROMPT.md`](adapters/UNIVERSAL_PROMPT.md) ke Custom Instructions atau System Prompt.

---

## Alur Kerja Tunggal (Anti-Bingung)

1. **Onboarding Daftar Model & Thinking (Sekali di Awal)** — Saat pertama kali dipanggil di sebuah engine, agent meminta screenshot atau teks daftar model AI + mode thinking (`Off` / `Low` / `Medium` / `High`) yang tersedia di aplikasi tersebut, lalu menguncinya permanen di `.ai-memory/RULES_LOCK.md`.
2. **Brainstorming Ultra-Irit (Otomatis Saat Diskusi)** — Saat berdiskusi ide atau membandingkan opsi, agent otomatis masuk mode *read-only* (tanpa baca repo sembarangan, tanpa ubah kode) dengan format *telegraphic* `<=15 baris` untuk menghemat token 70–85%.
3. **Pre-Flight Check -> Eksekusi Otonom (`gas`)** — Baik saat langsung memberi tugas coding maupun selesai brainstorming lalu bilang *"jalanin yang ini"*, agent berhenti sejenak untuk menampilkan rencana 1 baris + saran **Model** dan **Thinking Effort** terbaik. Setelah kamu pilih model dan membalas **`gas`** / **`lanjutkan`**, agent bekerja otonom sampai tuntas (*implement -> test -> self-audit -> fix -> polish*) tanpa berhenti menanyakan hal-hal sepele.

---

## Fitur Inti

1. **Instalasi Bersih per Agent (`scripts/setup_skill.py`)** — Hanya menyalin 1 file adapter + folder skill untuk agent yang dipilih sehingga root proyek tetap rapi.
2. **Kernel Padat & Progressive Disclosure (`SKILL.md`)** — Aturan statis di bagian atas (ramah *prompt caching*), modul spesialis dimuat hanya saat dibutuhkan.
3. **Ekonomi Token + Pertahanan Context-Rot (`modules/01`)** — Brainstorming *zero-bloat*, *2-Pass Skeleton Scan* (`CODEBASE_MAP.md` 0 token AI), *slice read* >200 baris, *parallel tool batching*, edit *diff-first*, isolasi ketat Web vs Pure Coding, serta **Consent-Gated Ignore Shield** (`node_modules/`, `.git/`, `*.lock`, `.env*` wajib izin eksplisit).
4. **Adaptive Cognitive Boost + Sub-Agent Orchestration (`modules/08`)** — Otomatis mendongkrak model ringan/lokal atau thinking `Off`/`Low` dengan *Forced Structured Reasoning*, memangkas *overthinking* di model frontier (`High`), dan mengatur delegasi *sub-agent* (paket `<=150 token`) jika host mendukungnya.
5. **Fast Pipeline & Self-Healing (`modules/02`)** — Piramida verifikasi 3 tingkat (*Tier 0 static <2s* -> *Tier 1 fail-fast delta test* -> *Tier 2 full pipeline*), output *silent-pass / loud-fail*, `CI=true` anti-hang + *timeout watchdog*, Anti-Cheat Test Gate, dan *3-Strike Root-Cause Circuit Breaker*.
6. **Living Memory + Auto-Prune (`modules/03` + `scripts/init_memory.py`)** — 5 file lokal di `.ai-memory/`: `CURRENT_STATE.md` (<=30 baris), `RULES_LOCK.md`, `CODEBASE_MAP.md`, `MISTAKES.md`, dan `TRACK_RECORD.md` (**strict append-only**, histori lama tidak pernah dihapus) + flag `--prune`.
7. **19 Modul Spesialis On-Demand (`modules/00` – `18` + `99`)** — Web Craft Anti-AI-Slop (`<=10%` AI feel + *10-Point Audit*), Web Live Runner, Pure Coding (non-web), Forensic Debugger, System Architect, Security Hardener, Human Copywriter, Lean DevOps, Rapid Researcher, Workflow & Prompt Alchemist, Data & Decision Analyst, Rapid Synthesis & Learning, hingga Universal Quality Gate (audit mandiri 6 poin).

---

## Pintasan Opsional

| Command | Fungsi |
| :--- | :--- |
| `/fast` | Lewati jeda pre-flight dan langsung eksekusi diff cepat + Tier 0 static check. |
| `/deep` | Paksa spesifikasi 5 slot + Contract-First + `10-system-architect.md` sebelum ngoding. |
| `/scan` | Segarkan `CODEBASE_MAP.md` dengan 2-Pass Skeleton Scan (0 token AI). |
| `/test` | Jalankan Tier 1 Delta Test (*fail-fast*); pakai `/test full` untuk Tier 2. |
| `/audit` | Jalankan `11-security-hardener.md` + `18-universal-quality-gate.md` + hygiene sweep. |
| `/models` | Daftarkan atau perbarui daftar model AI + mode thinking yang sedang dipakai. |
| `/handoff` | Simpan ringkasan sesi ke `CURRENT_STATE.md` dan `TRACK_RECORD.md` untuk pindah agent/model. |
