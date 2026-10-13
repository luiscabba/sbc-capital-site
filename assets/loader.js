/* SBC Capital site loader (variation D, "The wall is built").
   Loaded in <head> right after the Day/Night script, so it knows the mode before first paint.
   Plays once per visit (sessionStorage), and never for visitors who turn off motion. */
(function () {
  var root = document.documentElement;
  var reduce = false;
  try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  var seen = false;
  try { seen = sessionStorage.getItem('sbc-loaded') === '1'; } catch (e) {}
  if (reduce || seen || !Element.prototype.animate) return;
  try { sessionStorage.setItem('sbc-loaded', '1'); } catch (e) {}

  // Cover the page from the first paint, in the right colour for the mode.
  root.classList.add('sbc-loading');
  var css = document.createElement('style');
  css.textContent =
    'html.sbc-loading::after{content:"";position:fixed;inset:0;z-index:9998;background:#FFFFFF}' +
    'html.sbc-loading[data-mode="night"]::after{background:#1A1D24}' +
    '.sbc-loader{position:fixed;inset:0;z-index:9999;pointer-events:none}' +
    '.sbc-loader svg{display:block;width:100%;height:100%}';
  document.head.appendChild(css);

  // Safety net: never leave the page covered.
  var bail = setTimeout(function () { root.classList.remove('sbc-loading'); }, 4000);

  var NS = 'http://www.w3.org/2000/svg';
  var PAL = {
    day: { tops: ['#F7F9FE', '#EEF3FD', '#FAFBFF'], l: ['#DCE4F8', '#D3DDF6', '#E1E8F9'], r: ['#B8C7EE', '#AEBFEA', '#BFCDF0'],
      acc: ['#C4D2F3', '#9EB2E6', '#7893DA'], cob: ['#3D6BF0', '#1F4FD1', '#173A9C'], bg: '#FFFFFF' },
    night: { tops: ['#2E3A5A', '#2A3653', '#323F63'], l: ['#222B44', '#1F283F', '#252E49'], r: ['#171D2F', '#151A2B', '#1A2034'],
      acc: ['#3E5288', '#4A5E99', '#33456F'], cob: ['#5B82FF', '#2F5EEA', '#1B43B8'], bg: '#1A1D24' }
  };
  var GAP = 60, HOLD = 320, SIZE = 52, DROP = 420, RISE = 480;

  function cube(parent, cx, cy, s, cols) {
    var dx = s * 0.866, g = document.createElementNS(NS, 'g');
    var faces = [
      [cx, cy - s, cx + dx, cy - s / 2, cx, cy, cx - dx, cy - s / 2],
      [cx - dx, cy - s / 2, cx, cy, cx, cy + s, cx - dx, cy + s / 2],
      [cx, cy, cx + dx, cy - s / 2, cx + dx, cy + s / 2, cx, cy + s]
    ];
    for (var i = 0; i < 3; i++) {
      var pg = document.createElementNS(NS, 'polygon');
      pg.setAttribute('points', faces[i].join(' '));
      pg.setAttribute('fill', cols[i]); pg.setAttribute('stroke', cols[i]); pg.setAttribute('stroke-width', '.6');
      g.appendChild(pg);
    }
    parent.appendChild(g);
    return g;
  }

  function play() {
    var p = PAL[root.getAttribute('data-mode') === 'night' ? 'night' : 'day'];
    var W = window.innerWidth, H = window.innerHeight;
    var box = document.createElement('div'); box.className = 'sbc-loader'; box.setAttribute('aria-hidden', 'true');
    var svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    var bg = document.createElementNS(NS, 'rect'); bg.setAttribute('width', W); bg.setAttribute('height', H); bg.setAttribute('fill', p.bg);
    svg.appendChild(bg);
    var wall = document.createElementNS(NS, 'g'); svg.appendChild(wall);
    box.appendChild(svg); document.body.appendChild(box);
    // The overlay now covers the page, so the first-paint cover can go.
    root.classList.remove('sbc-loading'); clearTimeout(bail);

    // The same compact wall as the hero: 5 rows of 6, corners missing, one pass block.
    var R = 5, C = 6, holes = { '0,0': 1, '5,0': 1, '0,4': 1, '5,4': 1, '5,2': 1, '4,1': 1 },
      accs = { '1,1': 1, '3,0': 1, '4,3': 1, '0,2': 1, '2,3': 1 }, LIT = '3,1';
    var s = Math.min(W, H) * SIZE / 1100, dx = s * 0.866;
    var ww = (2 * C + 1) * dx, hh = (R - 1) * 1.5 * s + 2 * s;
    var ox = (W - ww) / 2 + dx, oy = (H - hh) / 2 + s, order = [];
    for (var r = R - 1; r >= 0; r--) for (var c = 0; c < C; c++) { if (!holes[c + ',' + r]) order.push([c, r]); }

    var lit = null, t = 0;
    order.forEach(function (cr, i) {
      var c = cr[0], r = cr[1], key = c + ',' + r, k = (c + 2 * r) % 3;
      var cx = ox + c * 2 * dx + (r % 2 ? dx : 0), cy = oy + r * 1.5 * s;
      var cols = accs[key] ? [p.acc[k], p.acc[(k + 1) % 3], p.acc[(k + 2) % 3]] : [p.tops[k], p.l[k], p.r[k]];
      var g = cube(wall, cx, cy, s, cols);
      if (key === LIT) lit = g;
      g.animate([{ transform: 'translateY(' + (-s * 2.2) + 'px)', opacity: 0 }, { transform: 'translateY(0)', opacity: 1 }],
        { duration: DROP, delay: i * GAP, easing: 'cubic-bezier(.25,.9,.3,1.15)', fill: 'both' });
      t = i * GAP + DROP;
    });

    // The pass lights last and comes to the front so nothing covers it as it rises.
    setTimeout(function () {
      if (!lit) return;
      var ps = lit.querySelectorAll('polygon');
      for (var i = 0; i < 3; i++) { ps[i].setAttribute('fill', p.cob[i]); ps[i].setAttribute('stroke', p.cob[i]); }
      wall.appendChild(lit);
      lit.getAnimations().forEach(function (a) { a.cancel(); });
      lit.animate([{ transform: 'translateY(0)' }, { transform: 'translateY(' + (-s * 0.7) + 'px)' }],
        { duration: RISE, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'forwards' });
    }, t);

    // The wall keeps floating through the hold, then lifts away while the page shows underneath.
    var out = t + RISE + HOLD;
    wall.animate([{ transform: 'translateY(0)' }, { transform: 'translateY(' + (-s * 0.25) + 'px)' }, { transform: 'translateY(0)' }],
      { duration: RISE + HOLD, delay: t, easing: 'ease-in-out' });
    wall.animate([{ transform: 'translateY(0)', opacity: 1 }, { transform: 'translateY(' + (-s * 2.2) + 'px)', opacity: 0 }],
      { duration: 700, delay: out, easing: 'cubic-bezier(.45,0,.2,1)', fill: 'forwards' });
    bg.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 620, delay: out + 160, easing: 'ease-out', fill: 'both' });
    setTimeout(function () { if (box.parentNode) box.parentNode.removeChild(box); }, out + 160 + 620 + 60);
  }

  if (document.readyState !== 'loading') play();
  else document.addEventListener('DOMContentLoaded', play);
})();
