/* ==========================================================================
   Working Process — cumulative sequential reveal: circle 1 lights up and
   stays lit, then line 1, then circle 2 (still keeping 1 + line 1 lit),
   and so on until everything is lit. Holds briefly, then resets
   everything to normal and restarts from step 1, forever.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
  var track = document.querySelector(".process-track");
  if (!track) return;

  var svg = track.querySelector(".process-track__lines");
  var steps = Array.prototype.slice.call(track.querySelectorAll(".process-step"));

  function drawLines() {
    svg.innerHTML = "";
    var trackRect = track.getBoundingClientRect();

    for (var i = 0; i < steps.length - 1; i++) {
      var circleA = steps[i].querySelector(".process-step__circle");
      var circleB = steps[i + 1].querySelector(".process-step__circle");
      var rectA = circleA.getBoundingClientRect();
      var rectB = circleB.getBoundingClientRect();

      var x1 = rectA.left + rectA.width / 2 - trackRect.left;
      var y1 = rectA.top + rectA.height / 2 - trackRect.top;
      var x2 = rectB.left + rectB.width / 2 - trackRect.left;
      var y2 = rectB.top + rectB.height / 2 - trackRect.top;

      var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", x1);
      line.setAttribute("y1", y1);
      line.setAttribute("x2", x2);
      line.setAttribute("y2", y2);
      line.classList.add("process-line");
      svg.appendChild(line);
    }
  }

  drawLines();
  window.addEventListener("resize", drawLines);

  var stepDelay = 1300;   // slow pace between each new activation
  var holdAtEnd = 1800;   // pause once everything is lit
  var started = false;

  function resetAll() {
    steps.forEach(function (s) { s.classList.remove("is-active"); });
    svg.querySelectorAll(".process-line").forEach(function (l) {
      l.classList.remove("is-active");
    });
  }

  function runLoop() {
    var lines = Array.prototype.slice.call(svg.querySelectorAll(".process-line"));

    // Build the cumulative sequence: circle1, line1, circle2, line2, ... circleN
    var sequence = [];
    for (var i = 0; i < steps.length; i++) {
      sequence.push(steps[i]);
      if (lines[i]) sequence.push(lines[i]);
    }

    var index = 0;

    function activateNext() {
      if (index >= sequence.length) {
        setTimeout(function () {
          resetAll();
          index = 0;
          activateNext();
        }, holdAtEnd);
        return;
      }

      sequence[index].classList.add("is-active");
      index++;
      setTimeout(activateNext, stepDelay);
    }

    activateNext();
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

  observer.observe(track);
});