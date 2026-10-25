# SEO measurement and evidence

The October 25, 2026 cleanup preserves the Google site-verification tag and publishes 18 canonical pages. The sitemap is https://sixthgeardigital.com/sitemap.xml. Successful HTTP checks do not establish Google indexing or rankings.

## Search Console baseline

Requires access to the site's verified Search Console property. No connected Search Console account was available during implementation.

1. Submit or refresh the sitemap and review its processing status.
2. Inspect the homepage, each of the four service pages, and representative industry pages. Check Google's selected canonical, index eligibility, last crawl and rendered page. Request indexing after confirming the live deployment.
3. Review Page indexing for excluded canonical pages and lingering legacy/template URLs. Legacy service URLs should redirect; templates should return 404. Do not block removed templates in robots.txt, so crawlers can see the removal.
4. Export Performance data by query and page for the last 3 months, with the previous period for comparison. Split branded queries from non-branded agency/service searches. Compare only periods with sufficient data.
5. Prioritize industry improvements using impressions, relevance, inquiry quality and sales feedback. Customer searches shown inside industry examples are not the agency pages' target queries.
6. Review monthly: indexed canonical pages, non-brand clicks, relevant query impressions, qualified organic inquiries, quotes and recorded wins. Search Console does not supply lead or revenue data; reconcile those with forms and CRM records.
7. Review the Core Web Vitals report when sufficient field data exists. Local browser or Lighthouse results are lab measurements and cannot establish real-user CWV compliance.

## Evidence needed from the owner

- Confirmed founder bio, relevant experience and qualifications before adding further expertise claims.
- Confirmed agency service geography before adding areaServed or location claims.
- Approved client examples with permission, dates, scope, budget where publishable, qualified lead definitions and supported results.
- A real screenshot or published page with explanatory annotations, where disclosure is permitted.

The current examples are explicitly illustrative; there are no invented client results or testimonials. The About page uses the existing founder identity and photograph.

## Deployment and follow-up

Legacy /ppc.html, /seo.html and /web-design.html redirect to their matching industrial service. /funnels.html redirects to industrial websites because its primary offer was landing pages and qualification. /code.html and /index.html redirect to the homepage. Preserve redirects for at least a year, and longer while useful links still point to them.

The Netlify build publishes only dist/. Source templates, generators, draft pages and content JSON remain in Git but are absent from the publish artifact. The build validates canonical URLs, titles, descriptions, JSON-LD, local destinations, fragments, images, fonts and exclusions. Run npm ci, npm run build, then npm run check.
