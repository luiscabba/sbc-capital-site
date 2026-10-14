"""Phone-only prototypes of Home (not deployed): _build/proto/a.html and b.html.
A: one visual per section (photos off on phones, the stone photo moves to a closing band).
B: photos kept as short landscape bands with the headline under them, plain closing band.
Desktop is untouched in both. Run from the repo root: python3 _build/proto_home.py
"""
import os

SRC = open('index.html', encoding='utf-8').read()

COMMON = '''
@media (max-width:900px){
  /* hero: the headline does the eyebrow's job; the wall is a supporting picture, not a third of the screen */
  .hero-text>div:first-child{display:none !important}
  .hero-wall{width:82% !important;margin:0 auto}
  /* the mark card lies flat on phones: no tilt, full width, turns with the button */
  .mark-panel>div{transform:none !important;margin-bottom:0 !important}
  .c3wrap{animation:none !important}
  .card3d{width:min(350px,calc(100vw - 40px)) !important;height:440px !important;transform:none !important}
  .card3d.flipped{transform:rotateY(180deg) !important}
  .c3f{padding:28px !important}
  .c3f ul{font-size:17px !important}
  .c3shadow{display:none}
  .mark-panel{padding:24px 20px 56px !important}
  /* headings that sat on photos become plain section headings */
  .how-h2,.mark-badge{position:static !important;background:transparent !important}
  .how-h2{padding:48px 20px 0 !important}
  .mark-badge{padding:48px 20px 0 !important}
  .mode-night .how-h2 h2{color:#FFFFFF !important}
  .mode-night .how-h2 span{color:#A9AFBA !important}
  .mode-night .mark-badge{color:#FFFFFF !important}
  .mode-night .mark-badge svg rect:not(.pulse){stroke:#FFFFFF}
  .mode-night .mark-badge svg text{fill:#FFFFFF}
  .how-side{padding-top:20px !important}
  .home-end-in{padding:64px 20px 56px !important}
  .home-end h2{font-size:36px !important}
}
@media (hover:none){.c3front>span:last-child{display:none}}
'''

A = COMMON + '''
@media (max-width:900px){
  .how-grid>div:first-child,.mark-grid>div:first-child{height:auto !important}
  .how-grid>div:first-child>img,.mark-grid>div:first-child>img{display:none !important}
}
'''

B = COMMON + '''
@media (max-width:900px){
  .how-grid>div:first-child,.mark-grid>div:first-child{height:auto !important;display:flex;flex-direction:column}
  .how-grid>div:first-child>img,.mark-grid>div:first-child>img{height:210px !important}
  .how-h2{padding-top:32px !important}.mark-badge{padding-top:32px !important}
}
'''


def end_band(photo):
    bg = ('<div aria-hidden="true" style="position:absolute;inset:0;z-index:-2;overflow:hidden"><img src="/assets/img/4d27b8120b3c93094094b2023236d91c.webp" alt="" style="width:100%;height:100%;object-fit:cover;object-position:82% 45%;display:block"></div>'
          '<div aria-hidden="true" style="position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(14,18,32,.55) 0%,rgba(14,18,32,.92) 70%)"></div>') if photo else ''
    return ('<section class="sec home-end" aria-label="Start" style="position:relative;isolation:isolate;overflow:hidden;background:#0E1220;color:#FFFFFF">' + bg +
            '<div class="home-end-in" style="padding:112px 72px;display:flex;flex-direction:column;gap:20px;max-width:640px">'
            '<h2 style="margin:0;font-weight:600;font-size:52px;line-height:1.04;letter-spacing:-.025em">Start where you stand.</h2>'
            '<p style="margin:0;font-size:18px;line-height:1.55;color:#DCE1EA">Companies register in five minutes. Buyers post a need for free.</p>'
            '<div style="display:flex;gap:12px;flex-wrap:wrap"><a href="/companies/apply/" style="background:#1F4FD1;color:#FFFFFF;font-size:16px;font-weight:600;padding:15px 22px;text-decoration:none">Start your application</a>'
            '<a href="/buyers/#talk" style="border:1px solid #FFFFFF;color:#FFFFFF;font-size:16px;font-weight:600;padding:14px 22px;text-decoration:none">Post a need</a></div></div></section>')


def build(css, photo):
    s = SRC.replace('</head>', '<style>' + css + '</style>\n</head>', 1)
    out, pos = [], 0
    for mode in ('day', 'night'):
        st = s.find('<div class="mode-%s"' % mode, pos)
        f = s.find('<footer', st)
        out.append(s[pos:f]); out.append(end_band(photo)); pos = f
    out.append(s[pos:])
    return ''.join(out)


os.makedirs('_build/proto', exist_ok=True)
open('_build/proto/a.html', 'w', encoding='utf-8').write(build(A, True))
open('_build/proto/b.html', 'w', encoding='utf-8').write(build(B, False))
print('ok')
