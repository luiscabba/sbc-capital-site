"""Home polish, after home_scroll.py:
  1. Smooth scrolling (Lenis, self-hosted in assets/vendor/) driven by GSAP's ticker so the locked sections stay in step.
     Off for reduced motion; touch keeps native scrolling.
  2. The night hero's solid button is cobalt, not white, so it no longer reads as a selected toggle.
  3. Hero wall: the cubes fly in and lock together when the page opens (after the loader), and burst apart as you
     scroll down while the cobalt block rises out of the crowd. Replaces motion.js's simple scroll lift.
Re-run safe. Run from the repo root: python3 _build/home_polish.py
"""
import re
s = open('index.html', encoding='utf-8').read()

# hero, night copy: the solid button was white, which read as a selected toggle; it is cobalt instead (day keeps ink)
OLD = '<a class="btn" href="/companies/" style="background-color: #FFFFFF; color: #1A1D24; font-size: 16px; font-weight: 600; padding: 15px 22px; text-decoration: none; display: inline-block">I represent a company</a>'
NEW = '<a class="btn btn-c" href="/companies/" style="background-color: #1F4FD1; color: #FFFFFF; font-size: 16px; font-weight: 600; padding: 15px 22px; text-decoration: none; display: inline-block">I represent a company</a>'
s = s.replace(OLD, NEW)
assert NEW in s

CSS = '''<style id="home-polish">
.btn-c:hover{background-color:#1A43B5 !important}
/* hero wall: GSAP drives two sets of vars per cube: --a* (forming) and --s* (splitting) */
@property --hy{syntax:'<length>';inherits:false;initial-value:0px}
html.gs .hero-wall .rise-cube,html.gs .hero-wall .halo{transform-box:fill-box;transform-origin:center;
  transform:translate(calc(var(--ax,0px) + var(--sx,0px)),calc(var(--ay,0px) + var(--sy,0px) + var(--hy))) rotate(calc(var(--ar,0deg) + var(--sr,0deg))) scale(calc(var(--as,1) * var(--ss,1)));
  opacity:calc(var(--ao,1) * var(--so,1));transition:--hy .35s cubic-bezier(.2,.7,.2,1)}
html.gs .hero-wall .rise-cube:hover{--hy:-12px}
html.gs .hero-wall .levsh{transform-box:fill-box}
/* smooth scrolling */
html.lenis,html.lenis body{height:auto}
.lenis.lenis-smooth{scroll-behavior:auto !important}
.lenis.lenis-stopped{overflow:hidden}
</style>
'''
s = re.sub(r'<style id="home-polish">.*?</style>\n', '', s, flags=re.S)
s = s.replace('</head>', CSS + '</head>', 1)

JS = '''<script src="/assets/vendor/lenis.min.js"></script>
<script id="home-smooth">
(function(){
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
  if(reduce||!window.Lenis||!window.gsap||!window.ScrollTrigger) return;
  // the wheel glides; touch keeps the phone's own scrolling
  var lenis=new Lenis({lerp:0.09,wheelMultiplier:1,smoothWheel:true,anchors:true});
  lenis.on('scroll',ScrollTrigger.update);
  gsap.ticker.add(function(t){lenis.raf(t*1000)});
  gsap.ticker.lagSmoothing(0);
  window.sbcLenis=lenis;
})();
</script>
<script id="hero-wall">
(function(){
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
  if(reduce||!window.gsap||!window.ScrollTrigger) return;
  document.documentElement.classList.add('gs');
  function rnd(i,k){var x=Math.sin(i*12.9898+k*78.233)*43758.5453;return x-Math.floor(x)}   // steady per cube, same every visit
  var built=[];
  function build(mode){
    var hero=document.querySelector('.mode-'+mode+' section[aria-label="Hero"]'); if(!hero) return null;
    var wall=hero.querySelector('.hero-wall'), cubes=[].slice.call(wall.querySelectorAll('.rise-cube'));
    var halo=wall.querySelector('.halo'), haloG=halo&&halo.parentNode, shadow=wall.querySelector('.levsh');
    var small=matchMedia('(max-width: 900px)').matches, k=small?.55:1;
    // centre of the wall, and each cube's way out from it
    var box=cubes.map(function(c){var b=c.getBBox();return {x:b.x+b.width/2,y:b.y+b.height/2}});
    var cx=box.reduce(function(a,b){return a+b.x},0)/box.length, cy=box.reduce(function(a,b){return a+b.y},0)/box.length;
    var far=0; box.forEach(function(b){far=Math.max(far,Math.hypot(b.x-cx,b.y-cy))});
    var lit=cubes.filter(function(c){return c.parentNode.classList.contains('litcell')})[0];
    return gsap.context(function(){
      // forming: from outside, turned and small, inner cubes first; the cobalt one drops in last
      var form=gsap.timeline({paused:true});
      cubes.forEach(function(c,i){
        var b=box[i], dx=b.x-cx, dy=b.y-cy, d=Math.hypot(dx,dy)||1, ux=dx/d, uy=dy/d, r=rnd(i,1);
        if(c===lit){
          form.fromTo(c,{'--ay':'-320px','--ao':0,'--as':1.25},{'--ay':'0px','--ao':1,'--as':1,duration:1.1,ease:'power4.out'},1.05);
          return;
        }
        var out=(260+r*260)*k;
        form.fromTo(c,{'--ax':ux*out+'px','--ay':(uy*out-60*rnd(i,2))+'px','--ar':((rnd(i,3)-.5)*80)+'deg','--as':.55,'--ao':0},
          {'--ax':'0px','--ay':'0px','--ar':'0deg','--as':1,'--ao':1,duration:1.25,ease:'expo.out'},(d/far)*.6+rnd(i,4)*.18);
      });
      if(haloG) form.fromTo(haloG,{opacity:0},{opacity:1,duration:.8,ease:'power1.out'},1.45);
      if(shadow) form.fromTo(shadow,{opacity:0},{opacity:.45,duration:1.2,ease:'power1.out'},.2);
      // splitting: the wall bursts outward as the hero scrolls away; the cobalt block rises and grows
      // desktop: the hero holds while it bursts; phones (hero taller than the screen): it bursts as it scrolls past
      var split=gsap.timeline({scrollTrigger:small?{trigger:hero,start:'top top',end:'bottom 20%',scrub:1}
        :{trigger:hero,start:'top top',end:'+=85%',pin:true,pinSpacing:true,scrub:1,anticipatePin:1,refreshPriority:1}});
      cubes.forEach(function(c,i){
        var b=box[i], dx=b.x-cx, dy=b.y-cy, d=Math.hypot(dx,dy)||1, ux=dx/d, uy=dy/d;
        if(c===lit){
          split.fromTo(c,{'--sy':'0px','--ss':1},{'--sy':(-200*k)+'px','--ss':1.5,ease:'power2.inOut',duration:1},0);
          if(halo) split.fromTo(halo,{'--sy':'0px','--ss':1},{'--sy':(-200*k)+'px','--ss':1.5,ease:'power2.inOut',duration:1},0);
          return;
        }
        var go=(180+(d/far)*520)*k*(.8+rnd(i,5)*.5);
        split.fromTo(c,{'--sx':'0px','--sy':'0px','--sr':'0deg','--ss':1,'--so':1},
          {'--sx':ux*go+'px','--sy':(uy*go-120*k*rnd(i,6))+'px','--sr':((rnd(i,7)-.5)*70)+'deg','--ss':.75+rnd(i,8)*.5,'--so':.1,ease:'power2.out',duration:1},rnd(i,9)*.12);
      });
      if(shadow) split.fromTo(shadow,{scale:1},{scale:.5,ease:'power2.in',duration:1},0);
      wall._form=form;
      ScrollTrigger.sort(); ScrollTrigger.refresh();
    }, wall);
  }
  function start(){
    // play the forming once the loader has lifted
    var go=function(){built.forEach(function(w){w&&w._form&&w._form.play()})};
    if(document.documentElement.classList.contains('sbc-ready')) return go();
    var mo=new MutationObserver(function(){if(document.documentElement.classList.contains('sbc-ready')){mo.disconnect();go()}});
    mo.observe(document.documentElement,{attributes:true,attributeFilter:['class']});
  }
  // only the copy on screen is measured (the hidden one has no size); a mode switch builds the other, already formed
  var mode=function(){return document.documentElement.getAttribute('data-mode')==='night'?'night':'day'};
  var cur=mode(), ctx=build(cur);
  built=[document.querySelector('.mode-'+cur+' .hero-wall')];
  start();
  new MutationObserver(function(){
    var m=mode(); if(m===cur) return;
    if(ctx) ctx.revert(); cur=m; ctx=build(m);
    var w=document.querySelector('.mode-'+m+' .hero-wall'); if(w&&w._form) w._form.progress(1);
    ScrollTrigger.refresh();
  }).observe(document.documentElement,{attributes:true,attributeFilter:['data-mode']});
})();
</script>
'''
s = re.sub(r'<script src="/assets/vendor/lenis.min.js"></script>\n<script id="home-smooth">.*?</script>\n(<script id="hero-wall">.*?</script>\n)?', '', s, flags=re.S)
s = s.replace('</body>', JS + '</body>', 1)
open('index.html', 'w', encoding='utf-8').write(s)
print('ok')
