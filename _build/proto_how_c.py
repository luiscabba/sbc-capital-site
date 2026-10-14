"""How it works, option C: B's frame and floating cubes, with the stack visual inside instead of the port.
The stack builds as you scroll (base slides in, review slab drops, lights come on, cobalt cap lands, buyer callout),
the stack drifts inside the frame, the grid behind it drifts slower, and the cubes float past at their own speeds.
  _build/proto/how-c.html   C  framed (white outline at night, ink by day)
  _build/proto/how-c2.html  C2 same, no frame
Run from the repo root: python3 _build/proto_how_c.py
"""
import os, re

SRC = open('index.html', encoding='utf-8').read()
STEPS = [('Apply and upload', 'One checklist, finished over several sittings.'),
         ('Two officers review', 'Each one separately. Pass, and you are SBC-Qualified for a year.'),
         ('SBC approves the introduction', 'Only then does the buyer see you.')]
H2 = 'Nothing reaches a buyer until SBC approves it.'


def stack_svg(mode):
    st = SRC.find('<div class="mode-%s"' % mode)
    a = SRC.find('<svg class="stack"', st)
    svg = SRC[a:SRC.find('</svg>', a) + 6]
    # drop the looping classes; the scroll drives it now
    svg = svg.replace('class="stack"', 'class="hc-stack"')
    svg = re.sub(r'class="st-an (\w+)"', r'class="sc-\1"', svg)
    return svg


def section(mode, framed):
    rows = ''.join('<li class="hc-row"><span class="hc-n">%02d</span><div><b>%s</b><span>%s</span></div></li>' % (i + 1, t, d)
                   for i, (t, d) in enumerate(STEPS))
    nd = '' if mode == 'day' else '-n'
    cubes = ('<img class="hc-cube hc-q1" data-speed="1.6" src="/assets/img/sbc/cube-frost%s.svg" alt="">' % nd +
             '<img class="hc-cube hc-q2" data-speed="2.4" src="/assets/img/sbc/cube-lit.svg" alt="">' +
             '<img class="hc-cube hc-q3" data-speed="3.2" src="/assets/img/sbc/cube-ghost%s.svg" alt="">' % nd)
    return ('<section class="sec hc%s" aria-label="How it works">' % ('' if framed else ' hc-free') +
            '<div class="hc-in"><div class="hc-art">' + cubes +
            '<div class="hc-frame"><div class="hc-grid" aria-hidden="true"></div><div class="hc-svg">%s</div></div></div>' % stack_svg(mode) +
            '<div class="hc-copy"><span class="hc-k">How it works</span><h2>%s</h2><ol class="hc-rows">%s</ol></div></div></section>' % (H2, rows))


CSS = '''<style id="how-proto-c">
.hc{position:relative;isolation:isolate;overflow:hidden;min-height:920px;display:flex;align-items:center}
.mode-day .hc{background:#FFFFFF;color:#1A1D24}.mode-night .hc{background:#1A1D24;color:#FFFFFF}
.hc-in{width:100%;max-width:1296px;margin:0 auto;padding:112px 72px;box-sizing:border-box;display:grid;grid-template-columns:minmax(0,580px) minmax(0,1fr);gap:80px;align-items:center}
.hc-art{position:relative}
.hc-frame{position:relative;aspect-ratio:1/1;width:100%;box-sizing:border-box;border:18px solid currentColor;overflow:hidden}
.mode-day .hc-frame{background:radial-gradient(circle at 45% 50%,#E4EAFA 0%,#F5F7FC 60%)}
.mode-night .hc-frame{background:radial-gradient(circle at 45% 50%,#25305A 0%,#171B26 65%)}
.hc-free .hc-frame{border-color:transparent;background:none}
/* faint isometric lines, drifting slower than the stack */
.hc-grid{position:absolute;inset:-20%;opacity:.55;will-change:transform}
.mode-day .hc-grid{background:repeating-linear-gradient(30deg,transparent 0 79px,rgba(31,79,209,.12) 79px 80px),repeating-linear-gradient(-30deg,transparent 0 79px,rgba(31,79,209,.12) 79px 80px)}
.mode-night .hc-grid{background:repeating-linear-gradient(30deg,transparent 0 79px,rgba(255,255,255,.08) 79px 80px),repeating-linear-gradient(-30deg,transparent 0 79px,rgba(255,255,255,.08) 79px 80px)}
.hc-free .hc-grid{inset:-10%;-webkit-mask:radial-gradient(circle,#000 30%,transparent 70%);mask:radial-gradient(circle,#000 30%,transparent 70%)}
.hc-svg{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:14% 6% 6% 6%;will-change:transform}
.hc-stack{display:block;width:100%;height:auto;overflow:visible}
.hc-stack text{font-family:'Readex Pro',system-ui,sans-serif}
.hc-stack .st-n{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.08em}
.hc-stack .st-b{font-weight:600;font-size:13px}.hc-stack .st-s{font-weight:300;font-size:12px}
/* cubes sit on the frame's corners and float past it */
.hc-cube{position:absolute;z-index:2;pointer-events:none;filter:drop-shadow(0 16px 20px rgba(14,18,32,.35));will-change:transform}
.hc-q1{left:-44px;top:4%;width:84px}
.hc-q2{right:-40px;bottom:-30px;width:110px}
.hc-q3{left:-84px;bottom:14%;width:50px}
.hc-copy{display:flex;flex-direction:column;gap:22px}
.hc-k{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.mode-day .hc-k{color:#5B6070}.mode-night .hc-k{color:#A9AFBA}
.hc h2{margin:0;font-weight:600;font-size:46px;line-height:1.06;letter-spacing:-.02em;text-wrap:balance}
.hc-rows{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
.hc-row{display:grid;grid-template-columns:52px minmax(0,1fr);gap:14px;padding:20px 8px;border-top:1px solid;transition:opacity .45s ease,background-color .45s ease}
.mode-day .hc-row{border-color:#D3D8E4}.mode-night .hc-row{border-color:#3A3F4A}
.hc-row b{display:block;font-weight:600;font-size:21px}
.hc-row div span{display:block;margin-top:4px;font-size:15px;line-height:1.5}
.mode-day .hc-row div span{color:#5B6070}.mode-night .hc-row div span{color:#A9AFBA}
.hc-n{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:13px;letter-spacing:.08em;padding-top:5px}
.js-hc .hc-row{opacity:.4}
.js-hc .hc-row.on{opacity:1}
.mode-day .hc-row.on{background:#F3F5FB}.mode-night .hc-row.on{background:#212530}
.mode-day .hc-row.on .hc-n{color:#1F4FD1}.mode-night .hc-row.on .hc-n{color:#7E9CFF}
@media (max-width:900px){
  .hc{min-height:0}
  .hc-in{grid-template-columns:1fr;padding:64px 20px 72px;gap:44px}
  .hc-art{width:calc(100% - 36px);max-width:360px;margin:0 auto}
  .hc-frame{border-width:12px}
  .hc-svg{padding:12% 1% 1% 1%}
  .hc h2{font-size:32px}
  .hc-q1{left:-26px;width:52px}.hc-q2{right:-24px;bottom:-22px;width:68px}.hc-q3{display:none}
}
@media (prefers-reduced-motion: reduce){.hc-svg,.hc-grid,.hc-cube{transform:none !important}.js-hc .hc-row{opacity:1}}
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
    var c=root.querySelector('.hc'); if(!c) return;
    c.classList.add('js-hc');
    var q=function(s){return c.querySelector(s)};
    var off=mode==='day'?'#DCE4F8':'#3A3F4A', on=mode==='day'?'#1F4FD1':'#7E9CFF';
    // parallax: the grid drifts slowest, the stack a little faster, the cubes fastest
    gsap.fromTo(q('.hc-grid'),{y:-40},{y:40,ease:'none',scrollTrigger:Object.assign({trigger:c},pass)});
    gsap.fromTo(q('.hc-svg'),{y:50},{y:-50,ease:'none',scrollTrigger:Object.assign({trigger:c},pass)});
    c.querySelectorAll('.hc-cube').forEach(function(el){
      var k=parseFloat(el.getAttribute('data-speed'));
      gsap.fromTo(el,{y:90*k},{y:-90*k,rotation:k*25,ease:'none',scrollTrigger:Object.assign({trigger:c},pass)});
    });
    // the stack builds as the section crosses the screen
    var rows=c.querySelectorAll('.hc-row');
    var tl=gsap.timeline({scrollTrigger:{trigger:c,start:'top 75%',end:'center 35%',scrub:0.6,
      onUpdate:function(st){var p=st.progress;rows.forEach(function(r,i){r.classList.toggle('on',p>=[0.08,0.4,0.7][i])})}}});
    tl.fromTo(q('.sc-st1'),{x:-140,opacity:0},{x:0,opacity:1,duration:.14,ease:'power2.out'},0)
      .fromTo(q('.sc-stl1'),{opacity:0},{opacity:1,duration:.05},.12)
      .fromTo(q('.sc-stbar'),{attr:{'stroke-dashoffset':120}},{attr:{'stroke-dashoffset':0},duration:.12,ease:'none'},.14)
      .fromTo(q('.sc-st2'),{y:-170,opacity:0},{y:0,opacity:1,duration:.16,ease:'bounce.out'},.24)
      .fromTo(q('.sc-stl2'),{opacity:0},{opacity:1,duration:.05},.38)
      .fromTo(q('.sc-sto1'),{attr:{fill:off}},{attr:{fill:on},duration:.03},.44)
      .fromTo(q('.sc-sto2'),{attr:{fill:off}},{attr:{fill:on},duration:.03},.5)
      .fromTo(q('.sc-st3'),{y:-170,opacity:0},{y:0,opacity:1,duration:.16,ease:'bounce.out'},.54)
      .fromTo(q('.sc-stl3'),{opacity:0},{opacity:1,duration:.05},.68)
      .fromTo(q('.sc-stlink'),{opacity:0},{opacity:1,duration:.06},.76)
      .fromTo(q('.sc-stbuy'),{y:10,opacity:0},{y:0,opacity:1,duration:.1},.82)
      .to({},{duration:.08});
  });
  new MutationObserver(function(){ScrollTrigger.refresh()}).observe(document.documentElement,{attributes:true,attributeFilter:['data-mode']});
})();
</script>
'''


def build(framed, out):
    s = SRC
    parts, pos = [], 0
    for mode in ('day', 'night'):
        st = s.find('<div class="mode-%s"' % mode, pos)
        a = s.find('<section class="sec" aria-label="How it works"', st)
        b = s.find('</section>', a) + len('</section>')
        parts.append(s[pos:a]); parts.append(section(mode, framed)); pos = b
    parts.append(s[pos:])
    s = ''.join(parts).replace('</head>', CSS + '</head>', 1).replace('</body>', JS + '</body>', 1)
    os.makedirs('_build/proto', exist_ok=True)
    open(out, 'w', encoding='utf-8').write(s)


build(True, '_build/proto/how-c.html')
build(False, '_build/proto/how-c2.html')
print('ok')
