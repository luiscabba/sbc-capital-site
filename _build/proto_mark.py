"""The mark section without the photo: three moving replacements, built on top of How it works C2.
Each one plays in the same scroll lock as the card turn, so the two halves move together.
  _build/proto/mark-d1.html  D1 The check runs: a company file is checked line by line, two officers sign, the mark is stamped
  _build/proto/mark-d2.html  D2 The seal is made: the mark draws itself, the cobalt square drops in, twelve months light around it
  _build/proto/mark-d3.html  D3 What the buyer sees: a supplier list filters down to the SBC-Qualified ones
Run from the repo root: python3 _build/proto_mark.py  (runs proto_how_c.py first)
"""
import subprocess, os
subprocess.run(['python3', '_build/proto_how_c.py'], check=True)
BASE = open('_build/proto/how-c2.html', encoding='utf-8').read()

ACC = {'day': '#1F4FD1', 'night': '#7E9CFF'}


def mini_mark(mode, size=22):
    ink = '#1A1D24' if mode == 'day' else '#FFFFFF'
    return ('<svg width="%d" height="%d" viewBox="0 0 100 100" aria-hidden="true"><rect x="6" y="6" width="88" height="88" fill="none" stroke="%s" stroke-width="8"/>'
            '<rect x="62" y="14" width="24" height="24" fill="%s"/></svg>' % (size, size, ink, ACC[mode]))


def vis_d1(mode):
    checks = [('Ownership', 'Who really owns it'), ('Sanctions', 'UAE, UN, OFAC, EU, UK lists'), ('Licences', 'Trade licence current'),
              ('Agent', 'Who speaks for the company'), ('ICV', 'In-country value score')]
    lis = ''.join('<li><div><b>%s</b><span>%s</span></div><span class="fx-st"><span class="fx-wait">Checking</span><span class="fx-ok">Clear</span></span></li>' % c for c in checks)
    return ('<div class="mx-vis"><div class="fx-file"><span class="fx-beam" aria-hidden="true"></span>'
            '<div class="fx-head"><span class="fx-k">Company file · sample</span><b>Harbor Line Marine LLC</b><span>Pumps and valves · Jebel Ali</span></div>'
            '<ul class="fx-checks">%s</ul>' % lis +
            '<div class="fx-officers"><span class="fx-sig"><i></i>Officer one</span><span class="fx-sig"><i></i>Officer two</span></div>'
            '<div class="fx-stamp">%s<div><b>SBC-Qualified</b><span>Valid for one year</span></div></div></div></div>' % mini_mark(mode, 46))


def vis_d2(mode):
    ticks = ''
    import math
    for i in range(12):
        a = math.radians(i * 30 - 90)
        x1, y1, x2, y2 = 200 + 196 * math.cos(a), 200 + 196 * math.sin(a), 200 + 222 * math.cos(a), 200 + 222 * math.sin(a)
        ticks += '<line class="sx-tick" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x1, y1, x2, y2)
    return ('<div class="mx-vis"><div class="sx-wrap"><svg class="sx" viewBox="-40 -40 480 480" aria-hidden="true">'
            '<g class="sx-ticks">%s</g>' % ticks +
            '<rect class="sx-box" x="70" y="70" width="260" height="260" pathLength="1"/>'
            '<text class="sx-t" x="186" y="236" text-anchor="middle">SBC</text>'
            '<rect class="sx-cap" x="240" y="94" width="66" height="66"/></svg>'
            '<div class="sx-cap-l"><span class="sx-l1">Checked, approved, marked.</span><span class="sx-l2">Twelve months, then checked again.</span></div></div></div>')


def vis_d3(mode):
    rows = [('HL', 'Harbor Line Marine', 'Pumps and valves · Jebel Ali', 1), ('DS', 'Dune Steel Works', 'Fabrication · Sharjah', 0),
            ('AS', 'Al Safa Fittings', 'Pipe fittings · Dubai', 1), ('CL', 'Creek Logistics', 'Freight · Deira', 0),
            ('GP', 'Gulfline Pumps', 'Pumps · Ajman', 0), ('NC', 'Northgate Coatings', 'Marine coatings · Abu Dhabi', 1)]
    lis = ''.join('<li class="lx-r %s"><span class="lx-av">%s</span><div><b>%s</b><span>%s</span></div>%s</li>' % (
        'q' if q else 'n', av, n, m, ('<span class="lx-mk">%s<span>Qualified</span></span>' % mini_mark(mode, 20)) if q else '') for av, n, m, q in rows)
    return ('<div class="mx-vis"><div class="lx"><div class="lx-top"><span class="lx-k">What a buyer sees · sample</span><b>Marine pumps, UAE</b>'
            '<div class="lx-bar"><span class="lx-count"><span class="lx-a">6 suppliers</span><span class="lx-b">3 SBC-Qualified</span></span>'
            '<span class="lx-f"><span class="lx-tog"><i></i></span>SBC-Qualified only</span></div></div><ul class="lx-list">%s</ul></div></div>' % lis)


CSS = r'''<style id="mark-proto">
/* the panel that replaces the photo */
.mx{position:absolute;inset:0;display:flex;flex-direction:column;gap:36px;padding:64px 72px;box-sizing:border-box;overflow:hidden}
.mode-day .mx{background:#F4F6FB}.mode-night .mx{background:#161A24}
.mx::before{content:"";position:absolute;inset:0;z-index:-1;opacity:.6}
.mode-day .mx::before{background:repeating-linear-gradient(30deg,transparent 0 79px,rgba(31,79,209,.08) 79px 80px),repeating-linear-gradient(-30deg,transparent 0 79px,rgba(31,79,209,.08) 79px 80px)}
.mode-night .mx::before{background:repeating-linear-gradient(30deg,transparent 0 79px,rgba(255,255,255,.05) 79px 80px),repeating-linear-gradient(-30deg,transparent 0 79px,rgba(255,255,255,.05) 79px 80px)}
.mx-vis{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
@media (min-width:901px){
  .mx .mark-badge{position:static !important;background:transparent !important;padding:0 !important;gap:14px !important;color:inherit !important}
  .mx .mark-badge svg{width:48px;height:48px}
  .mx .mark-badge span{font-size:22px !important}
  .mode-night .mx .mark-badge svg rect:not(.pulse){stroke:#FFFFFF}
  .mode-night .mx .mark-badge svg text{fill:#FFFFFF}
}
@media (max-width:900px){.mx{position:static;padding:0;background:none !important}.mx::before{display:none}.mx-vis{display:none}}
.mx b{font-weight:600}
.mx .k,.fx-k,.lx-k{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:11px;letter-spacing:.08em;text-transform:uppercase}

/* ===== D1 the check runs ===== */
.fx-file{position:relative;width:min(440px,100%);margin-bottom:40px;padding:28px 30px 30px;box-sizing:border-box;box-shadow:0 30px 60px rgba(14,18,32,.18);overflow:visible}
.mode-day .fx-file{background:#FFFFFF;color:#1A1D24}.mode-night .fx-file{background:#20242F;color:#FFFFFF;box-shadow:0 30px 60px rgba(0,0,0,.45)}
.fx-head{display:flex;flex-direction:column;gap:4px;padding-bottom:18px;border-bottom:1px solid}
.mode-day .fx-head{border-color:#E1E5EE}.mode-night .fx-head{border-color:#343947}
.fx-head b{font-size:20px}.fx-head>span:last-child{font-size:14px}
.mode-day .fx-k,.mode-day .fx-head>span:last-child,.mode-day .fx-checks div span{color:#666C7D}
.mode-night .fx-k,.mode-night .fx-head>span:last-child,.mode-night .fx-checks div span{color:#A9AFBA}
.fx-checks{list-style:none;margin:0;padding:6px 0;display:flex;flex-direction:column}
.fx-checks li{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:11px 0;border-bottom:1px solid}
.mode-day .fx-checks li{border-color:#EEF0F5}.mode-night .fx-checks li{border-color:#2B303C}
.fx-checks b{display:block;font-size:15px}.fx-checks div span{display:block;font-size:12.5px;margin-top:2px}
.fx-st{position:relative;width:86px;height:22px;flex:none;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
.fx-st>span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.mode-day .fx-wait{color:#9AA0AE;border:1px dashed #C9CEDA}.mode-night .fx-wait{color:#7C8394;border:1px dashed #454B5A}
.fx-ok{opacity:0}
.mode-day .fx-ok{background:#1F4FD1;color:#FFFFFF}.mode-night .fx-ok{background:#7E9CFF;color:#10131B}
.fx-officers{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding-top:18px}
.fx-sig{display:flex;flex-direction:column;gap:8px;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
.mode-day .fx-sig{color:#666C7D}.mode-night .fx-sig{color:#A9AFBA}
.fx-sig i{display:block;height:2px;transform-origin:left}
.mode-day .fx-sig i{background:#1A1D24}.mode-night .fx-sig i{background:#FFFFFF}
.fx-stamp{position:absolute;right:-56px;bottom:-62px;display:flex;align-items:center;gap:14px;padding:16px 20px;border:3px solid;transform-origin:center}
.mode-day .fx-stamp{background:#FFFFFF;border-color:#1F4FD1;color:#1A1D24;box-shadow:0 20px 40px rgba(31,79,209,.25)}
.mode-night .fx-stamp{background:#1A1D24;border-color:#7E9CFF;color:#FFFFFF;box-shadow:0 20px 40px rgba(126,156,255,.25)}
.fx-stamp b{display:block;font-size:17px}.fx-stamp div span{display:block;font-size:12.5px;margin-top:2px}
.mode-day .fx-stamp div span{color:#666C7D}.mode-night .fx-stamp div span{color:#A9AFBA}
.fx-beam{position:absolute;left:-12px;right:-12px;top:0;height:2px;opacity:0;z-index:2;pointer-events:none}
.mode-day .fx-beam{background:#1F4FD1;box-shadow:0 0 16px 3px rgba(31,79,209,.45)}
.mode-night .fx-beam{background:#7E9CFF;box-shadow:0 0 16px 3px rgba(126,156,255,.55)}

/* ===== D2 the seal is made ===== */
.sx-wrap{display:flex;flex-direction:column;align-items:center;gap:28px;width:100%}
.sx{width:min(440px,100%);height:auto;overflow:visible}
.sx-box{fill:none;stroke:currentColor;stroke-width:14;stroke-dasharray:1}
.sx-t{font-family:'Readex Pro',system-ui,sans-serif;font-weight:600;font-size:84px;fill:currentColor}
.mode-day .sx-cap{fill:#1F4FD1;filter:drop-shadow(0 10px 22px rgba(31,79,209,.5))}
.mode-night .sx-cap{fill:#7E9CFF;filter:drop-shadow(0 10px 26px rgba(126,156,255,.6))}
.sx-tick{stroke-width:5;stroke-linecap:square}
.mode-day .sx-tick{stroke:#1F4FD1}.mode-night .sx-tick{stroke:#7E9CFF}
.sx-cap-l{display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center}
.sx-l1{font-weight:600;font-size:22px}
.sx-l2{font-size:15px}.mode-day .sx-l2{color:#666C7D}.mode-night .sx-l2{color:#A9AFBA}

/* ===== D3 what the buyer sees ===== */
.lx{width:min(460px,100%);padding:24px;box-sizing:border-box;box-shadow:0 30px 60px rgba(14,18,32,.18)}
.mode-day .lx{background:#FFFFFF;color:#1A1D24}.mode-night .lx{background:#20242F;color:#FFFFFF;box-shadow:0 30px 60px rgba(0,0,0,.45)}
.lx-top{display:flex;flex-direction:column;gap:4px;padding-bottom:16px}
.lx-top>b{font-size:20px}
.mode-day .lx-k,.mode-day .lx-r div span,.mode-day .lx-f{color:#666C7D}
.mode-night .lx-k,.mode-night .lx-r div span,.mode-night .lx-f{color:#A9AFBA}
.lx-bar{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:12px;padding:10px 12px}
.mode-day .lx-bar{background:#F4F6FB}.mode-night .lx-bar{background:#1A1D24}
.lx-count{position:relative;display:block;width:150px;height:20px;font-weight:600;font-size:14px}
.lx-count>span{position:absolute;left:0;top:0;white-space:nowrap}
.lx-b{opacity:0}.mode-day .lx-b{color:#1F4FD1}.mode-night .lx-b{color:#7E9CFF}
.lx-f{display:flex;align-items:center;gap:8px;font-size:12.5px}
.lx-tog{position:relative;width:32px;height:18px;border-radius:9px;flex:none}
.mode-day .lx-tog{background:#C9CEDA}.mode-night .lx-tog{background:#454B5A}
.lx-tog i{position:absolute;left:2px;top:2px;width:14px;height:14px;border-radius:50%;background:#FFFFFF}
.lx-on{position:absolute;inset:0;border-radius:9px;opacity:0}
.lx-list{list-style:none;margin:0;padding:0}
.lx-r{display:grid;grid-template-columns:36px minmax(0,1fr) auto;gap:12px;align-items:center;padding:10px 0;border-top:1px solid;overflow:hidden;box-sizing:border-box}
.mode-day .lx-r{border-color:#EEF0F5}.mode-night .lx-r{border-color:#2B303C}
.lx-av{width:36px;height:36px;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:500}
.mode-day .lx-av{background:#EEF1F7;color:#5B6070}.mode-night .lx-av{background:#2B303C;color:#C9CEDA}
.lx-r b{display:block;font-size:15px}.lx-r div span{display:block;font-size:12.5px;margin-top:2px}
.lx-mk{display:flex;align-items:center;gap:6px;font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;transform-origin:right center}
.mode-day .lx-mk{color:#1F4FD1}.mode-night .lx-mk{color:#7E9CFF}
@media (prefers-reduced-motion: reduce){.fx-ok,.lx-b{opacity:1}.fx-wait,.lx-a,.lx-r.n{display:none}}
</style>
'''

FX = {'d1': r'''function(m,mode){
  var tl=gsap.timeline({paused:true}), beam=m.querySelector('.fx-beam');
  if(!beam) return tl;
  tl.fromTo(beam,{top:'0%',opacity:0},{top:'100%',opacity:1,duration:.4,ease:'none'},.05).to(beam,{opacity:0,duration:.03},.45);
  m.querySelectorAll('.fx-checks li').forEach(function(li,i){var t=.1+i*.07;
    tl.fromTo(li.querySelector('.fx-wait'),{opacity:1},{opacity:0,duration:.03},t)
      .fromTo(li.querySelector('.fx-ok'),{opacity:0,scale:.8},{opacity:1,scale:1,duration:.04,ease:'back.out(3)'},t);});
  m.querySelectorAll('.fx-sig i').forEach(function(e,i){tl.fromTo(e,{scaleX:0},{scaleX:1,duration:.07,ease:'power1.out'},.5+i*.08);});
  tl.fromTo(m.querySelector('.fx-stamp'),{opacity:0,scale:1.7,rotation:-16},{opacity:1,scale:1,rotation:-5,duration:.08,ease:'back.out(2)'},.7);
  return tl.set({},{},1);
}''',
      'd2': r'''function(m,mode){
  var tl=gsap.timeline({paused:true}), box=m.querySelector('.sx-box');
  if(!box) return tl;
  tl.fromTo(box,{attr:{'stroke-dashoffset':1}},{attr:{'stroke-dashoffset':0},duration:.3,ease:'power1.inOut'},.03)
    .fromTo(m.querySelector('.sx-t'),{opacity:0,y:16},{opacity:1,y:0,duration:.08},.25)
    .fromTo(m.querySelector('.sx-cap'),{y:-300,opacity:0},{y:0,opacity:1,duration:.14,ease:'bounce.out'},.36)
    .fromTo(m.querySelector('.sx-l1'),{opacity:0,y:10},{opacity:1,y:0,duration:.06},.5);
  m.querySelectorAll('.sx-tick').forEach(function(t,i){tl.fromTo(t,{opacity:.15},{opacity:1,duration:.02},.56+i*.025);});
  tl.fromTo(m.querySelector('.sx-l2'),{opacity:0,y:10},{opacity:1,y:0,duration:.06},.86)
    .fromTo(m.querySelector('.sx'),{rotation:-4,scale:.94},{rotation:0,scale:1,duration:1,ease:'none'},0);
  return tl.set({},{},1);
}''',
      'd3': r'''function(m,mode){
  var tl=gsap.timeline({paused:true}), knob=m.querySelector('.lx-tog i');
  if(!knob) return tl;
  var acc=mode==='day'?'#1F4FD1':'#7E9CFF', off=mode==='day'?'#C9CEDA':'#454B5A';
  tl.fromTo(knob,{x:0},{x:14,duration:.06,ease:'power2.out'},.1)
    .fromTo(m.querySelector('.lx-tog'),{backgroundColor:off},{backgroundColor:acc,duration:.06},.1)
    .fromTo(m.querySelector('.lx-a'),{opacity:1,y:0},{opacity:0,y:-8,duration:.05},.18)
    .fromTo(m.querySelector('.lx-b'),{opacity:0,y:8},{opacity:1,y:0,duration:.05},.2);
  m.querySelectorAll('.lx-r.n').forEach(function(r,i){var h=r.offsetHeight;
    tl.fromTo(r,{height:h,opacity:1,paddingTop:10,paddingBottom:10,borderTopWidth:1},{height:0,opacity:0,paddingTop:0,paddingBottom:0,borderTopWidth:0,duration:.1,ease:'power1.inOut'},.22+i*.06);});
  m.querySelectorAll('.lx-r.q .lx-mk').forEach(function(k,i){tl.fromTo(k,{opacity:0,scale:.4},{opacity:1,scale:1,duration:.06,ease:'back.out(3)'},.42+i*.08);});
  m.querySelectorAll('.lx-r.q b').forEach(function(b,i){tl.fromTo(b,{color:'inherit'},{color:acc,duration:.05},.42+i*.08);});
  return tl.set({},{},1);
}'''}


def build(key, vis, out):
    s = BASE
    parts, pos = [], 0
    for mode in ('day', 'night'):
        st = s.find('<div class="mode-%s"' % mode, pos)
        g = s.find('<div class="mark-grid"', st)
        c0 = s.find('<div style="position: relative; overflow: hidden">', g) + len('<div style="position: relative; overflow: hidden">')
        c1 = s.find('<div class="mark-panel"', g) - len('</div>')
        assert s[c1:c1 + 6] == '</div>'
        inner = s[c0:c1]
        badge = inner[inner.find('<div class="mark-badge"'):]
        parts.append(s[pos:c0]); parts.append('<div class="mx mx-%s">%s%s</div>' % (key, badge, vis(mode))); pos = c1
    parts.append(s[pos:])
    s = ''.join(parts)
    hook_old = "gsap.timeline({scrollTrigger:lock(mark,'120%')})"
    assert s.count(hook_old) == 1
    s = s.replace(hook_old, "gsap.timeline({scrollTrigger:Object.assign(lock(mark,'150%'),{onUpdate:function(st){markFx(mark,st.progress,mode)}})})")
    s = s.replace("      if(card){\n", "      if(card){\n        mark._fx=null;markFx(mark,0,mode);\n", 1)
    fx = ('<script>\nvar markMake=%s;\nfunction markFx(m,p,mode){if(!m._fx||m._fxMode!==mode){m._fx=markMake(m,mode);m._fxMode=mode}m._fx.progress(p)}\n</script>\n' % FX[key])
    s = s.replace('<script src="/assets/vendor/gsap.min.js"></script>', fx + '<script src="/assets/vendor/gsap.min.js"></script>', 1)
    s = s.replace('</head>', CSS + '</head>', 1)
    open(out, 'w', encoding='utf-8').write(s)


build('d1', vis_d1, '_build/proto/mark-d1.html')
build('d2', vis_d2, '_build/proto/mark-d2.html')
build('d3', vis_d3, '_build/proto/mark-d3.html')
print('ok')
