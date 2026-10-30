"""Shared, explicitly curated navigation for every current page."""
from html import escape
from pathlib import Path
from string import Template
import json

ROOT = Path(__file__).resolve().parents[1]


def navigation_fields(current_path, contact_target):
    def link(path, title):
        current = ' aria-current="page"' if path == current_path else ''
        return '<a href="'+escape(path, quote=True)+'"'+current+'>'+escape(title)+'</a>'

    industries = json.loads((ROOT/'content/industries.json').read_text())
    by_slug = {page['slug']:page for page in industries}
    featured = json.loads((ROOT/'content/home-industries.json').read_text())
    industries = [{**by_slug[item['slug']], 'short':item.get('title',by_slug[item['slug']]['short'])} for item in featured]
    nav_offers = [
        {'title':'SEO', 'service':'industrial-seo'},
        {'title':'Google Ads', 'service':'industrial-google-ads'},
        {'title':'Web design', 'service':'web-design-for-manufacturing-companies'},
        {'title':'Facebook ads', 'service':'industrial-facebook-ads'},
    ]
    values = {
        'home_current': ' aria-current="page"' if current_path == '/' else '',
        'about_current': ' aria-current="page"' if current_path == '/about/' else '',
        'industry_links': ''.join(link('/industries/'+page['slug']+'/', page['short'])
                                  for page in industries),
        'service_links': ''.join(link('/services/'+offer['service']+'/' if offer.get('service')
                                     else '/#growth-plan', offer['title']) for offer in nav_offers),
        'contact_target': escape(contact_target, quote=True),
    }
    return {
        'desktop_navigation': Template((ROOT/'templates/navigation-desktop.html').read_text()).substitute(values).strip(),
        'mobile_navigation': Template((ROOT/'templates/navigation-mobile.html').read_text()).substitute(values).strip(),
    }
