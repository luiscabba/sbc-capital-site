"""Home at phone width, option A (one visual per section), plus a closing band on every screen.
Safe to re-run: it replaces its own <style id="phone-a"> block and its own closing bands.
Run from the repo root: python3 _build/home_phone.py
"""
import re

END_PHOTO = '/assets/img/gulf/gulf-skyline-dawn.webp'   # Gulf skyline at dawn

CSS = '''<style id="phone-a">
/* Home, phones: one visual per section, like the other pages */
@media (max-width:900px){
  /* hero: the headline does the eyebrow's job; the wall supports it rather than filling a third of the screen */
  .hero-text>div:first-child{display:none !important}
  .hero-wall{width:82% !important;margin:0 auto}
  /* photos off; the headings that sat on them become plain section headings */
  .how-grid>div:first-child,.mark-grid>div:first-child{height:auto !important}
  .how-grid>div:first-child>img,.mark-grid>div:first-child>img{display:none !important}
  .how-h2,.mark-badge{position:static !important;background:transparent !important}
  .how-h2{padding:48px 20px 0 !important}
  .mark-badge{padding:48px 20px 0 !important}
  .mode-night .how-h2 h2{color:#FFFFFF !important}
  .mode-night .how-h2 span{color:#A9AFBA !important}
  .mode-night .mark-badge{color:#FFFFFF !important}
  .mode-night .mark-badge svg rect:not(.pulse){stroke:#FFFFFF}
  .mode-night .mark-badge svg text{fill:#FFFFFF}
  .how-side{padding-top:20px !important}
  /* the mark card stays 3D: same card, scaled to fit, a gentler tilt, still floating, turns with the button */
  .mark-panel{padding:36px 0 48px !important;overflow:visible !important}
  .mark-panel>div{transform:scale(.72) !important;transform-origin:top center;margin-bottom:-150px !important}
  .card3d{transform:rotateX(8deg) rotateY(-16deg)}
  .card3d.flipped{transform:rotateX(8deg) rotateY(164deg)}
  .home-end-in{padding:64px 20px 56px !important}
  .home-end h2{font-size:36px !important}
  .home-end .shade{background:linear-gradient(180deg,rgba(14,18,32,.55) 0%,rgba(14,18,32,.92) 70%) !important}
}
/* desktop: the mark section mirrors How it works (card left, photo right) so the two sections alternate */
@media (min-width:901px){.mark-grid>div:first-child{order:2}}
/* on touch screens there is no hover, so the card says how to turn it */
@media (hover:none){.c3front>span:last-child{font-size:0 !important}.c3front>span:last-child::after{content:"Tap the button below to turn it over";font-size:13px}}
</style>
'''


def band(mode):
    btn2 = 'border:1px solid #FFFFFF;color:#FFFFFF'
    return ('<section class="sec home-end" aria-label="Start" style="position:relative;isolation:isolate;overflow:hidden;background:#0E1220;color:#FFFFFF">'
            '<div aria-hidden="true" style="position:absolute;inset:0;z-index:-2;overflow:hidden"><img class="kb-ap" src="%s" alt="" loading="lazy" style="width:100%%;height:100%%;object-fit:cover;object-position:62%% 60%%;display:block"></div>' % END_PHOTO +
            '<div class="shade" aria-hidden="true" style="position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(14,18,32,.94) 0%,rgba(14,18,32,.72) 45%,rgba(14,18,32,.15) 85%)"></div>'
            '<div class="home-end-in" style="padding:112px 72px;display:flex;flex-direction:column;gap:20px;max-width:640px">'
            '<h2 style="margin:0;font-weight:600;font-size:52px;line-height:1.04;letter-spacing:-.025em">Start where you stand.</h2>'
            '<p style="margin:0;font-size:18px;line-height:1.55;color:#DCE1EA">Companies register in five minutes. Buyers post a need for free.</p>'
            '<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="/companies/apply/" style="background:#1F4FD1;color:#FFFFFF;font-size:16px;font-weight:600;padding:15px 22px;text-decoration:none">Start your application</a>'
            '<a href="/buyers/#talk" style="' + btn2 + ';font-size:16px;font-weight:600;padding:14px 22px;text-decoration:none">Post a need</a></div></div></section>')


s = open('index.html', encoding='utf-8').read()
s = re.sub(r'<style id="phone-a">.*?</style>\n', '', s, flags=re.S)
s = re.sub(r'<section class="sec home-end".*?</section>', '', s, flags=re.S)
s = s.replace('</head>', CSS + '</head>', 1)
out, pos = [], 0
for mode in ('day', 'night'):
    st = s.find('<div class="mode-%s"' % mode, pos)
    f = s.find('<footer', st)
    out.append(s[pos:f]); out.append(band(mode)); pos = f
out.append(s[pos:])
open('index.html', 'w', encoding='utf-8').write(''.join(out))
print('ok')
