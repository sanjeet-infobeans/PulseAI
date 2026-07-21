---
name: infobeans-brand
description: InfoBeans brand system for all PulseAI UI, copy, and visual output. Use whenever building or styling frontend components, writing UI microcopy, choosing colors/typography/icons, or reviewing anything user-facing for brand consistency.
---

# InfoBeans Brand OS — PulseAI

Authoritative brand reference for PulseAI. This governs color, typography, icon, and voice
**rules**. The layout mockup at `PulseAI/code.html` governs composition and component structure —
but where the two conflict, **this brand system wins** (confirmed: use `#EA1B3D`, not the mockup's
`#ba002a`; never put icons inside filled circles).

## Color palette — 10 colors only, no exceptions

| Token | Hex | Use |
|-------|-----|-----|
| Brand Red | `#EA1B3D` | Logo, accent, emphasize **one** key word/element per view. **Never body text.** |
| Desire Red | `#EB4C5E` | Icons, current-state highlight, accent |
| Dark Red | `#AA142D` | Dark backgrounds, icons |
| Deep Red | `#7C2235` | Dark backgrounds, icons |
| Charcoal Gray | `#373742` | Primary text, graphic elements, dark backgrounds |
| Medium Gray | `#676775` | Secondary text, mid-tone backgrounds |
| Light Gray | `#E6E6ED` | Backgrounds, borders, text on dark surfaces |
| Light Cream | `#FFF9ED` | Dominant page/section background |
| Peach | `#FFD0D8` | Accent + drop shadows only — **never as a fill** |
| White | `#FFFFFF` | Backgrounds, text on dark surfaces |

Hard rules: red is never body text; default background is Cream or White; default text is Charcoal;
**one red emphasis per screen/section maximum**. (Neutral panel tint `#f9f9ff` from the mockup is
permitted as a subtle surface-container only.)

## Typography

- **Lexend only.** Two weights only: **Light (300)** and **Normal (400)**. No other weights.
- Lexend has no italic — if italics are unavoidable, use Verdana.
- **Headings: sentence case.** Not Title Case, not ALL CAPS.
- **Eyebrows: ALL CAPS, 12px, Light, letter-spaced.** The one ALL-CAPS exception.

| Style | Size | Weight |
|-------|------|--------|
| Title / display | 48–36px | Light |
| H1 | 32px | Light |
| H2 | 28px | Normal |
| H3 | 24px | Normal |
| H4 | 20px | Normal |
| H5 | 16px | Normal |
| Eyebrow | 12px | Light — ALL CAPS |
| Body Large | 16px | Light |
| Body Medium | 14px | Light |
| Small | 9px | Light |

## Icons

- **Phosphor Icons** — `@phosphor-icons/react` in the app (mockup CDN is `@phosphor-icons/web`).
- **Thin or regular stroke only.** Never fill, duotone, heavy/bold stroke, cropped icons, or
  **icons inside filled circles**. Keep one consistent icon style per screen.

## Radius & spacing (PulseAI Tailwind tokens, from mockup, brand-corrected)

- Radius (near-square): `DEFAULT 0.125rem`, `lg 0.25rem`, `xl 0.5rem`, `full 0.75rem`.
- Spacing: `margin-desktop 48px`, `lg 40px`, `gutter 24px`, `md 24px`, `sm 16px`.
- Signature card: white bg, `1px #E6E6ED` border, soft shadow `0 4px 20px rgba(55,55,66,0.03)`;
  4px `#EA1B3D` left/top accent border to mark hierarchy.

## Voice (all UI copy)

Positioning: *"A global team of makers that help companies unstick their most important digital
initiatives."* Tagline: *"Creating WOW!"*

- **Outcome-first** — lead with the business result, then the capability.
- **Direct** — short sentences, active verbs, no hedging.
- **Parallel structure** — "Design. Build. Manage." not "we design, build, and manage things."
- **Confident, not boastful** — prove with specifics, not superlatives.
- **AI-forward** — "AI-powered", "agentic", "context-trained" are natural vocabulary.

Never: hyperbole without proof ("world-class", "best-in-class", "revolutionary"), passive voice in
headlines, jargon the audience wouldn't use, decorative filler ("In today's fast-paced world…").
**Writing mechanics:** no em dashes, no double hyphens; don't preface answers with "honest"; vary
sentence rhythm; don't stack three short declaratives.

## Audience model — calibrate every surface to one

| Persona | Cares about | Tone |
|---------|-------------|------|
| Executive | Risk, cost, competitive position | Strategic, concise, outcome-first |
| Director | Predictability, throughput, governance | Process, metrics, reliability |
| Engineer | Speed, trust, control | Direct, specific, no fluff |

PulseAI's primary dashboard audience is **Executive/Director** — lead with confidence, risk, and
delivery outcomes.
