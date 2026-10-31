#!/usr/bin/env python3
"""Verify rebrand routing with curl against the deployed site (no redirect following).
Run: python3 scripts/verify_legacy_routes.py [https://sixthgeardigital.com]
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = (sys.argv[1] if len(sys.argv) > 1 else 'https://sixthgeardigital.com').rstrip('/')
REDIRECTS = {
    '/services/industrial-seo': '/services/seo/',
    '/services/industrial-seo.html': '/services/seo/',
    '/services/industrial-google-ads': '/services/google-ads/',
    '/services/industrial-google-ads.html': '/services/google-ads/',
    '/services/industrial-facebook-ads': '/services/facebook-ads/',
    '/services/industrial-facebook-ads.html': '/services/facebook-ads/',
    '/services/industrial-lead-tracking': '/services/lead-tracking/',
    '/services/industrial-lead-tracking.html': '/services/lead-tracking/',
    '/web-design': '/services/web-design-for-manufacturing-companies/',
    '/services/industrial-websites': '/services/web-design-for-manufacturing-companies/',
    '/services/industrial-websites.html': '/services/web-design-for-manufacturing-companies/',
    '/web-design.html': '/services/web-design-for-manufacturing-companies/',
    '/funnels.html': '/services/web-design-for-manufacturing-companies/',
    '/ppc': '/services/google-ads/',
    '/ppc.html': '/services/google-ads/',
    '/seo': '/services/seo/',
    '/seo.html': '/services/seo/',
    '/services': '/', '/blog': '/',
    '/case-studies': '/', '/google-ads-results': '/',
}
GONE = [
    '/sunly-solar', '/seo-for-walking-tour-businesses',
    '/belan-j-ecommerce-seo', '/ppc-for-restaurants',
    '/local-seo-restaurants', '/tfa-speed-seo-audit',
    '/case-studies/walking-tour-seo-case-study',
]


def fetch(path):
    with tempfile.TemporaryDirectory() as folder:
        headers = Path(folder) / 'headers'
        body = Path(folder) / 'body'
        result = subprocess.run([
            'curl', '--silent', '--show-error', '--compressed',
            '--max-time', '30', '--dump-header', str(headers),
            '--output', str(body), '--write-out', '%{http_code}',
            ORIGIN + path,
        ], check=True, capture_output=True, text=True)
        location = next((line.split(':', 1)[1].strip() for line in
                         headers.read_text().splitlines()
                         if line.lower().startswith('location:')), None)
        return int(result.stdout), location, body.read_bytes()


def main():
    error_body = fetch('/404.html')[2]
    checks = [(path + suffix, 301, target) for path, target in REDIRECTS.items()
              for suffix in ('', '/')]
    checks += [(path + suffix, 410, None) for path in GONE for suffix in ('', '/')]
    checks += [('/contact', 301, '/contact/')]
    current = ['/', '/about/', '/contact/']
    for group in ('services', 'industries'):
        current += [f'/{group}/{page["slug"]}/' for page in
                    json.loads((ROOT / f'content/{group}.json').read_text())]
    checks += [(path, 200, None) for path in current]

    def verify(item):
        path, expected, target = item
        try:
            status, location, body = fetch(path)
            errors = []
            if status != expected:
                errors.append(f'expected {expected}, got {status}')
            if target and (not location or urljoin(ORIGIN, location) != ORIGIN + target):
                errors.append(f'expected Location {target}, got {location}')
            if expected != 301 and location:
                errors.append(f'unexpected Location {location}')
            if expected == 410 and body != error_body:
                errors.append('response body differs from existing 404 page')
            return {'path': path, 'status': status, 'location': location,
                    'errors': errors}
        except Exception as error:
            return {'path': path, 'errors': [str(error)]}

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(verify, checks))
    print(json.dumps({'origin': ORIGIN, 'checked': len(results),
                      'passed': sum(not row['errors'] for row in results),
                      'results': results}, indent=2))
    return int(any(row['errors'] for row in results))


if __name__ == '__main__':
    raise SystemExit(main())
