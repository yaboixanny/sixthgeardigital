#!/usr/bin/env python3
"""Generate the four static service routes, homepage links, and sitemap entries."""
from pathlib import Path
from string import Template
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://sixthgeardigital.com'
DATE = '2026-10-25'
SERVICES = json.loads((ROOT/'content/services.json').read_text())
INDUSTRIES = json.loads((ROOT/'content/industries.json').read_text())
TEMPLATE = Template((ROOT/'templates/service.html').read_text())
HERO = '/assets/images/industrial-services-512.webp'

def e(s): return escape(str(s),quote=True)
def route(s): return '/services/'+s['slug']+'/'

def links(current=None):
 return ''.join(f'<a href="{route(s)}"'+(' aria-current="page"' if s['slug']==current else '')+f'>{e(s["short"])}</a>' for s in SERVICES)

HEADINGS = {
 'industrial-google-ads':('Make the search match the commercial opportunity.','Campaign quality depends on targeting, the page a buyer reaches, and what happens when they get in touch.','Four foundations of industrial paid search.','Campaigns shaped around how your buyers buy.'),
 'industrial-seo':('Make technical expertise easy to discover.','Useful visibility begins with clear architecture, accurate content, and pages that answer a real buying question.','Build search visibility on useful foundations.','Cover the searches that support supplier selection.'),
 'industrial-websites':('Give every buying situation a clear next step.','The page should help a buyer understand fit and help your sales team start with useful information.','Design the whole inquiry journey.','Three page types. Three different sales conversations.'),
 'industrial-lead-tracking':('Keep the opportunity visible after first contact.','Source information, clear stages, and consistent follow-up make the reporting more useful to both marketing and sales.','Connect the stages that matter to sales.','Track opportunities at the pace they actually move.')
}
RELATIONS = {
 'industrial-google-ads': ['Use search findings to inform useful long-term service and application content.','Give each campaign a landing page and inquiry path suited to the buyer.','Connect paid inquiries with qualification, quotes, and recorded sales outcomes.'],
 'industrial-seo': ['Pursue selected commercial search demand alongside your organic content work.','Build clear, usable pages that support technical evaluation and contact.','Understand whether organic inquiries progress into suitable sales opportunities.'],
 'industrial-websites': ['Bring relevant commercial demand to a page designed for that buying situation.','Give the website a clear architecture and useful content for search discovery.','Connect the website’s forms and calls with an owner, next action, and outcome.'],
 'industrial-lead-tracking': ['Give campaign reviews feedback on inquiry fit and recorded sales outcomes.','Review the quality of opportunities arriving through organic search.','Capture the right inquiry details and create a dependable handoff from the website.']
}

EXAMPLE_FIELDS = [
 ('dispatch','Dispatch page',[('Job location','Site address or service area'),('Equipment & issue','Machine type and a short description'),('Urgency','When service is required'),('Callback details','Name and phone number')],'Route the request to the service desk with the job location, issue, and callback details.'),
 ('equipment','Equipment quote',[('Equipment requirement','Product category or model'),('Operating application','Use, capacity, or fit requirements'),('Purchase or rental','Buying intent and timing'),('Delivery location','Where the equipment is needed')],'Give the equipment representative enough context to discuss suitability, availability, and the quote.'),
 ('project','Project inquiry',[('Project scope','What the buyer is planning'),('Site or delivery location','Where the work or supply is needed'),('Project stage','Research, specification, or ready to quote'),('Target schedule','Milestones or required delivery dates')],'Start a project discovery conversation before arranging detailed plans or technical-file transfer.')
]
def form_examples():
 tabs=''.join(f'<button type="button" role="tab" id="tab-{key}" aria-controls="panel-{key}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{label}</button>' for i,(key,label,_,_) in enumerate(EXAMPLE_FIELDS))
 panels=''
 for i,(key,label,fields,note) in enumerate(EXAMPLE_FIELDS):
  rows=''.join(f'<div class="example-field"><span>{e(a)}</span><p>{e(b)}</p></div>' for a,b in fields)
  panels+=f'<div role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}" tabindex="0"'+(' hidden' if i else '')+f'><div class="example-fields">{rows}</div><p class="handoff-note"><strong>Sales handoff:</strong> {e(note)}</p></div>'
 return '<div class="form-examples"><p class="eyebrow accent">INTAKE DESIGN EXAMPLES</p><h3>See what sales needs from each inquiry.</h3><p>Select a buying situation to compare example fields and the handoff they support. These are field examples, not submission forms.</p><div class="example-tabs" role="tablist" aria-label="Inquiry examples">'+tabs+'</div>'+panels+'</div>'

for s in SERVICES:
 canonical=BASE+route(s); title=s['name']+' | Sixth Gear Digital'
 desc=s['description']
 h=HEADINGS[s['slug']]
 fields={k:e(v) for k,v in s.items() if isinstance(v,str)}
 fields.update(title=e(title),description=e(desc),canonical=e(canonical),hero_image=e(HERO),form_name='service-'+s['slug'],service_navigation=links(s['slug']),footer_links=links(s['slug']),challenge_title=e(h[0]),challenge_intro=e(h[1]),approach_title=e(h[2]),types_title=e(h[3]),example_title=e(s['example'][0]),form_examples=form_examples() if s['slug']=='industrial-websites' else '')
 fields['journey_steps']=''.join(f'<div><span>{i:02}</span><strong>{e(t)}</strong></div>' for i,t in enumerate(s['steps'],1))
 fields['outcome_cards']=''.join(f'<div class="outcome"><h2>{e(a)}</h2><p>{e(b)}</p></div>' for a,b in s['outcomes'])
 fields['challenge_cards']=''.join(f'<article class="card"><span class="card-number">{i:02} / CHALLENGE</span><h3>{e(a)}</h3><p>{e(b)}</p></article>' for i,(a,b) in enumerate(s['challenges'],1))
 fields['pillar_cards']=''.join(f'<article class="card service-pillar"><div class="pillar-top"><span class="card-number">{i:02}</span><span class="eyebrow">{e(s["short"])}</span></div><h3>{e(a)}</h3><p>{e(b)}</p><div class="pillar-strip">{e(c)}</div></article>' for i,(a,b,c) in enumerate(s['pillars'],1))
 fields['type_cards']=''.join(f'<article class="card type-card"><h3>{e(a)}</h3><p>{e(b)}</p><ul>'+''.join(f'<li>{e(x)}</li>' for x in c)+'</ul></article>' for a,b,c in s['types'])
 fields['example_stages']=''.join(f'<div class="example-stage"><h3>{label}</h3><p>{e(body)}</p></div>' for label,body in zip(['The buyer','The next step','The sales connection'],s['example'][1:]))
 fields['scope_cards']=''.join(f'<article class="card scope-card"><span class="card-number">{i:02} / SCOPE</span><h3>{e(a)}</h3><p>{e(b)}</p><a class="button'+('' if i==2 else ' button-secondary')+'" href="#audit-form">Discuss this scope <span aria-hidden="true">↗</span></a></article>' for i,(a,b) in enumerate(s['scope'],1))
 others=[x for x in SERVICES if x['slug']!=s['slug']]
 fields['related_services']=''.join(f'<a class="related-service" href="{route(other)}"><h3>{e(other["name"])}</h3><p>{e(reason)}</p><span>Explore {e(other["short"])} ↗</span></a>' for other,reason in zip(others,RELATIONS[s['slug']]))
 fields['faq_items']=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in s['faqs'])
 fields['industry_options']=''.join(f'<option value="{e(p["slug"])}">{e(p["short"])}</option>' for p in INDUSTRIES)
 fields['form_options']=''.join(f'<option value="{e(x)}">{e(x)}</option>' for x in s['form_options'])
 schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'isPartOf':{'@id':BASE+'/#website'},'name':title,'description':desc,'about':{'@id':canonical+'#service'},'breadcrumb':{'@id':canonical+'#breadcrumb'}},{'@type':'Service','@id':canonical+'#service','name':s['name'],'url':canonical,'description':desc,'provider':{'@type':'Organization','@id':BASE+'/#organization','name':'Sixth Gear Digital','url':BASE+'/'}},{'@type':'BreadcrumbList','@id':canonical+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Services','item':BASE+'/#services'},{'@type':'ListItem','position':3,'name':s['name'],'item':canonical}]}]}
 fields['structured_data']=json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')
 folder=ROOT/'services'/s['slug']; folder.mkdir(parents=True,exist_ok=True)
 (folder/'index.html').write_text(TEMPLATE.substitute(fields))

# Preserve homepage design while making each offering a real destination.
lead=SERVICES[0]
other_cards=''.join(f'<a class="core-service-card" href="{route(s)}"><span class="core-service-number">0{i}</span><h3>{e(s["name"])}</h3><p>{e(s["intro"])}</p><span class="core-service-link">Explore {e(s["short"])} ↗</span></a>' for i,s in enumerate(SERVICES[1:],2))
section=f'''<!-- SECTION: SERVICES -->
<section class="py-24 lg:py-32 bg-brand-midnight text-white" id="services"><div class="max-w-7xl mx-auto px-6 lg:px-12"><div class="max-w-3xl mb-16"><span class="text-xs font-bold uppercase tracking-widest text-brand-amber">Core Services</span><h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight mt-3">Connect the Search to the Sales Opportunity.</h2><p class="text-lg text-slate-400 mt-4">Google Ads leads the way, supported by useful search content, clear websites, and visibility into what happens after the inquiry.</p></div><div class="core-services-grid"><a class="core-service-card core-service-lead" href="{route(lead)}"><span class="core-service-number">01 / LEAD SERVICE</span><h3>{e(lead['name'])}</h3><p>{e(lead['intro'])}</p><ul><li>Keyword selection and commercial search intent</li><li>Location strategy and relevant landing pages</li><li>Calls, RFQs, and qualified opportunity tracking</li></ul><span class="core-service-link">Explore Industrial Google Ads ↗</span></a><div class="core-service-stack">{other_cards}</div></div></div></section>
'''
p=ROOT/'index.html'; html=p.read_text()
html,count=re.subn(r'<!-- SECTION: SERVICES -->.*?(?=<!-- SECTION: THE 4-STEP BLUEPRINT -->)',lambda _:section,html,flags=re.S)
assert count==1,'Homepage service markers missing'
footer_labels={'Google Ads for Industrial OEM':SERVICES[0],'Industrial Technical SEO':SERVICES[1],'Industrial Websites &amp; RFQs':SERVICES[2],'Lead &amp; Pipeline Measurement':SERVICES[3]}
for label,service in footer_labels.items():
 html=html.replace(f'href="#services">{label}</a>',f'href="{route(service)}">{e(service["short"])}</a>')
p.write_text(html)

p=ROOT/'sitemap.xml'; xml=re.sub(r'\s*<!-- SERVICE PAGES START -->.*?<!-- SERVICE PAGES END -->','',p.read_text(),flags=re.S)
entries='\n'.join(f'  <url>\n    <loc>{BASE}{route(s)}</loc>\n    <lastmod>{DATE}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{"0.9" if i==0 else "0.8"}</priority>\n  </url>' for i,s in enumerate(SERVICES))
xml=xml.replace('</urlset>',f'  <!-- SERVICE PAGES START -->\n{entries}\n  <!-- SERVICE PAGES END -->\n</urlset>');p.write_text(xml)
print('Built all four service routes; updated homepage service links and sitemap.')
