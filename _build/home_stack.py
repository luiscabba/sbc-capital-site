"""Home · How it works: replaces the three-platform visual with the stack (option G).
Run from the repo root: python3 _build/home_stack.py   (safe to re-run: it swaps whatever visual sits in .how-side)"""
import re

P = {'day':   dict(b=('#E7ECF9', '#D3DDF6', '#B8C7EE'), m=('#C9D4F3', '#B8C6EC', '#9EB2E6'), c=('#3D6BF0', '#1A43B5', '#173A9C'),
                   off='#DCE4F8', on='#1F4FD1', acc='#1F4FD1', sub='#5B6070', line='#A9B3C8', card='#1A1D24', cardfg='#FFFFFF', cardsub='#A9AFBA', bar='#1F4FD1', sh='rgba(26,29,36,.16)'),
     'night': dict(b=('#3A4258', '#232836', '#1C2130'), m=('#4A5675', '#262C3C', '#1E2434'), c=('#3D6BF0', '#1A43B5', '#173A9C'),
                   off='#3A3F4A', on='#7E9CFF', acc='#7E9CFF', sub='#A9AFBA', line='#5B6070', card='#FFFFFF', cardfg='#1A1D24', cardsub='#5B6070', bar='#7E9CFF', sh='rgba(0,0,0,.45)')}


def slab(cx, cy, cols):
    t, l, r = cols
    return ('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s"></polygon>' % (cx-120, cy, cx, cy+70, cx, cy+114, cx-120, cy+44, l) +
            '<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s"></polygon>' % (cx, cy+70, cx+120, cy, cx+120, cy+44, cx, cy+114, r) +
            '<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s"></polygon>' % (cx, cy-70, cx+120, cy, cx, cy+70, cx-120, cy, t))


def svg(mode):
    p = P[mode]; cx = 150
    return (
        '<div style="display: flex; justify-content: center"><svg class="stack" viewBox="0 0 500 310" width="460" role="img" '
        'aria-label="Three slabs stack into one block: your checklist is the base, the two officers&#39; review lands on it with two lights, and SBC&#39;s cobalt approval caps it. Only the finished stack reaches the buyer." '
        'style="display: block; max-width: 100%%; overflow: visible">'
        '<ellipse cx="%d" cy="296" rx="128" ry="16" fill="%s" style="filter: blur(8px)"></ellipse>' % (cx, p['sh']) +
        '<g class="st-an st1">' + slab(cx, 180, p['b']) +
        '<path class="st-an stbar" d="M%d 180 L%d 180" stroke="%s" stroke-width="3" stroke-dasharray="120" fill="none" transform="rotate(30 %d 180)"></path></g>' % (cx-60, cx+60, p['bar'], cx) +
        '<g class="st-an st2">' + slab(cx, 136, p['m']) +
        '<circle class="st-an sto1" cx="%d" cy="205" r="6" fill="%s"></circle><circle class="st-an sto2" cx="%d" cy="181" r="6" fill="%s"></circle></g>' % (cx+40, p['on'], cx+80, p['on']) +
        '<g class="st-an st3">' + slab(cx, 92, p['c']) + '</g>'
        # step numbers beside each slab
        '<g class="st-an stl1"><path d="M%d 210 L%d 210" stroke="%s"></path><text x="%d" y="214" class="st-n" fill="%s">01</text></g>' % (cx+124, cx+156, p['line'], cx+164, p['sub']) +
        '<g class="st-an stl2"><path d="M%d 166 L%d 166" stroke="%s"></path><text x="%d" y="170" class="st-n" fill="%s">02</text></g>' % (cx+124, cx+156, p['line'], cx+164, p['sub']) +
        '<g class="st-an stl3"><path d="M%d 116 L%d 116" stroke="%s"></path><text x="%d" y="120" class="st-n" fill="%s">03</text></g>' % (cx+124, cx+156, p['acc'], cx+164, p['acc']) +
        # only the whole stack reaches the buyer
        '<path class="st-an stlink" d="M%d 34 C %d 10, %d 4, 300 6" stroke="%s" stroke-width="2" stroke-dasharray="6 8" fill="none"></path>' % (cx+26, cx+80, cx+120, p['acc']) +
        '<g class="st-an stbuy"><rect x="300" y="-14" width="196" height="54" fill="%s"></rect>' % p['card'] +
        '<text x="314" y="8" class="st-b" fill="%s">The buyer sees you</text><text x="314" y="27" class="st-s" fill="%s">Only once the stack is whole</text></g>' % (p['cardfg'], p['cardsub']) +
        '</svg></div>')


CSS = '''<style id="stack-css">
/* Home · How it works: the stack. One 9s loop; on desktop motion.js scrubs it with scroll (--hp). */
.stack text{font-family:'Readex Pro',system-ui,sans-serif}
.stack .st-n{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.08em}
.stack .st-b{font-weight:600;font-size:13px}.stack .st-s{font-weight:300;font-size:12px}
.st-an{animation-duration:9s;animation-iteration-count:infinite;animation-timing-function:linear}
.st1{animation-name:st1}@keyframes st1{0%,3%{transform:translateX(-140px);opacity:0}12%{transform:none;opacity:1}93%{opacity:1;transform:none}98%,100%{opacity:0;transform:none}}
.st2{animation-name:st2}@keyframes st2{0%,31%{transform:translateY(-160px);opacity:0}33%{opacity:1}38%{transform:none;animation-timing-function:ease-out}40%{transform:translateY(-8px);animation-timing-function:ease-in}42%,93%{transform:none;opacity:1}98%,100%{opacity:0;transform:none}}
.st3{animation-name:st3}@keyframes st3{0%,62%{transform:translateY(-160px);opacity:0}64%{opacity:1}69%{transform:none;animation-timing-function:ease-out}71%{transform:translateY(-10px);animation-timing-function:ease-in}73%,93%{transform:none;opacity:1}98%,100%{opacity:0;transform:none}}
.stbar{animation-name:stbar}@keyframes stbar{0%,10%{stroke-dashoffset:120}26%,93%{stroke-dashoffset:0}100%{stroke-dashoffset:120}}
.mode-day .sto1{animation-name:sto1d}@keyframes sto1d{0%,44%{fill:#DCE4F8}46%,93%{fill:#1F4FD1}100%{fill:#DCE4F8}}
.mode-day .sto2{animation-name:sto2d}@keyframes sto2d{0%,54%{fill:#DCE4F8}56%,93%{fill:#1F4FD1}100%{fill:#DCE4F8}}
.mode-night .sto1{animation-name:sto1n}@keyframes sto1n{0%,44%{fill:#3A3F4A}46%,93%{fill:#7E9CFF}100%{fill:#3A3F4A}}
.mode-night .sto2{animation-name:sto2n}@keyframes sto2n{0%,54%{fill:#3A3F4A}56%,93%{fill:#7E9CFF}100%{fill:#3A3F4A}}
.stl1{animation-name:stl1}@keyframes stl1{0%,10%{opacity:0}14%,93%{opacity:1}98%,100%{opacity:0}}
.stl2{animation-name:stl2}@keyframes stl2{0%,40%{opacity:0}44%,93%{opacity:1}98%,100%{opacity:0}}
.stl3{animation-name:stl3}@keyframes stl3{0%,71%{opacity:0}75%,93%{opacity:1}98%,100%{opacity:0}}
.stlink{animation-name:stlink}@keyframes stlink{0%,74%{opacity:0}78%,93%{opacity:1}98%,100%{opacity:0}}
.stbuy{animation-name:stbuy}@keyframes stbuy{0%,76%{opacity:0;transform:translateY(10px)}81%,93%{opacity:1;transform:none}98%,100%{opacity:0}}
/* desktop: scroll builds the stack in step with the rows (rows light at --hp 0, .36, .70); it holds once complete */
.js-scroll .sec .st-an{animation-play-state:paused !important;animation-delay:calc(var(--hp,0) * -8.3s) !important}
/* reduced motion: the finished stack, still */
@media (prefers-reduced-motion: reduce){.st-an{animation:none !important}}
</style>
'''

s = open('index.html', encoding='utf-8').read()
s = re.sub(r'<style id="stack-css">.*?</style>\n', '', s, flags=re.S)
s = s.replace('</head>', CSS + '</head>', 1)
out, pos, n = [], 0, 0
for mode in ('day', 'night'):
    start = s.find('<div class="mode-%s"' % mode, pos)
    i = s.find('class="how-side"', start)
    a = s.find('<div style="display: flex; justify-content: center"><svg', i)
    b = s.find('</svg></div>', a) + len('</svg></div>')
    assert a > 0 and b > a and 'row' in s[b:b+200]
    out.append(s[pos:a]); out.append(svg(mode)); pos = b; n += 1
out.append(s[pos:])
open('index.html', 'w', encoding='utf-8').write(''.join(out))
print('replaced', n)
