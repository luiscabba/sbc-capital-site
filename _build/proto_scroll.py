"""Scroll-effects prototype of Home (not deployed): _build/proto/scroll.html
Three effects from the Scroll Lab, driven by GSAP ScrollTrigger:
  Parallax         How it works: the port drifts slower than the page; the heading card rises a little faster.
  3D on scroll     The mark: the SBC-Qualified card turns from 'It means' to 'It does not mean' as you scroll.
  Image to image   Closing band: a cobalt seam wipes the water plant being built into the finished skyline.
Phones: the photos stay hidden (option A), so parallax is desktop only; the card turn and the wipe run everywhere.
Run from the repo root: python3 _build/proto_scroll.py
"""
import os

s = open('index.html', encoding='utf-8').read()

# closing band: two stacked photos (groundwork below, skyline above it, revealed by the wipe) and a seam
old = '<img class="kb-ap" src="/assets/img/gulf/gulf-skyline-dawn.webp" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover;object-position:62% 60%;display:block"></div>'
new = ('<img class="i2i-a" src="/assets/img/gulf/gulf-water-plant.webp" alt="" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:60% 55%;display:block">'
       '<img class="i2i-b" src="/assets/img/gulf/gulf-skyline-dawn.webp" alt="" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 60%;display:block">'
       '<span class="i2i-seam"></span></div>')
assert s.count(old) == 2, s.count(old)
s = s.replace(old, new)

CSS = '''<style id="scroll-proto">
/* parallax: the photo is taller than its frame so it has room to drift */
.how-grid>div:first-child>img{height:124% !important;margin-top:-12%;will-change:transform}
/* 3D on scroll: GSAP writes --rx/--ry; this outranks the older scroll and flip rules */
html.gs body .c3wrap .card3d{transform:rotateX(var(--rx,9deg)) rotateY(var(--ry,-22deg)) !important;transition:none !important}
html.gs .turn{display:none}
html.gs .c3front>span:last-child{font-size:0 !important}
html.gs .c3front>span:last-child::after{content:"Keep scrolling to turn it over";font-size:13px}
/* image to image */
.home-end{min-height:560px;display:flex;align-items:center}
.i2i-b{clip-path:inset(0 0 0 100%)}
.i2i-seam{position:absolute;top:0;bottom:0;left:100%;width:2px;background:#7E9CFF;box-shadow:0 0 18px 2px rgba(126,156,255,.7)}
@media (max-width:900px){.home-end{min-height:480px}}
@media (prefers-reduced-motion: reduce){.i2i-b{clip-path:none}.i2i-seam{display:none}}
</style>
'''
s = s.replace('</head>', CSS + '</head>', 1)

JS = '''<script src="/assets/vendor/gsap.min.js"></script>
<script src="/assets/vendor/ScrollTrigger.min.js"></script>
<script>
(function(){
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
  if(reduce||!window.gsap||!window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  document.documentElement.classList.add('gs');
  var pass={start:'top bottom',end:'bottom top',scrub:0.5};   // the whole time the section is on screen

  function setup(mode){
    var root=document.querySelector('.mode-'+mode); if(!root) return;
    // parallax (desktop only: the photo is hidden on phones)
    ScrollTrigger.matchMedia({'(min-width: 901px)':function(){
      var sec=root.querySelector('section[aria-label="How it works"]');
      gsap.fromTo(sec.querySelector('.how-grid>div:first-child>img'),{yPercent:-6},{yPercent:6,ease:'none',scrollTrigger:Object.assign({trigger:sec},pass)});
      gsap.fromTo(sec.querySelector('.how-h2'),{y:40},{y:-40,ease:'none',scrollTrigger:Object.assign({trigger:sec},pass)});
    }});
    // 3D on scroll: front while the section rises, back by the time it leaves
    var mark=root.querySelector('section[aria-label="The mark"]'), card=mark.querySelector('.card3d');
    // hold the front long enough to read, turn, then hold the back
    gsap.timeline({scrollTrigger:{trigger:mark,start:'top 80%',end:'bottom 20%',scrub:0.6}})
      .fromTo(card,{'--ry':'-34deg','--rx':'14deg'},{'--ry':'-14deg','--rx':'10deg',ease:'none',duration:.35})
      .to(card,{'--ry':'196deg','--rx':'6deg',ease:'power1.inOut',duration:.45})
      .to(card,{'--ry':'200deg',ease:'none',duration:.2});
    // image to image: groundwork becomes the skyline as the band crosses the screen
    var end=root.querySelector('.home-end');
    var tl=gsap.timeline({scrollTrigger:{trigger:end,start:'top 85%',end:'bottom 35%',scrub:0.6}});
    tl.fromTo(end.querySelector('.i2i-b'),{clipPath:'inset(0 0 0 100%)'},{clipPath:'inset(0 0 0 0%)',ease:'none',duration:1},0)
      .fromTo(end.querySelector('.i2i-seam'),{left:'100%'},{left:'0%',ease:'none',duration:1},0)
      .fromTo(end.querySelector('.i2i-a'),{scale:1.08},{scale:1,ease:'none',duration:1},0);
  }
  setup('day'); setup('night');
  // the day and night copies swap when the mode changes; re-measure for the one now showing
  new MutationObserver(function(){ScrollTrigger.refresh()}).observe(document.documentElement,{attributes:true,attributeFilter:['data-mode']});
})();
</script>
'''
s = s.replace('</body>', JS + '</body>', 1)
os.makedirs('_build/proto', exist_ok=True)
open('_build/proto/scroll.html', 'w', encoding='utf-8').write(s)
print('ok')
