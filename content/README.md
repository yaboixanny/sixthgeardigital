# Industry pages

The thirteen sectors in `industries.json` are the editorial source for the static pages.

- Shared markup: `templates/industry.html` and `templates/industry-sections.html`
- Shared design: `assets/industry.css`
- Form and navigation behavior: `industrial.js`
- Page rendering, local SVG illustrations, homepage directory, sitemap: `scripts/build_industries.py`

Run `python3 scripts/build_industries.py` after editing the data or template. The script does not require third-party packages. Pages are published at clean trailing-slash URLs such as `/industries/cnc-machining-fabrication-marketing/`; their source files are committed for review and regenerated before publishing.

Each industry has a unique title, canonical URL, description, content, capability choices, and Netlify form name. Form submissions include the industry and source URL. Netlify must detect forms on deployment; delivery is not established by local preview.

The original twelve industries follow the current CNC structure: a one-sentence service introduction, buyer journey, four challenge cards, four service blocks, capabilities, illustrative search-to-quote example, website checklist, FAQs and contact form. Buyer journeys use the restored plain cards, without icons or decorative numbering. The hero has no summary cards or secondary example button.

Each industry's `marketing_content` contains its sector-specific copy. The service blocks must link to Google Ads, SEO, websites and lead tracking in that order. `buyer_journey` supplies the three buying steps; `challenges` supplies four cards; `capabilities` supplies the contact-form choices. `faq_schema` generates FAQPage markup from the same answers rendered in `faqs`. `submit_label` controls the form button and `lastmod` records the substantive page edit date. Edit these records and the shared templates, then rebuild; do not edit only a generated page.

The building-materials page uses `templates/building-materials.html` and `assets/building-materials.css`, selected through its `page_template` field. It follows the supplied reference’s bold Montserrat typography, split image-and-copy layout and blue palette. Montserrat is self-hosted in `assets/fonts/` with its OFL license. Its two original generated images are illustrative category images, not client project photography; optimized WebP variants are in `assets/images/`. The industry record remains the source for services, FAQs, product types and form options.

The homepage industry grid (`#industries`), below the three-day setup section, is curated in `home-industries.json` and rendered with `templates/home-industries.html`. Each entry links to an existing configured industry and uses a matching inline SVG icon. The footer keeps a second text-only industry directory. The section after the hero is rendered from `templates/home-difference.html`: six non-clickable comparison cards reveal on hover or keyboard focus; touch devices show both sides in full. Each industry page links to the directory and the agency's supporting services. There is no automatic related-industry fallback.

Campaign plans are illustrative. Replace them with client case studies only when supporting facts and publication permission are available. Product capabilities, certifications, and controlled drawing-handling workflows must come from approved business information.

When republishing changed industry content, update that industry's `lastmod` to the substantive edit date before regenerating the sitemap entries. The generator's `DATE` is only a fallback for older records.

# Core service pages

`services.json` contains the core service pages. A focused service record can use `extends` to inherit the parent service’s shared fields while providing its own copy, metadata and FAQs. Their exact trailing-slash URLs are served by committed `services/<slug>/index.html` files.

- Shared markup: `templates/service.html`
- Shared styling: `assets/industry.css` with `assets/services.css`
- Accessible website-intake example tabs: `assets/services.js`
- Page generation, homepage service section, and service sitemap entries: `scripts/build_services.py`

Run both generators after changes that affect cross-page navigation:

```sh
python3 scripts/build_services.py
python3 scripts/build_industries.py
python3 scripts/build_navigation.py
```

The industry renderer reads `services.json` for footer navigation. Service-to-service links use explicit editorial explanations in `build_services.py`; they are not selected by recency or generic similarity. The homepage's four featured offers are curated independently in `home-services.json` and rendered by `templates/home-services.html`: SEO, Google Ads, website design and Facebook ads. All four link to their service pages, including `/services/facebook-ads/`. Lead tracking remains available as a supporting service page. Each service form includes its own form name, service, source URL, industry, and selected priority.

The service template uses a local optimized copy of the supplied industrial image and uses scope options in place of unconfirmed template prices. Examples describe planned workflows rather than client results. The website intake examples are interactive field comparisons, not live customer RFQ submission forms.

# Production deployment and SEO maintenance

The homepage combines its contact invitation and FAQs in the `#growth-plan` section, with `#faq` on the accordion. “Get in touch” opens the native `#contact-dialog`; incoming `/#growth-plan` links also open it. The shorter form keeps the existing Netlify name `industrial-growth` and uses the shared submission handler in `industrial.js`.

Netlify now builds with `npm run build && npm run check` and publishes only `dist/` (see `netlify.toml`). Run `npm ci` first on a fresh checkout. The build runs both page generators, compiles homepage Tailwind CSS, and copies an explicit production allowlist. Do not change the publish directory back to the repository root: that exposes source templates and legacy drafts.

`_redirects` consolidates old service and `.html` routes. The sitemap contains only the 20 current canonical pages. `scripts/check_site.py` validates the generated publish artifact and confirms internal page links use clean URLs. `assets/home.css` is compiled from `styles/home.css`, `tailwind.config.cjs`, and homepage markup; do not edit the generated CSS directly.

The main site self-hosts a Latin Inter variable WOFF2 font; the building-materials page uses a self-hosted Montserrat variable WOFF2. Their OFL licenses are in `assets/fonts/`. The existing template photos are stored as 320px/512px WebP variants, matching the available source resolution rather than upscaling it. Higher-resolution original photography can replace them later. The homepage uses inline SVG icons rather than an icon font.

Service descriptions are authored independently of introductory copy. Industry `marketing_content.services` entries provide sector-specific guidance and explicit links to supporting service routes. Keep these relationships editorially relevant when adding a sector.

About content and examples must not claim client outcomes or geographic coverage without evidence. See `SEO-MEASUREMENT.md` for the account-dependent Search Console baseline and approved-evidence checklist.

# Writing style

Write for a reader around ninth grade. Use short sentences, familiar words and specific examples. Keep the tone helpful and matter-of-fact. Explain SEO, CRM and other marketing terms the first time they are used. Keep industry terms when they identify the actual work, and explain them where useful.

Use direct labels such as “service area,” “quote requests” and “follow-up.” Avoid sales slogans, pressure, “growth assessments,” “conversion pathways” and similar jargon. Buttons should describe the next step, such as “Get in touch” or “Send your message.” Preserve page topics, URLs and relevant internal links when editing copy.

The manufacturing website page uses `templates/website-service.html`, `assets/website.css` and the shared navigation assets. Its copy lives in its independent `services.json` record; its canonical is `/services/web-design-for-manufacturing-companies/`. It is the sole Web design entry in the Services dropdown and sitemap.

# Shared site navigation

All current pages use `scripts/navigation.py` with `templates/navigation-desktop.html` and `templates/navigation-mobile.html`. The service and industry generators render these fields directly; `scripts/build_navigation.py` updates the directly maintained homepage and About page. The build runs all three before publishing. Dropdown styling and behavior are in `assets/navigation.css` and `assets/navigation.js`. Industry destinations come from `industries.json`; the service dropdown explicitly lists SEO, Google Ads, Web design and Facebook ads. The manufacturing website page remains published and linked in the footer. Existing page-specific contact buttons keep their destinations.

The SEO, Google Ads and Facebook Ads pages use the website layout through `scripts/channel_services.py`. Their section copy is in `content/channel-services.json`; metadata, hero copy and FAQs remain in `services.json`. The seven alternating sections share `templates/service-split-section.html`, with common problem cards, FAQ and closing CTA. Existing website illustrations are intentionally reused for now. The website pages keep their original content through `templates/website-sections.html` and `templates/website-problems.html`.

# Manufacturing positioning

The homepage, About page and core services target manufacturing companies. `/services/web-design-for-manufacturing-companies/` is the only website-design service and is an independent record, not an inherited duplicate. The retired `/services/industrial-websites` variants permanently redirect to it. The SEO, Google Ads, Facebook Ads and lead-tracking services now use `/services/seo/`, `/services/google-ads/`, `/services/facebook-ads/` and `/services/lead-tracking/`. All old industrial-prefixed variants redirect directly to these canonical pages. The homepage and main industry dropdown feature the curated sectors from `home-industries.json`, including mining. All configured niche pages remain published. Keep internal links on the surviving website-design URL.

Industry FAQs share `templates/industry-faq.html` and `assets/industry-faq.css`, including the building-materials page. Each industry record supplies its own `faq_intro` and five question/answer pairs. The heading follows “Your [short industry name] marketing questions answered”; the contact button links to that page’s existing form. FAQPage schema is generated from the same visible answers.

Every industry has six tailored `agency_expectations` items, rendered with `templates/industry-expectations.html` after its marketing services. The shared `assets/industry-expectations.css` keeps the section consistent across both industry templates, with Urbanist item titles and 17px body copy. The main section heading retains its original size.

The CNC page selects `hero_style: cnc-background` and supplies its hero eyebrow, heading and description in `industries.json`. Its full-width hero uses `templates/cnc-hero.html` and `assets/cnc-hero.css`; replace the `--cnc-hero-image` URL with the final photograph. The current `assets/industries/cnc-hero-background.svg` is a neutral placeholder. Other industries retain `templates/industry-hero.html`.

## Industry page template

All 16 industry pages use `templates/industry-modern.html`. The shared order is: background hero, introductory split, six agency expectations, buyer-fit split (text left/image right), four-service revenue grid, tailored FAQ and closing discovery call. The CNC page is the original reference for this layout. The neutral hero background and each page's illustrations can be replaced with industry-specific photos when available.

Industry-specific copy lives in `content/industries.json`: `hero_eyebrow`, `hero_heading`, `hero_description`, `modern_intro`, `agency_expectations`, `buyer_fit`, `revenue_section`, FAQs and `modern_closing`. `scripts/industry_modern.py` renders the tailored introduction, buyer-fit section, service grid and closing CTA through `templates/industry-modern-introduction.html`, `templates/industry-buyer-fit.html`, `templates/industry-revenue.html` and `templates/industry-modern-final-cta.html`. The revenue cards have intentionally curated links in this order: Google Ads, SEO, Facebook Ads and web design; AI search is discussed within SEO. The CNC page currently retains its original introductory and closing templates, which carry the same layout.

The background hero and shared styles use `templates/cnc-hero.html`, `assets/cnc-hero.css` and `assets/cnc-hero.js`; the names are retained for compatibility. The neutral background is `assets/industries/cnc-hero-background.svg`. Each industry record chooses its introduction and buyer-fit illustration paths. Continue writing distinct, industry-relevant copy for each page, rather than copying another industry's content.

When adding an industry page, also add its entry to `content/home-industries.json` so it appears in the homepage “Built for your world” section and the industry navigation.
