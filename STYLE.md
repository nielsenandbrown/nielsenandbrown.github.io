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

**Size range.** NAB-101 specifies 50 to 250 people throughout. Changed to
**30 to 300** across all nine references on Allan's instruction.

**Illustrative labels.** NAB-101 requires "illustrative examples remain clearly
labelled as illustrative". All seven labels were removed on instruction, and the
sector section carrying the remaining disclaimer was deleted. The service boxes
now carry specific measured outcomes with no qualifier. Raised twice before
building; the decision stands and is recorded here rather than argued again.

**Sector examples.** NAB-101 lists "Real, practical examples by sector: four
sector cards". Deleted as duplicating the service boxes, which cover the same
four scenarios at the same four headcounts.

**Pricing.** NAB-101 says "no pricing figures anywhere on the page". There is now
a public pricing page, and the homepage bridge shows three price bands as the
hook into it. See the exception note above.

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

---

## Deliberate exceptions

Some flags are intentional. List them in `scripts/style-ignore.txt`, one
substring per line, and the checker will skip any match containing it.
Add a comment line above each explaining why.

Already listed: the GOV.UK source citation, and the proper nouns on the legal
pages (Information Commissioner's Office, Google's privacy policy, and so on).
