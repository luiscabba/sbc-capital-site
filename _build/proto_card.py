"""The mark section, rebuilt as just the card (on top of How it works C2 + locks).
The card is an ID-card proportioned object: pearl front with security-print lines, grain and a foil square in the mark;
deep ink back; a thin metal edge; a sheen that sweeps across as it moves; a floor shadow that narrows mid-turn.
Scroll: it arrives upright as the section scrolls in; then, locked, the light runs across, it turns over in one move, settles on the back.
Desktop: the pointer tilts it a few degrees. Reduced motion: still card plus a Turn button.
  _build/proto/card.html
Run from the repo root: python3 _build/proto_card.py  (runs proto_how_c.py first)
"""
import math, subprocess
subprocess.run(['python3', '_build/proto_how_c.py'], check=True)
s = open('_build/proto/how-c2.html', encoding='utf-8').read()


def guilloche(color, op):
    paths = []
    for k in range(18):
        base, amp, ph = 236 + k * 4.2, 9 + k * .7, k * .38
        d = 'M' + ' L'.join('%.1f %.1f' % (x, base + amp * math.sin(2 * math.pi * x / 170 + ph) + 6 * math.sin(2 * math.pi * x / 61 - ph)) for x in range(-10, 556, 6))
        paths.append('<path d="%s"/>' % d)
    return ('<svg class="mk-guil" viewBox="0 0 540 340" preserveAspectRatio="none" aria-hidden="true"><g fill="none" stroke="%s" stroke-opacity="%s" stroke-width=".8">%s</g></svg>'
            % (color, op, ''.join(paths)))


def grain(id_, mode_vals, blend):
    return ('<svg class="mk-grain" aria-hidden="true" style="mix-blend-mode:%s"><filter id="%s" x="0" y="0" width="100%%" height="100%%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="4" stitchTiles="stitch"/>'
            '<feColorMatrix type="matrix" values="%s"/></filter><rect width="100%%" height="100%%" filter="url(#%s)"/></svg>' % (blend, id_, mode_vals, id_))


def section(mode):
    front = ('<div class="mk-face mk-front">' + grain('mkg-%s-f' % mode, '0 0 0 0 .07  0 0 0 0 .09  0 0 0 0 .22  0 0 0 .16 0', 'multiply') +
             guilloche('#1F4FD1', '.13') +
             '<div class="mk-top"><div class="mk-mark"><span class="mk-foil"></span><b>SBC</b></div>'
             '<div class="mk-wm"><b>SBC-Qualified</b><span>SBC Capital · Dubai</span></div><span class="mk-valid">Valid 12 months</span></div>'
             '<div class="mk-body"><span class="mk-k">It means</span><ul><li>Identity, ownership, licences, screening and Gulf readiness reviewed</li>'
             '<li>Two SBC officers approved</li><li>Re-checked every year</li></ul></div><span class="mk-sheen"></span></div>')
    back = ('<div class="mk-face mk-back">' + grain('mkg-%s-b' % mode, '0 0 0 0 .6  0 0 0 0 .66  0 0 0 0 .85  0 0 0 .22 0', 'screen') +
            guilloche('#FFFFFF', '.07') +
            '<div class="mk-top"><div class="mk-mark mk-ghost"></div>'
            '<div class="mk-wm"><b>What it is not</b><span>Read before you rely on it</span></div></div>'
            '<div class="mk-body"><span class="mk-k">It does not mean</span><ul><li>A government licence or an accreditation</li>'
            '<li>A promised contract</li><li>An introduction to every opportunity</li></ul>'
            '<span class="mk-foot">SBC decides each introduction on its own.</span></div><span class="mk-sheen"></span></div>')
    edges = ''.join('<span class="mk-edge mk-e%s" aria-hidden="true"></span>' % e for e in 'rltb')
    return ('<section class="sec mk" aria-label="The mark"><div class="mk-bg" aria-hidden="true"></div><div class="mk-in">'
            '<div class="mk-head"><span class="mk-kick">SBC-Qualified</span><h2>What the mark means, and what it does not.</h2></div>'
            '<div class="mk-stage"><div class="mk-glow" aria-hidden="true"></div><div class="mk-floor" aria-hidden="true"></div>'
            '<div class="mk-float"><div class="mk-tilt"><div class="mk-card" role="img" aria-label="The SBC-Qualified card. Front: it means identity, ownership, licences, screening and Gulf readiness reviewed, two SBC officers approved, re-checked every year. Back: it does not mean a government licence or accreditation, a promised contract, or an introduction to every opportunity.">'
            + front + back + edges + '</div></div></div></div>'
            '<div class="mk-tabs" aria-hidden="true"><span class="mk-tab on">Front · It means</span><span class="mk-tab">Back · It does not mean</span><i class="mk-bar"></i></div>'
            '<button type="button" class="mk-turn" onclick="this.closest(\'.mk\').classList.toggle(\'is-back\')">Turn the card</button>'
            '</div></section>')


CSS = r'''<style id="card-proto">
.mk{position:relative;isolation:isolate;overflow:hidden;height:100vh;height:100svh;min-height:680px;display:flex;align-items:center}
.mode-day .mk{background:#FFFFFF;color:#1A1D24}.mode-night .mk{background:#1A1D24;color:#FFFFFF}
.mk-bg{position:absolute;inset:0;z-index:-2;opacity:.7;-webkit-mask:radial-gradient(ellipse 60% 70% at 50% 55%,#000 20%,transparent 75%);mask:radial-gradient(ellipse 60% 70% at 50% 55%,#000 20%,transparent 75%)}
.mode-day .mk-bg{background:repeating-linear-gradient(30deg,transparent 0 79px,rgba(31,79,209,.09) 79px 80px),repeating-linear-gradient(-30deg,transparent 0 79px,rgba(31,79,209,.09) 79px 80px)}
.mode-night .mk-bg{background:repeating-linear-gradient(30deg,transparent 0 79px,rgba(255,255,255,.06) 79px 80px),repeating-linear-gradient(-30deg,transparent 0 79px,rgba(255,255,255,.06) 79px 80px)}
.mk-in{width:100%;max-width:1296px;margin:0 auto;padding:48px 72px;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;gap:40px}
.mk-head{display:flex;flex-direction:column;align-items:center;gap:12px;text-align:center}
.mk-kick{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.mode-day .mk-kick{color:#1F4FD1}.mode-night .mk-kick{color:#7E9CFF}
.mk h2{margin:0;font-weight:600;font-size:40px;line-height:1.08;letter-spacing:-.02em;text-wrap:balance;max-width:20ch}

/* stage: perspective, a soft glow, a floor shadow, then float > tilt (pointer) > card (scroll) */
.mk-stage{position:relative;perspective:1800px;width:620px;max-width:100%;display:flex;justify-content:center;padding:10px 0 34px}
.mk-glow{position:absolute;left:50%;top:50%;width:150%;height:150%;transform:translate(-50%,-50%);z-index:-1;pointer-events:none}
.mode-day .mk-glow{background:radial-gradient(closest-side,rgba(31,79,209,.12),transparent)}
.mode-night .mk-glow{background:radial-gradient(closest-side,rgba(61,107,255,.26),transparent)}
.mk-floor{position:absolute;left:12%;right:12%;bottom:0;height:34px;border-radius:50%;filter:blur(16px);transform-origin:center}
.mode-day .mk-floor{background:rgba(26,29,36,.26)}.mode-night .mk-floor{background:rgba(0,0,0,.6);box-shadow:0 0 50px 10px rgba(31,79,209,.25)}
.mk-float{transform-style:preserve-3d;animation:mkfloat 6s ease-in-out infinite}
@keyframes mkfloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.mk-tilt{transform-style:preserve-3d}
.mk-card{--rx:10deg;--ry:-14deg;--ty:0px;--s:1;--sheen:160%;position:relative;width:600px;max-width:calc(100vw - 48px);aspect-ratio:1.586/1;transform-style:preserve-3d;
  transform:translateY(var(--ty)) scale(var(--s)) rotateX(var(--rx)) rotateY(var(--ry));transition:transform .9s cubic-bezier(.2,.7,.2,1)}
html.gs .mk-card{transition:none}
.mk.is-back .mk-card{--ry:186deg}
.mk-face{position:absolute;inset:0;border-radius:16px;overflow:hidden;backface-visibility:hidden;-webkit-backface-visibility:hidden;padding:34px 38px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between}
.mk-front{transform:translateZ(4px);background:linear-gradient(135deg,#FFFFFF 0%,#F8FAFF 45%,#EAEFFA 100%);color:#1A1D24;
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.9),inset 0 0 0 2px rgba(31,79,209,.07),inset 0 -60px 80px -50px rgba(19,36,88,.18)}
.mk-back{transform:rotateY(180deg) translateZ(4px);color:#FFFFFF;box-shadow:inset 0 0 0 1px rgba(255,255,255,.12),inset 0 60px 80px -50px rgba(126,156,255,.18)}
.mode-day .mk-back{background:linear-gradient(135deg,#28345A 0%,#171C2B 58%,#0E1119 100%)}
.mode-night .mk-back{background:linear-gradient(135deg,#36477A 0%,#1F2944 58%,#141A2C 100%)}
.mk-grain{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.mk-guil{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.mk-sheen{position:absolute;inset:0;pointer-events:none;background-size:260% 100%;background-position:var(--sheen) 0;background-repeat:no-repeat}
.mk-front .mk-sheen{background-image:linear-gradient(105deg,transparent 40%,rgba(255,255,255,.95) 47%,rgba(160,184,255,.38) 51%,transparent 58%)}
.mk-back .mk-sheen{background-image:linear-gradient(105deg,transparent 40%,rgba(255,255,255,.16) 47%,rgba(126,156,255,.22) 51%,transparent 58%)}
/* edges: a thin metal rim, inset from the rounded corners */
.mk-edge{position:absolute}
.mk-er,.mk-el{top:14px;bottom:14px;width:8px}
.mk-er{right:-4px;transform:rotateY(90deg)}.mk-el{left:-4px;transform:rotateY(-90deg)}
.mk-et,.mk-eb{left:14px;right:14px;height:8px}
.mk-et{top:-4px;transform:rotateX(90deg)}.mk-eb{bottom:-4px;transform:rotateX(-90deg)}
.mode-day .mk-edge{background:linear-gradient(90deg,#E3E8F5,#9CA9CF 50%,#C9D2EA)}
.mode-night .mk-edge{background:linear-gradient(90deg,#6B7AA8,#2B3454 50%,#4C5A86)}
/* card content */
.mk-top{position:relative;display:flex;align-items:center;gap:16px}
.mk-mark{position:relative;width:58px;height:58px;flex:none;box-sizing:border-box;border:3.5px solid #1A1D24;display:flex;align-items:flex-end;justify-content:center;padding-bottom:9px}
.mk-mark b{font-weight:600;font-size:17px;letter-spacing:-.01em;line-height:1}
.mk-foil{position:absolute;right:5px;top:5px;width:15px;height:15px;background:linear-gradient(135deg,#1F4FD1 0%,#3D6BF0 30%,#B9C9FF 50%,#3D6BF0 70%,#1F4FD1 100%);background-size:300% 300%;background-position:var(--sheen) 50%;box-shadow:0 0 10px rgba(61,107,255,.45)}
.mk-ghost{border:1.5px dashed rgba(255,255,255,.7)}
.mk-wm{display:flex;flex-direction:column;gap:3px;min-width:0}
.mk-wm b{font-weight:600;font-size:21px;letter-spacing:-.01em}
.mk-wm span,.mk-valid,.mk-k{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase}
.mk-front .mk-wm span,.mk-front .mk-valid{color:#666C7D}.mk-back .mk-wm span{color:#A9B3CC}
.mk-valid{margin-left:auto;align-self:flex-start;padding:5px 8px;border:1px solid rgba(31,79,209,.25);color:#1F4FD1 !important}
.mk-body{position:relative;display:flex;flex-direction:column;gap:12px}
.mk-front .mk-k{color:#1F4FD1}.mk-back .mk-k{color:#9DB4FF}
.mk-body ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px}
.mk-body li{position:relative;padding-left:20px;font-size:17px;line-height:1.4}
.mk-body li::before{content:"";position:absolute;left:0;top:.48em;width:8px;height:8px}
.mk-front li::before{background:#1F4FD1}.mk-back li::before{border:1.5px solid #9DB4FF;box-sizing:border-box}
.mk-foot{font-size:13px;color:#A9B3CC;margin-top:4px}
/* which side */
.mk-tabs{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:28px;padding-bottom:10px;font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.mk-tab{text-align:center;transition:color .3s ease}
.mode-day .mk-tab{color:#9AA0AE}.mode-night .mk-tab{color:#6E7486}
.mode-day .mk-tab.on{color:#1A1D24}.mode-night .mk-tab.on{color:#FFFFFF}
.mk-bar{position:absolute;left:0;bottom:0;width:calc(50% - 14px);height:2px;transition:transform .45s cubic-bezier(.6,0,.2,1)}
.mode-day .mk-bar{background:#1F4FD1}.mode-night .mk-bar{background:#7E9CFF}
.mk.is-back .mk-bar{transform:translateX(calc(100% + 28px))}
.mk-turn{min-height:44px;padding:0 18px;background:transparent;border:1px solid currentColor;color:inherit;font-family:'Readex Pro',sans-serif;font-size:15px;cursor:pointer}
html.gs .mk-turn{display:none}
@media (max-width:900px){
  .mk{min-height:600px}
  .mk-in{padding:28px 20px;gap:28px}
  .mk h2{font-size:28px}
  .mk-stage{width:100%}
  .mk-card{width:min(320px,calc(100vw - 56px));aspect-ratio:.7/1}
  .mk-face{padding:24px 22px;border-radius:14px}
  .mk-top{flex-wrap:wrap;gap:12px}
  .mk-valid{margin-left:0;order:3}
  .mk-wm b{font-size:18px}
  .mk-body li{font-size:15px}
  .mk-tabs{gap:16px;font-size:10px}
  .mk-bar{width:calc(50% - 8px)}.mk.is-back .mk-bar{transform:translateX(calc(100% + 16px))}
}
@media (prefers-reduced-motion: reduce){.mk-float{animation:none}}
</style>
'''

MARK_JS = r'''// ===== The mark: the card rises, is read, turns over, is read again; all while locked =====
      var mk=root.querySelector('.mk');
      if(mk){
        var card=mk.querySelector('.mk-card'), floor=mk.querySelector('.mk-floor'), tabs=mk.querySelectorAll('.mk-tab');
        var side=function(p){var b=p>=0.47;mk.classList.toggle('is-back',b);tabs[0].classList.toggle('on',!b);tabs[1].classList.toggle('on',b)};
        side(0);
        var stage=mk.querySelector('.mk-stage');
        // arrive: while the section scrolls in, the card comes up small and softly tilted and settles upright,
        // so it is already in place (never lying back, never cut off) by the time the section holds
        gsap.timeline({scrollTrigger:{trigger:mk,start:'top 92%',end:'top top',scrub:.8}})
          .fromTo(card,{'--rx':'26deg','--ry':'-26deg','--ty':'90px','--s':.78},{'--rx':'10deg','--ry':'-14deg','--ty':'0px','--s':1,ease:'power2.out',duration:1},0)
          .fromTo(stage,{opacity:0},{opacity:1,ease:'power1.out',duration:.6},0)
          .fromTo(floor,{scaleX:.6,opacity:.3},{scaleX:1,opacity:1,ease:'power2.out',duration:1},0);
        // held: light runs across the front, a beat to read it, one turn, a beat on the back
        gsap.timeline({scrollTrigger:Object.assign(lock(mk,'130%'),{onUpdate:function(st){side(st.progress)}})})
          .fromTo(card,{'--sheen':'160%'},{'--sheen':'-60%',duration:.24,ease:'power1.inOut',immediateRender:false},0)
          .fromTo(card,{'--ry':'-14deg'},{'--ry':'-9deg',duration:.24,ease:'none',immediateRender:false},0)
          .fromTo(card,{'--ry':'-9deg'},{'--ry':'186deg',duration:.4,ease:'power2.inOut',immediateRender:false},.26)
          .fromTo(card,{'--ty':'0px','--rx':'10deg'},{'--ty':'-26px','--rx':'4deg',duration:.2,ease:'power1.out',immediateRender:false},.26)
          .fromTo(card,{'--ty':'-26px','--rx':'4deg'},{'--ty':'0px','--rx':'10deg',duration:.2,ease:'power1.in',immediateRender:false},.46)
          .fromTo(floor,{scaleX:1,opacity:1},{scaleX:.45,opacity:.55,duration:.2,ease:'power1.out',immediateRender:false},.26)
          .fromTo(floor,{scaleX:.45,opacity:.55},{scaleX:1,opacity:1,duration:.2,ease:'power1.in',immediateRender:false},.46)
          .fromTo(card,{'--sheen':'160%'},{'--sheen':'-60%',duration:.26,ease:'power1.inOut',immediateRender:false},.44)
          .fromTo(card,{'--ry':'186deg'},{'--ry':'181deg',duration:.34,ease:'none',immediateRender:false},.66);
        // desktop: the pointer tilts it a little
        if(matchMedia('(hover: hover) and (pointer: fine)').matches){
          var tilt=mk.querySelector('.mk-tilt');
          var rx=gsap.quickTo(tilt,'rotationX',{duration:.6,ease:'power3.out'}), ry=gsap.quickTo(tilt,'rotationY',{duration:.6,ease:'power3.out'});
          mk.addEventListener('pointermove',function(e){var r=stage.getBoundingClientRect();
            ry(((e.clientX-r.left)/r.width-.5)*10); rx(-((e.clientY-r.top)/r.height-.5)*8)});
          mk.addEventListener('pointerleave',function(){rx(0);ry(0)});
        }
      }
      '''

# swap the mark section in both modes
parts, pos = [], 0
for mode in ('day', 'night'):
    st = s.find('<div class="mode-%s"' % mode, pos)
    a = s.find('<section class="sec" aria-label="The mark"', st)
    b = s.find('</section>', a) + len('</section>')
    parts.append(s[pos:a]); parts.append(section(mode)); pos = b
parts.append(s[pos:])
s = ''.join(parts)
a = s.find('// ===== The mark'); b = s.find('// ===== Closing band')
assert a > 0 and b > a
s = s[:a] + MARK_JS + s[b:]
s = s.replace('</head>', CSS + '</head>', 1)
open('_build/proto/card.html', 'w', encoding='utf-8').write(s)
print('ok')
