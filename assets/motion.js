/* Scroll motion for the SBC Capital home page.
   Each section gets its scroll progress as CSS variables; the stylesheet does the moving.
   Skipped entirely when the visitor has turned off motion. */
(function () {
  var root = document.documentElement;
  var reduce = false;
  try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  if (reduce) return;

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  // Phones and touch screens get the light version: no per-frame scroll work.
  // Each section plays its motion once, as cheap transitions, when it comes into view (assets/motion-lite.css).
  var lite = false;
  try { lite = window.matchMedia('(max-width: 900px), (hover: none)').matches; } catch (e) {}
  if (lite) {
    root.classList.add('js-reveal');
    ready(function () {
      var reveal = document.querySelectorAll('.how-h2, .mark-badge, .mark-panel > div');
      for (var j = 0; j < reveal.length; j++) reveal[j].classList.add('rv');
      var secs = document.querySelectorAll('.sec');
      if (!('IntersectionObserver' in window)) {
        for (var a = 0; a < reveal.length; a++) reveal[a].classList.add('in');
        for (var b = 0; b < secs.length; b++) secs[b].classList.add('on');
        return;
      }
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add(en.target.classList.contains('sec') ? 'on' : 'in'); io.unobserve(en.target); }
        });
      }, { threshold: 0.2 });
      for (var k = 0; k < reveal.length; k++) io.observe(reveal[k]);
      for (var s = 0; s < secs.length; s++) io.observe(secs[s]);
    });
    return;
  }
  root.classList.add('js-scroll');

  ready(function () {
    // Hero: every block of the floating wall gets its own lift, so the wall comes apart as you scroll.
    var blocks = document.querySelectorAll('.hero-wall .rise-cube');
    for (var i = 0; i < blocks.length; i++) {
      var lit = blocks[i].parentNode.classList.contains('litcell');
      var d = lit ? 300 : 40 + ((i * 37) % 9) * 22;
      blocks[i].style.setProperty('--d', d);
    }

    // Reveals: headline panels, the mark badge and the card rise in once as they come into view.
    var reveal = document.querySelectorAll('.how-h2, .mark-badge, .mark-panel > div');
    for (var j = 0; j < reveal.length; j++) reveal[j].classList.add('rv');
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
        });
      }, { threshold: 0.2 });
      for (var k = 0; k < reveal.length; k++) io.observe(reveal[k]);
    } else {
      for (var m = 0; m < reveal.length; m++) reveal[m].classList.add('in');
    }

    var secs = document.querySelectorAll('.sec');
    var ticking = false;
    function update() {
      ticking = false;
      var vh = window.innerHeight;
      for (var n = 0; n < secs.length; n++) {
        var s = secs[n];
        if (s.offsetParent === null) continue; // the hidden day or night copy
        var r = s.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) continue;
        var p = clamp((vh - r.top) / (vh + r.height));
        s.style.setProperty('--p', p.toFixed(4));
        var label = s.getAttribute('aria-label');
        if (label === 'Hero') {
          s.style.setProperty('--sp', clamp(-r.top / r.height).toFixed(4));
        } else if (label === 'How it works') {
          // the block crosses the platforms as the section scrolls through the middle of the screen
          var hp = clamp((p - 0.22) / 0.42);
          s.style.setProperty('--hp', hp.toFixed(4));
          var rows = s.querySelectorAll('.how-side .row, .how-side .rowd'); // .rowd: the night copy's rows
          var marks = [0, 0.36, 0.7];
          for (var q = 0; q < rows.length; q++) rows[q].classList.toggle('lit', hp >= marks[q]);
        } else if (label === 'The mark') {
          s.style.setProperty('--mp', clamp((p - 0.18) / 0.42).toFixed(4));
        }
      }
    }
    function onScroll() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    // the day and night copies swap when the mode changes; recompute for the one now showing
    new MutationObserver(onScroll).observe(root, { attributes: true, attributeFilter: ['data-mode'] });
    update();
  });
})();
