#!/usr/bin/env python3
"""Apply shared navigation to the directly maintained homepage and About page."""
from pathlib import Path
import re
from navigation import navigation_fields

ROOT = Path(__file__).resolve().parents[1]
for filename, route, contact in [('index.html', '/', '#growth-plan'), ('about.html', '/about/', '/#growth-plan')]:
    path = ROOT/filename
    html = path.read_text()
    fields = navigation_fields(route, contact)
    for pattern, key in [(r'<nav\b[^>]*aria-label="Main navigation"[^>]*>.*?</nav>', 'desktop_navigation'),
                         (r'<nav\b[^>]*id="mobile-menu"[^>]*>.*?</nav>', 'mobile_navigation')]:
        html, count = re.subn(pattern, lambda _: fields[key], html, flags=re.S)
        assert count == 1, filename+': missing navigation'
    if '/assets/navigation.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="/assets/navigation.css"><script src="/assets/navigation.js" defer></script></head>')
    path.write_text(html)
print('Updated shared homepage and About navigation.')
