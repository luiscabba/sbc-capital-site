"""Home polish, after home_scroll.py:
  1. Smooth scrolling (Lenis, self-hosted in assets/vendor/) driven by GSAP's ticker so the locked sections stay in step.
     Off for reduced motion; touch keeps native scrolling.
  2. The night hero's solid button is cobalt, not white, so it no longer reads as a selected toggle.
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
'''
s = re.sub(r'<script src="/assets/vendor/lenis.min.js"></script>\n<script id="home-smooth">.*?</script>\n', '', s, flags=re.S)
s = s.replace('</body>', JS + '</body>', 1)
open('index.html', 'w', encoding='utf-8').write(s)
print('ok')
