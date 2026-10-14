"""Home polish, after home_scroll.py:
  1. Smooth scrolling (Lenis, self-hosted in assets/vendor/) driven by GSAP's ticker so the locked sections stay in step.
     Off for reduced motion; touch keeps native scrolling.
  2. The two audience buttons (hero, closing band) get equal weight: same outline style with an arrow,
     so neither reads as a selected toggle. Hover fills.
Re-run safe. Run from the repo root: python3 _build/home_polish.py
"""
import re
s = open('index.html', encoding='utf-8').read()

ARROW = '<span class="pa" aria-hidden="true">&rarr;</span>'
# hero, day and night copies
pairs = [
    ('<a class="btn" href="/companies/" style="background-color: #1A1D24; color: #FFFFFF; font-size: 16px; font-weight: 600; padding: 15px 22px; text-decoration: none; display: inline-block">I represent a company</a>',
     '<a class="path" href="/companies/">I represent a company' + ARROW + '</a>'),
    ('<a class="btn" href="/companies/" style="background-color: #FFFFFF; color: #1A1D24; font-size: 16px; font-weight: 600; padding: 15px 22px; text-decoration: none; display: inline-block">I represent a company</a>',
     '<a class="path" href="/companies/">I represent a company' + ARROW + '</a>'),
    ('<a class="ghost" href="/buyers/" style="background-color: transparent; color: #1A1D24; border: 1px solid #1A1D24; font-size: 16px; font-weight: 600; padding: 14px 22px; text-decoration: none; display: inline-block">I buy for a Gulf entity</a>',
     '<a class="path" href="/buyers/">I buy for a Gulf entity' + ARROW + '</a>'),
    ('<a class="ghostd" href="/buyers/" style="background-color: transparent; color: #FFFFFF; border: 1px solid #8A90A0; font-size: 16px; font-weight: 600; padding: 14px 22px; text-decoration: none; display: inline-block">I buy for a Gulf entity</a>',
     '<a class="path" href="/buyers/">I buy for a Gulf entity' + ARROW + '</a>'),
    # closing band (on the photo, both copies identical)
    ('<a class="btn" href="/companies/apply/" style="background:#1F4FD1;color:#FFFFFF;font-size:16px;font-weight:600;padding:15px 22px;text-decoration:none">Start your application</a>',
     '<a class="path path-on" href="/companies/apply/">Start your application' + ARROW + '</a>'),
    ('<a href="/buyers/#talk" style="border:1px solid #FFFFFF;color:#FFFFFF;font-size:16px;font-weight:600;padding:14px 22px;text-decoration:none">Post a need</a>',
     '<a class="path path-on" href="/buyers/#talk">Post a need' + ARROW + '</a>'),
]
for old, new in pairs:
    s = s.replace(old, new)
for _, new in pairs:
    assert new in s, new

CSS = '''<style id="home-polish">
/* audience buttons: two equal paths, neither looks switched on */
.path{display:inline-flex;align-items:center;gap:12px;min-height:52px;padding:0 22px;box-sizing:border-box;font-size:16px;font-weight:600;text-decoration:none;border:1.5px solid;background:transparent;transition:background-color .25s ease,color .25s ease,border-color .25s ease}
.path .pa{display:inline-block;transition:transform .25s cubic-bezier(.2,.7,.2,1)}
.path:hover .pa,.path:focus-visible .pa{transform:translateX(4px)}
.mode-day .path{color:#1A1D24;border-color:#1A1D24}
.mode-day .path:hover{background:#1A1D24;color:#FFFFFF}
.mode-night .path{color:#FFFFFF;border-color:rgba(255,255,255,.7)}
.mode-night .path:hover{background:#FFFFFF;color:#1A1D24;border-color:#FFFFFF}
/* on the closing photo, both modes */
.mode-day .path-on,.mode-night .path-on{color:#FFFFFF;border-color:rgba(255,255,255,.8)}
.mode-day .path-on:hover,.mode-night .path-on:hover{background:#FFFFFF;color:#1A1D24;border-color:#FFFFFF}
.path:focus-visible{outline:2px solid #7E9CFF;outline-offset:3px}
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
