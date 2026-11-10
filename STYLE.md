# Nielsen & Brown: brand and copy style

How the site looks and sounds since the November 2026 rebuild. The previous
rules (no contractions, no possessives, no prices on the page) are retired; the
old version of this file is in git history if you need it.

## Checking

```
python3 scripts/check-style.py           # every page except the legal ones
python3 scripts/check-style.py --all     # every page
```

Exits 1 if anything is found, so it can gate a build. Flag what it finds rather
than silently fixing: some matches are deliberate. Deliberate exceptions go in
`scripts/style-ignore.txt`, one substring per line, with a comment saying why.
How the pages are built (shared CSS, script, head, nav, footer) is in
`scripts/site/README.md`.

---

## Who we're writing for

Decision makers at UK businesses with **10 to 300 people**. Often not the MD:
the Operations, Technical, Commercial or Marketing Director who has been handed
"sort out AI". They're busy, practical and sceptical of consultancy talk.

## What we're saying

We work out where AI fits, then we implement it and make it stick. Most firms
either advise or build; we do both, with one team from first plan to everyday
use. Everything is fixed scope and fixed price, and the prices are published.

The free AI Readiness Score is a hook, not the business. Point to it as the
low-commitment option ("Not ready to talk?"), never as the main offer.

## Tone of voice

| Do | Don't |
|---|---|
| Plain, short, direct. Say the thing. | Consultancy speak ("leverage", "unlock value", "transformation journey") |
| Practical and specific: the job, the tool, the result | Abstract promises about the future of work |
| Confident, warm, human | Luxury or exclusive ("discerning", "curated", "elevated") |
| "We" for the company | "I", or naming anyone but Allan |
| Contractions and possessives are fine: "we'll", "your team's" | Stiff spelled-out forms just to avoid them |
| Fewer words. If a section can lose a sentence, it should | Paragraphs where a list or a heading would do |
| Prices and durations stated plainly: "£995, half a day" | "Contact us for pricing" |
| Honest limits: "If a step doesn't earn the next one, you stop there." | Hard sell |

Examples from the site to match: "We work out where AI fits. Then we implement
it and make it stick." · "30 minutes. No pitch deck." · "Check it's the right
job. Then build it." · "Three ways in. All priced up front."

## Rules the checker enforces

| # | Rule | Write | Not |
|---|------|-------|-----|
| 1 | No em dashes | a comma, a colon, or a full stop | text — like this |
| 2 | British spelling | organisation, programme, licence | organization, program, license |
| 3 | Sentence case headings | Three ways in | Three Ways In |
| 4 | No banned terms | see below | |
| 5 | Company name takes the ampersand | Nielsen & Brown | Nielsen and Brown |
| 6 | No unsourced statistics | a named, checkable source, or no number | "cut admin by 70%" |
| 7 | Founder visibility | Allan Nielsen, Co-founder; "we" | naming Sam, "two founders", "the two co-owners" |
| 8 | Client names as the client gives them | Tom Mathew | Thomas Mathew |

### Banned terms

`bespoke` · `retainer` · `tailored` · `owner-led` · `UK AI Bill`

Use instead: **custom-built** for bespoke, **ongoing support** (or Continuing
Partnership) for retainer, **built around your business** for tailored.

## Proof

- **No anonymous numbers.** Don't use a statistic unless it has a source we can
  name and check. Scenario examples are fine if they're labelled "a typical
  example, not results from a named client" and carry no figures.
- **Testimonials.** All current quotes are from one client, Dunsters Farm (a
  family-owned foodservice wholesaler; the work was an AI readiness and
  opportunity assessment with its directors). Present them as one leadership
  team, never as separate clients. Use only the approved wordings:
  - Tom Mathew, Commercial Director: the long quote.
  - Hannah Barlow, Managing Director; Tom Curtin, Operations Director; Dean
    Smalley, Head of IT & Systems: the short versions.

  Headshots are in `assets/people/*-dunsters-farm.jpg`. The quotes praise
  strategy work, so don't place them as proof of a build.
- **Memberships:** pro-manchester and Manchester Digital, shown as white badges
  in their own colours.

---

## Visual brand

### Colours

The palette is fixed (it matches the business cards). Tokens live in
`assets/site/site.css`:

| Token | Hex | Use |
|---|---|---|
| `--cream` | `#FAF8F3` | page background |
| `--paper` | `#F2EDE6` | alternate sections, soft panels |
| `--sand` | `#E9DCC0` | tags, highlights |
| `--line` | `#DCD3BF` | borders and dividers |
| `--charcoal` | `#2C2C29` | headings, dark sections, footer |
| `--ink` | `#3A382F` | body text |
| `--muted` / `--muted-dark` | `#6B6759` / `#B5B1A0` | secondary text on light / dark |
| `--gold` / `--gold-text` | `#B8924A` / `#85652A` | accents, ticks; gold text on light grounds |
| `--action` / `--action-dark` | `#A64B2A` / `#8E3F23` | booking buttons only |

Gold is an accent, never body text on cream (it fails contrast); use
`--gold-text` there. The terracotta `--action` is reserved for calls to action.

### Type

- **Jost** for everything: headings 600, body 400.
- **Cormorant Garamond italic** only for the large pull quote in testimonials.
- Headings are tight (`letter-spacing: -.02em`) and short.

### Logo

Lowercase stacked wordmark, "nielsen &" over "brown", in Jost Semi-bold with a
gold ampersand. Files in `assets/brand/`:

| File | Use |
|---|---|
| `NB_Logo_Stacked_Charcoal.svg` / `.png` | light backgrounds (nav) |
| `NB_Logo_Stacked_Cream.svg` / `.png` | dark backgrounds (footer) |
| `NB_Logo_Stacked_Strap_*.svg` / `.png` | with "AI strategy and delivery for UK businesses", for large uses only |
| `NB_Icon_nb.svg` / `.png` | n&b circle: avatars, favicons, social |

Use the SVGs on the web and in print; the PNGs where SVG isn't accepted. Never
use the strapline version at nav size: it becomes unreadable.

### Layout

- Lots of space, few words per section, one idea per section.
- Prices sit on cards with the duration and a short list of what you get.
- Phones get their own representation of dense content (swipe rows, collapsible
  lists, tables as cards, a sticky "Book a call" bar) through the shared mobile
  classes described in `scripts/site/README.md`. Desktop and mobile should each
  look designed, not squeezed.
- Every page ends with a route to a call: "30 minutes. No pitch deck."

---

## Notes carried over

- **Ampersand form.** Upright, not italic, matching every brand asset.
- **CTA colour.** Terracotta `#A64B2A` sits outside the original palette on the
  board's instruction. It also fixes contrast: cream on gold was 2.73:1, cream
  on terracotta is 5.40:1.
- **Readiness score facts.** The score is out of **120** (24 of the 32 questions
  are scored). The app does not benchmark against other businesses, so never
  promise "how you compare to businesses like yours".
- **Don't make content visibility depend on an animation completing.** With
  Reduce Motion on, a zero-length animation never applies its end state, so
  anything starting at `opacity: 0` stays invisible.
