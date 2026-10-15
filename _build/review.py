"""Builds review/index.html (How the review works), the interim version.

Answers, in order, what a newcomer asks: what gets checked, who checks it, what if I fall short,
what happens after I pass. Facts SBC has not given yet are [bracketed]. Head, header and footer come
from companies/index.html so the pages stay in step. Run from the repo root:  python3 _build/review.py
"""
import re

SRC = open('companies/index.html', encoding='utf-8').read()

head = SRC[:SRC.find('</head>')]
head = head.replace('<title>SBC Capital · For companies</title>', '<title>SBC Capital · How the review works</title>')
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="The five things SBC Capital checks before any Gulf buyer sees a company, who checks them, and what happens if you pass or fall short.">', head)


def chrome(mode):
    start = SRC.find('<div class="mode-%s">' % mode)
    hs = SRC.find('<header', start); he = SRC.find('</header>', hs) + 9
    fs = SRC.find('<footer', he); fe = SRC.find('</footer>', fs) + 9
    hd, ft = SRC[hs:he], SRC[fs:fe]
    hd = hd.replace(' aria-current="page">For companies', '>For companies')
    hd = re.sub(r'(href="/companies/" style="[^"]*); font-weight: 600"', r'\1"', hd)
    hd = re.sub(r'(href="/review/" style="[^"]*)">How the review works', r'\1; font-weight: 600" aria-current="page">How the review works', hd)
    hd = hd.replace('href="/companies/#apply"', 'href="/companies/apply/"')
    return SRC[start:hs], hd, ft


CHECKS = [
    ('Identity', 'The company is real, registered and in good standing.', 'Certificate of incorporation or trade licence', 'Company registries'),
    ('Ownership to the final owner', 'Every holding company, traced until we reach the people who own it.', 'Shareholder register and an ownership chart', 'Company registries in each country in the chain'),
    ('Licences and certifications', 'Your trade licence, sector licences and quality or industry certifications are current and name the same company.', 'Copies of each licence and certification', 'Confirmed with the issuing body where it can be'),
    ('Screening', 'The company, its owners and its directors, screened against <span class="rw-ph">[sanctions lists]</span>, politically exposed person (PEP) lists and adverse media. Then again every month while you hold the mark. <span class="rw-tbc">Working answer, for SBC to confirm.</span>', 'Names and dates of birth of owners and directors', 'Screening run and dated in your file'),
    ('Gulf readiness', 'Your local content (ICV, In-Country Value) and local presence, assessed against the target country&#39;s rules. An ICV certificate or a local agent is not a pass condition.', 'Any ICV certificate, local entity or agent agreement you already have', 'The target country&#39;s rules. If you are short, your action plan says what to get and lists local agents SBC has reviewed.'),
]

CSS = r'''<style>
/* ===== How the review works ===== */
.rw-k{font-family:'IBM Plex Mono',monospace;font-weight:500;letter-spacing:.06em;font-size:12px;color:var(--cv-sub)}
.rw-ph{color:var(--cv-ink);text-decoration:underline dashed;text-decoration-color:var(--cv-mute);text-decoration-thickness:1px;text-underline-offset:4px}
.rw-tbc{font-size:13px;color:var(--cv-sub)}
/* hero: the review file */
.rw-file{flex:1 1 0;min-width:0;display:flex;justify-content:center}
.rw-card{width:100%;max-width:520px;background:var(--cv-card);border:1px solid var(--cv-line);box-shadow:30px 40px 70px var(--cv-sh);transform:perspective(1600px) rotateY(-12deg) rotateX(4deg);transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.rw-file:hover .rw-card{transform:perspective(1600px) rotateY(-3deg) rotateX(1deg)}
.rw-ch{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px 22px;border-bottom:1px solid var(--cv-line);font-size:15px}
.rw-ch span{font-size:13px;color:var(--cv-sub)}
.rw-row{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:13px 22px;border-top:1px solid var(--cv-line);font-size:15px}
.rw-row:first-of-type{border-top:0}
.rw-st{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--cv-acc);white-space:nowrap}
.rw-st i{width:12px;height:12px;background:#1F4FD1;flex:none}
.rw-sign{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:14px 22px;border-top:1px solid var(--cv-line);background:var(--cv-soft)}
.rw-sign span{display:flex;align-items:center;gap:8px;font-size:13px}
.rw-sign i{width:12px;height:12px;border:1.5px solid var(--cv-acc);box-sizing:border-box;flex:none;background:var(--cv-acc)}
.rw-foot{display:flex;align-items:center;gap:12px;padding:16px 22px;border-top:1px solid var(--cv-line);font-size:14px;font-weight:600}
.rw-qm{width:30px;height:30px;flex:none;color:var(--cv-ink)}
.rw-qm .lit{fill:#1F4FD1}
/* load: the file fills in after the loader lifts */
.sbc-ready .rw-row .rw-st{animation:rwtick .45s ease calc(.5s + var(--i) * .22s) backwards}
@keyframes rwtick{from{opacity:0;transform:translateX(-8px)}}
.sbc-ready .rw-sign i{animation:rwsig .4s ease calc(1.8s + var(--i) * .3s) backwards}
@keyframes rwsig{from{background:transparent}}
.sbc-ready .rw-foot .lit{transform-box:fill-box;transform-origin:center;animation:rwlit .5s cubic-bezier(.2,.8,.2,1.4) 2.6s backwards}
@keyframes rwlit{from{transform:scale(0)}}

/* the five checks: a real table, because it is a matrix */
.rw-wrap{padding:104px 72px;display:flex;flex-direction:column;gap:40px}
.rw-head{display:flex;flex-direction:column;gap:14px;max-width:720px}
.rw-head p{margin:0;font-size:18px;line-height:1.55;color:var(--cv-sub)}
.rw-t{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5}
.rw-t th,.rw-t td{text-align:left;vertical-align:top;padding:20px 18px;border-top:1px solid var(--cv-line)}
.rw-t thead th{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.06em;color:var(--cv-sub);border-top:0;padding-top:0}
.rw-t tbody th{font-weight:600;font-size:17px;width:24%}
.rw-t tbody th span{display:flex;gap:12px;align-items:baseline}
.rw-t tbody th i{width:10px;height:10px;background:#1F4FD1;flex:none;transform:translateY(-1px)}
.rw-t td{color:var(--cv-ink)}
.rw-t td.rw-how{color:var(--cv-sub)}
.rw-t tbody tr{transition:background-color .2s ease}
.rw-t tbody tr:hover{background:var(--cv-soft)}
.rw-note{font-size:14px;color:var(--cv-sub)}

/* two officers: the mark only completes when both have signed */
.rw-two{display:flex;align-items:center;gap:56px;padding:104px 72px;flex-wrap:wrap}
.rw-two .cv-copy{flex:1 1 380px}
.rw-pair{flex:1 1 460px;min-width:0;display:flex;align-items:center;justify-content:center;gap:22px}
.rw-off{flex:0 1 190px;box-sizing:border-box;padding:22px;background:var(--cv-card);border:1px solid var(--cv-line);display:flex;flex-direction:column;gap:12px;font-size:14px;color:var(--cv-sub)}
.rw-off b{font-size:16px;font-weight:600;color:var(--cv-ink)}
.rw-off svg{width:34px;height:34px}
.rw-mark{flex:none;width:150px;height:150px;color:var(--cv-ink)}
.rw-mark .edge{stroke-dasharray:704;stroke-dashoffset:0}
.rw-mark .h1,.rw-mark .h2{transform-box:fill-box;transform-origin:left}
.js-play .rw-two:not(.on) .rw-mark .edge{stroke-dashoffset:704}
.js-play .rw-two:not(.on) .rw-mark .h1,.js-play .rw-two:not(.on) .rw-mark .h2{transform:scaleX(0)}
.rw-two .rw-mark .edge{transition:stroke-dashoffset 1.2s ease .2s}
.rw-two .rw-mark .h1{transition:transform .5s ease 1.4s}
.rw-two .rw-mark .h2{transition:transform .5s ease 2s}
.rw-plus{font-size:28px;color:var(--cv-mute);font-weight:300}

/* two outcomes */
.rw-fork{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.rw-out{position:relative;padding:32px;display:flex;flex-direction:column;gap:18px;border:1px solid var(--cv-line);background:var(--cv-card)}
.rw-out h3{margin:0;font-size:24px;font-weight:600;letter-spacing:-.01em}
.rw-out ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:12px}
.rw-out li{display:grid;grid-template-columns:14px 1fr;gap:12px;font-size:16px;line-height:1.5}
.rw-out li i{width:10px;height:10px;margin-top:7px;box-sizing:border-box}
.rw-short li i{border:1.5px solid var(--cv-ink)}
.rw-pass{border-color:#1F4FD1;box-shadow:0 30px 60px rgba(31,79,209,.16)}
.rw-pass li i{background:#1F4FD1}
.rw-tag{align-self:flex-start;font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.06em;padding:5px 9px}
.rw-short .rw-tag{background:var(--cv-soft);color:var(--cv-ink)}
.rw-pass .rw-tag{background:#1F4FD1;color:#FFFFFF}

/* twelve months, then a re-check */
.rw-year{display:flex;flex-direction:column;gap:12px}
.rw-months{display:grid;grid-template-columns:repeat(12,minmax(0,1fr)) minmax(0,1.6fr);gap:4px;align-items:end}
.rw-months span{display:block;height:46px;background:var(--cv-rev);border:1px solid var(--cv-revb);box-sizing:border-box}
.rw-months span:first-child{background:#1F4FD1;border-color:#1F4FD1}
.rw-months .re{height:70px;background:var(--cv-btn);border-color:var(--cv-btn);display:flex;align-items:flex-end;padding:8px;color:var(--cv-btnfg);font-size:12px;font-weight:600}
.rw-axis{display:grid;grid-template-columns:repeat(12,minmax(0,1fr)) minmax(0,1.6fr);gap:4px;font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--cv-sub)}
.js-play .rw-yr:not(.on) .rw-months span{transform:scaleY(0)}
.rw-months span{transform-origin:bottom;transition:transform .45s cubic-bezier(.2,.7,.2,1) calc(var(--i) * .06s)}
.rw-facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;margin-top:20px}
.rw-fees{display:flex;justify-content:space-between;gap:16px;font-size:14px;color:var(--cv-sub)}
.rw-fees b{color:var(--cv-ink);font-weight:600}
.rw-facts div{display:flex;flex-direction:column;gap:6px;padding-top:14px;border-top:2px solid var(--cv-ink);font-size:15px;line-height:1.5;color:var(--cv-sub)}
.rw-facts b{color:var(--cv-ink);font-weight:600;font-size:17px}

/* closing: two doors */
.rw-end{position:relative;isolation:isolate;overflow:hidden;background:#0E1220;color:#FFFFFF}
.rw-end .ap-photo{position:absolute;inset:0;z-index:-2}
.rw-end .ap-shade{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(14,18,32,.94) 0%,rgba(14,18,32,.72) 45%,rgba(14,18,32,.2) 80%)}
.rw-end-in{padding:112px 72px;display:flex;flex-direction:column;gap:22px;max-width:620px}
.rw-end h2{margin:0;font-weight:600;font-size:52px;line-height:1.04;letter-spacing:-.025em}
.rw-end p{margin:0;font-size:19px;color:#DCE1EA}
.rw-doors{display:flex;gap:12px;flex-wrap:wrap}
.rw-doors .a{background:#1F4FD1;color:#FFFFFF;font-size:16px;font-weight:600;padding:16px 24px;text-decoration:none;transition:background-color .2s ease,transform .2s ease}
.rw-doors .a:hover{background:#173A9C;transform:translateY(-2px)}
.rw-doors .b{border:1px solid #FFFFFF;color:#FFFFFF;font-size:16px;font-weight:600;padding:15px 24px;text-decoration:none;transition:background-color .2s ease,color .2s ease}
.rw-doors .b:hover{background:#FFFFFF;color:#1A1D24}

@media (min-width:901px) and (max-width:1180px){.rw-pair{flex-wrap:wrap;gap:12px}.rw-off{flex:1 1 0}.rw-plus:last-of-type{display:none}.rw-mark{flex-basis:100%;width:120px;height:120px;margin-top:8px}}
@media (max-width:1100px){.rw-wrap,.rw-two{padding:80px 32px}.rw-end-in{padding:88px 32px}.rw-facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:900px){
  .rw-card{transform:none}
  .rw-wrap,.rw-two{padding:56px 20px;gap:28px}
  .rw-t thead{display:none}
  .rw-t,.rw-t tbody,.rw-t tr,.rw-t th,.rw-t td{display:block;width:auto}
  .rw-t tbody tr{padding:18px 0;border-top:1px solid var(--cv-line)}
  .rw-t tbody th,.rw-t td{border-top:0;padding:4px 0}
  .rw-t tbody th{width:auto;padding-bottom:8px}
  .rw-t td::before{content:attr(data-l);display:block;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.06em;color:var(--cv-sub);margin-top:6px}
  .rw-pair{flex-wrap:wrap;gap:12px}
  .rw-off{padding:16px;flex:1 1 0}
  .rw-plus:last-of-type{display:none}
  .rw-mark{width:110px;height:110px;flex-basis:100%;margin-top:8px}
  .rw-fork{grid-template-columns:1fr}
  .rw-out{padding:24px}
  .rw-months,.rw-axis{grid-template-columns:repeat(12,minmax(0,1fr)) minmax(0,4fr)}
  .rw-months span{height:30px}.rw-months .re{height:46px;font-size:11px;padding:5px;white-space:nowrap}
  .rw-axis span:not(:first-child):not(:nth-child(6)):not(:last-child){visibility:hidden}
  .rw-facts{grid-template-columns:1fr;gap:18px}
  .rw-end-in{padding:72px 20px}
  .rw-end h2{font-size:38px}
  .rw-end .ap-shade{background:linear-gradient(180deg,rgba(14,18,32,.9),rgba(14,18,32,.75))}
}
@media (prefers-reduced-motion: reduce){
  .rw-mark .edge,.rw-mark .h1,.rw-mark .h2,.rw-months span{transition:none !important;stroke-dashoffset:0 !important;transform:none !important}
}
</style>
'''

QM = '<svg class="rw-qm" viewBox="0 0 100 100" aria-hidden="true"><rect x="6" y="6" width="88" height="88" fill="none" stroke="currentColor" stroke-width="7"></rect><rect class="lit" x="62" y="10" width="28" height="28"></rect></svg>'


def bg(gx, gy, lines=False):
    l = '<div class="cv-far"></div><div class="cv-near"></div>' if lines else ''
    return '<div class="cv-bg" aria-hidden="true"><div class="cv-glow" style="--gx:%s;--gy:%s"></div>%s</div>' % (gx, gy, l)


def hero():
    rows = ''.join('<div class="rw-row"><span>%s</span><span class="rw-st" style="--i:%d"><i></i>Reviewed</span></div>' % (c[0], i) for i, c in enumerate(CHECKS))
    return ('<section class="sec cv-sec" aria-label="Hero">' + bg('70%', '48%', True) +
            '<div class="cv-hero"><div class="cv-copy"><h1 class="rise">How the review works.</h1>'
            '<p class="rise2">Before any Gulf buyer sees your company, two SBC officers check five things. Here is each one, what you send, and what happens next.</p>'
            '<div class="cv-btns rise3"><a class="btn cv-btn" href="/companies/apply/">Apply</a><a class="cv-ghost" href="#checks">See the five checks</a></div></div>'
            '<div class="rw-file"><div class="rw-card" role="img" aria-label="An example review file: five checks marked reviewed, signed by two officers, ending in the SBC-Qualified mark">'
            '<div class="rw-ch">Review file<span>Your company</span></div>' + rows +
            '<div class="rw-sign"><span><i style="--i:0"></i>Officer 1 signed</span><span><i style="--i:1"></i>Officer 2 signed</span></div>'
            '<div class="rw-foot">' + QM + 'SBC-Qualified · valid 12 months</div></div></div></div></section>')


def checks(sfx):
    rows = ''.join('<tr><th scope="row"><span><i aria-hidden="true"></i>%s</span></th><td data-l="SBC confirms">%s</td><td data-l="You send">%s</td><td class="rw-how" data-l="Verified against">%s</td></tr>' % c for c in CHECKS)
    return ('<section class="sec cv-sec" id="checks%s" aria-label="The five checks">' % sfx +
            '<div class="rw-wrap"><div class="rw-head by-head"><h2>Five checks, each on the record.</h2><p>Every check is dated in your file, so a buyer sees exactly what was confirmed and when.</p></div>'
            '<table class="rw-t"><thead><tr><th scope="col">Check</th><th scope="col">SBC confirms</th><th scope="col">You send</th><th scope="col">Verified against</th></tr></thead><tbody>' + rows + '</tbody></table>'
            '<span class="rw-note"><b style="font-weight:600;color:var(--cv-ink)">AED 12,500 review fee, once.</b> The checklist arrives within 2 working days of registering. You upload at your own pace. <span class="rw-tbc">Working answer, for SBC to confirm.</span></span></div></section>')


def officers():
    seal = '<svg viewBox="0 0 100 100" aria-hidden="true"><rect x="8" y="8" width="84" height="84" fill="none" stroke="#1F4FD1" stroke-width="8"></rect><path d="M30 52l14 14 26-30" fill="none" stroke="#1F4FD1" stroke-width="9"></path></svg>'
    mark = ('<svg class="rw-mark" viewBox="0 0 200 200" role="img" aria-label="The SBC-Qualified mark completes only when both officers have signed">'
            '<rect class="edge" x="12" y="12" width="176" height="176" fill="none" stroke="currentColor" stroke-width="12"></rect>'
            '<rect class="h1" x="118" y="22" width="30" height="60" fill="#1F4FD1"></rect><rect class="h2" x="148" y="22" width="30" height="60" fill="#3D6BF0"></rect></svg>')
    return ('<section class="sec cv-sec rw-two-sec" aria-label="Who reviews">' + bg('68%', '50%') +
            '<div class="rw-two"><div class="cv-copy by-head"><h2>Two officers. Both must pass you.</h2>'
            '<p>Each officer reviews your whole file on their own. If either has a question, it comes back to you, never to a buyer. The review takes about 10 working days once your file is complete. <span class="rw-tbc">Working answer, for SBC to confirm.</span></p>'
            '<p class="cv-fine">Officers: <span class="rw-ph">[roles and qualifications]</span></p>'
            '<p class="cv-fine">Software prepares the file. Only an SBC officer decides.<br>Data held to UAE and Saudi data protection law.</p></div>'
            '<div class="rw-pair"><div class="rw-off">' + seal + '<b>Officer 1</b>Reviews all five checks</div><span class="rw-plus" aria-hidden="true">+</span>'
            '<div class="rw-off">' + seal + '<b>Officer 2</b>Reviews them again, separately</div><span class="rw-plus" aria-hidden="true">=</span>' + mark + '</div></div></section>')


def outcomes():
    return ('<section class="sec cv-sec" aria-label="The decision">' +
            '<div class="rw-wrap"><div class="rw-head by-head"><h2>Pass or fall short, you know where you stand.</h2></div>'
            '<div class="rw-fork">'
            '<div class="rw-out rw-short"><span class="rw-tag">If you fall short</span><h3>You are Conditionally Qualified.</h3><ul>'
            '<li><i></i><span>You get an action plan listing exactly what to fix. SBC approves it.</span></li>'
            '<li><i></i><span>Nothing reaches a buyer. You are not introduced until you are SBC-Qualified.</span></li>'
            '<li><i></i><span>Resubmit within <span class="rw-ph">[re-check window]</span>. <span class="rw-ph">[Resubmission fee terms]</span></span></li>'
            '<li><i></i><span>Falling short is not shared with anyone.</span></li></ul></div>'
            '<div class="rw-out rw-pass"><span class="rw-tag">If you pass</span><h3>You are SBC-Qualified for 12 months.</h3><ul>'
            '<li><i></i><span>SBC introduces you when a buyer&#39;s need fits.</span></li>'
            '<li><i></i><span>Each introduction is approved by SBC on its own.</span></li>'
            '<li><i></i><span>Passing is not a licence or a promised contract.</span></li></ul></div>'
            '</div></div></section>')


def year():
    months = ''.join('<span style="--i:%d"></span>' % i for i in range(12)) + '<span class="re" style="--i:12">Re-check</span>'
    axis = ''.join('<span>%s</span>' % m for m in ['Pass'] + ['M%d' % i for i in range(2, 13)] + ['Year 2'])
    return ('<section class="sec cv-sec rw-yr" aria-label="After you pass">' + bg('60%', '60%') +
            '<div class="rw-wrap"><div class="rw-head by-head"><h2>Twelve months, then a re-check.</h2><p>The mark stays valid for a year. Then SBC checks your file again so it never goes stale.</p></div>'
            '<div class="rw-year" role="img" aria-label="Pass after the AED 12,500 review, twelve months of validity, then a yearly AED 4,500 re-check"><div class="rw-fees" aria-hidden="true"><span><b>AED 12,500</b> review, once</span><span><b>AED 4,500</b> re-check, yearly</span></div><div class="rw-months">' + months + '</div><div class="rw-axis" aria-hidden="true">' + axis + '</div></div>'
            '<div class="rw-facts"><div><b>AED 4,500 a year</b><span>To stay qualified after the first year.</span><span class="rw-tbc">Working answer, for SBC to confirm.</span></div>'
            '<div><b>Screening, every month</b><span>Re-screened while you hold the mark. A sanctions match withdraws it at once.</span><span class="rw-tbc">Working answer, for SBC to confirm.</span></div>'
            '<div><b>Can be withdrawn</b><span>Also if <span class="rw-ph">[other withdrawal conditions]</span>.</span></div>'
            '<div><b>Buyers can confirm it</b><span>At <span class="rw-ph">[verification route]</span>.</span></div></div>'
            '<span class="rw-tbc">Underlined items in brackets are still being confirmed by SBC.</span></div></section>')


def end(sfx):
    return ('<section class="sec rw-end" id="start%s" aria-label="Start">' % sfx +
            '<div class="ap-photo" aria-hidden="true"><img class="kb-ap" src="/assets/img/f79104e9e1a1881a050247fd0ea926eb.webp" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"></div><div class="ap-shade" aria-hidden="true"></div>'
            '<div class="rw-end-in"><h2>Start with the checklist.</h2><p>Five minutes to register. The checklist arrives within 2 working days.</p><span class="rw-tbc" style="color:#A9AFBA">Working answer, for SBC to confirm.</span>'
            '<div class="rw-doors"><a class="a" href="/companies/apply/">Start your application</a><a class="b" href="/buyers/#talk">I&#39;m a buyer: post a need</a></div></div></section>')


SCRIPT = r'''<script>
(function(){
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
  if(reduce||!('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('js-play');
  var heads=document.querySelectorAll('.by-head');
  heads.forEach(function(el){el.classList.add('cvr')});
  var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add(en.target.classList.contains('by-head')?'in':'on');io.unobserve(en.target)}})},{threshold:.3});
  heads.forEach(function(el){io.observe(el)});
  document.querySelectorAll('.rw-two,.rw-yr').forEach(function(el){io.observe(el)});
})();
</script>
'''


def mode_copy(mode):
    sfx = '' if mode == 'day' else '-n'
    open_div, hd, ft = chrome(mode)
    body = hero().replace('href="#checks"', 'href="#checks%s"' % sfx) + checks(sfx) + officers() + outcomes() + year() + end(sfx)
    return open_div + hd + body + ft + '</div></div>'


site_open = SRC[SRC.find('<body>'):SRC.find('<div class="mode-day">')]
html = head + CSS + '</head>\n' + site_open + mode_copy('day') + mode_copy('night') + '</div>\n</div>\n' + SCRIPT + '</body>\n</html>\n'
open('review/index.html', 'w', encoding='utf-8').write(html)
print('review/index.html', len(html), 'bytes')
