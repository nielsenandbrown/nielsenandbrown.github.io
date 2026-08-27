#!/usr/bin/env python3
"""
Check site copy against the rules in STYLE.md.

    python3 scripts/check-style.py              # the homepage, per NAB-106
    python3 scripts/check-style.py --all        # every page
    python3 scripts/check-style.py blog.html    # specific files

NAB-106 scopes the check to "the live homepage", so that is the default.
The legal pages are a different register: they name institutions
("Information Commissioner's Office") that the rules cannot sensibly apply to.

Exits 1 if anything is found, so it can gate a build.
Deliberate exceptions go in scripts/style-ignore.txt.
"""
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORE_FILE = os.path.join(ROOT, "scripts", "style-ignore.txt")

# name -> (pattern, hint)
RULES = [
    ("possessive apostrophe", r"\b\w+['’]s\b",
     "write 'the data from the client', not 'the client's data'"),
    ("em dash", r"—",
     "use a comma, a colon, or a full stop"),
    ("contraction", r"\b\w+['’](t|s|re|ve|ll|d|m)\b",
     "spell it out: do not, we will, it is"),
    ("pricing figure", r"[£$€]\s?[\d,]+(?:\.\d+)?",
     "no pricing anywhere on the site",
     {"pricing.html"}),   # the pricing page is the deliberate exception
    ("non-British spelling",
     r"(?i)\b(organiz\w*|analyz\w*|optimiz\w*|specializ\w*|recogniz\w*|"
     r"colou?r(?<!colour)\w*|cent(?:er|ers)\b|program(?!me)s?\b|license[ds]?\b)",
     "use organisation, analyse, colour, centre, programme, licence"),
    ("banned term", r"(?i)\b(bespoke|retainers?|tailored|owner[- ]led|UK AI Bill)\b",
     "custom-built / ongoing support / built around your business"),
    ("spelled-out company name", r"Nielsen and Brown",
     "the company name always takes the ampersand"),
]

TITLE_CASE = re.compile(r"^(?:[A-Z][a-z]+[ ,]+){2,}[A-Z][a-z]+$")
SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "is",
         "it", "of", "on", "or", "the", "to", "we", "you", "your"}


def load_ignores():
    if not os.path.exists(IGNORE_FILE):
        return []
    out = []
    for line in open(IGNORE_FILE, encoding="utf8"):
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def visible_text(src):
    """Strip scripts, styles, comments and tags; keep a line map."""
    s = re.sub(r"<(script|style)\b.*?</\1>", lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
    s = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)


def headings(src):
    for m in re.finditer(r"<(h[1-4])\b[^>]*>(.*?)</\1>", src, re.S | re.I):
        text = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        if text:
            yield src[:m.start()].count("\n") + 1, text


def check(path, ignores):
    src = open(path, encoding="utf8").read()
    text = visible_text(src)
    found = []

    base = os.path.basename(path)
    for rule in RULES:
        name, pattern, hint = rule[0], rule[1], rule[2]
        exempt = rule[3] if len(rule) > 3 else ()
        if base in exempt:
            continue
        for m in re.finditer(pattern, text):
            snippet = re.sub(r"\s+", " ", text[max(0, m.start() - 55):m.end() + 55]).strip()
            if any(ig in snippet or ig in m.group(0) for ig in ignores):
                continue
            line = text[:m.start()].count("\n") + 1
            found.append((line, name, m.group(0).strip(), snippet, hint))

    for line, text_h in headings(src):
        words = [w for w in re.findall(r"[A-Za-z']+", text_h)]
        if len(words) < 3:
            continue
        capped = [w for w in words[1:] if w[0].isupper() and w.lower() in SMALL]
        if capped and TITLE_CASE.match(text_h):
            if not any(ig in text_h for ig in ignores):
                found.append((line, "title-case heading", text_h, text_h,
                              "headings are sentence case"))
    return found


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if args:
        files = args
    elif "--all" in sys.argv:
        files = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    else:
        files = [os.path.join(ROOT, "index.html")]
    ignores = load_ignores()

    total = 0
    for path in files:
        rel = os.path.relpath(path, ROOT)
        found = check(path, ignores)
        if not found:
            print(f"\033[32m✓\033[0m {rel}")
            continue
        print(f"\033[33m•\033[0m {rel} — {len(found)} to review")
        for line, name, match, snippet, hint in sorted(found):
            print(f"    {rel}:{line}  [{name}] {match!r}")
            print(f"       …{snippet}…")
            print(f"       \033[2m{hint}\033[0m")
        total += len(found)

    print()
    if total:
        print(f"{total} item(s) to review. NAB-106: flag these rather than "
              f"silently fixing, some may be deliberate.")
        print(f"Deliberate exceptions go in {os.path.relpath(IGNORE_FILE, ROOT)}")
        return 1
    print("Clean against every rule in STYLE.md.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
