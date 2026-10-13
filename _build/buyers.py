"""Builds buyers/index.html (For buyers).

Picks from the For buyers canvas: Hero A (the shortlist), How A (the thread, reworked),
Pack B (the layers), Terms A (free, and yours to decide), Talk B (post a need).
The head, header and footer come from companies/index.html so the pages stay in step.
Run from the repo root:  python3 _build/buyers.py
"""
import re

SRC = open('companies/index.html', encoding='utf-8').read()

# ---------- shared chrome from For companies ----------
head = SRC[:SRC.find('</head>')]
head = head.replace('<title>SBC Capital · For companies</title>', '<title>SBC Capital · For buyers</title>')
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="SBC Capital checks international suppliers before Gulf buyers meet them. Posting a need is free.">', head)


def chrome(mode):
    start = SRC.find('<div class="mode-%s">' % mode)
    hs = SRC.find('<header', start); he = SRC.find('</header>', hs) + 9
    fs = SRC.find('<footer', he); fe = SRC.find('</footer>', fs) + 9
    hd, ft = SRC[hs:he], SRC[fs:fe]
    hd = hd.replace(' aria-current="page">For companies', '>For companies')
    hd = re.sub(r'(href="/companies/" style="[^"]*); font-weight: 600"', r'\1"', hd)
    hd = re.sub(r'(href="/buyers/" style="[^"]*)">For buyers', r'\1; font-weight: 600" aria-current="page">For buyers', hd)
    sfx = '' if mode == 'day' else '-n'
    hd = hd.replace('href="/companies/#apply"', 'href="#talk%s"' % sfx).replace('>Apply</a>', '>Talk to SBC</a>')
    open_div = SRC[start:hs]  # mode wrapper + modefade div
    return open_div, hd, ft


# ---------- page styles ----------
CSS = r'''<style>
/* ===== For buyers ===== */
.by-qm{display:block;flex:none;color:var(--cv-ink)}
.by-qm .lit{fill:#1F4FD1}
/* Hero A: the shortlist */
.bh-stage{position:relative;flex:1 1 0;min-width:0;container-type:inline-size;aspect-ratio:700/540}
.bh-c{position:absolute;width:62%}
.bh-c1{left:4%;top:56%;z-index:3;--ld:1.05s}.bh-c2{left:14%;top:31%;z-index:2;--ld:.7s}.bh-c3{left:24%;top:6%;z-index:1;--ld:.35s}
/* load: once the site loader lifts (html.sbc-ready), the shortlist arrives card by card, each check ticks, then the mark lights */
.sbc-ready .bh-card{animation:bhin 1.1s cubic-bezier(.2,.7,.2,1) var(--ld) backwards}
@keyframes bhin{from{opacity:0;transform:perspective(1400px) rotateY(-50deg) translate3d(110px,26px,0)}}
.sbc-ready .bh-chips span{animation:bhchip .4s ease calc(var(--ld) + .55s + var(--i) * .16s) backwards}
@keyframes bhchip{from{opacity:.35}}
.sbc-ready .bh-chips i{animation:bhtick .35s ease calc(var(--ld) + .55s + var(--i) * .16s) backwards}
@keyframes bhtick{from{background:transparent;box-shadow:inset 0 0 0 1.5px var(--cv-mute)}}
.sbc-ready .bh-id .by-qm .lit{transform-box:fill-box;transform-origin:center;animation:bhlit .5s cubic-bezier(.2,.8,.2,1.4) calc(var(--ld) + 1.3s) backwards}
@keyframes bhlit{from{transform:scale(0)}}
.sbc-ready .bh-q{animation:bhq .5s ease calc(var(--ld) + 1.4s) backwards}
@keyframes bhq{from{opacity:0;translate:-8px 0}}
.sbc-ready .bh-shadow{animation:bhsh 1.2s ease .5s backwards}@keyframes bhsh{from{opacity:0;transform:scaleX(.4)}}
.sbc-ready .bh-ghost{animation:bhgh 1.4s ease 1.6s backwards}@keyframes bhgh{from{opacity:0}}
.bh-c2 .bh-card{opacity:.92}.bh-c3 .bh-card{opacity:.78}
.bh-fl{animation:cvfl 6s ease-in-out infinite}.bh-c2 .bh-fl{animation-duration:7s;animation-delay:.7s}.bh-c3 .bh-fl{animation-duration:6.4s;animation-delay:1.4s}
.bh-card{--ry:-16deg;box-sizing:border-box;padding:3.2cqw 3.4cqw;background:var(--cv-card);border:1px solid var(--cv-revb);box-shadow:24px 30px 60px var(--cv-sh);transform:perspective(1400px) rotateY(var(--ry));display:flex;flex-direction:column;gap:2cqw;transition:transform .5s cubic-bezier(.2,.7,.2,1),box-shadow .5s ease,opacity .5s ease}
.bh-c:hover .bh-card{transform:perspective(1400px) rotateY(-4deg) translateX(-12px);box-shadow:0 30px 60px rgba(31,79,209,.18);opacity:1}
.bh-top{display:flex;justify-content:space-between;align-items:center;gap:12px}
.bh-id{display:flex;align-items:center;gap:1.7cqw;min-width:0}
.bh-id .by-qm{width:max(26px,4.8cqw);height:max(26px,4.8cqw)}
.bh-id>span{display:flex;flex-direction:column;min-width:0}
.bh-id b{font-weight:600;font-size:max(14px,2.45cqw);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bh-id>span>span{font-size:max(12px,1.85cqw);color:var(--cv-sub)}
.bh-q{font-size:max(9px,1.45cqw);color:var(--cv-acc);white-space:nowrap}
.bh-chips{display:flex;flex-wrap:wrap;gap:1.1cqw}
.bh-chips span{display:flex;align-items:center;gap:6px;padding:.85cqw 1.45cqw;background:var(--cv-soft);font-size:max(11px,1.7cqw)}
.bh-chips i{width:7px;height:7px;background:#1F4FD1;flex:none}
.bh-ghost{position:absolute;opacity:.2;filter:blur(1.5px)}
.bh-shadow{position:absolute;left:8%;top:88%;width:78%;height:12%}
.js-scroll .bh-c{translate:0 calc(var(--sp,0) * var(--dy,0px))}
.js-scroll .bh-c1{--dy:60px}.js-scroll .bh-c3{--dy:-70px}

/* How A, reworked: the thread with who-does-what beside it */
.bw-rail{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column}
.bw-rail li{display:grid;grid-template-columns:28px 1fr auto;align-items:center;gap:12px;padding:14px 0;border-top:1px solid var(--cv-line);font-size:16px;color:var(--cv-mute);transition:color .4s ease}
.bw-rail li .mono{font-size:11px}
.bw-rail li .who{font-size:10px;padding:4px 8px;border:1px solid var(--cv-line);transition:background-color .4s ease,color .4s ease,border-color .4s ease}
.bw-rail li.lit{color:var(--cv-ink)}
.bw-rail li.lit .who{border-color:var(--cv-ink)}
.bw-rail li.lit .who.sbc{background:#1F4FD1;border-color:#1F4FD1;color:#FFFFFF}
.bw-rail li.lit .who.you{background:var(--cv-ink);color:var(--cv-bg)}
.bw-vis{flex:1 1 0;min-width:0;display:flex;justify-content:center}
.bw-win{width:100%;max-width:600px;background:var(--cv-card);border:1px solid var(--cv-line);box-shadow:40px 50px 80px var(--cv-sh);transform:perspective(1600px) rotateY(-10deg) rotateX(4deg);transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.bw-vis:hover .bw-win{transform:perspective(1600px) rotateY(-3deg) rotateX(1deg)}
.bw-h{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px 22px;border-bottom:1px solid var(--cv-line)}
.bw-h>span{display:flex;flex-direction:column;gap:2px;font-size:15px;min-width:0}
.bw-h>span span{font-size:13px;color:var(--cv-sub)}
.bw-st{flex:none;font-size:10px;padding:6px 10px;background:var(--cv-soft);color:var(--cv-acc)}
.bw-body{display:flex;flex-direction:column;gap:14px;padding:22px;min-height:470px;box-sizing:border-box}
.bw-m{max-width:82%;box-sizing:border-box;padding:14px 18px;display:flex;flex-direction:column;gap:8px;font-size:16px;line-height:1.4;transition:opacity .5s ease,translate .5s cubic-bezier(.2,.7,.2,1)}
.bw-m .mono{font-size:10px}
.bw-you{align-self:flex-end;background:var(--cv-band);color:#FFFFFF}
.bw-you .mono{color:#A9AFBA}
.bw-sbc{align-self:flex-start;background:var(--cv-card);border:1px solid var(--cv-revb);color:var(--cv-ink)}
.bw-sbc .mono{color:var(--cv-acc)}
.bw-ok{border-color:#1F4FD1;box-shadow:0 14px 30px rgba(31,79,209,.12)}
.bw-co{display:flex;flex-direction:column;gap:0}
.bw-co span{display:flex;align-items:center;gap:10px;padding:8px 0;border-top:1px solid var(--cv-line);font-size:14px}
.bw-co img{width:22px;flex:none}
.bw-co em{font-style:normal;color:var(--cv-sub);margin-left:auto;font-size:12px}
.bw-sig{display:flex;align-items:center;gap:12px}
.bw-sig .by-qm{width:34px;height:34px}
.bw-sig>span{display:flex;flex-direction:column;font-size:13px;color:var(--cv-sub)}
.bw-sig a{color:var(--cv-acc);font-size:13px}
.bw-meet{flex-direction:row;align-items:center;justify-content:space-between;gap:14px}
.bw-meet>span{display:flex;flex-direction:column;gap:6px}
.bw-date{padding:8px 12px;background:#1F4FD1;font-size:13px;font-weight:600;white-space:nowrap}
.bw-dots{align-self:flex-start;display:flex;gap:5px;padding:14px 16px;border:1px solid var(--cv-line);transition:opacity .3s ease}
.bw-dots i{width:6px;height:6px;background:var(--cv-mute);animation:dot 1s ease-in-out infinite}
.bw-dots i:nth-child(2){animation-delay:.15s}.bw-dots i:nth-child(3){animation-delay:.3s}
@keyframes dot{0%,100%{opacity:.25}50%{opacity:1}}
.js-thread .bw-m:not(.in){opacity:0;translate:0 14px}
.js-thread .bw-dots:not(.in){display:none}
.no-js-hide{display:none}

/* Pack B: the layers */
.bp-stage{position:relative;flex:1 1 0;min-width:0;container-type:inline-size;aspect-ratio:100/88}
.bp-l{position:absolute;left:0;right:0;bottom:16cqw;height:10cqw;z-index:calc(1 + var(--j));translate:0 calc(var(--j) * var(--gap,-11cqw))}
.js-scroll .bp-stage{--k:clamp(0, calc((var(--p,0) - .16) * 3.2), 1)}
.js-scroll .bp-l{--gap:calc(-3.6cqw - 7.4cqw * var(--k))}
.js-scroll .bp-lab{opacity:clamp(0, calc((var(--k) - var(--j) * .13) * 4), 1)}
.bp-pw{position:absolute;left:4cqw;top:-12cqw;transition:translate .35s cubic-bezier(.2,.7,.2,1)}
.bp-plate{width:34cqw;height:34cqw;box-sizing:border-box;transform:rotateX(58deg) rotateZ(45deg);background:var(--bg);border:1px solid var(--bd);box-shadow:0 0 0 1px rgba(255,255,255,.45) inset,18px 18px 30px var(--cv-sh)}
.bp-tie{position:absolute;left:52cqw;top:5cqw;width:6cqw;height:1px;background:var(--cv-revb)}
.bp-lab{position:absolute;left:60cqw;top:5cqw;translate:0 -50%;display:flex;flex-direction:column;gap:2px;transition:opacity .4s ease}
.bp-lab b{font-weight:600;font-size:max(13px,2.3cqw);line-height:1.2}
.bp-lab .mono{font-size:max(9px,1.35cqw);color:var(--cv-mute)}
.bp-top .bp-lab b{color:var(--cv-acc)}
.bp-top .bp-tie{background:#1F4FD1}
.bp-l:hover .bp-pw{translate:0 -1.6cqw}
.bp-l:hover .bp-lab b{color:var(--cv-acc)}
.bp-shadow{position:absolute;left:0;width:62cqw;bottom:2cqw;height:10cqw}
.mode-day .bp-l{--bg:var(--d-bg);--bd:var(--d-bd)}
.mode-night .bp-l{--bg:var(--n-bg);--bd:var(--n-bd)}

/* Terms A */
.bt-wrap{padding:104px 72px 72px;display:flex;flex-direction:column;gap:56px}
.bt-fine{margin-top:36px}
.bt-row{display:flex;justify-content:center;gap:56px;flex-wrap:wrap}
.bt-p{position:relative;flex:0 1 440px;min-width:0}
.bt-in{box-sizing:border-box;min-height:330px;padding:40px;display:flex;flex-direction:column;justify-content:space-between;gap:28px}
.bt-p1 .bt-in{animation:cvfls 6s ease-in-out infinite}.bt-p2 .bt-in{animation:cvfls 7s .8s ease-in-out infinite}
.bt-free{background:linear-gradient(160deg,#3D6BF0 0%,#1F4FD1 60%,#173A9C 100%);color:#FFFFFF;box-shadow:0 40px 70px rgba(31,79,209,.32)}
.bt-tag{align-self:flex-start;font-size:11px;color:#DCE5FF;border:1px solid rgba(220,229,255,.6);padding:3px 7px}
.bt-aed{font-weight:600;font-size:88px;line-height:1;letter-spacing:-.03em}
.bt-free p{margin:0;font-size:18px;color:#DCE5FF}
.bt-you{background:var(--cv-card);border:1px solid var(--cv-line);box-shadow:0 40px 70px var(--cv-sh)}
.bt-co{display:flex;align-items:center;gap:12px}
.bt-co img{width:40px;flex:none}
.bt-co>span{display:flex;flex-direction:column}.bt-co b{font-weight:600;font-size:17px}.bt-co>span span{font-size:13px;color:var(--cv-sub)}
.bt-big{font-weight:600;font-size:30px;line-height:1.15}
.bt-ch{display:flex;flex-direction:column;gap:12px}
.bt-btns{display:flex}
.bt-b{font:600 15px 'Readex Pro',system-ui,sans-serif;padding:12px 18px;cursor:pointer;background:transparent;color:var(--cv-ink);border:1px solid var(--cv-ink);transition:background-color .2s ease,color .2s ease,border-color .2s ease}
.bt-b+.bt-b{border-left:0}
.bt-b:hover{background:#1F4FD1;color:#FFFFFF;border-color:#1F4FD1}
.bt-b[aria-pressed="true"]{background:var(--cv-ink);color:var(--cv-bg)}
.bt-say{font-size:14px;color:var(--cv-sub);min-height:20px}
.bt-shadow{position:absolute;left:0;right:0;top:100%;margin-top:28px;width:100%;height:60px}
.bt-fine{font-size:13px;color:var(--cv-mute);text-align:center}

/* Talk B */
.bk{position:relative;isolation:isolate;overflow:hidden;background:#0E1220;color:#FFFFFF;min-height:640px;display:flex;align-items:center}
.bk-photo{position:absolute;left:44%;top:0;right:0;bottom:0;z-index:-2;overflow:hidden}
.bk-photo img{width:100%;height:100%;object-fit:cover;object-position:60% 50%;display:block;filter:brightness(.85)}
.bk-shade{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#0E1220 0%,#0E1220 44%,rgba(14,18,32,.35) 58%,rgba(14,18,32,0) 75%)}
.js-scroll .bk .bk-photo{translate:0 calc((var(--p,0) - .5) * -60px)}
.bk-in{flex:1;display:flex;align-items:center;gap:56px;padding:96px 72px;box-sizing:border-box;flex-wrap:wrap}
.bk-copy{flex:0 1 420px;display:flex;flex-direction:column;gap:20px}
.bk h2{margin:0;font-weight:600;font-size:56px;line-height:1.04;letter-spacing:-.025em}
.bk-copy p{margin:0;font-size:19px;color:#DCE1EA}
.bk-card{flex:0 1 460px;min-width:0;box-sizing:border-box;padding:30px;background:#FFFFFF;color:#1A1D24;box-shadow:0 40px 80px rgba(0,0,0,.45);animation:cvfls 7s ease-in-out infinite}
.bk-card form{display:flex;flex-direction:column;gap:14px}
.bk-card label{font-size:15px}
.bk-fi{font:300 16px 'Readex Pro',system-ui,sans-serif;color:#1A1D24;background:#FFFFFF;border:1px solid #A9AEB8;border-radius:0;padding:13px 14px;width:100%;box-sizing:border-box}
.bk-fi:focus{outline:none;border-color:#1F4FD1;box-shadow:0 0 0 3px rgba(31,79,209,.2)}
textarea.bk-fi{min-height:88px;resize:vertical}
.bk-err{font-size:14px;color:#B3261E;min-height:0}
.bk-go{align-self:flex-start;font:600 16px 'Readex Pro',system-ui,sans-serif;background:#1F4FD1;color:#FFFFFF;border:0;padding:15px 22px;cursor:pointer;transition:background-color .2s ease,transform .2s ease}
.bk-go:hover{background:#173A9C;transform:translateY(-2px)}
.bk-proto{font-size:13px;color:#5B6070}
.bk-done{display:flex;flex-direction:column;gap:12px}
.bk-done[hidden],.bk-card form[hidden]{display:none}
.bk-done .by-qm{width:44px;height:44px;color:#1A1D24}
.bk-done b{font-weight:600;font-size:22px}
.bk-done span{font-size:14px;color:#5B6070}
.bk-done button{align-self:flex-start;font:600 14px 'Readex Pro',system-ui,sans-serif;color:#1F4FD1;background:none;border:0;padding:4px 0;cursor:pointer}

@media (max-width:1100px){
  .bk-in{padding:80px 32px}
  .bt-wrap{padding:80px 32px}
}
@media (max-width:900px){
  .bh-stage{aspect-ratio:350/440}
  .bh-c{width:88%}
  .bh-c1{left:0;top:64%}.bh-c2{left:6%;top:34%}.bh-c3{left:12%;top:4%}
  .bh-top{flex-direction:column;align-items:flex-start;gap:8px}
  .bh-id b{white-space:normal}
  .bh-shadow{top:90%}
  .bh-card{padding:14px 16px;gap:12px;--ry:-10deg}
  .bh-ghost{display:none}
  .bw-win{transform:none}
  .bw-body{min-height:0;padding:16px}
  .bw-m{max-width:92%;font-size:15px}
  .bw-h{padding:14px 16px}
  .bp-stage{aspect-ratio:100/96}
  .bp-pw{left:0}
  .bp-tie{left:47cqw;width:4cqw}
  .bp-lab{left:53cqw}
  .bt-wrap{padding:56px 20px;gap:40px}
  .bt-row{gap:48px}
  .bt-in{min-height:0;padding:28px}
  .bt-aed{font-size:64px}
  .bt-big{font-size:24px}
  .bk{min-height:0;display:block}
  .bk-photo{left:0;bottom:auto;height:360px}
  .bk-shade{background:linear-gradient(180deg,rgba(14,18,32,.55) 0%,rgba(14,18,32,.85) 200px,#0E1220 360px)}
  .bk-in{padding:72px 20px 56px;gap:32px}
  .bk h2{font-size:38px}
  .bk-card{padding:22px}
}
/* phones and touch: play once when the section comes into view (assets/motion.js adds .js-reveal) */
@media (max-width:900px),(hover:none){
  .bh-fl,.bt-in,.bk-card,.bw-win{will-change:transform}
}
.js-reveal .bp-l{translate:0 calc(var(--j) * -3.6cqw);transition:translate .9s cubic-bezier(.2,.7,.2,1) calc(var(--j) * .12s)}
.js-reveal .bp-lab{opacity:0;transition:opacity .5s ease calc(.35s + var(--j) * .12s)}
.js-reveal .on .bp-l{translate:0 calc(var(--j) * var(--gap,-11cqw))}
.js-reveal .on .bp-lab{opacity:1}
@media (max-width:900px){.js-reveal .on .bp-l,.bp-l{--gap:-12cqw}}
@media (prefers-reduced-motion: reduce){
  .bh-fl,.bt-in,.bk-card,.bk-photo img,.bw-dots i{animation:none !important}
  .bp-l,.bp-lab{transition:none !important}
}
</style>
'''

# ---------- small parts ----------
QM = '<svg class="by-qm" viewBox="0 0 100 100" aria-hidden="true"><rect x="6" y="6" width="88" height="88" fill="none" stroke="currentColor" stroke-width="6"></rect><rect class="lit" x="62" y="10" width="28" height="28"></rect></svg>'


def cube(mode, kind):
    n = '-n' if mode == 'night' and kind in ('ghost', 'ink', 'frost', 'accent') else ''
    return '/assets/img/sbc/cube-%s%s.svg' % (kind, n)


def bg(gx, gy, lines=True):
    l = '<div class="cv-far"></div><div class="cv-near"></div>' if lines else ''
    return '<div class="cv-bg" aria-hidden="true"><div class="cv-glow" style="--gx:%s;--gy:%s"></div>%s</div>' % (gx, gy, l)


def hero(mode, sfx):
    cards = [('bh-c3', 'Water treatment contractor', 'Germany'),
             ('bh-c2', 'Cybersecurity training', 'United Kingdom'),
             ('bh-c1', 'Rail signalling engineer', 'India')]
    chips = ''.join('<span style="--i:%d"><i></i>%s</span>' % (i, c) for i, c in enumerate(('Ownership', 'Sanctions', 'Licences', 'ICV')))
    cs = ''.join('<div class="bh-c %s"><div class="bh-fl"><div class="bh-card"><div class="bh-top"><span class="bh-id">%s<span><b>%s</b><span>%s</span></span></span><span class="mono bh-q">SBC-Qualified</span></div><div class="bh-chips">%s</div></div></div></div>'
                 % (c, QM, t, w, chips) for c, t, w in cards)
    ghosts = ''.join('<img class="bh-ghost" src="%s" alt="" style="left:%s;top:%s;width:%s">' % (cube(mode, 'ghost'), l, t, w)
                     for l, t, w in (('90%', '4%', '7%'), ('95%', '30%', '6%'), ('92%', '74%', '6.5%'), ('-2%', '86%', '5.5%')))
    return ('<section class="sec cv-sec" aria-label="Hero">' + bg('72%', '50%') +
            '<div class="cv-hero"><div class="cv-copy"><span class="cv-k rise">For Gulf buyers</span><h1 class="rise">Suppliers, already checked.</h1><p class="rise2">Posting a need is free.</p>'
            '<div class="cv-btns rise3"><a class="btn cv-btn" href="#talk%s">Talk to SBC</a><a class="cv-ghost" href="#pack%s">See what arrives</a></div></div>' % (sfx, sfx) +
            '<div class="bh-stage" role="img" aria-label="A shortlist of three international suppliers, each marked SBC-Qualified, with ownership, sanctions, licences and ICV checked">'
            + ghosts + '<img class="bh-shadow" src="/assets/img/sbc/shadow.svg" alt="">' + cs + '</div></div></section>')


def how(mode, sfx):
    steps = [('01', 'Post your need', 'you', 'You · free'),
             ('02', 'SBC matches checked companies', 'sbc', 'SBC'),
             ('03', 'An SBC officer approves', 'sbc', 'SBC'),
             ('04', 'You meet, pack in hand', 'you', 'You')]
    rail = ''.join('<li data-s="%d"><span class="mono">%s</span><span>%s</span><span class="mono who %s">%s</span></li>' % (i + 1, n, t, k, w)
                   for i, (n, t, k, w) in enumerate(steps))
    cos = ''.join('<span><img src="%s" alt="">%s<em>%s</em></span>' % (cube(mode, k), t, w) for k, t, w in
                  (('lit', 'Water treatment contractor', 'Germany'), ('frost', 'Desalination engineer', 'Spain'), ('ink', 'Pipeline specialist', 'South Korea')))
    return ('<section class="sec cv-sec" id="how%s" aria-label="How it works for buyers">' % sfx + bg('70%', '50%') +
            '<div class="cv-split"><div class="cv-copy by-head"><span class="cv-k">How it works</span><h2>You post. SBC does the rest.</h2><ol class="bw-rail" aria-label="Who does each step">' + rail + '</ol></div>'
            '<div class="bw-vis"><div class="bw-win" aria-label="An example thread for one need">'
            '<div class="bw-h"><span>Your need<span>Water treatment contractor · Abu Dhabi</span></span><span class="mono bw-st" aria-live="polite">Meeting set</span></div>'
            '<div class="bw-body">'
            '<div class="bw-m bw-you" data-s="1" data-st="Posted"><span class="mono">01 · You · free</span><span>We need a water treatment contractor in Abu Dhabi.</span></div>'
            '<div class="bw-dots" data-for="2" aria-hidden="true"><i></i><i></i><i></i></div>'
            '<div class="bw-m bw-sbc" data-s="2" data-st="Matched"><span class="mono">02 · SBC matches</span><span>Three checked companies fit.</span><span class="bw-co">' + cos + '</span></div>'
            '<div class="bw-dots" data-for="3" aria-hidden="true"><i></i><i></i><i></i></div>'
            '<div class="bw-m bw-sbc bw-ok" data-s="3" data-st="Approved"><span class="mono">03 · An SBC officer approves</span><span>Approved for introduction.</span>'
            '<span class="bw-sig">' + QM + '<span>Signed · [officer name]<a href="#pack%s">The pack is attached</a></span></span></div>' % sfx +
            '<div class="bw-m bw-you bw-meet" data-s="4" data-st="Meeting set"><span><span class="mono">04 · You meet</span><span>Introduction meeting</span></span><span class="bw-date">[date]</span></div>'
                        '</div></div></div></div></section>')


def pack(mode, sfx):
    # bottom of the stack first; the officer's approval caps it
    L = [('Ownership to the final owner', 'Checked [date]', '#F8F9FD', '#D3DBF1', '#262B38', '#3A3F4A'),
         ('Sanctions screening', 'Run [date]', '#F3F5FB', '#D3DBF1', '#2A3040', '#3E4558'),
         ('Certificates', 'Valid', '#EEF2FC', '#C9D2EA', '#2C3448', '#434C66'),
         ('Local agent', 'Appointed', '#E7ECF9', '#C3CFEE', '#2F3A5C', '#3E4C78'),
         ('ICV certificate', 'Issued [date]', '#DCE4F8', '#B8C6EC', '#33416B', '#465A92'),
         ('Officer approval', 'Signed [date]', '#1F4FD1', '#1F4FD1', '#1F4FD1', '#5B82FF')]
    layers = ''.join('<div class="bp-l%s" style="--j:%d;--d-bg:%s;--d-bd:%s;--n-bg:%s;--n-bd:%s"><div class="bp-pw"><div class="bp-plate"></div></div><span class="bp-tie"></span><span class="bp-lab"><b>%s</b><span class="mono">%s</span></span></div>'
                     % (' bp-top' if j == 5 else '', j, a, b, c, d, t, s) for j, (t, s, a, b, c, d) in enumerate(L))
    return ('<section class="sec cv-sec" id="pack%s" aria-label="What arrives">' % sfx + bg('64%', '54%') +
            '<div class="cv-split"><div class="cv-copy by-head"><span class="cv-k">What arrives</span><h2>Five checks, one pack.</h2><p class="cv-sub">Each dated. Signed by an officer.</p></div>'
            '<div class="bp-stage" role="img" aria-label="The introduction pack as a stack: ownership to the final owner, sanctions screening, certificates, local agent and ICV certificate, capped by the officer&#39;s signed approval">'
            '<img class="bp-shadow" src="/assets/img/sbc/shadow.svg" alt="">' + layers + '</div></div></section>')


def terms(mode, sfx):
    return ('<section class="sec cv-sec" id="cost%s" aria-label="What it costs">' % sfx +
            '<div class="cv-bg" aria-hidden="true"><div class="cv-glow" style="--gx:36%%;--gy:60%%"></div><div class="cv-glow" style="--gx:68%%;--gy:60%%;opacity:.7"></div><div class="cv-far"></div><div class="cv-near"></div></div>'
            '<div class="bt-wrap"><div class="cv-head by-head"><span class="cv-k">What it costs you</span><h2>Nothing. And the choice stays yours.</h2></div>'
            '<div class="bt-row">'
            '<div class="bt-p bt-p1"><div class="bt-in bt-free"><span class="mono bt-tag">Buyer fee</span><span class="bt-aed">AED 0</span><p>To post a need and meet suppliers</p></div><img class="bt-shadow" src="/assets/img/sbc/shadow.svg" alt=""></div>'
            '<div class="bt-p bt-p2"><div class="bt-in bt-you"><span class="bt-co"><img src="%s" alt=""><span><b>Water treatment contractor</b><span>Introduced by SBC</span></span></span>' % cube(mode, 'lit') +
            '<span class="bt-big">You decide who to hire.</span><div class="bt-ch"><div class="bt-btns" role="group" aria-label="Try it"><button type="button" class="bt-b" data-say="Taken forward. You contract with them directly.">Take it forward</button><button type="button" class="bt-b" data-say="Passed. Nothing is owed.">Pass</button></div><span class="bt-say" aria-live="polite"></span></div></div><img class="bt-shadow" src="/assets/img/sbc/shadow.svg" alt=""></div>'
            '</div><span class="bt-fine">An introduction is not a promised contract. Your own procurement rules still apply.</span></div></section>')


def talk(mode, sfx):
    return ('<section class="sec bk" id="talk%s" aria-label="Talk to SBC">' % sfx +
            '<div class="bk-photo" aria-hidden="true"><img class="kb-ap" src="/assets/img/585baed4eca919820a1c25863c794e77.webp" alt="" loading="lazy"></div><div class="bk-shade" aria-hidden="true"></div>'
            '<div class="bk-in"><div class="bk-copy by-head"><span class="cv-k ap-k">For Gulf buyers · free</span><h2>Post a need.</h2><p>Two lines is enough to start.</p></div>'
            '<div class="bk-card"><form novalidate>'
            '<label for="nd%s">What do you need?</label><textarea class="bk-fi" id="nd%s" name="need" placeholder="A contractor to upgrade a water treatment plant"></textarea>' % (sfx, sfx) +
            '<label for="wh%s">Where</label><select class="bk-fi" id="wh%s" name="where"><option>United Arab Emirates</option><option>Saudi Arabia</option><option>Qatar</option><option>Kuwait</option><option>Bahrain</option><option>Oman</option></select>' % (sfx, sfx) +
            '<span class="bk-err" aria-live="polite"></span><button type="submit" class="bk-go">Talk to SBC</button><span class="bk-proto">Prototype: this form does not send anything yet.</span></form>'
            '<div class="bk-done" hidden tabindex="-1">' + QM + '<b>Thank you. SBC will be in touch.</b><span>Prototype: nothing was sent.</span><button type="button">Post another need</button></div>'
            '</div></div></section>')


SCRIPT = r'''<script>
(function(){
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
  var hasIO='IntersectionObserver' in window;
  // headings rise in once
  if(!reduce){
    var heads=document.querySelectorAll('.by-head');
    heads.forEach(function(el){el.classList.add('cvr')});
    if(hasIO){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{threshold:.2});heads.forEach(function(el){io.observe(el)})}
    else heads.forEach(function(el){el.classList.add('in')});
  }

  // How it works: the thread plays on a loop while it is on screen, SBC typing before each reply
  document.querySelectorAll('.bw-win').forEach(function(win){
    var sec=win.closest('section'), msgs=win.querySelectorAll('.bw-m'), dots=win.querySelectorAll('.bw-dots'),
        rail=sec.querySelectorAll('.bw-rail li'), st=win.querySelector('.bw-st'), timers=[], vis=false, running=false;
    function show(n){
      msgs.forEach(function(m){m.classList.toggle('in',+m.getAttribute('data-s')<=n)});
      rail.forEach(function(r){r.classList.toggle('lit',+r.getAttribute('data-s')<=n)});
      st.textContent=n?win.querySelector('.bw-m[data-s="'+n+'"]').getAttribute('data-st'):'New need';
    }
    function typing(k,on){dots.forEach(function(d){if(+d.getAttribute('data-for')===k)d.classList.toggle('in',on)})}
    function at(t,fn){timers.push(setTimeout(fn,t))}
    function run(){
      running=true;timers.forEach(clearTimeout);timers=[];
      show(0);                         // the last round fades out together
      var t=700;
      [1,2,3,4].forEach(function(k){
        if(k===2||k===3){at(t,function(){typing(k,true)});t+=900;}
        at(t,function(){typing(k,false);show(k)});t+=k===1?700:1100;
      });
      at(t+2600,function(){running=false;if(vis)run()}); // hold the finished thread, then go again
    }
    if(reduce||!hasIO){show(4);return}
    win.classList.add('js-thread');show(0);
    // the hidden day or night copy never intersects, so only the visible one runs
    new IntersectionObserver(function(es){es.forEach(function(en){vis=en.isIntersecting;if(vis&&!running)run()})},{threshold:.35}).observe(win);
  });

  // What it costs: try the choice
  document.querySelectorAll('.bt-btns').forEach(function(g){
    var say=g.parentNode.querySelector('.bt-say');
    g.querySelectorAll('.bt-b').forEach(function(b){b.setAttribute('aria-pressed','false');b.addEventListener('click',function(){
      g.querySelectorAll('.bt-b').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});say.textContent=b.getAttribute('data-say');
    })});
  });

  // Post a need (prototype: nothing is sent)
  document.querySelectorAll('.bk-card').forEach(function(card){
    var f=card.querySelector('form'), done=card.querySelector('.bk-done'), err=card.querySelector('.bk-err'), ta=f.querySelector('textarea');
    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(!ta.value.trim()){err.textContent='Add a line about what you need.';ta.focus();return}
      err.textContent='';f.hidden=true;done.hidden=false;done.focus();
    });
    done.querySelector('button').addEventListener('click',function(){f.reset();done.hidden=true;f.hidden=false;ta.focus()});
  });
})();
</script>
'''


def mode_copy(mode):
    sfx = '' if mode == 'day' else '-n'
    open_div, hd, ft = chrome(mode)
    body = hero(mode, sfx) + how(mode, sfx) + pack(mode, sfx) + terms(mode, sfx) + talk(mode, sfx)
    return open_div + hd + body + ft + '</div></div>'


site_open = SRC[SRC.find('<body>'):SRC.find('<div class="mode-day">')]
html = (head + CSS + '</head>\n' + site_open + mode_copy('day') + mode_copy('night') + '</div>\n</div>\n' + SCRIPT + '</body>\n</html>\n')
open('buyers/index.html', 'w', encoding='utf-8').write(html)
print('buyers/index.html', len(html), 'bytes')
