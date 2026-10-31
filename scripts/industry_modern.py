"""Reusable split section and service grid for the modern industry page layout."""
from pathlib import Path
from string import Template
from html import escape

ROOT = Path(__file__).resolve().parents[1]
ICONS = {
    'google-ads': '<path d="M3 6h13v12H3zM6 9h7M6 12h5m8-9v6m-3-3h6M8 18v3m-3 0h6"/>',
    'seo': '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6M7 12V9m3 3V7m3 5V8"/>',
    'facebook-ads': '<path d="M4 7h5l10-4v16L9 15H4zM9 7v8m-3 0 2 6h4l-2-6m12-7v6"/>',
    'web-design-for-manufacturing-companies': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 9h20M6 6.5h.01M9 6.5h.01M6 13h5v4H6zM14 13h4m-4 4h4"/>'
}

def e(value):
    return escape(str(value), quote=True)

def render_modern_sections(page):
    fit = page['buyer_fit']
    split = Template((ROOT/'templates/industry-buyer-fit.html').read_text()).substitute(
        heading=e(fit['heading']), intro=e(fit['intro']),
        paragraphs=''.join('<p>'+e(p)+'</p>' for p in fit['paragraphs']),
        bullets=''.join('<li>'+e(p)+'</li>' for p in fit['bullets']),
        closing=e(fit['closing']), image=e(fit['image']), image_alt=e(fit['image_alt']))
    revenue = page['revenue_section']
    assert [card['service'] for card in revenue['cards']] == list(ICONS), page['slug']
    cards = []
    for card in revenue['cards']:
        service = card['service']
        assert (ROOT/'services'/service/'index.html').exists(), service
        icon = '<span class="industry-revenue-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+ICONS[service]+'</svg></span>'
        cards.append('<article class="industry-revenue-card">'+icon+'<h3>'+e(card['title'])+'</h3><p class="industry-revenue-subtitle">'+e(card['subtitle'])+'</p><p>'+e(card['body'])+'</p><a href="/services/'+e(service)+'/">'+e(card['link_label'])+' <span aria-hidden="true">→</span></a></article>')
    grid = Template((ROOT/'templates/industry-revenue.html').read_text()).substitute(heading=e(revenue['heading']),cards=''.join(cards))
    return split + '\n' + grid


def render_modern_intro(page):
    data = page['modern_intro']
    fields = {key:e(value) for key,value in data.items() if isinstance(value,str)}
    fields['intro_bullets'] = ''.join('<li><strong>'+e(label)+':</strong> '+e(body)+'</li>' for label,body in data['intro_bullets'])
    return Template((ROOT/'templates/industry-modern-introduction.html').read_text()).substitute(fields)

def render_modern_cta(page):
    data = page['modern_closing']
    fields = {key:e(value) for key,value in data.items() if isinstance(value,str)}
    check = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="m8 12 3 3 5-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    fields['final_bullets'] = ''.join('<li>'+check+e(bullet)+'</li>' for bullet in data['final_bullets'])
    return Template((ROOT/'templates/industry-modern-final-cta.html').read_text()).substitute(fields)
