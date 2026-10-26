#!/usr/bin/env python3
"""Check the actual publish artifact for SEO, links and deployment hygiene."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
BASE = 'https://sixthgeardigital.com'
errors = []
def check(condition, message):
    if not condition: errors.append(message)

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids=set(); self.links=[]; self.assets=[]; self.canon=[]; self.descriptions=[]; self.h1=0; self.title=''; self.in_title=False; self.schemas=[]; self.in_schema=False; self.schema=''; self.noindex=False
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            check(a['id'] not in self.ids, 'Duplicate ID: '+a['id'])
            self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='title': self.in_title=True
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='link' and a.get('rel')=='canonical': self.canon.append(a.get('href'))
        if tag=='link' and a.get('rel')=='stylesheet': self.assets.append(a.get('href'))
        if tag in ('script','img') and a.get('src'): self.assets.append(a['src'])
        if tag=='img':
            check('alt' in a and 'width' in a and 'height' in a,'Image missing alt or dimensions')
            for candidate in a.get('srcset','').split(','):
                if candidate.strip(): self.assets.append(candidate.strip().split()[0])
        if tag=='meta' and a.get('name')=='description': self.descriptions.append(a.get('content'))
        if tag=='meta' and a.get('name')=='robots': self.noindex='noindex' in a.get('content','')
        if tag=='script' and a.get('type')=='application/ld+json': self.in_schema=True;self.schema=''
    def handle_data(self,data):
        if self.in_title:self.title+=data
        if self.in_schema:self.schema+=data
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag=='script' and self.in_schema:
            self.schemas.append(json.loads(self.schema));self.in_schema=False

pages={p.relative_to(DIST).as_posix():Page(p.read_text()) for p in DIST.rglob('*.html')}
urls=[e.text for e in ET.parse(DIST/'sitemap.xml').findall('.//{*}loc')]
check(len(urls)==18 and len(set(urls))==18,'Expected 18 unique canonical sitemap URLs')
def resolve(path,source='index.html'):
    if path.startswith('/'): rel=path.lstrip('/')
    else:rel=(Path(source).parent/path).as_posix()
    if not rel or rel.endswith('/'):rel+='index.html'
    return rel
seen_titles=set();seen_desc=set()
for source,page in pages.items():
    if source=='404.html':
        check(page.noindex,'404 must have noindex')
    else:
        expected=BASE+('/' if source=='index.html' else '/about/' if source=='about/index.html' else '/' + source.removesuffix('index.html') if source.startswith(('services/','industries/')) else '/'+source)
        check(page.canon==[expected],f'{source}: wrong canonical')
        check(expected in urls,f'{source}: missing from sitemap')
        check(page.h1==1,f'{source}: expected one H1')
        check(len(page.descriptions)==1 and page.descriptions[0],f'{source}: missing description')
        check(page.title not in seen_titles,f'{source}: duplicate title');seen_titles.add(page.title)
        check(page.descriptions[0] not in seen_desc,f'{source}: duplicate description');seen_desc.add(page.descriptions[0])
        check(bool(page.schemas),f'{source}: missing schema')
        check(not page.noindex,f'{source}: unexpected noindex')
    text=(DIST/source).read_text()
    check(not re.search(r'\$(title|canonical|buyer_brief|headline)',text),f'{source}: template placeholder')
    check('cdn.tailwindcss.com' not in text and 'fonts.googleapis.com' not in text,f'{source}: runtime CDN remains')
    for link in page.links+page.assets:
        parsed=urlparse(link)
        if not parsed.scheme and not parsed.netloc and link in page.links:
            check(not parsed.path.endswith('.html'), f'{source}: internal link uses an .html URL: {link}')
        if parsed.scheme or parsed.netloc:continue
        target=resolve(unquote(parsed.path),source) if parsed.path else source
        check((DIST/target).is_file(),f'{source}: broken destination {link}')
        if parsed.fragment and target in pages:check(parsed.fragment in pages[target].ids,f'{source}: missing fragment {link}')
for forbidden in ['templates','scripts','content','code.html','ppc.html','seo.html','web-design.html','funnels.html','node_modules','package.json']:
    check(not (DIST/forbidden).exists(),'Source/legacy file published: '+forbidden)
for name in ['ppc.html','seo.html','web-design.html','funnels.html','code.html','index.html','about.html']:
    check('/'+name+' ' in (DIST/'_redirects').read_text(),'Missing redirect '+name)
for page in json.loads((ROOT/'content/industries.json').read_text()):
    check(f'/industries/{page["slug"]}.html /industries/{page["slug"]}/ 301!' in (DIST/'_redirects').read_text(), 'Missing clean URL redirect '+page['slug'])
# CSS assets must resolve, too (including font files).
for file in (DIST/'assets').glob('*.css'):
    for url in re.findall(r'url\([\'"]?([^\)\'\"]+)',file.read_text()):
        if url.startswith('/'):check((DIST/url.lstrip('/')).is_file(),'Missing CSS asset '+url)
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(urls)} canonical pages; metadata, JSON-LD, internal links, fragments, assets, redirects and publish exclusions.')
