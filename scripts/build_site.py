#!/usr/bin/env python3
"""Publish an explicit allowlist. Templates, drafts and source data stay private to Git."""
from pathlib import Path
import shutil
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()
for name in ('index.html', 'about.html', '404.html', 'robots.txt', 'sitemap.xml', 'industrial.css', 'industrial.js', '_redirects'):
    shutil.copy2(ROOT / name, DIST / name)
for folder in ('services', 'industries'):
    (DIST / folder).mkdir()
for item in json.loads((ROOT / 'content/services.json').read_text()):
    slug = item['slug']
    (DIST / 'services' / slug).mkdir()
    shutil.copy2(ROOT / 'services' / slug / 'index.html', DIST / 'services' / slug / 'index.html')
for item in json.loads((ROOT / 'content/industries.json').read_text()):
    name = item['slug'] + '.html'
    shutil.copy2(ROOT / 'industries' / name, DIST / 'industries' / name)
(DIST / 'assets').mkdir()
for name in ('home.css', 'fonts.css', 'industry.css', 'services.css', 'services.js', 'alex-founder.webp'):
    shutil.copy2(ROOT / 'assets' / name, DIST / 'assets' / name)
for folder in ('industries', 'images', 'fonts'):
    shutil.copytree(ROOT / 'assets' / folder, DIST / 'assets' / folder)
print('Built dist/: finished pages and production assets only.')
