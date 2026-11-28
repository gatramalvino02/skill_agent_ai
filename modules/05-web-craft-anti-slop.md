# Module 05: Web Craft & Anti-AI-Slop Engine (Target: <=10% AI Feel)

Build modern, living, human-crafted websites and UIs with restrained taste, real visual rhythm, crisp typography, and authentic copy — never generic or stiff AI output.

Respect `anti_ai_slop` settings in `config.yaml` (`full` | `web-ui` | `copy` | `code` | `off`).

---

## Part A: Visual & Aesthetic Hard Bans

- **Zero Neon / Gimmick Clichés**: No neon glow borders, no glowing radial orbs/blobs behind cards, no purple/indigo-to-cyan gradients, no cyberpunk dark-mode clichés, no animated rainbow/shimmer gradient text.
- **Zero Glassmorphism Spam**: No heavy `backdrop-blur-2xl/3xl` translucent cards stacked everywhere, no muddy oversized drop shadows.
- **Zero Cookie-Cutter AI SaaS Layout**: Never build the default cliché template (`centered pill badge` + `centered gradient H1` + `2 buttons` + `3 fake stat numbers` + `3 identical icon cards` + `fake testimonial carousel`).
- **Zero Fake Stat Strips**: Never pad heroes with meaningless numbers (`100% Preview`, `99.9% Uptime`, `24/7 AI Power`, `10x Faster`). Show numbers ONLY when real and specific.
- **Zero Emoji Icons**: Never prefix navbar items, headings, or feature titles with emojis (`🚀`, `✨`, `⚡`, `🔥`).
- **Zero Flat Default Typography**: Never leave unstyled system `Inter` / `Roboto` / `Arial` for both display and body with weak size contrast.
- **Zero Cramped Above-the-Fold**: Give the Hero real vertical breathing room (`min-h-[82vh]` or generous vertical rhythm `py-24`–`py-36`) so Section 01 never crowds the initial viewport.

---

## Part B: Mandatory 15-Line Design Contract (Lock BEFORE Writing CSS/HTML/JSX)

Before writing UI code, commit to ONE cohesive human design direction:

1. **Aesthetic Lane** (pick ONE and stay consistent):
   - `editorial-craft`: Warm stone/off-white canvas (`#F7F5F0` / `#FAF9F6`), deep charcoal ink (`#171717`), crisp editorial serif or grotesk display + clean sans body, hairline `1px` borders, generous whitespace.
   - `warm-minimal`: Soft layered neutral surfaces (`#F5F4F0` + `#FFFFFF`), calm tactile controls, quiet precision, one restrained earth/slate/forest accent.
   - `swiss-grid`: Structural grid lines, bold asymmetric grotesk typography, tabular alignment, stark functional clarity, one disciplined accent.
   - `high-contrast-utility`: Refined matte charcoal (`#0F1012` / `#141518`) OR crisp light tool canvas (`#FAFAFA`), `1px` hairline borders (`rgba(..., 0.08–0.12)`), zero neon glow, sharp typographic hierarchy.
2. **Typography Pairing**:
   - Pair ONE expressive display font (`Instrument Serif`, `Newsreader`, `Plus Jakarta Sans`, `Space Grotesk`, `Bricolage Grotesque`, `Geist`, `DM Sans`) with ONE clean body font + monospace (`JetBrains Mono` / `IBM Plex Mono`) strictly for code, metadata, or tabular numbers.
   - Optical hierarchy: tight display tracking (`-0.025em` to `-0.04em`), crisp line-height (`1.05`–`1.15` headlines, `1.6` body), comfortable reading measure (`52–68ch`).
3. **Color Discipline (60-30-10)**:
   - 1 primary canvas (avoid flat pure `#000000` or sterile `#FFFFFF` everywhere without tonal layers).
   - 1 secondary surface (3–6% tonal shift) + 1 primary ink + 1 muted ink (WCAG AA contrast).
   - **At most 1 purposeful accent color** used sparingly for primary CTAs and active states.
4. **Living Web Rhythm & Signature Interaction**:
   - Vary layout composition every section (e.g., asymmetric 7/5 hero -> clean editorial 2-column statement -> structured case-study rows or asymmetric bento -> focused CTA). Never repeat the same 3-column card grid twice.
   - Make the page feel **alive, not stiff**: tactile `hover`/`active`/`focus-visible` states with subtle weight, crisp `150–200ms ease-out` transitions (color, border, 3–4px micro-shift, staggered entrance reveals), real loading/empty/error states — zero bouncy/floating gimmick loops.
   - Verify Desktop (`1440px`) and Mobile (`375px`) with zero horizontal overflow, >=44px touch targets, semantic landmarks (`<main>`, `<nav>`), keyboard `focus-visible`, `alt`/`aria-label`, and `prefers-reduced-motion` respect.

---

## Part C: Copywriting & Naming — Zero AI Rhetoric (ID & EN)

- **Zero Placeholder Copy**: Never use `Lorem Ipsum`, `John Doe`, `Jane Doe`, or `Acme Corp`. Write realistic, context-authentic copy from the very first draft.
- **Banned AI Formula Patterns**:
  - Never use `"Banyak X hanya fokus pada A — saya melakukan B"` or `"It's not just X — it's Y"`.
  - Limit em-dashes (`—`) to max 1 per entire page (or zero).
  - Avoid repetitive 3-adjective lists (`"cepat, andal, dan skalabel"` / `"fast, seamless, and intuitive"`).
- **Banned Fake AI Startup Names**: Never invent cliché compounds like `ChurnGuard`, `RetinaScan`, `PulseCohort`, `FlowSync`, `ElevatAI`, `NexGen`, `AuraDocs`, `NovaMind`. Use plain, honest, descriptive titles instead.
- **Banned Cliché Words**:
  - **Indonesian**: `di era digital yang serba cepat ini`, `solusi komprehensif`, `meningkatkan efisiensi secara signifikan`, `tak hanya itu`, `lebih dari sekadar`, `mengoptimalkan potensi`, `tanpa batas`, `revolusioner`, `hadir untuk menjawab kebutuhan`, `pengalaman yang tak terlupakan`, `inovatif dan terdepan`, `ekosistem cerdas`.
  - **English**: `delve`, `tapestry`, `embark`, `realm`, `testament`, `game-changer`, `revolutionize`, `unleash`, `unlock the power of`, `elevate your`, `seamless`, `cutting-edge`, `robust`, `harness`, `leverage`, `foster`, `navigate the landscape`, `supercharge`.
- **Direct Voice**: Prefer concrete specifics (*"Push ke GitHub, deploy selesai 12 detik"*) and honest UI labels (`Lihat Proyek`, `Hubungi via Email`).

---

## Part D: Mandatory 10-Point Self-Audit (Run Before Live Verification)

If ANY item fails, fix it immediately before running `modules/07-web-live-runner.md`:

1. [ ] Zero neon glows, zero purple/cyan AI gradients, zero decorative floating blobs.
2. [ ] Zero excessive glassmorphism or heavy muddy drop shadows.
3. [ ] Hero has generous vertical breathing room (Section 01 does not crowd above-the-fold).
4. [ ] Expressive display font + clean body font + clear typographic contrast.
5. [ ] Color palette stays within 1 canvas + 1 surface + ink + max 1 restrained accent.
6. [ ] Section layouts vary visibly (no repeated 3-card icon grids) with tactile micro-interactions.
7. [ ] Zero fake/padded stat numbers (`100% Preview`, `99.9%`, `10x`).
8. [ ] Zero fake AI startup names or placeholder copy (`Lorem Ipsum`, `John Doe`, `NexGen`).
9. [ ] Zero `"Bukan X — tapi Y"` AI rhetoric or banned cliché vocabulary.
10. [ ] Zero placeholder stubs (`TODO`, dead links, unstyled states) and clean mobile (`375px`) layout.
