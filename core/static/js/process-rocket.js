/* ==========================================================================
   Home page — crossfades through the process frame images in order,
   looping forever, once scrolled into view.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
  var frames = Array.prototype.slice.call(document.querySelectorAll(".home-process__frame"));
  if (!frames.length) return;

  var stack = document.querySelector(".home-process__stack");
  var frameHold = 1400;
  var started = false;

  function runLoop() {
    var index = 0;

    function next() {
      frames.forEach(function (f) { f.classList.remove("is-active"); });
      frames[index].classList.add("is-active");
      index = (index + 1) % frames.length;
      setTimeout(next, frameHold);
    }

    next();
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && !started) {
          started = true;
          runLoop();
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.3 }
  );

  if (stack) observer.observe(stack);
});