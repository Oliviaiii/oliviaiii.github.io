// Minimal progressive enhancement. The site is fully usable without JS.
(function () {
  var y = document.getElementById('year');
  if (y) y.textContent = String(new Date().getFullYear());

  // Highlight in-page nav links while scrolling (index page only).
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  if (!links.length || !('IntersectionObserver' in window)) return;
  var targets = links.map(function (a) { return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id); });
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  targets.forEach(function (t) { io.observe(t); });
})();
