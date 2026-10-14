"""How it works, option C: B's frame and floating cubes, with the stack visual inside instead of the port.
The stack builds as you scroll (base slides in, review slab drops, lights come on, cobalt cap lands, buyer callout),
the stack drifts inside the frame, the grid behind it drifts slower, and the cubes float past at their own speeds.
  _build/proto/how-c.html   C  framed (white outline at night, ink by day)
  _build/proto/how-c2.html  C2 same, no frame
Run from the repo root: python3 _build/proto_how_c.py
"""
import os, re

import subprocess
subprocess.run(['python3', '_build/proto_scroll.py'], check=True)
SRC = open('_build/proto/scroll.html', encoding='utf-8').read()
_a = SRC.find('<script src="/assets/vendor/gsap.min.js"></script>')
_b = SRC.find('</script>', SRC.find('<script>', _a)) + len('</script>')
SRC = SRC[:_a] + SRC[_b:]
STEPS = [('Apply and upload', 'One checklist, finished over several sittings.', 'You'),
         ('Two officers review', 'Each one separately. Pass, and you are SBC-Qualified for a year.', 'SBC · two officers'),
         ('SBC approves the introduction', 'Only then does the buyer see you.', 'SBC')]
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
    rows = ''.join('<li class="hc-row"><span class="hc-node" aria-hidden="true"></span><div><span class="hc-meta"><span class="hc-n">%02d</span> · %s</span><b>%s</b><span class="hc-d">%s</span></div></li>' % (i + 1, who, t, d)
                   for i, (t, d, who) in enumerate(STEPS))
    rows = '<span class="hc-rail" aria-hidden="true"><span class="hc-fill"></span></span>' + rows
    nd = '' if mode == 'day' else '-n'
    cubes = ('<img class="hc-cube hc-q1" data-speed="1.6" src="/assets/img/sbc/cube-frost%s.svg" alt="">' % nd +
             '<img class="hc-cube hc-q2" data-speed="2.4" src="/assets/img/sbc/cube-lit.svg" alt="">' +
             '<img class="hc-cube hc-q3" data-speed="3.2" src="/assets/img/sbc/cube-ghost%s.svg" alt="">' % nd)
    return ('<section class="sec hc%s" aria-label="How it works">' % ('' if framed else ' hc-free') +
            '<div class="hc-in"><div class="hc-art">' + cubes +
            '<div class="hc-frame"><div class="hc-grid" aria-hidden="true"></div><div class="hc-svg">%s</div></div></div>' % stack_svg(mode) +
            '<div class="hc-copy"><span class="hc-k">How it works</span><h2>%s</h2><ol class="hc-rows">%s</ol><div class="hc-bar" aria-hidden="true"><i></i><i></i><i></i></div></div></div></section>' % (H2, rows))


CSS = '''<style id="how-proto-c">
.hc{position:relative;isolation:isolate;overflow:hidden;height:100vh;height:100svh;min-height:640px;display:flex;align-items:center}
.mode-day .hc{background:#FFFFFF;color:#1A1D24}.mode-night .hc{background:#1A1D24;color:#FFFFFF}
.hc-in{width:100%;max-width:1296px;margin:0 auto;padding:48px 72px;box-sizing:border-box;display:grid;grid-template-columns:auto minmax(0,1fr);gap:88px;align-items:center}
.hc-art{position:relative;width:min(560px,calc(100vh - 150px));width:min(560px,calc(100svh - 150px))}
.hc-frame{position:relative;aspect-ratio:1/1;width:100%;box-sizing:border-box;border:18px solid currentColor;overflow:hidden}
.mode-day .hc-frame{background:radial-gradient(circle at 45% 50%,#E4EAFA 0%,#F5F7FC 60%)}
.mode-night .hc-frame{background:radial-gradient(circle at 45% 50%,#25305A 0%,#171B26 65%)}
.hc-free .hc-frame{border-color:transparent;background:none}
.hc-grid{position:absolute;inset:-20%;opacity:.55;will-change:transform}
.mode-day .hc-grid{background:repeating-linear-gradient(30deg,transparent 0 79px,rgba(31,79,209,.12) 79px 80px),repeating-linear-gradient(-30deg,transparent 0 79px,rgba(31,79,209,.12) 79px 80px)}
.mode-night .hc-grid{background:repeating-linear-gradient(30deg,transparent 0 79px,rgba(255,255,255,.08) 79px 80px),repeating-linear-gradient(-30deg,transparent 0 79px,rgba(255,255,255,.08) 79px 80px)}
.hc-free .hc-grid{inset:-10%;-webkit-mask:radial-gradient(circle,#000 30%,transparent 70%);mask:radial-gradient(circle,#000 30%,transparent 70%)}
.hc-svg{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:14% 6% 6% 6%;will-change:transform}
.hc-stack{display:block;width:100%;height:auto;overflow:visible}
.hc-stack text{font-family:'Readex Pro',system-ui,sans-serif}
.hc-stack .st-n{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.08em}
.hc-stack .st-b{font-weight:600;font-size:13px}.hc-stack .st-s{font-weight:300;font-size:12px}
.hc-cube{position:absolute;z-index:2;pointer-events:none;filter:drop-shadow(0 16px 20px rgba(14,18,32,.35));will-change:transform}
.hc-q1{left:-44px;top:4%;width:84px}
.hc-q2{right:-40px;bottom:-30px;width:110px}
.hc-q3{left:-84px;bottom:14%;width:50px}
.hc-copy{display:flex;flex-direction:column;gap:22px;max-width:520px}
.hc-k{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.mode-day .hc-k{color:#5B6070}.mode-night .hc-k{color:#A9AFBA}
.hc h2{margin:0 0 14px;font-weight:600;font-size:46px;line-height:1.06;letter-spacing:-.02em;text-wrap:balance}
/* the steps: a rail on the left that fills as the slabs land; one square node per step, like a slab seen from above */
.hc-rows{position:relative;list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:30px}
.hc-rail{position:absolute;left:7px;top:8px;bottom:8px;width:2px}
.mode-day .hc-rail{background:#E1E5EE}.mode-night .hc-rail{background:#2E3340}
.hc-fill{position:absolute;inset:0;transform-origin:top;transform:scaleY(0)}
.mode-day .hc-fill{background:#1F4FD1}.mode-night .hc-fill{background:#7E9CFF}
.hc-row{position:relative;display:grid;grid-template-columns:16px minmax(0,1fr);gap:24px;align-items:start;transition:opacity .4s ease}
.hc-node{position:relative;z-index:1;width:16px;height:16px;margin-top:3px;box-sizing:border-box;border:2px solid;transition:background-color .3s ease,border-color .3s ease,box-shadow .3s ease}
.mode-day .hc-node{border-color:#C3C9D6;background:#FFFFFF}.mode-night .hc-node{border-color:#4A5060;background:#1A1D24}
.hc-meta{display:block;font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px}
.mode-day .hc-meta{color:#666C7D}.mode-night .hc-meta{color:#A9AFBA}
.hc-row b{display:block;font-weight:600;font-size:22px;line-height:1.25}
.hc-d{display:block;margin-top:6px;font-size:16px;line-height:1.55;max-width:42ch}
.mode-day .hc-d{color:#5B6070}.mode-night .hc-d{color:#A9AFBA}
.hc-bar{display:none}
/* states, set by the scroll: upcoming steps wait faintly, finished ones stay readable, the current one is lit */
.js-hc .hc-row{opacity:.35}
.js-hc .hc-row.done{opacity:.7}
.js-hc .hc-row.now{opacity:1}
.mode-day .hc-row.done .hc-node,.mode-day .hc-row.now .hc-node{background:#1F4FD1;border-color:#1F4FD1}
.mode-night .hc-row.done .hc-node,.mode-night .hc-row.now .hc-node{background:#7E9CFF;border-color:#7E9CFF}
.mode-day .hc-row.now .hc-node{box-shadow:0 0 0 6px rgba(31,79,209,.16)}
.mode-night .hc-row.now .hc-node{box-shadow:0 0 0 6px rgba(126,156,255,.2)}
.mode-day .hc-row.now .hc-n{color:#1F4FD1}.mode-night .hc-row.now .hc-n{color:#7E9CFF}
@media (max-width:900px){
  /* phones: heading, the frame, then one step at a time with a three-part bar */
  .hc{min-height:560px}
  .hc-in{display:flex;flex-direction:column;align-items:stretch;padding:24px 20px;gap:22px}
  .hc-copy{display:contents}
  .hc-k{display:none}
  .hc h2{order:1;font-size:28px;margin:0}
  .hc-art{order:2;width:min(300px,calc(100svh - 400px),calc(100% - 52px));margin:0 auto}
  .hc-rows{order:3;display:grid;gap:0;min-height:118px}
  .hc-rail,.hc-node{display:none}
  .hc-row{grid-area:1/1;grid-template-columns:1fr;gap:0}
  .js-hc .hc-row,.js-hc .hc-row.done{opacity:0}
  .js-hc .hc-row.now{opacity:1}
  .hc-row b{font-size:20px}.hc-d{font-size:15px}
  .hc-bar{order:4;display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
  .hc-bar i{height:3px}
  .mode-day .hc-bar i{background:#E1E5EE}.mode-night .hc-bar i{background:#2E3340}
  .mode-day .hc-bar i.on{background:#1F4FD1}.mode-night .hc-bar i.on{background:#7E9CFF}
  .hc-frame{border-width:12px}
  .hc-svg{padding:12% 1% 1% 1%}
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
  document.documentElement.classList.add('gs');
  // the lock: the section holds still (pinned) for this much extra scrolling while its animation plays out
  function lock(el,len){return {trigger:el,start:'center center',end:'+='+len,pin:true,pinSpacing:true,scrub:0.6,anticipatePin:1}}

  function build(mode){
    var root=document.querySelector('.mode-'+mode);
    return gsap.context(function(){
      // ===== How it works: the stack builds while the section is locked =====
      var c=root.querySelector('.hc');
      if(c){
        c.classList.add('js-hc');
        var q=function(s){return c.querySelector(s)};
        var off=mode==='day'?'#DCE4F8':'#3A3F4A', on=mode==='day'?'#1F4FD1':'#7E9CFF';
        var rows=c.querySelectorAll('.hc-row'), bars=c.querySelectorAll('.hc-bar i'), fill=q('.hc-fill');
        function state(p){
          var cur=p<0.36?0:(p<0.66?1:2);
          rows.forEach(function(r,i){r.classList.toggle('now',i===cur);r.classList.toggle('done',i<cur)});
          bars.forEach(function(b,i){b.classList.toggle('on',i<=cur)});
          if(fill) fill.style.transform='scaleY('+Math.max(0,Math.min(1,(p-0.08)/0.62))+')';
        }
        state(0);
        var tl=gsap.timeline({scrollTrigger:Object.assign(lock(c,'160%'),{onUpdate:function(st){state(st.progress)}})});
        // parallax while locked: grid slowest, stack faster, cubes fastest
        tl.fromTo(q('.hc-grid'),{y:-30},{y:30,ease:'none',duration:1},0)
          .fromTo(q('.hc-svg'),{y:40},{y:-40,ease:'none',duration:1},0);
        c.querySelectorAll('.hc-cube').forEach(function(el){
          // phones: shorter travel so the cubes stay on the frame's corners, clear of the text
          var k=parseFloat(el.getAttribute('data-speed')), amp=matchMedia('(max-width: 900px)').matches?14:70;
          tl.fromTo(el,{y:amp*k},{y:-amp*k,rotation:k*25,ease:'none',duration:1},0);
        });
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
          .fromTo(q('.sc-stbuy'),{y:10,opacity:0},{y:0,opacity:1,duration:.1},.82);
      }
      // ===== The mark: the card turns over while locked =====
      var mark=root.querySelector('section[aria-label="The mark"]'), card=mark&&mark.querySelector('.card3d');
      if(card){
        gsap.timeline({scrollTrigger:lock(mark,'120%')})
          .fromTo(card,{'--ry':'-34deg','--rx':'14deg'},{'--ry':'-14deg','--rx':'10deg',ease:'none',duration:.3})
          .to(card,{'--ry':'196deg','--rx':'6deg',ease:'power1.inOut',duration:.45})
          .to(card,{'--ry':'200deg',ease:'none',duration:.25});
      }
      // ===== Closing band: the groundwork becomes the skyline while locked =====
      var end=root.querySelector('.home-end');
      if(end&&end.querySelector('.i2i-b')){
        gsap.timeline({scrollTrigger:lock(end,'100%')})
          .fromTo(end.querySelector('.i2i-b'),{clipPath:'inset(0 0 0 100%)'},{clipPath:'inset(0 0 0 0%)',ease:'none',duration:1},0)
          .fromTo(end.querySelector('.i2i-seam'),{left:'100%'},{left:'0%',ease:'none',duration:1},0)
          .fromTo(end.querySelector('.i2i-a'),{scale:1.08},{scale:1,ease:'none',duration:1},0);
      }
    }, root);
  }
  // only the copy on screen (day or night) gets triggers; switching modes rebuilds them for the other copy
  var mode=function(){return document.documentElement.getAttribute('data-mode')==='night'?'night':'day'};
  var cur=mode(), ctx=build(cur);
  new MutationObserver(function(){
    var m=mode(); if(m===cur) return;
    ctx.revert(); cur=m; ctx=build(m); ScrollTrigger.refresh();
  }).observe(document.documentElement,{attributes:true,attributeFilter:['data-mode']});
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
