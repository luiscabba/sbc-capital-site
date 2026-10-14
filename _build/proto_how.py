"""Two parallax redesigns of Home's How it works, for review only (not deployed from main).
  _build/proto/how-a.html  A · The steps stack up: the port drifts behind three step cards that ride over it
                                at different speeds and settle into one stack, cobalt on top.
  _build/proto/how-b.html  B · The window: the port moves inside a big SBC-mark frame; the steps light up
                                beside it while cubes drift past in front.
Both start from the live index.html and keep everything else as it is. GSAP is self-hosted in assets/vendor/.
Run from the repo root: python3 _build/proto_how.py
"""
import os

SRC = open('index.html', encoding='utf-8').read()
PORT = '/assets/img/gulf/gulf-port-night.webp'
STEPS = [('Apply and upload', 'One checklist, finished over several sittings.', 'You', 'Your company'),
         ('Two officers review', 'Each one separately. Pass, and you are SBC-Qualified for a year.', 'SBC', 'Two officers'),
         ('SBC approves the introduction', 'Only then does the buyer see you.', 'SBC', 'Approval')]
H2 = 'Nothing reaches a buyer until SBC approves it.'


def section_a(mode):
    cards = ''.join(
        '<li class="ha-card ha-c%d" data-depth="%d"><span class="ha-n">%02d</span><div><b>%s</b><span>%s</span></div><span class="ha-who">%s</span></li>'
        % (i + 1, i, i + 1, t, d, who) for i, (t, d, who, _) in enumerate(STEPS))
    return ('<section class="sec ha" aria-label="How it works">'
            '<div class="ha-bg" aria-hidden="true"><img src="%s" alt=""></div><div class="ha-shade" aria-hidden="true"></div>' % PORT +
            '<div class="ha-in"><div class="ha-copy"><span class="ha-k">How it works</span><h2>%s</h2>'
            '<p>Three steps, each resting on the one before. A buyer only ever sees the finished stack.</p></div>'
            '<ol class="ha-stack" aria-label="The three steps">%s</ol></div>'
            '<span class="ha-cap" aria-hidden="true">Jebel Ali style port at night · generated image</span></section>' % (H2, cards))


def section_b(mode):
    rows = ''.join(
        '<li class="hb-row" data-i="%d"><span class="hb-n">%02d</span><div><b>%s</b><span>%s</span></div></li>' % (i, i + 1, t, d)
        for i, (t, d, _, _) in enumerate(STEPS))
    cubes = ''.join('<img class="hb-cube" data-speed="%s" src="/assets/img/sbc/%s" alt="" style="left:%s;top:%s;width:%s">' % c for c in [
        ('2.2', 'cube-lit.svg', '46%', '74%', '64px'), ('1.4', 'cube-frost.svg' if mode == 'day' else 'cube-frost-n.svg', '6%', '18%', '52px'),
        ('3.0', 'cube-ghost.svg' if mode == 'day' else 'cube-ghost-n.svg', '90%', '64%', '46px')])
    return ('<section class="sec hb" aria-label="How it works">' + cubes +
            '<div class="hb-in"><div class="hb-frame" aria-hidden="true"><div class="hb-win"><img src="%s" alt=""></div><span class="hb-lit"></span></div>' % PORT +
            '<div class="hb-copy"><span class="hb-k">How it works</span><h2>%s</h2><ol class="hb-rows">%s</ol></div></div></section>' % (H2, rows))


CSS = '''<style id="how-proto">
/* ===== A · the steps stack up ===== */
.ha{position:relative;isolation:isolate;overflow:hidden;background:#0B0E19;color:#FFFFFF;min-height:1080px;display:flex;align-items:center}
.ha-bg{position:absolute;inset:-14% 0;z-index:-2}
.ha-bg img{width:100%;height:100%;object-fit:cover;object-position:30% center;display:block}
.ha-shade{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(11,14,25,.86) 0%,rgba(11,14,25,.5) 48%,rgba(11,14,25,.15) 100%),linear-gradient(0deg,rgba(11,14,25,.7) 0%,transparent 40%)}
.ha-in{width:100%;max-width:1296px;margin:0 auto;padding:120px 72px;box-sizing:border-box;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,520px);gap:64px;align-items:center}
.ha-copy{display:flex;flex-direction:column;gap:18px;max-width:520px}
.ha-k{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#C9CEDA}
.ha h2{margin:0;font-weight:600;font-size:52px;line-height:1.04;letter-spacing:-.025em;text-wrap:balance}
.ha-copy p{margin:0;font-size:18px;line-height:1.55;color:#DCE1EA;max-width:44ch}
.ha-stack{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:22px}
.ha-card{position:relative;display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:16px;align-items:center;padding:24px 26px;background:#FFFFFF;color:#1A1D24;box-shadow:0 30px 60px rgba(0,0,0,.45);will-change:transform}
.ha-card b{display:block;font-weight:600;font-size:21px;line-height:1.25}
.ha-card div span{display:block;margin-top:4px;font-size:15px;line-height:1.5;color:#5B6070}
.ha-n{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:13px;letter-spacing:.08em;color:#5B6070}
.ha-who{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:11px;letter-spacing:.08em;text-transform:uppercase;padding:5px 8px;border:1px solid #D3D8E4;color:#5B6070}
.ha-c2{background:#EEF2FC}
.ha-c3{background:#1F4FD1;color:#FFFFFF}
.ha-c3 div span,.ha-c3 .ha-n{color:#DCE5FF}
.ha-c3 .ha-who{border-color:rgba(255,255,255,.5);color:#FFFFFF}
.ha-c1{z-index:1}.ha-c2{z-index:2}.ha-c3{z-index:3}
.ha-cap{position:absolute;right:20px;bottom:16px;font-family:'IBM Plex Mono',monospace;font-size:11px;color:rgba(255,255,255,.7)}
@media (max-width:900px){
  .ha{min-height:0}
  .ha-in{grid-template-columns:1fr;padding:72px 20px 88px;gap:40px}
  .ha h2{font-size:34px}
  .ha-shade{background:linear-gradient(180deg,rgba(11,14,25,.82) 0%,rgba(11,14,25,.55) 50%,rgba(11,14,25,.8) 100%)}
  .ha-card{padding:18px;grid-template-columns:32px minmax(0,1fr);gap:12px}
  .ha-who{display:none}
  .ha-card b{font-size:18px}
}
/* ===== B · the window ===== */
.hb{position:relative;isolation:isolate;overflow:hidden;min-height:900px;display:flex;align-items:center}
.mode-day .hb{background:#FFFFFF;color:#1A1D24}.mode-night .hb{background:#1A1D24;color:#FFFFFF}
.hb-in{width:100%;max-width:1296px;margin:0 auto;padding:112px 72px;box-sizing:border-box;display:grid;grid-template-columns:minmax(0,560px) minmax(0,1fr);gap:72px;align-items:center}
.hb-frame{position:relative;aspect-ratio:1/1;width:100%;box-sizing:border-box;border:18px solid currentColor}
.hb-win{position:absolute;inset:0;overflow:hidden}
.hb-win img{position:absolute;left:0;top:-30%;width:100%;height:160%;object-fit:cover;object-position:30% center;display:block;will-change:transform}
.hb-lit{position:absolute;right:6%;top:6%;width:26%;height:26%;background:#1F4FD1;box-shadow:0 20px 40px rgba(31,79,209,.45)}
.hb-copy{display:flex;flex-direction:column;gap:22px}
.hb-k{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.mode-day .hb-k{color:#5B6070}.mode-night .hb-k{color:#A9AFBA}
.hb h2{margin:0;font-weight:600;font-size:46px;line-height:1.06;letter-spacing:-.02em;text-wrap:balance}
.hb-rows{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
.hb-row{display:grid;grid-template-columns:52px minmax(0,1fr);gap:14px;padding:20px 8px;border-top:1px solid;transition:opacity .45s ease,background-color .45s ease}
.mode-day .hb-row{border-color:#D3D8E4}.mode-night .hb-row{border-color:#3A3F4A}
.hb-row b{display:block;font-weight:600;font-size:21px}
.hb-row div span{display:block;margin-top:4px;font-size:15px;line-height:1.5}
.mode-day .hb-row div span{color:#5B6070}.mode-night .hb-row div span{color:#A9AFBA}
.hb-n{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:13px;letter-spacing:.08em;padding-top:5px}
.js-hb .hb-row{opacity:.4}
.js-hb .hb-row.on{opacity:1}
.mode-day .js-hb .hb-row.on,.mode-day .hb-row.on{background:#F3F5FB}.mode-night .hb-row.on{background:#212530}
.hb-row.on .hb-n{color:#1F4FD1}.mode-night .hb-row.on .hb-n{color:#7E9CFF}
.hb-cube{position:absolute;z-index:2;pointer-events:none;filter:drop-shadow(0 16px 20px rgba(14,18,32,.3));will-change:transform}
@media (max-width:900px){
  .hb{min-height:0}
  .hb-in{grid-template-columns:1fr;padding:64px 20px 72px;gap:36px}
  .hb-frame{border-width:12px;max-width:340px}
  .hb h2{font-size:32px}
  .hb-cube{display:none}
}
@media (prefers-reduced-motion: reduce){.ha-card,.hb-win img,.hb-cube{transform:none !important}.js-hb .hb-row{opacity:1}}
</style>
'''

JS = '''<script src="/assets/vendor/gsap.min.js"></script>
<script src="/assets/vendor/ScrollTrigger.min.js"></script>
<script>
(function(){
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
  if(reduce||!window.gsap||!window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  var pass={start:'top bottom',end:'bottom top',scrub:0.5};
  ['day','night'].forEach(function(mode){
    var root=document.querySelector('.mode-'+mode); if(!root) return;
    var a=root.querySelector('.ha');
    if(a){
      // the photo drifts slowly; the copy a little faster
      gsap.fromTo(a.querySelector('.ha-bg'),{yPercent:-8},{yPercent:8,ease:'none',scrollTrigger:Object.assign({trigger:a},pass)});
      gsap.fromTo(a.querySelector('.ha-copy'),{y:60},{y:-60,ease:'none',scrollTrigger:Object.assign({trigger:a},pass)});
      // the cards start spread apart and settle into one stack, each at its own speed, cobalt last and fastest
      var cards=a.querySelectorAll('.ha-card');
      var small=matchMedia('(max-width: 900px)').matches;
      var spread=small?[0,70,140]:[0,140,280], settle=small?[0,-34,-68]:[0,-48,-96];
      cards.forEach(function(c,i){
        gsap.fromTo(c,{y:spread[i],rotation:i===2?-2:0},{y:settle[i],rotation:0,ease:'none',
          scrollTrigger:{trigger:a,start:'top 85%',end:'center 40%',scrub:0.6}});
      });
    }
    var b=root.querySelector('.hb');
    if(b){
      b.classList.add('js-hb');
      gsap.fromTo(b.querySelector('.hb-win img'),{yPercent:-12},{yPercent:12,ease:'none',scrollTrigger:Object.assign({trigger:b},pass)});
      gsap.fromTo(b.querySelector('.hb-lit'),{y:30},{y:-30,ease:'none',scrollTrigger:Object.assign({trigger:b},pass)});
      b.querySelectorAll('.hb-cube').forEach(function(c){
        var k=parseFloat(c.getAttribute('data-speed'));
        gsap.fromTo(c,{y:120*k},{y:-120*k,rotation:k*30,ease:'none',scrollTrigger:Object.assign({trigger:b},pass)});
      });
      var rows=b.querySelectorAll('.hb-row');
      rows.forEach(function(r,i){
        ScrollTrigger.create({trigger:b,start:'top '+(70-i*14)+'%',onEnter:function(){r.classList.add('on')},onLeaveBack:function(){r.classList.remove('on')}});
      });
    }
  });
  new MutationObserver(function(){ScrollTrigger.refresh()}).observe(document.documentElement,{attributes:true,attributeFilter:['data-mode']});
})();
</script>
'''


def build(fn, out):
    s = SRC
    parts, pos = [], 0
    for mode in ('day', 'night'):
        st = s.find('<div class="mode-%s"' % mode, pos)
        a = s.find('<section class="sec" aria-label="How it works"', st)
        b = s.find('</section>', a) + len('</section>')
        parts.append(s[pos:a]); parts.append(fn(mode)); pos = b
    parts.append(s[pos:])
    s = ''.join(parts).replace('</head>', CSS + '</head>', 1).replace('</body>', JS + '</body>', 1)
    os.makedirs('_build/proto', exist_ok=True)
    open(out, 'w', encoding='utf-8').write(s)


build(section_a, '_build/proto/how-a.html')
build(section_b, '_build/proto/how-b.html')
print('ok')
