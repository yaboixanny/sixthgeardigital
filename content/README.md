# Industry pages

The twelve sectors in `industries.json` are the editorial source for the static pages.

- Shared markup: `templates/industry.html` and `templates/industry-sections.html`
- Shared design: `assets/industry.css`
- Form and navigation behavior: `industrial.js`
- Page rendering, local SVG illustrations, homepage directory, sitemap: `scripts/build_industries.py`

Run `python3 scripts/build_industries.py` after editing the data or template. The script does not require third-party packages. Pages are published at clean trailing-slash URLs such as `/industries/cnc-machining-fabrication-marketing/`; their source files are committed for review and regenerated before publishing.

Each industry has a unique title, canonical URL, description, content, capability choices, and Netlify form name. Form submissions include the industry and source URL. Netlify must detect forms on deployment; delivery is not established by local preview.

All twelve industries follow the current CNC structure: a one-sentence service introduction, buyer journey, four challenge cards, four service blocks, capabilities, illustrative search-to-quote example, website checklist, FAQs and contact form. Buyer journeys use the restored plain cards, without icons or decorative numbering. The hero has no summary cards or secondary example button.

Each industry's `marketing_content` contains its sector-specific copy. The service blocks must link to Google Ads, SEO, websites and lead tracking in that order. `buyer_journey` supplies the three buying steps; `challenges` supplies four cards; `capabilities` supplies the contact-form choices. `faq_schema` generates FAQPage markup from the same answers rendered in `faqs`. `submit_label` controls the form button and `lastmod` records the substantive page edit date. Edit these records and the shared templates, then rebuild; do not edit only a generated page.

The homepage directory is the curated list of sectors requested by the site owner. Each industry page links to the directory and the agency's supporting services. There is no automatic related-industry fallback.

Campaign plans are illustrative. Replace them with client case studies only when supporting facts and publication permission are available. Product capabilities, certifications, and controlled drawing-handling workflows must come from approved business information.

When republishing changed industry content, update that industry's `lastmod` to the substantive edit date before regenerating the sitemap entries. The generator's `DATE` is only a fallback for older records.

# Core service pages

`services.json` contains the four service pages. Their exact trailing-slash URLs are served by committed `services/<slug>/index.html` files.

- Shared markup: `templates/service.html`
- Shared styling: `assets/industry.css` with `assets/services.css`
- Accessible website-intake example tabs: `assets/services.js`
- Page generation, homepage service section, and service sitemap entries: `scripts/build_services.py`

Run both generators after changes that affect cross-page navigation:

```sh
python3 scripts/build_services.py
python3 scripts/build_industries.py
```

The industry renderer reads `services.json` for footer navigation. Service-to-service links use explicit editorial explanations in `build_services.py`; they are not selected by recency or generic similarity. Google Ads is the primary homepage offer. Each service form includes its own form name, service, source URL, industry, and selected priority.

The service template uses a local optimized copy of the supplied industrial image and uses scope options in place of unconfirmed template prices. Examples describe planned workflows rather than client results. The website intake examples are interactive field comparisons, not live customer RFQ submission forms.

# Production deployment and SEO maintenance

Netlify now builds with `npm run build && npm run check` and publishes only `dist/` (see `netlify.toml`). Run `npm ci` first on a fresh checkout. The build runs both page generators, compiles homepage Tailwind CSS, and copies an explicit production allowlist. Do not change the publish directory back to the repository root: that exposes source templates and legacy drafts.

`_redirects` consolidates old service and `.html` routes. The sitemap contains only the 18 current canonical pages. `scripts/check_site.py` validates the generated publish artifact and confirms internal page links use clean URLs. `assets/home.css` is compiled from `styles/home.css`, `tailwind.config.cjs`, and homepage markup; do not edit the generated CSS directly.

The site self-hosts a single Latin Inter variable WOFF2 font, with its OFL license in `assets/fonts/`. The existing template photos are stored as 320px/512px WebP variants, matching the available source resolution rather than upscaling it. Higher-resolution original photography can replace them later. The homepage uses inline SVG icons rather than an icon font.

Service descriptions are authored independently of introductory copy. Industry `marketing_content.services` entries provide sector-specific guidance and explicit links to supporting service routes. Keep these relationships editorially relevant when adding a sector.

About content and examples must not claim client outcomes or geographic coverage without evidence. See `SEO-MEASUREMENT.md` for the account-dependent Search Console baseline and approved-evidence checklist.

# Writing style

Write for a reader around ninth grade. Use short sentences, familiar words and specific examples. Keep the tone helpful and matter-of-fact. Explain SEO, CRM and other marketing terms the first time they are used. Keep industry terms when they identify the actual work, and explain them where useful.

Use direct labels such as “service area,” “quote requests” and “follow-up.” Avoid sales slogans, pressure, “growth assessments,” “conversion pathways” and similar jargon. Buttons should describe the next step, such as “Get in touch” or “Send your message.” Preserve page topics, URLs and relevant internal links when editing copy.
