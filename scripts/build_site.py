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
for name in ('index.html', '404.html', 'robots.txt', 'sitemap.xml', 'industrial.css', 'industrial.js', '_redirects'):
    shutil.copy2(ROOT / name, DIST / name)
for folder in ('services', 'industries'):
    (DIST / folder).mkdir()
(DIST / 'about').mkdir()
shutil.copy2(ROOT / 'about.html', DIST / 'about' / 'index.html')
for item in json.loads((ROOT / 'content/services.json').read_text()):
    slug = item['slug']
    (DIST / 'services' / slug).mkdir()
    shutil.copy2(ROOT / 'services' / slug / 'index.html', DIST / 'services' / slug / 'index.html')
for item in json.loads((ROOT / 'content/industries.json').read_text()):
    slug = item['slug']
    (DIST / 'industries' / slug).mkdir()
    shutil.copy2(ROOT / 'industries' / slug / 'index.html', DIST / 'industries' / slug / 'index.html')
(DIST / 'assets').mkdir()
for name in ('home.css', 'robot-arm.css', 'robot-arm.js', 'fonts.css', 'industry.css', 'industry-faq.css', 'building-materials.css', 'services.css', 'website.css', 'navigation.css', 'navigation.js', 'website-success.svg', 'website-redesign.svg', 'website-lifecycle.svg', 'website-connections.svg', 'website-project-cost.svg', 'website-search-migration.svg', 'website-rebrand.svg', 'services.js', 'alex-founder.webp'):
    shutil.copy2(ROOT / 'assets' / name, DIST / 'assets' / name)
for folder in ('industries', 'images', 'fonts'):
    shutil.copytree(ROOT / 'assets' / folder, DIST / 'assets' / folder)
print('Built dist/: finished pages and production assets only.')
