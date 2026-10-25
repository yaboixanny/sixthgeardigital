#!/usr/bin/env python3
"""Render industry content into static pages, homepage links, SVGs, and sitemap.
Run from any directory: python3 scripts/build_industries.py
Edit content/industries.json and templates/industry.html, then regenerate.
"""
from pathlib import Path
from string import Template
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://sixthgeardigital.com'
PAGES = json.loads((ROOT / 'content/industries.json').read_text())
TEMPLATE = Template((ROOT / 'templates/industry.html').read_text())
DATE = '2026-10-25'

def e(value):
    return escape(str(value), quote=True)

# Original schematic illustrations, kept local and intentionally non-photographic.
DRAWINGS = [
    '<rect x="130" y="175" width="220" height="86" rx="9"/><path d="M350 200h115v36H350M130 200H92v36h38M168 175v86M314 175v86M190 175v-25h25v25M265 261v35h25v-35"/><path class="hot" d="M202 150v-32h-80q-35 0-35 35v165h190v-22"/><circle cx="277" cy="317" r="7"/>',
    '<path d="M230 135h120v45H230zM248 180h84v140h-84zM270 320h40v48h-40zM230 135l-35-36h190l-35 36M248 205h84M248 290h84"/><path class="hot" d="M290 368v22M180 200h-30v100h30M400 200h30v100h-30"/><circle cx="252" cy="157" r="7"/><circle cx="328" cy="157" r="7"/>',
    '<path d="M100 175h280v130H100zM380 215h66l55 58v32H380M400 230h35l31 35h-66z"/><circle cx="170" cy="313" r="26"/><circle cx="439" cy="313" r="26"/><path class="hot" d="M125 203h225M125 223h180M125 243h130M130 276h220"/><path d="M85 340h430"/>',
    '<path d="M100 160h400v165H100zM85 160l30-25h370l30 25M117 325v20M483 325v20M130 190h82v63h-82zM242 190h82v63h-82zM370 190h88v135h-88zM414 190v135"/><path class="hot" d="M130 221h82M242 221h82M388 259h8M436 259h8"/><path d="M90 346h420"/>',
    '<path d="M110 250h185v65H110zM140 250v-65h105v65M145 185l18-32h103v97M266 153v162M305 150v170h135M325 150v150h115M215 215l29 35M155 215h39"/><circle cx="152" cy="315" r="27"/><circle cx="265" cy="315" r="23"/><path class="hot" d="M350 270h115v30H350zM350 225h115v40H350z"/>',
    '<rect x="100" y="170" width="400" height="155" rx="5"/><path d="M120 325v20h360v-20M200 170v155M380 170v155M400 195h80v50h-80zM130 195v80M150 195v80M170 195v80M415 170v-35h30v35"/><path class="hot" d="M302 193l-48 67h40l-17 45 60-78h-45z"/><circle cx="420" cy="275" r="8"/><circle cx="455" cy="275" r="8"/>',
    '<path d="M115 135h370v210H115zM145 165h225v130H145zM145 315h225M390 165h70v65h-70zM390 250h70v65h-70zM140 345v15M460 345v15M258 165v40M242 205h32v30h-32zM170 285h175"/><path class="hot" d="M258 235v25M230 285v-25h55v25M400 182h50M400 201h30"/><circle cx="415" cy="266" r="5"/><circle cx="440" cy="266" r="5"/>',
    '<path d="M80 285h340v30H80zM420 230h60l48 55v30h-88M440 244h30l24 31h-54zM130 285v-85h230v85M130 200l115-55 115 55M245 145v140"/><circle cx="118" cy="324" r="18"/><circle cx="165" cy="324" r="18"/><circle cx="350" cy="324" r="18"/><circle cx="465" cy="324" r="23"/><path class="hot" d="M190 214v71M300 214v71M155 245h180"/>',
    '<path d="M110 145h380v190H110zM135 175h220v160M245 175v160M380 175h85v65h-85zM385 265h75M385 282h75M385 299h75"/><path class="hot" d="M415 190v35M400 199l30 17M430 199l-30 17M415 190l-5 5M415 190l5 5M415 225l-5-5M415 225l5-5"/><path d="M223 245v25M266 245v25M95 335h410"/>',
    '<path d="M85 210l215-100 215 100M110 200v145M490 200v145M300 110v235M110 345h380M110 200l190 145M490 200L300 345M180 167v178M420 167v178"/><path class="hot" d="M85 210h430M110 345h380M180 167l120 58 120-58"/>',
    '<path d="M130 115v245M240 115v245M350 115v245M460 115v245M110 135h370M110 225h370M110 315h370M120 360h30M230 360h30M340 360h30M450 360h30"/><path class="hot" d="M130 135l110 90-110 90M240 135l110 90-110 90M350 135l110 90-110 90"/>',
    '<path d="M140 340h170v20H140zM170 340v-60h90v60M215 280l65-85M280 195l-70-70M210 125l-65 35M145 160l-30 35M145 160l15 40M350 300h155v35H350M370 335v25M485 335v25"/><circle cx="215" cy="280" r="21"/><circle cx="280" cy="195" r="20"/><circle cx="210" cy="125" r="16"/><path class="hot" d="M233 259l31-46M262 180l-38-39M350 285h155M390 285v-45h75v45"/>'
]

def illustration(index, page):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 490" role="img" aria-labelledby="title"><title id="title">{e(page['short'])} schematic illustration</title><defs><pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#29374e" stroke-width=".6"/></pattern></defs><rect width="600" height="490" fill="#131b2e"/><rect width="600" height="490" fill="url(#grid)"/><circle cx="300" cy="242" r="181" fill="none" stroke="#364358" stroke-dasharray="3 9"/><style>.hot{{stroke:#fd833f}}</style><g stroke="#b7cbe5" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">{DRAWINGS[index]}</g><g stroke="#596b86" fill="none"><path d="M80 385H520M80 377v16M520 377v16M65 110v240M58 110h14M58 350h14"/></g><g fill="#8da3c0" font-family="monospace" font-size="10" letter-spacing="2"><text x="80" y="87">SG / INDUSTRY {index+1:02}</text><text x="415" y="87">CAPABILITY</text></g></svg>'''

for index, page in enumerate(PAGES):
    slug = page['slug']
    assert re.fullmatch(r'[a-z0-9-]+', slug), slug
    canonical = f'{BASE}/industries/{slug}.html'
    title = f"{page['short']} Marketing | Sixth Gear Digital"
    description = page['description']
    challenge_cards = ''.join(f'<article class="card"><span class="card-number">{i:02} / CHALLENGE</span><h3>{e(t)}</h3><p>{e(b)}</p></article>' for i,(t,b) in enumerate(page['challenges'],1))
    playbook_cards = ''.join(f'<article class="card play-card"><span class="card-number">{i:02}</span><h3>{e(t)}</h3><p>{e(b)}</p></article>' for i,(t,b) in enumerate(page['playbook'],1))
    capability_cards = ''.join(f'<article class="card capability-card"><span class="capability-mark" aria-hidden="true">{i:02}</span><div><h3>{e(t)}</h3><p>{e(b)}</p></div></article>' for i,(t,b) in enumerate(page['capabilities'],1))
    labels = ['Buyer intent', 'Relevant destination', 'Sales handoff']
    scenario_cards = ''.join(f'<div class="scenario-card"><h3>{i:02} / {label}</h3><p>{e(body)}</p></div>' for i,(label,body) in enumerate(zip(labels,page['scenario']),1))
    faq_items = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in page['faqs'])
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'isPartOf':{'@id':BASE+'/#website'},'about':{'@type':'Service','name':page['short']+' marketing','provider':{'@type':'Organization','@id':BASE+'/#organization','name':'Sixth Gear Digital','url':BASE+'/'}},'breadcrumb':{'@id':canonical+'#breadcrumb'}},
        {'@type':'BreadcrumbList','@id':canonical+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Industries','item':BASE+'/#industries'},{'@type':'ListItem','position':3,'name':page['short'],'item':canonical}]}]}
    fields = {k:e(v) for k,v in page.items() if isinstance(v,str)}
    brief = page['buyer_brief']
    brief_links = ' and '.join(f'<a href="/services/{e(link["service"])}/">{e(link["label"])}</a>' for link in brief['links'])
    fields['buyer_brief'] = '<section class="section container buyer-brief"><p class="eyebrow accent">PLANNING THE BUYER JOURNEY</p><h2>What makes a useful inquiry in this sector?</h2><div class="grid three">' + ''.join(f'<article class="card"><h3>{label}</h3><p>{e(brief[key])}</p></article>' for key,label in [('decision','The buying decision'),('page','The page and intake'),('handoff','The qualification check')]) + '</div><p class="context-links">Build this journey with ' + brief_links + '.</p></section>'

    fields.update(title=e(title),description=e(description),canonical=e(canonical),number=f'{index+1:02}',form_name='industry-'+slug,short_lower=e(page['short'].lower()),goal_placeholder=e('For example: '+page['goal'].lower()),challenge_cards=challenge_cards,playbook_cards=playbook_cards,capability_cards=capability_cards,scenario_cards=scenario_cards,faq_items=faq_items,query_tags=''.join(f'<span class="tag">{e(x)}</span>' for x in page['queries']),intake_tags=''.join(f'<span class="tag">{e(x)}</span>' for x in page['intake']),capability_options=''.join(f'<option value="{e(t)}">{e(t)}</option>' for t,_ in page['capabilities']),structured_data=json.dumps(schema,ensure_ascii=False).replace('<','\\u003c'))
    services = json.loads((ROOT / 'content/services.json').read_text())
    fields['service_links'] = ''.join(f'<a href="/services/{e(service["slug"])}/">{e(service["short"])}</a>' for service in services)
    (ROOT / 'industries' / f'{slug}.html').write_text(TEMPLATE.substitute(fields))
    (ROOT / 'assets/industries' / f'{slug}.svg').write_text(illustration(index,page))

# The homepage is the curated directory for the twelve user-requested industries.
# Industry pages link back to this hub and to supporting agency services;
# no automatic cross-industry related-content recommendations are generated.
links = ''.join(f'''<a class="industry-directory-card" href="/industries/{e(p['slug'])}.html"><span class="industry-directory-number">{i:02} / INDUSTRY</span><h3>{e(p['short'])}</h3><p>{e(p['goal'])}</p><span class="industry-directory-link">Explore {e(p['short'].lower())} marketing <span aria-hidden="true">↗</span></span></a>''' for i,p in enumerate(PAGES,1))
section = f'''<!-- SECTION: WHO WE HELP -->
<section class="py-24 lg:py-32 bg-brand-surface border-b border-brand-border" id="industries">
<div class="max-w-7xl mx-auto px-6 lg:px-12"><div class="max-w-3xl mb-16"><span class="text-xs font-bold uppercase tracking-widest text-brand-orange">Operational Sectors</span><h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-brand-charcoal tracking-tight mt-3">Built for the Way Industrial Buyers Buy.</h2><p class="text-lg text-brand-muted mt-4">Explore a marketing approach built around your equipment, capabilities, and commercial sales cycle.</p></div><div class="industry-directory">{links}</div></div></section>
'''
p = ROOT / 'index.html'
s = p.read_text()
s, count = re.subn(r'<!-- SECTION: WHO WE HELP -->.*?(?=<!-- SECTION: OPPORTUNITY MODEL MATRIX -->)',lambda _:section,s,flags=re.S)
assert count == 1, 'Homepage industry section marker missing'
p.write_text(s)

# Preserve existing pages, then replace only the generated industry sitemap block.
p = ROOT / 'sitemap.xml'
s = re.sub(r'\s*<!-- INDUSTRY PAGES START -->.*?<!-- INDUSTRY PAGES END -->','',p.read_text(),flags=re.S)
entries = '\n'.join(f'  <url>\n    <loc>{BASE}/industries/{p["slug"]}.html</loc>\n    <lastmod>{DATE}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>' for p in PAGES)
s = s.replace('</urlset>',f'  <!-- INDUSTRY PAGES START -->\n{entries}\n  <!-- INDUSTRY PAGES END -->\n</urlset>')
p.write_text(s)
print(f'Built {len(PAGES)} industry pages and illustrations; updated homepage directory and sitemap.')
