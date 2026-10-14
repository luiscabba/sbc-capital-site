"""Final polish for Home (runs after home_polish.py; safe to run again).

- Closing band: pins when its bottom meets the screen's bottom, so the photo wipe always
  finishes and no blank band shows above or below it.
- How it works at 1024: tighter columns so step 03 is never cut off and the heading balances.
- Hero eyebrow at narrow desktops: one line, no separator left dangling.
- Phones: the stack's step numbers and callout readable; the mark's small mono text at 12px;
  the card's turn stays clear of the heading.
Run from the repo root:  python3 _build/home_finish.py
"""
P = 'index.html'
s = open(P, encoding='utf-8').read()

OLD = "gsap.timeline({scrollTrigger:lock(end,'100%')})"
NEW = "gsap.timeline({scrollTrigger:Object.assign(lock(end,'70%'),{start:'bottom bottom'})})"
if OLD in s:
    s = s.replace(OLD, NEW)
assert NEW in s

CSS = r'''<style id="home-finish">
/* ===== Home final polish ===== */
@media (min-width:901px) and (max-width:1180px){
  .hc-in{padding:40px 40px !important;gap:48px !important}
  .hc-art{width:min(440px,calc(100vh - 210px)) !important;width:min(440px,calc(100svh - 210px)) !important}
  .hc-copy{gap:16px !important}
  .hc-copy h2{text-wrap:balance}
  .cv-copy > div:first-child,.hero-text > div:first-child{font-size:11px !important;letter-spacing:.06em !important;gap:8px 10px !important;flex-wrap:nowrap !important;white-space:nowrap}
}
.hc-copy h2,.mk-head h2,.home-end h2{text-wrap:balance}
.mk-head{position:relative;z-index:3}
@media (max-width:600px){
  .hc-stack .st-n{font-size:20px}
  .hc-stack .st-b{font-size:19px}
  .hc-stack .st-s{display:none}
  .mk-k{font-size:12px !important}
  .mk-tabs{font-size:11px !important;align-items:end}
  .mk-stage{padding-top:44px !important}
}
</style>
'''
if '<style id="home-finish">' not in s:
    s = s.replace('</head>', CSS + '</head>', 1)
open(P, 'w', encoding='utf-8').write(s)
print('home_finish: ok')
