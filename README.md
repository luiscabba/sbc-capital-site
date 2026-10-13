# SBC Capital public site

Static site for SBC Capital, designed and built by texxen.

- `index.html`: Home (floating wall hero, how it works, the SBC-Qualified mark)
- `companies/` (and `companies/apply/`), `buyers/`, `review/`: the audience pages
- `contact/`, `privacy/`, `mark-terms/`: interim pages; SBC's unconfirmed facts are [bracketed]
- `_build/`: Python page builders (not deployed); For buyers, How the review works and the interim pages take their head, header and footer from `companies/index.html`, so rerun them after header or footer changes
- `assets/`: photos and favicon

Day and night modes follow the visitor's system setting, and the sun and moon switch in the header overrides it.
Hosted on Vercel; every push to `main` redeploys.
