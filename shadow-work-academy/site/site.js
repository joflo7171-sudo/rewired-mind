// Presentation only: header shadow on scroll and gentle reveal. No network, storage, or tracking.
(function () {
  var h = document.querySelector('header.site');
  function onScroll() { if (h) h.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els = document.querySelectorAll('.card,.mod,.shot,.struggles li,.steps li,details.faq,.pricebox,.inc li,.notice');
  function revealAll() { Array.prototype.forEach.call(document.querySelectorAll('.reveal'), function (e) { e.classList.add('in'); }); }
  window.addEventListener('beforeprint', revealAll);
  if (reduce || !('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  Array.prototype.forEach.call(els, function (el, i) {
    var r = el.getBoundingClientRect();
    if (r.top < window.innerHeight) { el.classList.add('reveal', 'in'); return; } // already visible: never hide
    el.style.setProperty('--d', (i % 3) * 0.07 + 's'); el.classList.add('reveal'); io.observe(el);
  });
})();
