#!/usr/bin/env python3
"""Generate the four static service routes, homepage links, and sitemap entries."""
from pathlib import Path
from string import Template
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://sixthgeardigital.com'
DATE = '2026-10-26'
SERVICES = json.loads((ROOT/'content/services.json').read_text())
INDUSTRIES = json.loads((ROOT/'content/industries.json').read_text())
TEMPLATE = Template((ROOT/'templates/service.html').read_text())
HERO = '/assets/images/industrial-services-512.webp'

def e(s): return escape(str(s),quote=True)
def route(s): return '/services/'+s['slug']+'/'

def links(current=None):
 return ''.join(f'<a href="{route(s)}"'+(' aria-current="page"' if s['slug']==current else '')+f'>{e(s["short"])}</a>' for s in SERVICES)

HEADINGS = {
 'industrial-google-ads':('Make your ads useful to the people who see them.','The search term, the page and the response all affect whether an ad brings useful work.','How we manage your Google Ads.','Different needs call for different ads.'),
 'industrial-seo':('Help buyers find clear answers.','Your website should make it easy to understand what you do and how to contact you.','How we improve your website for search.','Pages for the questions buyers ask.'),
 'industrial-websites':('Make the next step easy to find.','A useful page answers the buyer’s questions and helps your team respond.','How we plan and build your pages.','Three pages for three different needs.'),
 'industrial-lead-tracking':('Keep track of requests after they arrive.','Clear records help your team know who needs a reply and what happens next.','How we organize requests and follow-up.','Keep track of each type of request.')
}
RELATIONS = {
 'industrial-google-ads': ['Use what you learn from ads to improve the pages people find through search.','Give each ad a clear page where people can call or ask for a quote.','See which ad inquiries lead to quotes and jobs.'],
 'industrial-seo': ['Run ads for selected services while you improve the website.','Make your pages clear and easy to use.','Find out whether search visitors become useful customer inquiries.'],
 'industrial-websites': ['Help people find your service pages through ads.','Help people find your pages through search.','Keep track of calls, forms and follow-up after someone visits your site.'],
 'industrial-lead-tracking': ['Use sales feedback to see which ads bring useful work.','Review the inquiries that come from search.','Ask useful questions on your forms and send requests to the right person.']
}
EXAMPLE_FIELDS = [
 ('dispatch','Repair service',[('Job location','Where the equipment is'),('Equipment and problem','Machine type and what went wrong'),('How urgent is it?','When help is needed'),('Contact details','Name and phone number')],'Your service team can check the job, location and urgency before calling back.'),
 ('equipment','Equipment quote',[('Equipment needed','Type or model'),('What is the job?','How the equipment will be used'),('Purchase or rental','Which option and when it is needed'),('Delivery location','Where the equipment needs to go')],'Your sales team can check fit and availability before preparing a quote.'),
 ('project','Project quote',[('Type of work','What the buyer is planning'),('Site or delivery location','Where the work is needed'),('Project stage','Early planning or ready for a quote'),('Required dates','When the work needs to happen')],'Your team can discuss the basics before asking for plans or other files.')
]

def form_examples():
 tabs=''.join(f'<button type="button" role="tab" id="tab-{key}" aria-controls="panel-{key}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{label}</button>' for i,(key,label,_,_) in enumerate(EXAMPLE_FIELDS))
 panels=''
 for i,(key,label,fields,note) in enumerate(EXAMPLE_FIELDS):
  rows=''.join(f'<div class="example-field"><span>{e(a)}</span><p>{e(b)}</p></div>' for a,b in fields)
  panels+=f'<div role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}" tabindex="0"'+(' hidden' if i else '')+f'><div class="example-fields">{rows}</div><p class="handoff-note"><strong>What happens next:</strong> {e(note)}</p></div>'
 return '<div class="form-examples"><p class="eyebrow accent">EXAMPLE FORM QUESTIONS</p><h3>Ask the questions your team needs answered.</h3><p>Choose a type of request to see example questions. These examples do not send a message.</p><div class="example-tabs" role="tablist" aria-label="Form question examples">'+tabs+'</div>'+panels+'</div>'

for s in SERVICES:
 canonical=BASE+route(s); title=s['name']+' | Sixth Gear Digital'
 desc=s['description']
 h=HEADINGS[s['slug']]
 fields={k:e(v) for k,v in s.items() if isinstance(v,str)}
 fields.update(title=e(title),description=e(desc),canonical=e(canonical),hero_image=e(HERO),form_name='service-'+s['slug'],service_navigation=links(s['slug']),footer_links=links(s['slug']),challenge_title=e(h[0]),challenge_intro=e(h[1]),approach_title=e(h[2]),types_title=e(h[3]),example_title=e(s['example'][0]),form_examples=form_examples() if s['slug']=='industrial-websites' else '')
 fields['journey_steps']=''.join(f'<div><span>{i:02}</span><strong>{e(t)}</strong></div>' for i,t in enumerate(s['steps'],1))
 fields['outcome_cards']=''.join(f'<div class="outcome"><h2>{e(a)}</h2><p>{e(b)}</p></div>' for a,b in s['outcomes'])
 # The website service uses a simpler hero; retain the shared layout elsewhere.
 simplified_hero = s['slug'] == 'industrial-websites'
 fields['service_navigation_block'] = '' if simplified_hero else '<nav class="service-nav container" aria-label="Core services">'+fields['service_navigation']+'</nav>'
 fields['hero_badge'] = '' if simplified_hero else '<span class="badge"><i></i>'+fields['badge']+'</span>'
 fields['secondary_hero_action'] = '' if simplified_hero else '<a class="button button-secondary" href="#approach">See how we work <span aria-hidden="true">↓</span></a>'
 fields['outcomes_block'] = '' if simplified_hero else '<div class="service-outcomes grid three">'+fields['outcome_cards']+'</div>'
 fields['challenge_cards']=''.join(f'<article class="card"><span class="card-number">{i:02} / CHALLENGE</span><h3>{e(a)}</h3><p>{e(b)}</p></article>' for i,(a,b) in enumerate(s['challenges'],1))
 fields['pillar_cards']=''.join(f'<article class="card service-pillar"><div class="pillar-top"><span class="card-number">{i:02}</span><span class="eyebrow">{e(s["short"])}</span></div><h3>{e(a)}</h3><p>{e(b)}</p><div class="pillar-strip">{e(c)}</div></article>' for i,(a,b,c) in enumerate(s['pillars'],1))
 fields['type_cards']=''.join(f'<article class="card type-card"><h3>{e(a)}</h3><p>{e(b)}</p><ul>'+''.join(f'<li>{e(x)}</li>' for x in c)+'</ul></article>' for a,b,c in s['types'])
 fields['example_stages']=''.join(f'<div class="example-stage"><h3>{label}</h3><p>{e(body)}</p></div>' for label,body in zip(['The buyer','The next step','Your team’s response'],s['example'][1:]))
 fields['scope_cards']=''.join(f'<article class="card scope-card"><span class="card-number">{i:02} / OPTION</span><h3>{e(a)}</h3><p>{e(b)}</p><a class="button'+('' if i==2 else ' button-secondary')+'" href="#audit-form">Ask about this option <span aria-hidden="true">↗</span></a></article>' for i,(a,b) in enumerate(s['scope'],1))
 others=[x for x in SERVICES if x['slug']!=s['slug']]
 fields['related_services']=''.join(f'<a class="related-service" href="{route(other)}"><h3>{e(other["name"])}</h3><p>{e(reason)}</p><span>Explore {e(other["short"])} ↗</span></a>' for other,reason in zip(others,RELATIONS[s['slug']]))
 fields['faq_items']=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in s['faqs'])
 fields['industry_options']=''.join(f'<option value="{e(p["slug"])}">{e(p["short"])}</option>' for p in INDUSTRIES)
 fields['form_options']=''.join(f'<option value="{e(x)}">{e(x)}</option>' for x in s['form_options'])
 schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'isPartOf':{'@id':BASE+'/#website'},'name':title,'description':desc,'about':{'@id':canonical+'#service'},'breadcrumb':{'@id':canonical+'#breadcrumb'}},{'@type':'Service','@id':canonical+'#service','name':s['name'],'url':canonical,'description':desc,'provider':{'@type':'Organization','@id':BASE+'/#organization','name':'Sixth Gear Digital','url':BASE+'/'}},{'@type':'BreadcrumbList','@id':canonical+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Services','item':BASE+'/#services'},{'@type':'ListItem','position':3,'name':s['name'],'item':canonical}]}]}
 fields['structured_data']=json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')
 folder=ROOT/'services'/s['slug']; folder.mkdir(parents=True,exist_ok=True)
 (folder/'index.html').write_text(TEMPLATE.substitute(fields))

# Homepage offers are curated separately from the complete service-page directory.
# Facebook Ads currently starts a contact conversation instead of linking to a draft page.
home_offers = json.loads((ROOT/'content/home-services.json').read_text())
service_by_slug = {service['slug']:service for service in SERVICES}
icons = {
 'seo':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5M7.5 12l2-3 2 2 2-4"/>',
 'ads':'<path d="m5 3 14 9-7 1-3 7-4-17Z"/><path d="m13 15 4 6M17 4l1-2m3 6 2-1"/>',
 'website':'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18m-12 0v11M6 6.5h.01m3 0h.01m3 0h.01m0 6.5h6m-6 3h4"/>',
 'facebook':'<path d="M3 10h4l12-5v14L7 14H3v-4Zm4 4 2 7h3l-2-6m12-8 1-1m-1 12 1 1"/>'
}
home_cards = []
for offer in home_offers:
 icon = '<span class="services-showcase-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'+icons[offer['icon']]+'</svg></span>'
 if offer.get('service'):
  service = service_by_slug[offer['service']]
  action = f'<a class="services-showcase-link" href="{route(service)}" aria-label="Learn more about {e(offer["title"])}">Learn more <span aria-hidden="true">→</span></a>'
 else:
  assert offer['action']=='contact'
  action = '<button class="services-showcase-link" type="button" data-contact-open data-contact-service="'+e(offer['title'])+'" aria-haspopup="dialog" aria-controls="contact-dialog">'+e(offer['action_label'])+' <span aria-hidden="true">→</span></button>'
 home_cards.append('<article class="services-showcase-card"><div class="services-showcase-card-heading">'+icon+'<h3>'+e(offer['title'])+'</h3></div><p>'+e(offer['description'])+'</p>'+action+'</article>')
section = Template((ROOT/'templates/home-services.html').read_text()).substitute(cards=''.join(home_cards))
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
