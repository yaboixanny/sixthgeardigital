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
    services = json.loads((ROOT/'content/services.json').read_text())
    offers = json.loads((ROOT/'content/home-services.json').read_text())
    nav_offers = []
    for offer in offers:
        nav_offers.append(offer)
        if offer.get('service') == 'industrial-websites':
            nav_offers.extend({'title':service['name'], 'service':service['slug']}
                              for service in services
                              if service.get('extends') == 'industrial-websites')
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
