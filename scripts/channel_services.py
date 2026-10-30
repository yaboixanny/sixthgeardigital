"""Render channel-specific copy with the same layout as the website service pages."""
from html import escape
from pathlib import Path
from string import Template
import json
from navigation import navigation_fields

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://sixthgeardigital.com'
SPLIT = Template((ROOT/'templates/service-split-section.html').read_text())
IMAGES = [
 ('website-success.svg', 680, 'A manufacturing website connects search traffic, content, analytics and quote requests.'),
 ('website-redesign.svg', 680, 'A manufacturing product website with specifications, quote forms and sales software connections.'),
 ('website-lifecycle.svg', 620, 'An illustrative lifecycle compares leaving a website unchanged with reviewing and improving it.'),
 ('website-connections.svg', 680, 'A website connects content, email, analytics, careers, CRM and inventory tools.'),
 ('website-project-cost.svg', 620, 'A project is planned through discovery, design, build, launch and support.'),
 ('website-search-migration.svg', 620, 'A website launch plan maps pages and checks redirects, indexing and tracking.'),
 ('website-rebrand.svg', 620, 'A website refresh brings brand colors, typography and messaging together.'),
]
SECTION_CLASSES = ['', 'website-redesign', 'website-lifecycle', 'website-connections', 'website-cost', 'website-rankings', 'website-rebranding']
SECTION_IDS = ['website-success-title','website-redesign-title','website-lifecycle-title','website-connections-title','website-cost-title','website-rankings-title','website-rebranding-title']


def e(value):
    return escape(str(value), quote=True)


def render_channel_service(service, content, footer_links):
    canonical = BASE+'/services/'+service['slug']+'/'
    title = service['name']+' | Sixth Gear Digital'
    assert len(content['sections']) == 7
    sections = []
    for index, section in enumerate(content['sections']):
        body = ''.join('<p>'+e(paragraph)+'</p>' for paragraph in section['paragraphs'])
        if section['points']:
            body += '<ul>'+''.join('<li><strong>'+e(label)+':</strong> '+e(text)+'</li>' for label,text in section['points'])+'</ul>'
        if section.get('link'):
            link = section['link']
            assert link['href'] in ['/services/web-design-for-manufacturing-companies/', '/services/industrial-lead-tracking/']
            body += '<p><a class="channel-context-link" href="'+e(link['href'])+'">'+e(link['label'])+'</a></p>'
        image,height,alt = IMAGES[index]
        sections.append(SPLIT.substitute(section_class=SECTION_CLASSES[index],section_id=SECTION_IDS[index],grid_class=' website-redesign-grid' if index%2 else '',heading=e(section['heading']),lead=e(section['lead']),content=body,image='/assets/'+image,image_height=height,image_alt=e(alt)))
    problems = content['problems']
    assert len(problems['items']) == 4
    cards = ''.join('<article><span class="website-problem-icon" aria-hidden="true">×</span><div><h3>'+e(heading)+'</h3><p>'+e(text)+'</p></div></article>' for heading,text in problems['items'])
    problem_html = Template((ROOT/'templates/service-problems.html').read_text()).substitute(problem_heading=e(problems['heading']),problem_lead=e(problems['lead']),problem_intro=e(problems['intro']),problem_cards=cards)
    faqs = service['faqs']
    assert len(faqs) == 5
    cta = content['cta']
    check = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11v1a9 9 0 1 1-5-8"/><path d="m8 11 4 4L22 5"/></svg>'
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':service['description'],'isPartOf':{'@id':BASE+'/#website'},'about':{'@id':canonical+'#service'},'breadcrumb':{'@id':canonical+'#breadcrumb'}},
        {'@type':'Service','@id':canonical+'#service','name':service['name'],'url':canonical,'description':service['description'],'provider':{'@type':'Organization','@id':BASE+'/#organization','name':'Sixth Gear Digital','url':BASE+'/'}},
        {'@type':'BreadcrumbList','@id':canonical+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Services','item':BASE+'/#services'},{'@type':'ListItem','position':3,'name':service['name'],'item':canonical}]},
        {'@type':'FAQPage','@id':canonical+'#faq','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]},
    ]}
    fields = {
        'title':e(title),'description':e(service['description']),'canonical':e(canonical),
        'structured_data':json.dumps(schema,ensure_ascii=False).replace('<','\\u003c'),
        'hero_breadcrumb':'','hero_badge':'','headline':e(service['headline']),'accent':e(service['accent']),'intro':e(service['intro']),
        'service_content_sections':''.join(sections),'service_problem_section':problem_html,
        'website_faq_start':e(content['faq_title']),'website_faq_end':'Questions Answered.','website_faq_intro':e(content['faq_intro']),
        'faq_aria_label':e(service['name']+' questions'),
        'faq_items':''.join('<details><summary>'+e(q)+'</summary><p>'+e(a)+'</p></details>' for q,a in faqs),
        'website_final_label':'','website_final_heading':e(cta['heading']),
        'website_final_intro_html':e(cta['intro']).replace('30-minute call','<strong>30-minute call</strong>'),
        'website_final_bullets':''.join('<li>'+check+e(point)+'</li>' for point in cta['points']),
        'website_final_prompt':e(cta['prompt']),'footer_links':footer_links,
    }
    fields.update(navigation_fields('/services/'+service['slug']+'/', '/#growth-plan'))
    return Template((ROOT/'templates/website-service.html').read_text()).substitute(fields)
