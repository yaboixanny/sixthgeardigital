# Industry pages

The twelve sectors in `industries.json` are the editorial source for the static pages.

- Shared markup: `templates/industry.html`
- Shared design: `assets/industry.css`
- Form and navigation behavior: `industrial.js`
- Page rendering, local SVG illustrations, homepage directory, sitemap: `scripts/build_industries.py`

Run `python3 scripts/build_industries.py` after editing the data or template. The script does not require third-party packages. Generated `.html` and `.svg` files are committed so the existing static hosting can serve them without a build step.

Each industry has a unique title, canonical URL, description, content, capability choices, and Netlify form name. Form submissions include the industry and source URL. Netlify must detect forms on deployment; delivery is not established by local preview.

The homepage directory is the curated list of sectors requested by the site owner. Each industry page links to the directory and the agency's supporting services. There is no automatic related-industry fallback.

Campaign plans are illustrative. Replace them with client case studies only when supporting facts and publication permission are available. Product capabilities, certifications, and controlled drawing-handling workflows must come from approved business information.

When republishing changed industry content, update `DATE` in the generator to the substantive edit date before regenerating the sitemap entries.

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

The service template retains the supplied industrial image and uses scope options in place of unconfirmed template prices. Examples describe planned workflows rather than client results. The website intake examples are interactive field comparisons, not live customer RFQ submission forms.
