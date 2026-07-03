/* ==========================================================================
   Stat counter — animates numbers from 0 to their target once the stats
   section scrolls into view. Values like "24/7" that aren't a clean
   number just display as-is, no animation.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
  var counters = document.querySelectorAll("[data-count-target]");
  if (!counters.length) return;

  function animateCounter(el) {
    var raw = el.getAttribute("data-count-target").trim();
    var match = raw.match(/^(\d+)([+%]?)$/);

    if (!match) {
      // Not a clean number (e.g. "24/7") — just show it directly.
      el.textContent = raw;
      return;
    }

    var target = parseInt(match[1], 10);
    var suffix = match[2] || "";
    var duration = 1200;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var current = Math.floor(progress * target);
      el.textContent = current + suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target + suffix;
      }
    }

    requestAnimationFrame(step);
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.4 }
  );

  counters.forEach(function (el) {
    observer.observe(el);
  });
});