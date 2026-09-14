"""Build preview.html from test.html per nb-landing-page-restructure-spec.md."""
import re, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
s = open(ROOT + 'test.html', encoding='utf8').read()


def must_replace(text, old, new, count=1):
    assert text.count(old) >= 1, 'not found: ' + old[:80]
    return text.replace(old, new, count)


# ── Locate top-level blocks by their opening markers, in DOM order ──────────
ORDER = [
    ('hero', '<section id="hero"'),
    ('partners', '<section id="partners"'),
    ('proof', '<div id="proof"'),
    ('audience', '<section id="audience"'),
    ('engagement', '<section id="engagement"'),
    ('pain', '<section id="pain"'),
    ('opportunity', '<section id="opportunity"'),
    ('credibility', '<section id="credibility"'),
    ('wheel', '<section id="wheel"'),
    ('services', '<section id="services"'),
    ('assurance', '<section id="assurance"'),
    ('faq', '<section id="faq"'),
    ('cta-banner', '<section id="cta-banner"'),
    ('trust-bar', '<div id="trust-bar"'),
    ('contact', '<section id="contact"'),
    ('_endmain', '</main>'),
    ('blog', '<section id="blog"'),
    ('_footer', '<!-- ═══════════════════════════════════════════════\n     FOOTER'),
]
pos = {k: s.index(m) for k, m in ORDER}
keys = [k for k, _ in ORDER]
seg = {k: s[pos[k]:pos[keys[i + 1]]] for i, k in enumerate(keys[:-1])}

# ── 1. Hero ─────────────────────────────────────────────────────────────────
hero = seg['hero']
proof_cards = re.findall(r'<div class="nb-proof-card">.*?</p>\s*</div>', seg['proof'], re.S)
assert len(proof_cards) == 4
proof_items = '\n'.join(
    '      ' + c.replace('nb-proof-card', 'hero-proof-item').replace('\n    ', '\n      ')
    for c in proof_cards)

old_actions = hero[hero.index('    <div class="hero-actions">'):hero.index('  </div>\n</section>')]
new_actions = '''    <div class="hero-actions">
      <a href="https://score.nielsenandbrown.com" class="btn-book" data-ga="cta_hero_primary">
        Get your free AI readiness report
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
      <a href="#contact" class="btn-outline" data-ga="cta_hero_secondary">Book your free discovery call</a>
    </div>

    <div class="hero-proof" aria-label="What this looks like in practice">
''' + proof_items + '''
    </div>
'''
hero = hero.replace(old_actions, new_actions, 1)
seg['hero'] = hero

# ── 2. Audience, merged with "Where teams like yours get stuck" ─────────────
seg['audience'] = '''<section id="audience" class="nb-sec nb-sec--dark" aria-labelledby="audience-heading">
  <div class="nb-wrap">
    <div class="nb-eyebrow">Is this you</div>
    <h2 class="nb-h2" id="audience-heading">Built for one kind of business, <em>not every business.</em></h2>
    <p class="nb-lede">We turn down work that is not a fit, on purpose.</p>
    <div class="nb-qualify">
      <ul class="nb-qlist">
        <li><span class="nb-tick" aria-hidden="true">&#10003;</span><span>You have no clear AI policy, or staff are not following the one you have</span></li>
        <li><span class="nb-tick" aria-hidden="true">&#10003;</span><span>Someone on the leadership team is curious about AI, but nobody currently owns getting it done</span></li>
        <li><span class="nb-tick" aria-hidden="true">&#10003;</span><span>Every tool promises a lot, and nobody has had the time to work out which one fits how the team works</span></li>
        <li><span class="nb-tick" aria-hidden="true">&#10003;</span><span>Data, compliance, or client trust means you cannot just let staff loose on any AI tool</span></li>
        <li><span class="nb-tick" aria-hidden="true">&#10003;</span><span>You are already paying for AI licences but cannot measure the ROI</span></li>
      </ul>
      <div class="nb-qside">
        <h4>Not a big-consultancy budget</h4>
        <p>Enterprise AI consultancies price for enterprise clients. We are built and priced for a business your size, not a FTSE 250 one. If three or more of these sound like you, the next step is a short call, not a proposal.</p>
        <a href="#contact" class="btn-book" data-ga="cta_qualify">Book your free discovery call</a>
      </div>
    </div>
  </div>
</section>

'''

# ── 3. Engagement, with the four services merged in ─────────────────────────
eng = seg['engagement']
head_old = eng[eng.index('    <div class="nb-eyebrow">'):eng.index('<div class="ladder">')]
head_new = '''    <div class="nb-eyebrow">What we do and what it costs</div>
    <h2 class="nb-h2" id="engagement-heading">Four things we help with, and what each one costs</h2>
    <ul class="nb-svc-lines">
      <li><a href="/services/ai-strategy-and-roadmap"><h3>AI strategy and roadmap</h3></a><p>Find the three to five places AI is most likely to help, then turn the strongest into a plan the team can start on.</p></li>
      <li><a href="/services/team-enablement"><h3>Team enablement and adoption</h3></a><p>Get the team using AI safely and well in their actual day-to-day work, from leaders to frontline staff.</p></li>
      <li><a href="/services/workflow-automation"><h3>Workflow automation and custom tools</h3></a><p>Where off-the-shelf does not fit, build something that plugs into the systems the team already uses.</p></li>
      <li><a href="/services/governance-and-compliance"><h3>Governance and compliance</h3></a><p>A plain-English usage policy, a risk register and clear ownership, so AI use can be shown to be done properly.</p></li>
    </ul>
    <p class="nb-lede nb-tier-lede">Every engagement has a fixed scope, a fixed price, and something you keep at the end of it. Select any one to see exactly what you receive.</p>
'''
eng = eng.replace(head_old, head_new, 1)

start_old = eng[eng.index('<section class="panel on" id="start"'):eng.index('<section class="panel" id="next"')]
start_new = '''<section class="panel on" id="start" role="tabpanel" aria-labelledby="t1">
        <div class="feature feature--pointer">
          <span class="tag">Free, self serve</span>
          <h3>AI Readiness Score</h3>
          <p class="sub">Where AI earns its place in your business, and just as usefully, where it does not.</p>
          <a class="nb-pointer" href="#score">See what the score tells you <span aria-hidden="true">&darr;</span></a>
        </div>
      </section>

      '''
eng = eng.replace(start_old, start_new, 1)

g4 = eng.index('          <div class="group">\n            <div class="grouphead">\n              <span class="gnum">4</span>')
g_end = eng.index('        </div>\n      </section>', g4)
eng = eng[:g4].rstrip() + '\n' + eng[g_end:]

close_start = eng.index('<div class="wrap">\n  <section class="close">')
eng = eng[:close_start] + '''<div class="nb-wrap">
    <p class="nb-process-link">Diagnostic, roadmap, delivery and ongoing support are set out stage by stage. <a href="/how-we-work">See the full process</a></p>
  </div>
</section>

'''
eng = must_replace(eng, '<section id="engagement" class="nb-sec nb-sec--mid" aria-labelledby="engagement-heading">',
    '<section id="engagement" class="nb-sec nb-sec--mid" aria-labelledby="engagement-heading">\n  <span id="services" class="nb-anchor" aria-hidden="true"></span>')
seg['engagement'] = eng

# ── 4. Score (new) ──────────────────────────────────────────────────────────
score = '''<section id="score" class="nb-sec nb-sec--dark nb-score" aria-labelledby="score-heading">
  <div class="nb-wrap">
    <div class="nb-score-inner">
      <div>
        <div class="nb-eyebrow">AI Readiness Score, free</div>
        <h2 class="nb-h2" id="score-heading">Know where you stand before you invest</h2>
      </div>
      <div>
        <ul class="nb-score-lines">
          <li>32 questions across 2 frameworks, about 20 minutes, and no call booked.</li>
          <li>Your score out of 120, where the business is strongest and weakest, and where to act first.</li>
          <li>A verdict on whether you are ready to invest yet, and one action worth taking this week.</li>
        </ul>
        <a class="btn-book" href="https://score.nielsenandbrown.com" data-ga="readiness_score_start">Get your free AI readiness report
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
      </div>
    </div>
  </div>
</section>

'''

# ── 5. Credibility ──────────────────────────────────────────────────────────
cred = seg['credibility']
cred = must_replace(cred,
    '<p>We work best with businesses of roughly 10 to 300 people. Not repackaged enterprise consulting, not a solo freelancer.</p>',
    '<p>Priced and scoped for a business your size. Not repackaged enterprise consulting, not a solo freelancer.</p>')
cred = must_replace(cred, '    </div>\n  </div>\n</section>', '''    </div>
    <p class="nb-tools">We build with Anthropic, OpenAI, Google, Grok, Lovable and n8n, and are members of pro-manchester and Manchester Digital.</p>
    <p class="nb-safe-line">Safeguards are part of the work, not bolted on afterwards. <a href="/governance">See how we keep AI use safe</a></p>
  </div>
</section>''')
seg['credibility'] = cred

# ── 6. FAQ, trimmed to four ─────────────────────────────────────────────────
faq = seg['faq']
items = re.findall(r'      <div class="faq-item" role="listitem">.*?\n      </div>\n', faq, re.S)
assert len(items) == 6
keep_q = ['Will this feel like a big consultancy engagement', 'Is this only for big companies',
          'How much does it cost', 'How do we keep our data safe']
kept = [i for q in keep_q for i in items if '<span>' + q + '</span>' in i]
assert len(kept) == 4
kept = [i.replace('cannot cover strategy, training, and building all at once',
                  'cannot cover strategy, enablement, and building all at once') for i in kept]
list_start = faq.index('      <div class="faq-item"')
list_end = faq.index('    </div>\n  </div>\n</section>')
faq = faq[:list_start] + ''.join(kept) + faq[list_end:]
faq = must_replace(faq, '    </div>\n  </div>\n</section>',
    '    </div>\n    <p class="nb-faq-more"><a href="/faq">See all questions</a></p>\n  </div>\n</section>')
seg['faq'] = faq

# ── 7. Blog, shrunk ─────────────────────────────────────────────────────────
blog = seg['blog']
blog = re.sub(r'\s*<p class="section-intro">.*?</p>', '', blog, count=1, flags=re.S)
blog = re.sub(r'\s*<p class="blog-cta-body">.*?</p>', '', blog, count=1, flags=re.S)
blog = must_replace(blog, '<section id="blog"', '<section id="blog" class="blog--compact"')
seg['blog'] = blog

# ── Reassemble ──────────────────────────────────────────────────────────────
new_main = (seg['hero'] + seg['audience'] + seg['engagement'] + score +
            seg['credibility'] + seg['faq'] + seg['contact'])
s = s[:pos['hero']] + new_main + s[pos['_endmain']:pos['blog']] + seg['blog'] + s[pos['_footer']:]

# ── Nav ─────────────────────────────────────────────────────────────────────
nav_old = s[s.index('    <ul class="nav-links" id="nav-links">'):s.index('    </ul>', s.index('nav-links')) + len('    </ul>')]
s = s.replace(nav_old, '''    <ul class="nav-links" id="nav-links">
      <li><a href="/how-we-work">How it works</a></li>
      <li><a href="#engagement">What we do</a></li>
      <li><a href="#engagement">Pricing</a></li>
      <li><a href="#audience">Who it is for</a></li>
      <li><a href="#contact" class="nav-cta btn-book">Book a call</a></li>
    </ul>''', 1)

# ── Footer ──────────────────────────────────────────────────────────────────
s = must_replace(s, '''          <li><a href="#services">Strategy and roadmap</a></li>
          <li><a href="#services">Team training</a></li>
          <li><a href="#services">Custom-built tools</a></li>
          <li><a href="#services">Governance and compliance</a></li>''',
'''          <li><a href="/services/ai-strategy-and-roadmap">Strategy and roadmap</a></li>
          <li><a href="/services/team-enablement">Team enablement</a></li>
          <li><a href="/services/workflow-automation">Custom-built tools</a></li>
          <li><a href="/services/governance-and-compliance">Governance and compliance</a></li>''')
s = must_replace(s, '<li><a href="#engagement">How we work</a></li>', '<li><a href="/how-we-work">How we work</a></li>')
s = must_replace(s, '<p>Helping UK businesses with 10 to 300 people use AI in a practical, safe, and properly sized way.</p>',
                    '<p>Helping UK businesses use AI in a practical, safe, and properly sized way.</p>')

# ── Head: noindex, #wheel redirect, metadata wording ────────────────────────
s = must_replace(s, '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"/>',
    '<meta name="robots" content="noindex, follow"/>  <!-- preview only: restore the index directive at rollout -->')
s = must_replace(s, '<title>', '''<script>
    // #wheel moved to /how-we-work. Old links (footer, email, LinkedIn) must not
    // land on a dead scroll, so send them on before anything renders.
    if (location.hash === '#wheel') location.replace('/how-we-work');
  </script>
  <title>''')
s = s.replace('Strategy, training, automation', 'Strategy, enablement, automation')
s = s.replace('Strategy · Training · Software', 'Strategy · Enablement · Software')

# ── JSON-LD: FAQPage moves to /faq; enablement wording ──────────────────────
m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
d = json.loads(m.group(2))
d['@graph'] = [g for g in d['@graph'] if g['@type'] != 'FAQPage']
org = d['@graph'][0]
org['knowsAbout'] = ['AI Enablement' if k == 'AI Training' else k for k in org['knowsAbout']]
org['description'] = org['description'].replace('training and workshops', 'team enablement')
for g in d['@graph']:
    if g['@type'] == 'ProfessionalService':
        for it in g['hasOfferCatalog']['itemListElement']:
            sv = it['itemOffered']
            if sv['name'] == 'Team Training & Adoption':
                sv['name'] = 'Team Enablement & Adoption'
                sv['description'] = sv['description'].replace('Role based AI training', 'Role based AI enablement').replace(' Group workshops and train the trainer programmes.', ' Group sessions and internal champion programmes.')
s = s[:m.start(2)] + '\n  ' + json.dumps(d, indent=2, ensure_ascii=False).replace('\n', '\n  ') + '\n  ' + s[m.end(2):]

# ── JS: section tracking IDs ────────────────────────────────────────────────
s = must_replace(s,
    "var sectionIds = ['proof','audience','pain','opportunity','credibility','wheel','services','engagement','assurance','partners','faq','cta-banner','contact'];",
    "var sectionIds = ['audience','engagement','score','credibility','faq','contact'];")

# ── CSS: drop the Why now block, add the new pieces ─────────────────────────
wn_a = s.index('/* ── Why now evidence columns')
wn_b = s.index('@media (max-width: 820px) {', wn_a)
wn_b = s.index('}\n}\n', wn_b) + 4
s = s[:wn_a] + s[wn_b:]

CSS = '''
/* ── Restructure preview ─────────────────────────────────────────────── */
/* #services merged into #engagement. A zero-height anchor at the very top of
   the section, on the same scroll margin as every section, so old links land
   exactly where #engagement does. */
.nb-anchor { display: block; height: 0; scroll-margin-top: 104px; }

/* Hero proof strip: the four micro-proofs moved up from the dark strip. */
.hero-proof { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin-top: 3.2rem;
  border-top: 1px dashed var(--stone); clip-path: inset(0 0 0 1px);
  animation: heroFadeUp 0.9s 1s var(--ease-out) both; }
.hero-proof-item { padding: 1.4rem 1.6rem 0.2rem; border-left: 1px dashed var(--stone); }
.hero-proof-item .nb-kicker { font-size: var(--fs-kicker); letter-spacing: 0.14em; text-transform: uppercase; color: var(--gold-deep); font-weight: 600; margin-bottom: 0.5rem; }
.hero-proof-item .nb-shift { font-family: var(--font-display); font-size: 1.5rem; font-weight: 600; display: flex; align-items: baseline; gap: 0.5rem; margin-bottom: 0.35rem; }
.hero-proof-item .nb-from { color: var(--muted-2); font-size: 1.05rem; }
.hero-proof-item .nb-to { color: var(--gold-deep); }
.hero-proof-item p { font-size: 0.95rem; color: var(--muted); line-height: 1.55; }
#hero .hero-sub { margin-bottom: 2.4rem; }
@media (prefers-reduced-motion: reduce) { .hero-proof { opacity: 1 !important; transform: none !important; } }

/* Four service lines above the price tiers. */
.nb-svc-lines { list-style: none; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; margin: 0 0 2.6rem; border-top: 1px solid var(--line); }
.nb-svc-lines li { padding: 1.3rem 1.4rem 1.3rem 0; }
.nb-svc-lines li + li { padding-left: 1.4rem; border-left: 1px solid var(--line); }
.nb-svc-lines h3 { font-family: var(--font-display); font-size: 1.35rem; font-weight: 600; color: var(--charcoal); line-height: 1.2; margin-bottom: 0.4rem; }
.nb-svc-lines a { text-decoration: none; }
.nb-svc-lines a:hover h3, .nb-svc-lines a:focus-visible h3 { color: var(--gold-deep); }
.nb-svc-lines p { font-size: var(--fs-small); color: var(--ink); line-height: 1.55; }
.nb-tier-lede { margin-bottom: 1.8rem; }
#engagement .feature--pointer { padding: 2.2rem 2.4rem; }
#engagement .feature--pointer h3 { font-family: var(--font-display); font-size: 2rem; font-weight: 600; color: #fff; margin: 0.6rem 0 0.4rem; }
#engagement .feature--pointer .sub { margin-bottom: 1.2rem; }
.nb-pointer { color: var(--gold); font-weight: 500; letter-spacing: 0.04em; border-bottom: 1px solid rgba(184,146,74,0.5); }
.nb-pointer:hover, .nb-pointer:focus-visible { color: #fff; border-color: #fff; }
.nb-process-link { font-size: var(--fs-body); color: var(--ink); margin-top: 0.4rem; }
.nb-process-link a, .nb-safe-line a, .nb-faq-more a { color: var(--gold-deep); font-weight: 500; border-bottom: 1px solid var(--gold); margin-left: 0.3rem; }
@media (max-width: 1000px) {
  .nb-svc-lines { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .nb-svc-lines li:nth-child(3) { padding-left: 0; border-left: none; }
  .nb-svc-lines li:nth-child(n+3) { border-top: 1px solid var(--line); }
}
@media (max-width: 640px) {
  /* one column on phones: two columns left "2 days -> 3 hours" wrapping over three lines */
  .hero-proof { grid-template-columns: minmax(0, 1fr); clip-path: inset(1px 0 0 0); }
  .hero-proof-item { border-top: 1px dashed var(--stone); border-left: none; padding: 1.1rem 0 0.9rem; }
  .hero-proof-item .nb-shift { white-space: nowrap; }
  .nb-svc-lines { grid-template-columns: minmax(0, 1fr); }
  .nb-svc-lines li, .nb-svc-lines li + li { padding-left: 0; border-left: none; }
  .nb-svc-lines li + li { border-top: 1px solid var(--line); }
}
@media (max-width: 1000px) and (min-width: 641px) {
  .hero-proof { grid-template-columns: repeat(2, minmax(0, 1fr)); clip-path: inset(1px 0 0 1px); }
  .hero-proof-item { border-top: 1px dashed var(--stone); }
}

/* Score: three lines and a button. */
.nb-score-inner { display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr); gap: 3rem; align-items: center; }
.nb-score .nb-h2 { margin-bottom: 0; }
.nb-score-lines { list-style: none; margin: 0 0 1.6rem; }
.nb-score-lines li { position: relative; padding: 0 0 0.7rem 1.4rem; font-size: var(--fs-body); line-height: 1.55; color: var(--cream-3); }
.nb-score-lines li::before { content: ""; position: absolute; left: 0; top: 0.62em; width: 6px; height: 6px; border-radius: 50%; background: var(--gold); }
@media (max-width: 900px) { .nb-score-inner { grid-template-columns: minmax(0, 1fr); gap: 1.6rem; } }

/* Credibility additions. */
.nb-tools { margin-top: 2.2rem; font-size: var(--fs-body); color: var(--ink); max-width: 52rem; }
.nb-safe-line { margin-top: 0.6rem; font-size: var(--fs-body); color: var(--ink); max-width: 52rem; }
.nb-faq-more { margin-top: 1.6rem; font-size: var(--fs-body); }
.nb-faq-more a { margin-left: 0; }

/* Blog strip, compact. */
#blog.blog--compact { padding-top: 3rem; padding-bottom: 3rem; }

/* Vertical rhythm. The spec targets 5 viewport heights at 1440x900, so
   sections run on 4rem rather than 5.5rem. Spacing only, nothing cut. */
@media (min-width: 681px) {
  .nb-sec, #contact { padding-top: 4rem; padding-bottom: 4rem; }
}
#hero { min-height: 0; padding-top: 8rem; }
#engagement .nb-h2 { max-width: 60rem; }
#footer { padding-top: 3.5rem; padding-bottom: 2.5rem; }
'''
s = s.replace('</style>', CSS + '</style>', 1)

# ── JS: the contact handler assumed a form on every page; the new pages have none
s = must_replace(s, "  form.addEventListener('submit', async (e) => {",
                    "  if (form) form.addEventListener('submit', async (e) => {")

# ── JS: anchor correction gave up whenever the browser's own smooth scroll moved the page
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anchorfix.py')).read())
s = must_replace(s, OLD, NEW)

open(ROOT + 'preview.html', 'w', encoding='utf8').write(s)
print('preview.html written', len(s))
