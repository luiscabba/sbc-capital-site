"""Builds the interim Contact, Privacy and Terms of the SBC-Qualified mark pages.

Each is a reading page with its own shape: Contact is a set of ways in, Privacy a plain notice,
the mark terms a means / does-not-mean split plus the rules. Facts SBC has not given are [bracketed].
Head, header and footer come from companies/index.html. Run from the repo root:  python3 _build/info_pages.py
"""
import os
import re

SRC = open('companies/index.html', encoding='utf-8').read()


def page_head(title, desc):
    h = SRC[:SRC.find('</head>')]
    h = h.replace('<title>SBC Capital · For companies</title>', '<title>SBC Capital · %s</title>' % title)
    return re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % desc, h)


def chrome(mode):
    start = SRC.find('<div class="mode-%s">' % mode)
    hs = SRC.find('<header', start); he = SRC.find('</header>', hs) + 9
    fs = SRC.find('<footer', he); fe = SRC.find('</footer>', fs) + 9
    hd = SRC[hs:he].replace(' aria-current="page">For companies', '>For companies')
    hd = re.sub(r'(href="/companies/" style="[^"]*); font-weight: 600"', r'\1"', hd)
    return SRC[start:hs], hd, SRC[fs:fe]


def ph(t):
    return '<span class="ip-ph">[%s]</span>' % t


CSS = r'''<style>
.ip{max-width:1180px;margin:0 auto;padding:96px 72px 112px;box-sizing:border-box;display:flex;flex-direction:column;gap:56px}
.ip-top{display:flex;flex-direction:column;gap:18px;max-width:760px}
.ip-top h1{margin:0;font-weight:600;font-size:58px;line-height:1.04;letter-spacing:-.025em;text-wrap:balance}
.ip-top p{margin:0;font-size:19px;line-height:1.55;color:var(--cv-sub)}
.ip-note{font-size:14px;color:var(--cv-sub)}
.ip h2{margin:0;font-weight:600;font-size:24px;letter-spacing:-.01em}
.ip p,.ip li{font-size:16px;line-height:1.65}
.ip ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:10px}
.ip li{display:grid;grid-template-columns:14px 1fr;gap:12px}
.ip li::before{content:"";width:8px;height:8px;margin-top:9px;background:#1F4FD1}
/* contact: the ways in */
.ip-ways{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;border-top:2px solid var(--cv-ink)}
.ip-ways div{display:flex;flex-direction:column;gap:8px;padding:22px 24px 22px 0;border-right:1px solid var(--cv-line);margin-right:24px}
.ip-ways div:last-child{border-right:0;margin-right:0}
.ip-ways span{font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.06em;color:var(--cv-sub)}
.ip-ways b{font-weight:600;font-size:18px;line-height:1.4}
.ip-routes{display:flex;flex-direction:column}
.ip-routes a{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:22px 4px;border-top:1px solid var(--cv-line);color:var(--cv-ink);text-decoration:none;font-size:20px;transition:background-color .2s ease,padding .25s ease}
.ip-routes a:last-child{border-bottom:1px solid var(--cv-line)}
.ip-routes a span{font-size:15px;color:var(--cv-sub)}
.ip-routes a b{font-weight:600}
.ip-routes a:hover{background:var(--cv-soft);padding-left:14px}
.ip-routes i{font-style:normal;color:var(--cv-acc);font-size:22px;transition:transform .2s ease}
.ip-routes a:hover i{transform:translateX(6px)}
/* privacy: a plain notice with its contents beside it */
.ip-read{display:grid;grid-template-columns:220px minmax(0,680px);gap:64px;align-items:start}
.ip-toc{position:sticky;top:24px;display:flex;flex-direction:column;gap:2px;border-left:2px solid var(--cv-line)}
.ip-toc a{padding:7px 14px;font-size:14px;color:var(--cv-sub);text-decoration:none;margin-left:-2px;border-left:2px solid transparent;transition:color .2s ease,border-color .2s ease}
.ip-toc a:hover{color:var(--cv-ink);border-left-color:#1F4FD1}
.ip-body{display:flex;flex-direction:column;gap:40px}
.ip-body section{display:flex;flex-direction:column;gap:12px;scroll-margin-top:24px}
.ip-body p{margin:0}
/* mark terms: means / does not mean */
.ip-split{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.ip-split>div{padding:32px;display:flex;flex-direction:column;gap:18px}
.ip-yes{background:var(--cv-card);border:1px solid #1F4FD1;box-shadow:0 30px 60px rgba(31,79,209,.14)}
.ip-no{background:var(--cv-soft);border:1px solid var(--cv-line)}
.ip-no li::before{background:transparent;border:1.5px solid var(--cv-ink);box-sizing:border-box}
.ip-head{display:flex;align-items:center;gap:14px}
.ip-head svg{width:40px;height:40px;flex:none;color:var(--cv-ink)}
.ip-head svg .lit{fill:#1F4FD1}
.ip-rules{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px}
.ip-rules>div{display:flex;flex-direction:column;gap:10px;padding-top:16px;border-top:2px solid var(--cv-ink)}
.ip-rules p{margin:0;color:var(--cv-sub)}
.ip-rules b{color:var(--cv-ink)}
@media (max-width:1100px){.ip{padding:80px 32px 96px}.ip-read{grid-template-columns:1fr;gap:28px}.ip-toc{position:static;flex-direction:row;flex-wrap:wrap;border-left:0;gap:4px 16px}.ip-toc a{padding:4px 0;border:0;margin:0}}
@media (max-width:900px){
  .ip{padding:48px 20px 72px;gap:40px}
  .ip-top h1{font-size:38px}
  .ip-ways{grid-template-columns:1fr 1fr}
  .ip-ways div:first-child{grid-column:1/-1}
  .ip-toc{gap:0 20px}
  .ip-toc a{display:inline-flex;align-items:center;min-height:44px;padding:0}
  .ip-ways div{border-right:0;margin-right:0;padding:18px 12px 18px 0;border-bottom:1px solid var(--cv-line)}
  .ip-routes a{font-size:17px;flex-wrap:wrap}
  .ip-split,.ip-rules{grid-template-columns:1fr}
  .ip-split>div{padding:24px}
}
</style>
'''

QM = '<svg viewBox="0 0 100 100" aria-hidden="true"><rect x="6" y="6" width="88" height="88" fill="none" stroke="currentColor" stroke-width="7"></rect><rect class="lit" x="62" y="10" width="28" height="28"></rect></svg>'
FOOT = '<span class="ip-note">Underlined items in brackets are still being confirmed by SBC.</span>'


def contact(sfx):
    return ('<main class="ip">'
            '<div class="ip-top"><h1>Talk to SBC Capital.</h1><p>One team answers companies and buyers. We reply within %s.</p></div>' % ph('response time') +
            '<div class="ip-ways">'
            '<div><span>Office</span><b>Meydan Grandstand<br>Dubai, United Arab Emirates</b>%s</div>' % ph('floor and unit') +
            '<div><span>Email</span><b>%s</b></div>' % ph('email address') +
            '<div><span>Phone</span><b>%s</b></div>' % ph('phone number') +
            '<div><span>Hours</span><b>%s</b>Gulf Standard Time</div></div>' % ph('working hours') +
            '<div class="ip-routes" aria-label="Where to go next">'
            '<a href="/companies/apply/"><span><b>An international company?</b><br>Register for the SBC review.</span><i aria-hidden="true">&#8594;</i></a>'
            '<a href="/buyers/#talk%s"><span><b>A Gulf buyer?</b><br>Post a need. It costs you nothing.</span><i aria-hidden="true">&#8594;</i></a>' % sfx +
            '<a href="/mark-terms/"><span><b>Checking the SBC-Qualified mark?</b><br>Read what it means and how to confirm it.</span><i aria-hidden="true">&#8594;</i></a></div>'
            + FOOT + '</main>')


PRIV = [
    ('collect', 'What we collect', [
        'From companies: your registration answers and the documents for the five checks (ownership, sanctions details, licences, agent agreement, ICV certificate).',
        'From buyers: the need you post and the contact details you give us.',
        'From visitors: %s. The site remembers your day or night choice in your own browser only.' % ph('analytics, if any')]),
    ('why', 'Why we use it', [
        'To run the review, to make introductions SBC has approved, and to contact you about them. We do not sell it.']),
    ('who', 'Who sees it', [
        'The SBC officers who review your file.',
        'A buyer sees a company&#39;s pack only after SBC approves that introduction.',
        'Our service providers: %s.' % ph('hosting and processors')]),
    ('long', 'How long we keep it', ['%s.' % ph('Retention period and basis')]),
    ('rights', 'Your rights', [
        'Ask us to show, correct or delete what we hold about you at %s.' % ph('privacy email'),
        'This notice follows %s.' % ph('governing data protection law')]),
]


def privacy(sfx):
    toc = ''.join('<a href="#%s%s">%s</a>' % (k, sfx, t) for k, t, _ in PRIV)
    body = ''.join('<section id="%s%s" aria-label="%s"><h2>%s</h2><ul>%s</ul></section>' % (k, sfx, t, t, ''.join('<li><span>%s</span></li>' % x for x in xs)) for k, t, xs in PRIV)
    return ('<main class="ip">'
            '<div class="ip-top"><h1>Privacy.</h1><p>How SBC Capital handles what you share with us. This is an interim notice; the full policy is being finalised. Last updated %s.</p></div>' % ph('date') +
            '<div class="ip-read"><nav class="ip-toc" aria-label="On this page">' + toc + '</nav><div class="ip-body">' + body + FOOT + '</div></div></main>')


def terms(sfx):
    yes = ''.join('<li><span>%s</span></li>' % x for x in [
        'The company passed all five checks: ownership to the final owner, sanctions, licences and certificates, local agent, and ICV (In-Country Value) certificate.',
        'Two SBC officers reviewed the file separately and both approved it.',
        'It is valid for 12 months from the date of passing.',
        'Sanctions are re-screened every month while the mark is held (working answer, for SBC to confirm).'])
    no = ''.join('<li><span>%s</span></li>' % x for x in [
        'A government licence, registration or approval.',
        'A promised contract, tender award or introduction.',
        'That SBC acts as the company&#39;s agent. SBC refers companies to checked local agents.',
        'A judgement on the quality of the company&#39;s work %s.' % ph('to confirm')])
    return ('<main class="ip">'
            '<div class="ip-top"><h1>Terms of the <span style="white-space:nowrap">SBC-Qualified</span> mark.</h1><p>What the mark means, what it does not, and how it stays honest. Interim terms; the binding version follows %s.</p></div>' % ph('date') +
            '<div class="ip-split"><div class="ip-yes"><div class="ip-head">' + QM + '<h2>It means</h2></div><ul>' + yes + '</ul></div>'
            '<div class="ip-no"><div class="ip-head"><h2>It does not mean</h2></div><ul>' + no + '</ul></div></div>'
            '<div class="ip-rules">'
            '<div><h2>Using the mark</h2><p>Only while it is valid, and only as %s.</p></div>' % ph('display rules: where, how, minimum size') +
            '<div><h2>Re-check and withdrawal</h2><p><b>AED 4,500 a year</b> to re-check after the first year. Withdrawn at once on a sanctions match, and also if %s. Appeals: %s.</p></div>' % (ph('other withdrawal conditions'), ph('appeal route')) +
            '<div><h2>Confirming a company</h2><p>Buyers can confirm a company&#39;s status at %s.</p></div></div>' % ph('verification route') +
            FOOT + '</main>')


PAGES = [('contact', 'Contact', 'How to reach SBC Capital in Dubai, for international companies and Gulf buyers.', contact),
         ('privacy', 'Privacy', 'How SBC Capital handles what companies and buyers share with it.', privacy),
         ('mark-terms', 'Terms of the SBC-Qualified mark', 'What the SBC-Qualified mark means, what it does not, and how it is re-checked and withdrawn.', terms)]

site_open = SRC[SRC.find('<body>'):SRC.find('<div class="mode-day">')]
for slug, title, desc, fn in PAGES:
    copies = ''
    for mode in ('day', 'night'):
        sfx = '' if mode == 'day' else '-n'
        o, hd, ft = chrome(mode)
        copies += o + hd + '<div class="cv-sec" style="flex:1">' + fn(sfx) + '</div>' + ft + '</div></div>'
    html = page_head(title, desc) + CSS + '</head>\n' + site_open + copies + '</div>\n</div>\n</body>\n</html>\n'
    os.makedirs(slug, exist_ok=True)
    open(slug + '/index.html', 'w', encoding='utf-8').write(html)
    print(slug, len(html))
