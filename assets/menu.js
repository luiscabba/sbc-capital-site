/* Phone menu (below 901px): builds a full-screen sheet from each page's own header,
   once per mode copy, so links, the current page and the page action never drift.
   Header row: mark, the page action (Apply or Talk to SBC), a labelled Menu button. */
(function () {
  var root = document.documentElement;
  var HINT = {
    '/': 'What SBC does, in one minute',
    '/companies/': 'Get reviewed and introduced',
    '/buyers/': 'Meet approved suppliers, free',
    '/review/': 'The five checks and who signs'
  };
  var ICON = '<span class="hm-ic" aria-hidden="true"><i></i><i></i></span>';
  var sheets = [];
  var lastBtn = null;

  function build(hd, n) {
    var wrap = hd.closest('.mode-day, .mode-night');
    var mode = wrap && wrap.classList.contains('mode-night') ? 'night' : 'day';
    var act = hd.querySelector('.hd-act');
    var cta = act && act.querySelector('a.btn');
    var logo = hd.querySelector('a[aria-label="SBC Capital home"]');
    var links = hd.querySelectorAll('.hd-nav a');
    var modeGroup = act && act.querySelector('[role="group"]');
    var ar = act && act.querySelector('.ar-soon');
    var id = 'hm-sheet-' + mode + n;

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'hd-menu';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', id);
    btn.innerHTML = ICON + '<span>Menu</span>';
    btn.addEventListener('click', function () { open(btn); });
    act.appendChild(btn);

    var sh = document.createElement('div');
    sh.className = 'hm-sheet hm-' + mode;
    sh.id = id;
    sh.setAttribute('role', 'dialog');
    sh.setAttribute('aria-modal', 'true');
    sh.setAttribute('aria-label', 'Menu');

    var bar = document.createElement('div');
    bar.className = 'hm-bar';
    if (logo) { var l = logo.cloneNode(true); l.className = 'hm-logo'; l.removeAttribute('style'); bar.appendChild(l); }
    var right = document.createElement('div');
    right.className = 'hm-r';
    if (cta) { var c = cta.cloneNode(true); c.className = 'hm-act'; c.removeAttribute('style'); right.appendChild(c); }
    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'hd-menu hm-close';
    close.setAttribute('aria-label', 'Close menu');
    close.innerHTML = '<span class="hm-ic x" aria-hidden="true"><i></i><i></i></span><span>Close</span>';
    close.addEventListener('click', shut);
    right.appendChild(close);
    bar.appendChild(right);
    sh.appendChild(bar);

    var nav = document.createElement('nav');
    nav.className = 'hm-nav';
    nav.setAttribute('aria-label', 'Main');
    Array.prototype.forEach.call(links, function (a, i) {
      var r = document.createElement('a');
      r.href = a.getAttribute('href');
      r.style.setProperty('--d', (i * 45) + 'ms');
      if (a.getAttribute('aria-current')) r.setAttribute('aria-current', 'page');
      var hint = HINT[a.getAttribute('href')] || '';
      r.innerHTML = '<span><b></b>' + (hint ? '<small></small>' : '') + '</span><span class="hm-arr" aria-hidden="true">&rarr;</span>';
      r.querySelector('b').textContent = a.textContent.trim();
      if (hint) r.querySelector('small').textContent = hint;
      nav.appendChild(r);
    });
    sh.appendChild(nav);

    var foot = document.createElement('div');
    foot.className = 'hm-foot';
    if (cta) { var big = cta.cloneNode(true); big.className = 'hm-cta'; big.removeAttribute('style'); foot.appendChild(big); }
    var row = document.createElement('div');
    row.className = 'hm-row';
    if (modeGroup) {
      var g = modeGroup.cloneNode(true); g.removeAttribute('style'); g.className = 'hm-mode';
      Array.prototype.forEach.call(g.querySelectorAll('button'), function (b) { b.removeAttribute('style'); });
      row.appendChild(g);
    }
    if (ar) { var a2 = ar.cloneNode(true); a2.removeAttribute('style'); a2.className = 'hm-ar'; row.appendChild(a2); }
    foot.appendChild(row);
    sh.appendChild(foot);

    // any link in the sheet (including #talk on this page) closes it first
    sh.addEventListener('click', function (e) { if (e.target.closest('a')) shut(); });
    document.body.appendChild(sh);
    sheets.push(sh);
  }

  function visibleSheet() {
    var m = root.getAttribute('data-mode') || 'day';
    for (var i = 0; i < sheets.length; i++) if (sheets[i].classList.contains('hm-' + m)) return sheets[i];
    return sheets[0];
  }
  function open(btn) {
    lastBtn = btn;
    root.classList.add('hm-open');
    document.querySelectorAll('.hd .hd-menu').forEach(function (b) { b.setAttribute('aria-expanded', 'true'); });
    var s = visibleSheet();
    var f = s && s.querySelector('.hm-close');
    if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 30);
  }
  function shut() {
    if (!root.classList.contains('hm-open')) return;
    root.classList.remove('hm-open');
    document.querySelectorAll('.hd .hd-menu').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    var m = root.getAttribute('data-mode') || 'day';
    var back = document.querySelector('.mode-' + m + ' .hd .hd-menu') || lastBtn;
    if (back && back.offsetParent) back.focus({ preventScroll: true });
  }

  function init() {
    document.querySelectorAll('.hd').forEach(build);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') shut();
      if (e.key === 'Tab' && root.classList.contains('hm-open')) {
        var s = visibleSheet(); if (!s) return;
        var f = s.querySelectorAll('a[href], button');
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
        else if (!s.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
      }
    });
    var mq = window.matchMedia('(min-width: 901px)');
    var onWide = function () { if (mq.matches) shut(); };
    if (mq.addEventListener) mq.addEventListener('change', onWide); else if (mq.addListener) mq.addListener(onWide);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
