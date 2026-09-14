"""Generate the eight new routes from preview.html's shell (spec: New routes)."""
import re, json, html, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
SCRATCH = os.path.dirname(os.path.abspath(__file__)) + '/'
BASE = 'https://www.nielsenandbrown.com'
HOME = '/preview.html'          # swap to '/' at rollout
ORG_ID = BASE + '/#organization'

pv = open(ROOT + 'preview.html', encoding='utf8').read()
DATA = json.load(open(SCRATCH + 'pdata.json'))
P = DATA['P']
e = lambda t: html.escape(str(t), quote=False)

# ── Pull reusable pieces out of preview.html ────────────────────────────────
def between(text, a, b, include_a=True):
    i = text.index(a); j = text.index(b, i)
    return text[i if include_a else i + len(a):j]

head = pv[:pv.index('</head>')]
head = re.sub(r'<script>\s*// #wheel moved.*?</script>\s*', '', head, flags=re.S)
head = re.sub(r'<script type="application/ld\+json">.*?</script>', '%%JSONLD%%', head, flags=re.S)
head = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/@emailjs[^>]*></script>\s*', '', head)
body_top = pv[pv.index('</head>'):pv.index('<main>')]
tail = pv[pv.index('<!-- ═══════════════════════════════════════════════\n     FOOTER'):]

# wheel and assurance content come from test.html, where those sections still live
test = open(ROOT + 'test.html', encoding='utf8').read()
wheel_cards = between(test, '<div class="nb-cards nb-cards--5">', '    </div>\n  </div>\n</section>')
assurance_cards = between(test, '<div class="nb-cards nb-cards--6">', '    </div>\n  </div>\n</section>')
services = re.findall(
    r'<div class="nb-slabel">(.*?)</div>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>\s*<div class="nb-example">\s*(<div class="nb-psr">.*?</div>\s*</div>)',
    test, re.S)
assert len(services) == 4
# the free stage: heading, standfirst, stat rows and button, without the tag or
# the wrapper div that closes before the report illustration
readiness = between(test, '<span class="tag">Free, self serve</span>', '<div class="reportwrap"', include_a=False)
readiness = readiness.rstrip()
assert readiness.endswith('</div>'); readiness = readiness[:-len('</div>')].rstrip()
readiness = readiness.replace('stand<br>before', 'stand before')   # a hidden <br> would run the words together
bullets = between(test, '<ul class="herobullets">', '</ul>') + '</ul>'
note = between(test, '<p class="note">', '</p>') + '</p>'


def repoint(fragment):
    """Same-page anchors in the shared nav and footer must point at the preview home."""
    fragment = re.sub(r'href="#hero"', f'href="{HOME}"', fragment)
    fragment = re.sub(r'href="#([a-z][\w-]*)"', lambda m: f'href="{HOME}#{m.group(1)}"', fragment)
    fragment = fragment.replace('href="founders.html"', 'href="/founders.html"')
    return fragment


body_top = repoint(body_top)
tail = repoint(tail)


def depth_fix(text, depth):
    if depth == 0:
        return text
    up = '../' * depth
    text = re.sub(r'((?:href|src)=")(?!https?:|/|#|mailto:|tel:|data:)([^"]+)"', lambda m: m.group(1) + up + m.group(2) + '"', text)
    text = text.replace('url("assets/', f'url("{up}assets/')
    return text


PAGE_CSS = '''
/* ── New route pages ─────────────────────────────────────────────────── */
.nb-page-head { padding-top: 9rem !important; }
.nb-h1 { font-family: var(--font-display); font-size: clamp(2.4rem, 5vw, 3.6rem); font-weight: 500; color: var(--charcoal); line-height: 1.08; max-width: 48rem; margin-bottom: 1.3rem; text-wrap: balance; }
.nb-crumb { font-size: var(--fs-eyebrow); margin-bottom: 1.4rem; color: var(--muted-2); }
.nb-crumb a { color: var(--gold-deep); border-bottom: 1px solid var(--gold); }
.nb-prose { max-width: 46rem; }
.nb-prose h2 { font-family: var(--font-display); font-size: clamp(1.7rem, 3.2vw, 2.2rem); font-weight: 600; color: var(--charcoal); line-height: 1.2; margin: 0 0 1rem; }
.nb-prose p, .nb-prose li { font-size: var(--fs-body); color: var(--ink); line-height: 1.7; }
.nb-prose p + p { margin-top: 1rem; }
.nb-prose ul { margin: 1rem 0 1rem 1.2rem; list-style: disc; }
.nb-prose li::marker { color: var(--gold-deep); }
.nb-prose li { margin-bottom: 0.4rem; }
.nb-prose a, .nb-inline-links a { color: var(--gold-deep); border-bottom: 1px solid var(--gold); }
.nb-small { font-size: var(--fs-small) !important; color: var(--muted-2) !important; }
.nb-inline-links { display: flex; flex-wrap: wrap; gap: 0.6rem 2rem; margin-top: 2rem; font-size: var(--fs-body); font-weight: 500; }
.nb-stage { padding: 2.6rem 0; border-top: 1px solid var(--line); }
.nb-stage-head { display: grid; grid-template-columns: 3.2rem minmax(0, 1fr) auto; gap: 0 1.2rem; align-items: baseline; margin-bottom: 1.4rem; }
.nb-stage-num { font-family: var(--font-display); font-size: 2.4rem; color: var(--gold-deep); line-height: 1; }
.nb-stage-head h3 { font-family: var(--font-display); font-size: 1.7rem; font-weight: 600; color: var(--charcoal); }
.nb-stage-band { font-size: var(--fs-eyebrow); letter-spacing: 0.12em; text-transform: uppercase; color: var(--gold-deep); font-weight: 600; white-space: nowrap; }
.nb-stage-note { grid-column: 2 / 4; font-size: var(--fs-body); color: var(--ink); margin-top: 0.3rem; }
.nb-products { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(260px, 100%), 1fr)); gap: 1rem; }
.nb-product { background: var(--cream); border: 1px solid var(--line); padding: 1.4rem 1.5rem; display: flex; flex-direction: column; }
.nb-product h4 { font-family: var(--font-display); font-size: 1.35rem; font-weight: 600; color: var(--charcoal); line-height: 1.2; }
.nb-product .nb-price { font-family: var(--font-display); font-size: 1.25rem; color: var(--gold-deep); margin: 0.2rem 0 0.5rem; }
.nb-product .nb-dur { font-size: var(--fs-eyebrow); letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted-2); margin-bottom: 0.6rem; }
.nb-product p { font-size: var(--fs-small); color: var(--ink); line-height: 1.55; flex-grow: 1; }
.nb-product a { margin-top: 1rem; color: var(--gold-deep); font-weight: 500; border-bottom: 1px solid var(--gold); align-self: flex-start; }
.nb-stage-free { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 2.4rem; background: var(--charcoal); color: var(--cream-3); padding: 2.4rem 2.6rem; }
.nb-stage-free .tag { font-size: var(--fs-eyebrow); letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold); font-weight: 500; }
.nb-stage-free h2 { font-family: var(--font-display); color: #fff; font-size: 2rem; font-weight: 600; line-height: 1.15; margin: 0.6rem 0 0.8rem; }
.nb-stage-free .rule { display: none; }
.nb-stage-free .sub { color: var(--cream-3); font-size: var(--fs-body); margin-bottom: 1.2rem; }
.nb-stage-free .statlist { list-style: none; margin: 0 0 1.4rem; border-top: 1px solid rgba(242,237,230,.14); }
.nb-stage-free .statlist li { display: flex; align-items: baseline; gap: 16px; padding: 8px 0; border-bottom: 1px solid rgba(242,237,230,.14); }
.nb-stage-free .statlist b { font-family: var(--font-display); font-size: 24px; color: var(--gold); min-width: 40px; text-align: right; }
.nb-stage-free .statlist span { font-size: 16px; color: rgba(242,237,230,.86); }
.nb-stage-free .herobullets { list-style: none; margin: 0 0 1rem; }
.nb-stage-free .herobullets li { position: relative; padding: 0 0 0.6rem 1.3rem; font-size: var(--fs-small); color: rgba(242,237,230,.9); line-height: 1.5; }
.nb-stage-free .herobullets li::before { content: ""; position: absolute; left: 0; top: 0.6em; width: 6px; height: 6px; border-radius: 50%; background: var(--gold); }
.nb-stage-free .note { font-size: var(--fs-small); color: rgba(242,237,230,.65); }
.nb-results { display: grid; gap: 2rem; }
.nb-result { display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 2.4rem; padding-top: 2rem; border-top: 1px solid var(--line); }
.nb-result h2 { font-family: var(--font-display); font-size: 1.7rem; font-weight: 600; color: var(--charcoal); line-height: 1.2; margin-top: 0.4rem; }
.nb-result h2 a:hover { color: var(--gold-deep); }
.nb-page-cta { display: flex; flex-wrap: wrap; align-items: center; gap: 1.2rem 2rem; }
.nb-page-cta h2 { flex: 1 1 100%; font-family: var(--font-display); font-size: clamp(1.8rem, 3.4vw, 2.4rem); font-weight: 600; color: #fff; }
.nb-page-cta p { flex: 1 1 100%; color: var(--cream-3); font-size: var(--fs-body); max-width: 44rem; margin-top: -0.4rem; }
.nb-page-cta .nb-cta-alt { color: var(--gold); border-bottom: 1px solid rgba(184,146,74,.6); font-weight: 500; }
@media (max-width: 900px) {
  .nb-stage-free, .nb-result { grid-template-columns: minmax(0, 1fr); }
  .nb-stage-head { grid-template-columns: 2.6rem minmax(0, 1fr); }
  .nb-stage-band { grid-column: 2; }
  .nb-stage-note { grid-column: 2; }
}
'''


def cta_block(alt_href, alt_text):
    return f'''<section class="nb-sec nb-sec--dark" aria-labelledby="cta-heading">
  <div class="nb-wrap">
    <div class="nb-page-cta">
      <h2 id="cta-heading">Talk it through with a person</h2>
      <p>A short call to find one realistic AI project, one risk worth avoiding, and the sensible next step. First calls are always free.</p>
      <a href="{HOME}#contact" class="btn-book" data-ga="cta_page_book">Book a call
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
      <a href="{alt_href}" class="nb-cta-alt">{alt_text}</a>
    </div>
  </div>
</section>
'''


def page_head(eyebrow, h1, lede, crumb=None):
    c = f'    <p class="nb-crumb"><a href="{crumb[0]}">{crumb[1]}</a></p>\n' if crumb else ''
    return f'''<section class="nb-sec nb-page-head" aria-labelledby="page-heading">
  <div class="nb-wrap">
{c}    <div class="nb-eyebrow">{eyebrow}</div>
    <h1 class="nb-h1" id="page-heading">{h1}</h1>
    <p class="nb-lede">{lede}</p>
  </div>
</section>
'''


def build(path, title, desc, slug, og_alt, main, jsonld_nodes):
    depth = path.count('/')
    url = BASE + '/' + path.rsplit('.html', 1)[0]
    og_image = f'{BASE}/assets/og/{slug}.png'
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', h, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*"/>', f'<meta name="description" content="{e(desc)}"/>', h)
    h = re.sub(r'<link rel="canonical" href="[^"]*"/>', f'<link rel="canonical" href="{url}"/>', h)
    h = re.sub(r'<meta property="og:url" content="[^"]*"/>', f'<meta property="og:url" content="{url}"/>', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*"/>', f'<meta property="og:title" content="{e(title)}"/>', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*"/>', f'<meta property="og:description" content="{e(desc)}"/>', h)
    h = re.sub(r'<meta property="og:image" content="[^"]*"/>', f'<meta property="og:image" content="{og_image}"/>', h)
    h = re.sub(r'<meta property="og:image:alt" content="[^"]*"/>', f'<meta property="og:image:alt" content="{e(og_alt)}"/>', h)
    h = re.sub(r'<meta name="twitter:title" content="[^"]*"/>', f'<meta name="twitter:title" content="{e(title)}"/>', h)
    h = re.sub(r'<meta name="twitter:description" content="[^"]*"/>', f'<meta name="twitter:description" content="{e(desc)}"/>', h)
    h = re.sub(r'<meta name="twitter:image" content="[^"]*"/>', f'<meta name="twitter:image" content="{og_image}"/>', h)
    graph = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title, 'description': desc,
         'isPartOf': {'@id': BASE + '/#website'}, 'publisher': {'@id': ORG_ID}}] + jsonld_nodes}
    h = h.replace('%%JSONLD%%', '<script type="application/ld+json">\n  ' +
                  json.dumps(graph, indent=2, ensure_ascii=False).replace('\n', '\n  ') + '\n  </script>')
    h = h.replace('</style>', PAGE_CSS + '</style>', 1)
    doc = h + body_top + '<main>\n\n' + main + '\n</main>\n\n' + tail
    doc = depth_fix(doc, depth)
    os.makedirs(os.path.dirname(ROOT + path) or ROOT, exist_ok=True)
    open(ROOT + path, 'w', encoding='utf8').write(doc)
    return path


written = []

# ── /how-we-work ────────────────────────────────────────────────────────────
GROUPS = [
    ('2', 'A first working step', 'Six ways in. Most clients take one and stop there if it is not working.', '£995 to £2,950', 'NEXT'),
    ('3', 'Acceleration', 'Proof at scale, built and measured.', '£3,500 to £4,500', 'ACCEL'),
    ('4', 'The core programme', 'Evidence based, not self reported. Priced and bought separately.', '£4,500 and £5,500', 'CORE'),
    ('5', 'Beyond the roadmap', 'Where the roadmap gets built, and stays working.', 'Scoped per engagement', 'AFTER'),
]


def product_card(pid):
    p = P[pid]
    extra = ''.join(f'<p class="nb-small">{e(p[k])}</p>' for k in ('req', 'bundle') if p.get(k))
    return (f'<article class="nb-product"><h4>{e(p["name"])}</h4><div class="nb-price">{e(p["price"])}</div>'
            f'<div class="nb-dur">{e(p["dur"])}</div><p>{e(p["blurb"])}</p>{extra}'
            f'<a href="{HOME}#{pid}">See what you get</a></article>')


stages = f'''<div class="nb-stage">
      <div class="nb-stage-head"><span class="nb-stage-num">1</span><h3>Where do we start</h3><span class="nb-stage-band">No cost</span>
        <p class="nb-stage-note">A straight answer about where the business actually stands, before anyone spends anything.</p></div>
      <div class="nb-stage-free">
        <div>
          <span class="tag">Free, self serve</span>{readiness}
        </div>
        <div>
          {bullets}
          {note}
        </div>
      </div>
    </div>
'''
for num, name, gnote, band, key in GROUPS:
    cards = '\n        '.join(product_card(pid) for pid in DATA[key])
    stages += f'''    <div class="nb-stage">
      <div class="nb-stage-head"><span class="nb-stage-num">{num}</span><h3>{name}</h3><span class="nb-stage-band">{e(band)}</span>
        <p class="nb-stage-note">{gnote}</p></div>
      <div class="nb-products">
        {cards}
      </div>
    </div>
'''

main = page_head('How we work', 'Five questions, then five stages',
                 'Every engagement runs on the same thinking and follows the same route: a free score first, then small fixed steps, and larger work only once a first step has shown it is worth doing.')
main += f'''<section id="wheel" class="nb-sec nb-sec--mid" aria-labelledby="wheel-heading">
  <div class="nb-wrap">
    <div class="nb-eyebrow">How we think about it</div>
    <h2 class="nb-h2" id="wheel-heading">Five straightforward questions to make sure every AI decision drives clear business value rather than guesswork.</h2>
    <p class="nb-lede">We call this the AI Business Strategy Wheel internally. You just get the five questions, worked through together.</p>
    {wheel_cards}    </div>
  </div>
</section>

<section id="stages" class="nb-sec" aria-labelledby="stages-heading">
  <div class="nb-wrap">
    <div class="nb-eyebrow">The stages</div>
    <h2 class="nb-h2" id="stages-heading">Five stages, each priced and bought separately</h2>
    <p class="nb-lede">Every engagement has a fixed scope, a fixed price, and something you keep at the end of it. Most clients take one stage, see the result, and decide from there.</p>
    {stages}  </div>
</section>
'''
main += cta_block(f'{HOME}#engagement', 'Back to pricing')
written.append(build('how-we-work.html', 'How we work | Nielsen & Brown',
    'The five questions behind every AI decision, and the five stages of work from the free AI Readiness Score to ongoing support, each with a fixed scope and price.',
    'how-we-work', 'How we work: five questions, then five stages', main, []))

# ── /services/* ─────────────────────────────────────────────────────────────
SLUGS = ['ai-strategy-and-roadmap', 'team-enablement', 'workflow-automation', 'governance-and-compliance']
TITLE_FIX = {'Team training and adoption': 'Team enablement and adoption'}
for slug, (label, name, para, psr) in zip(SLUGS, services):
    name = TITLE_FIX.get(name, name)
    extra_link = '<a href="/governance">How we keep AI use safe</a>' if slug == 'governance-and-compliance' else ''
    main = page_head(label, name, para, crumb=(f'{HOME}#engagement', 'What we do'))
    main += f'''<section class="nb-sec nb-sec--mid" aria-labelledby="practice-heading">
  <div class="nb-wrap">
    <div class="nb-eyebrow">In practice</div>
    <h2 class="nb-h2" id="practice-heading">What it looks like in practice</h2>
    <div class="nb-example nb-prose">
      {psr}
    </div>
    <div class="nb-inline-links">
      <a href="/results">See more results</a>
      <a href="{HOME}#engagement">See what it costs</a>
      {extra_link}
    </div>
  </div>
</section>
'''
    main += cta_block('/results', 'See more results')
    plain = re.sub(r'<[^>]+>', '', para)
    service_node = {'@type': 'Service', '@id': f'{BASE}/services/{slug}#service', 'name': html.unescape(name),
                    'description': html.unescape(plain), 'serviceType': html.unescape(name),
                    'provider': {'@id': ORG_ID}, 'areaServed': {'@type': 'Country', 'name': 'United Kingdom'},
                    'url': f'{BASE}/services/{slug}'}
    written.append(build(f'services/{slug}.html', f'{html.unescape(name)} | Nielsen & Brown',
        html.unescape(plain), slug, html.unescape(name), main, [service_node]))

# ── /results ────────────────────────────────────────────────────────────────
blocks = ''
for slug, (label, name, para, psr) in zip(SLUGS, services):
    name = TITLE_FIX.get(name, name)
    blocks += f'''      <article class="nb-result">
        <div><div class="nb-eyebrow">{label}</div><h2><a href="/services/{slug}">{name}</a></h2></div>
        <div class="nb-example">{psr}</div>
      </article>
'''
main = page_head('Results', 'What the work looks like in practice',
                 'Four examples, one for each thing we help with: the problem, what was done, and what changed.')
main += f'''<section class="nb-sec nb-sec--mid" aria-label="Examples">
  <div class="nb-wrap">
    <div class="nb-results">
{blocks}    </div>
    <div class="nb-inline-links"><a href="{HOME}#engagement">See what each engagement costs</a></div>
  </div>
</section>
'''
main += cta_block(f'{HOME}#engagement', 'See pricing')
written.append(build('results.html', 'Results | Nielsen & Brown',
    'What the work looks like in practice across AI strategy, team enablement, workflow automation and governance: the problem, what was done, and the result.',
    'results', 'Results: what the work looks like in practice', main, []))

# ── /governance ─────────────────────────────────────────────────────────────
main = page_head('Staying safe', 'The time savings, without the worry',
                 'AI should not come with a quiet build-up of data risk, compliance risk, or a mistake in front of a client. The safeguards are part of the work itself, not bolted on afterwards.')
main += f'''<section class="nb-sec nb-sec--mid" aria-labelledby="safeguards-heading">
  <div class="nb-wrap">
    <div class="nb-eyebrow">Built into every engagement</div>
    <h2 class="nb-h2" id="safeguards-heading">Six safeguards, from the first day</h2>
    {assurance_cards}    </div>
  </div>
</section>

<section class="nb-sec" aria-labelledby="adm-heading">
  <div class="nb-wrap"><div class="nb-prose">
    <div class="nb-eyebrow">The law, in plain English</div>
    <h2 id="adm-heading">Automated decisions: what changed in February 2026</h2>
    <p>The Data (Use and Access) Act 2025 replaced Article 22 of UK GDPR with new Articles 22A to 22D, in force from 5 February 2026. The rules apply when a decision about a person is made solely by automated processing, meaning with no meaningful human involvement, and has a legal or similarly significant effect on them.</p>
    <p>Those decisions are now allowed in more situations than before, but only with safeguards in place. The business must:</p>
    <ul>
      <li>tell people about decisions made about them</li>
      <li>let them make representations about a decision</li>
      <li>let them get a person to intervene</li>
      <li>let them contest the decision</li>
    </ul>
    <p>Stricter limits still apply where special category data is involved, such as health information. A significant decision based solely on automated processing of that data needs the explicit consent of the person, or a legal basis that specifically allows it.</p>
    <p>The ICO consulted on updated guidance in spring 2026. The practical point for a business is simple: where a decision affects someone significantly, such as hiring, pay or access to a service, keep a person involved who has the authority and the information to change the outcome, not someone approving whatever the system says, and write down how that works.</p>
    <p class="nb-small">General information, not legal advice. Source: <a href="https://www.legislation.gov.uk/ukpga/2025/18/section/80" target="_blank" rel="noopener">Data (Use and Access) Act 2025, section 80</a>.</p>
  </div></div>
</section>

<section class="nb-sec nb-sec--mid" aria-labelledby="iso-heading">
  <div class="nb-wrap"><div class="nb-prose">
    <div class="nb-eyebrow">Standards</div>
    <h2 id="iso-heading">ISO/IEC 42001, and whether it applies to you</h2>
    <p>ISO/IEC 42001, published in December 2023, is the international standard for an AI management system: the policies, objectives and processes an organisation uses to develop, provide or use AI responsibly. Like ISO/IEC 27001 for information security, it can be certified by an independent auditor.</p>
    <p>Certification is voluntary. It tends to matter when a large client, a tender or a regulator asks for evidence that AI use is governed properly.</p>
    <p>The groundwork overlaps with what we put in place anyway: a usage policy, a risk register, clear ownership, and a record of how AI is used. That is a sensible starting point whether or not certification is ever the goal.</p>
    <div class="nb-inline-links">
      <a href="{HOME}#engagement">See where to start</a>
      <a href="/services/governance-and-compliance">Governance and compliance</a>
    </div>
  </div></div>
</section>
'''
main += cta_block(f'{HOME}#engagement', 'See pricing')
written.append(build('governance.html', 'AI governance and safeguards | Nielsen & Brown',
    'The safeguards built into every engagement, what the UK rules on automated decision-making mean for your business, and where ISO/IEC 42001 fits.',
    'governance', 'AI governance and safeguards', main, []))

# ── /faq ────────────────────────────────────────────────────────────────────
faq_region = between(test, '<div class="faq-list" role="list">', '<section id="cta-banner"')
home_faq = {q: a for q, a in re.findall(
    r'<button type="button" class="faq-question"[^>]*>\s*<span>([^<]*)</span>.*?<div class="faq-answer">(.*?)</div>', faq_region, re.S)}
assert len(home_faq) == 6, home_faq.keys()
FAQS = [
    ('Will this feel like a big consultancy engagement', home_faq['Will this feel like a big consultancy engagement']),
    ('What does Nielsen &amp; Brown actually do', home_faq['What does Nielsen &amp; Brown actually do'].replace(
        'training the team to use it', 'helping the team use it')),   # spec: enablement, not training
    ('Is this only for big companies', home_faq['Is this only for big companies'].replace(
        'strategy, training, and building', 'strategy, enablement, and building')),
    ('What is the best first project for a business our size', home_faq['What is the best first project for a business our size']),
    ('How much does it cost', home_faq['How much does it cost'].replace('href="#engagement"', f'href="{HOME}#engagement"')),
    ('How do we keep our data safe', home_faq['How do we keep our data safe']),
    ('What does a typical engagement look like',
     f'Most businesses start with the free AI Readiness Score. The next step is small, fixed and specific, and most clients take one and stop there if it is not working. Larger work, such as automation at scale or a full diagnostic and roadmap, follows once a first step has shown it is worth doing. Every stage has a fixed scope and a fixed price. <a href="/how-we-work">See the stages in full</a>.'),
    ('How is Nielsen &amp; Brown different from a freelance AI consultant',
     'A freelancer is usually one person with one specialism. We cover strategy, enablement, building and governance as one team, so there is no need to coordinate several suppliers or manage the handovers between them.'),
    ('Should we buy AI software or build a custom tool',
     'Buy where a good off-the-shelf tool fits how the team works. Build where it does not. We are independent of any single software company, so the recommendation is based on what fits the business, not on what we are paid to sell.'),
    ('What AI governance does a business our size actually need',
     'At a minimum: an AI usage policy, a simple risk register, clear ownership of decisions, a person checking anything customer-facing or higher risk, and a record of how AI is used. That baseline is part of every engagement, not an add-on. <a href="/governance">More on how we keep AI use safe</a>.'),
    ('Where are you based, and do you work across the UK',
     'We are based at Bartle House, Oxford Court, in Manchester, and work with businesses across the UK. Most of the work is remote, and where on site work is needed, such as in person sessions, we travel.'),
]
icon = '<span class="faq-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg></span>'
items = ''.join(f'''      <div class="faq-item" role="listitem">
        <button type="button" class="faq-question" aria-expanded="false">
          <span>{q}</span>
          {icon}
        </button>
        <div class="faq-answer">{a.strip()}</div>
      </div>
''' for q, a in FAQS)
main = page_head('Questions people ask', 'Frequently asked questions',
                 'Straight answers on cost, data, how the work runs, and what to expect. If the answer you need is not here, the first call is free.')
main += f'''<section id="faq" class="nb-sec nb-sec--mid" aria-label="Questions and answers">
  <div class="nb-wrap">
    <div class="faq-list" role="list">
{items}    </div>
  </div>
</section>
'''
main += cta_block(f'{HOME}#engagement', 'See pricing')
faq_node = {'@type': 'FAQPage', '@id': BASE + '/faq#faq', 'mainEntity': [
    {'@type': 'Question', 'name': html.unescape(q),
     'acceptedAnswer': {'@type': 'Answer', 'text': html.unescape(re.sub(r'<[^>]+>', '', a)).strip()}} for q, a in FAQS]}
written.append(build('faq.html', 'Frequently asked questions | Nielsen & Brown',
    'Answers to common questions about working with Nielsen & Brown: cost, data safety, typical engagements, where we are based, and whether to buy or build AI tools.',
    'faq', 'Frequently asked questions', main, [faq_node]))

print('\n'.join('  wrote ' + w for w in written))
