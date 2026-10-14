# SBC Capital public site

Static site for SBC Capital, designed and built by texxen.

- `index.html`: Home (floating wall hero, how it works, the SBC-Qualified mark)
- `companies/` (and `companies/apply/`), `buyers/`, `review/`: the audience pages
- `contact/`, `privacy/`, `mark-terms/`: interim pages; SBC's unconfirmed facts are [bracketed]
- `_build/`: Python page builders (not deployed); For buyers, How the review works and the interim pages take their head, header and footer from `companies/index.html`, so rerun them after header or footer changes. Home is patched in order: `home_stack.py`, `home_phone.py`, `home_gulf.py`, then `home_scroll.py` (the scroll-locked How it works, card and closing wipe; it runs the `proto_*` chain and writes index.html, once), then `home_polish.py` (smooth scrolling, cobalt night hero button, the hero wall forming and bursting)
- `assets/`: photos and favicon; `site.css` holds the shared header rules (phone header, cobalt night Apply) and `menu.js` builds the phone menu sheet from each page's own header, so nav changes in the header carry into the menu automatically

Day and night modes follow the visitor's system setting, and the sun and moon switch in the header overrides it.
Hosted on Vercel; every push to `main` redeploys.
