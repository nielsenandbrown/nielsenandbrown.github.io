# Nielsen &amp; Brown — copy style rules

The rules the site copy is written to. Consolidated from the ticket document
`NAB-Website-Update-Tickets.docx`, where they were split across NAB-101
(acceptance criteria) and NAB-106 (QA checklist).

## Checking

```
python3 scripts/check-style.py           # the homepage, per NAB-106
python3 scripts/check-style.py --all     # every page
```

Exits 1 if anything is found, so it can gate a build. NAB-106 scopes the pass
to "the live homepage", so that is the default. The legal pages are a different
register and name institutions the rules cannot sensibly apply to, which is why
they are not checked unless you ask.

---

## The rules

| # | Rule | Write | Not |
|---|------|-------|-----|
| 1 | No possessive apostrophes | the data from the client | the client's data |
| 2 | No em dashes | a comma, or a colon | text — like this |
| 3 | No contractions | do not, we will, it is | don't, we'll, it's |
| 4 | No pricing figures | "a short, low-cost way to test" | "£4,500" |
| 5 | British spelling | organisation, programme, licence | organization, program, license |
| 6 | Sentence case headings | Four ways to start | Four Ways To Start |
| 7 | No banned terms | see list below | — |
| 8 | Company name takes the ampersand | Nielsen &amp; Brown | Nielsen and Brown |

**Rule 4 exception:** the engagement selector publishes fixed prices, and it now
appears on both the homepage and `pricing.html`, so the checker skips that rule on
those two files. Every other page still fails on a price.

### Banned terms

`bespoke` · `retainer` · `tailored` · `owner-led` · `UK AI Bill`

Use instead: **custom-built** for bespoke, **ongoing support** for retainer,
**built around your business** for tailored.

### Also required

- Illustrative examples stay clearly labelled as illustrative (NAB-101)
- No percentage statistics in the "Why now" section (NAB-105)
- The ampersand renders upright, semibold, in warm gold, matching the brand
  assets in `assets/brand/` (see note below)

---

## Two things the source tickets disagree on

Recorded here so the next person does not have to rediscover them.

**Scope.** NAB-101 qualifies several rules as applying to *body copy*.
NAB-106 states them unqualified. Whether they cover form labels, button text,
validation messages and the cookie banner is not defined anywhere. The checker
reports everything and leaves the judgement to a person, which is why NAB-106
says to flag rather than silently fix.

**Ampersand form.** NAB-102 specifies the ampersand "set in italic". Every
supplied brand asset uses an **upright** ampersand, and the upright form was
chosen. NAB-102's wording is out of date, not the assets.

**Founders line.** NAB-101 requires a founders line naming both co-founders in
the "Who we are" section. It was removed by later instruction and the FAQ
reference changed to "the two co-owners". The ticket's acceptance criteria no
longer match the build.

**How we work.** NAB-101 lists a "How we work: three steps" section. It was
removed as duplicating "How we work together", which covers the same ground.
Links that pointed at it now go to "How we think about it" (the five-question
method) or "How we work together" (the four engagement options).

**Size range.** NAB-101 specifies 50 to 250 people throughout. Changed first to
30 to 300, then to **10 to 300**, across all 13 references on all three pages.

**Illustrative labels.** NAB-101 requires "illustrative examples remain clearly
labelled as illustrative". All seven labels were removed on instruction, and the
sector section carrying the remaining disclaimer was deleted. The service boxes
now carry specific measured outcomes with no qualifier. Raised twice before
building; the decision stands and is recorded here rather than argued again.

**Headcount chips.** NAB-101 requires each service example to carry "an approximate
headcount chip". All four were removed on instruction. The section heading still
reads "each proven on a business your size", which the chips were what evidenced.

**Why now percentages.** The "also required" note above, from NAB-105, says no
percentage statistics in this section, and the section was rewritten to strip two.
A 76% Gartner figure has since been added back by instruction, so the section now
carries one. NAB-105 no longer matches the build.

**Why now sources.** The section is three columns: the GOV.UK 5.6M, the Gartner
76%, and a DSIT block. A McKinsey EBIT figure was supplied and then withdrawn.
The DSIT wording is as supplied and has not been checked against the report; it
was queried as possibly describing skills as a barrier rather than readiness, and
confirmed for use as written.

**Sector examples.** NAB-101 lists "Real, practical examples by sector: four
sector cards". Deleted as duplicating the service boxes, which cover the same
four scenarios at the same four headcounts.

**Pricing.** NAB-101 says "no pricing figures anywhere on the page". There is now
a public pricing page, and the homepage bridge shows three price bands as the
hook into it. See the exception note above.

**Engagement lineup.** Rebuilt from `nb-pricing-engagement-larger-type (4).html`.
Second Opinion (£1,950) and Board and Leadership Briefing (£1,500) retired; AI
Starting Point (£995) and AI in Practice (£1,250) added; AI Foundations Day
repriced £2,500 to £2,195. The entry band is now £995 to £2,950. AI in Practice
carries a bundle price, £995 when booked within thirty days of an AI Starting
Point session, which is a new field the card and detail templates were extended
to support.

**Readiness panel.** Layout and copy both come from the pricing mockup, with the
lede, the six bullets and the closing line supplied directly. Two notes for
whoever picks this up next:

- The score is stated as **out of 120**, not 160. Tech spec M-3: 24 of the 32
  questions are scored, 120 raw maximum. The 160 in the original mockup was
  wrong and has been corrected on instruction.
- The mockup's *"How you compare to businesses of similar size and sector"* is
  deliberately **not** on the page. `copy.v1.ts` states benchmarking is out of
  scope and G-2 forbids the report from inventing a peer comparison, so the
  bullet would have promised something the report does not contain. Replaced
  with the Strategy Wheel line, which also explains the second of the two
  frameworks the stat row advertises. Revisit if the app ever gains
  benchmarking.

The report illustration is kept. The report exists and is emailed; the app
config only forbids promising one **on screen**.

The CTA reads "Get your free AI readiness report", which diverges from the
`cta` string in `copy.v1.ts` ("Take the AI Readiness Score"). Deliberate, on
instruction. If the score app's own landing page is meant to match, that string
needs changing there too.

**Engagement section.** NAB-101 lists "How we work together: four engagement options
with duration and best-for line". That section was removed and replaced by the full
priced engagement selector, moved high up the page, directly after "Is this you".

**CTA colour.** NAB-101 sets the brand palette. Booking CTAs now use burnt terracotta
`#A64B2A`, deliberately outside it, on the board's instruction. It also fixes a
contrast failure: cream on gold was 2.73:1, below WCAG AA. Cream on terracotta is
5.40:1.

**Type scale.** Body copy and micro-labels increased by roughly 2px and 1px
respectively, driven by `--fs-*` tokens in `:root`. Cormorant headings, the hero
headline, the before/after figures and the nav are deliberately unchanged.

**Type scale, revised.** Ticket 1 was reissued at +1.5px, superseding the earlier
+2px version. Applied from the original baseline, so nine elements are 0.5px
smaller than the +2px build. The nav is excluded; the before/after figures and the
budget card heading are included despite being Cormorant, because the reissued
ticket lists them explicitly.

**Nav breakpoint.** Raised from 768px to 1240px. The five-item nav already wrapped
between roughly 769 and 1090px, which included iPad landscape at 1024px. Adding a
sixth item made that worse, so the desktop nav now only shows where it fits.

**Muted grey.** `--muted-2` darkened from #9C9989 (2.46:1, failing) to #6E6A5A
(4.66:1). A companion `--muted-on-dark` #B5B1A0 covers the same role on charcoal,
where darkening would have made things worse.

---

## Deliberate exceptions

Some flags are intentional. List them in `scripts/style-ignore.txt`, one
substring per line, and the checker will skip any match containing it.
Add a comment line above each explaining why.

Already listed: the GOV.UK source citation, and the proper nouns on the legal
pages (Information Commissioner's Office, Google's privacy policy, and so on).
