(function () {
  document.querySelectorAll('.sgr:not([data-ready])').forEach(function (root) {
    root.setAttribute('data-ready', '');
    var NS = 'http://www.w3.org/2000/svg';
    var $ = function (s) { return root.querySelector('[data-' + s + ']'); };
    var el = {
      src: $('src'), bin: $('bin'), fall: $('fall'), hose: $('hose'), car: $('car'), led: $('led'),
      up: $('up'), sh: $('sh'), fo: $('fo'), elb: $('el'), gr: $('gr'), held: $('held'),
      fl: $('fl'), fr: $('fr'), count: $('count'), hint: $('hint')
    };

    var DUR = 3200, L1 = 200, L2 = 185, SY = 226;
    var SRC = 230, BIN = 750, RAISED = 470, DROPY = 520, SRCY = 648, BINY = 638;
    var SDX = [0, -60, 60, -30, 30], SDY = [-4, 6, 6, 2, 2];
    var BDX = [0, -42, 42, -21, 21, -63, 63, 0], BDY = [0, 4, 4, -10, -10, 2, 2, -20];

    var autoSec = parseFloat(root.getAttribute('data-auto'));
    if (isNaN(autoSec)) autoSec = 3;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) autoSec = 0;

    function tok(x, y) {
      var t = document.createElementNS(NS, 'text');
      t.setAttribute('class', 'tok');
      t.setAttribute('transform', 'translate(' + x + ' ' + y + ')');
      t.textContent = '$';
      return t;
    }
    var srcToks = SDX.map(function (dx, i) { var t = tok(SRC + dx, SRCY + SDY[i]); el.src.appendChild(t); return t; });
    var binToks = BDX.map(function (dx, i) { var t = tok(BIN + dx, BINY + BDY[i]); t.setAttribute('opacity', '0'); el.bin.appendChild(t); return t; });

    var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
    var seg = function (x, a, b) { return clamp((x - a) / (b - a), 0, 1); };
    var ease = function (x) { return (1 - Math.cos(Math.PI * x)) / 2; };
    var lerp = function (a, b, x) { return a + (b - a) * x; };
    var f2 = function (v) { return v.toFixed(2); };

    var count = 0, start = null, queue = 0, lastEnd = null, visible = true;
    var paused = autoSec === 0, previousFrame = null;
    var pauseButton = root.parentElement.querySelector('[data-robot-pause]');
    function updatePause() {
      pauseButton.textContent = paused ? 'Play animation' : 'Pause animation';
      pauseButton.setAttribute('aria-pressed', String(paused));
    }
    updatePause();
    pauseButton.addEventListener('click', function () { paused = !paused; if (paused) { start = null; queue = 0; draw(0); } updatePause(); });

    function draw(t) {
      var k = count % 5, sx = SRC + SDX[k], low = SRCY + SDY[k] - 58, nx = SRC + SDX[(count + 1) % 5];
      var cx = sx, wy = RAISED, grip = 0, tilt = 0, x;
      if (t < 0.12) { wy = lerp(RAISED, low, ease(seg(t, 0, 0.12))); }
      else if (t < 0.18) { wy = low; grip = ease(seg(t, 0.12, 0.18)); }
      else if (t < 0.30) { wy = lerp(low, RAISED, ease(seg(t, 0.18, 0.30))); grip = 1; }
      else if (t < 0.60) { x = seg(t, 0.30, 0.60); cx = lerp(sx, BIN, ease(x)); grip = 1; tilt = 7 * Math.sin(2 * Math.PI * x); }
      else if (t < 0.68) { cx = BIN; wy = lerp(RAISED, DROPY, ease(seg(t, 0.60, 0.68))); grip = 1; }
      else if (t < 0.74) { cx = BIN; wy = DROPY; grip = 1 - ease(seg(t, 0.68, 0.74)); }
      else if (t < 0.80) { cx = BIN; wy = lerp(DROPY, RAISED, ease(seg(t, 0.74, 0.80))); }
      else { x = seg(t, 0.80, 1); cx = lerp(BIN, nx, ease(x)); tilt = -7 * Math.sin(2 * Math.PI * x); }

      var active = t > 0;
      var held = active && t >= 0.15 && t < 0.69;
      var falling = active && t >= 0.69 && t < 0.80;
      var delivered = count + (active && t >= 0.80 ? 1 : 0);

      // inverse kinematics: shoulder at (cx, SY), wrist at (cx, wy), elbow bends right
      var d = wy - SY;
      var th1 = Math.PI / 2 - Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
      var ex = cx + L1 * Math.cos(th1), ey = SY + L1 * Math.sin(th1);
      var th2 = Math.atan2(wy - ey, cx - ex);
      var deg = 180 / Math.PI;

      el.car.setAttribute('transform', 'translate(' + f2(cx) + ' 0)');
      el.sh.setAttribute('transform', 'translate(' + f2(cx) + ' ' + SY + ')');
      el.up.setAttribute('transform', 'translate(' + f2(cx) + ' ' + SY + ') rotate(' + f2(th1 * deg) + ')');
      el.elb.setAttribute('transform', 'translate(' + f2(ex) + ' ' + f2(ey) + ')');
      el.fo.setAttribute('transform', 'translate(' + f2(ex) + ' ' + f2(ey) + ') rotate(' + f2(th2 * deg) + ')');
      el.gr.setAttribute('transform', 'translate(' + f2(cx) + ' ' + f2(wy) + ') rotate(' + f2(tilt) + ')');
      var gap = lerp(34, 19, grip);
      el.fl.setAttribute('transform', 'translate(' + f2(-gap) + ' 0)');
      el.fr.setAttribute('transform', 'translate(' + f2(gap) + ' 0)');
      var hx = cx + 24, hy = 214;
      el.hose.setAttribute('d', 'M' + f2(hx) + ' ' + hy + ' Q' + f2((hx + ex) / 2 + 22) + ' ' + f2((hy + ey) / 2 + 30) + ' ' + f2(ex) + ' ' + f2(ey));
      el.led.setAttribute('fill', held ? '#3BE07A' : '#5A6472');
      el.held.setAttribute('opacity', held ? 1 : 0);

      var slot = Math.min(count, 7), ff = seg(t, 0.69, 0.80);
      el.fall.setAttribute('opacity', falling ? 1 : 0);
      el.fall.setAttribute('transform', 'translate(' + f2(lerp(BIN, BIN + BDX[slot], ff)) + ' ' + f2(lerp(DROPY + 58, BINY + BDY[slot], ff * ff)) + ') rotate(' + f2(ff * (BDX[slot] >= 0 ? 6 : -6)) + ')');

      var refill = !active || t < 0.15 ? 1 : (t < 0.80 ? 0 : seg(t, 0.85, 1));
      srcToks.forEach(function (s, i) { s.setAttribute('opacity', i === k ? f2(refill) : 1); });
      binToks.forEach(function (b, i) { b.setAttribute('opacity', i < delivered ? 1 : 0); });
      el.count.textContent = String(delivered % 1000).padStart(3, '0');
    }

    function tick(ts) {
      var delta = previousFrame === null ? 0 : ts - previousFrame;
      previousFrame = ts;
      if (document.hidden || !visible || (paused && queue === 0 && start === null)) {
        if (start !== null) start += delta;
        if (lastEnd !== null) lastEnd += delta;
        requestAnimationFrame(tick);
        return;
      }
      if (lastEnd === null) lastEnd = ts;
      if (start !== null) {
        if (ts - start >= DUR) {
          count++; lastEnd = ts;
          if (queue > 0) { queue--; start = ts; } else { start = null; }
        }
      } else if (queue > 0) {
        queue--; start = ts;
      } else if (!paused && autoSec > 0 && visible && ts - lastEnd >= autoSec * 1000) {
        start = ts;
      }
      if (start !== null || ts === lastEnd) draw(start === null ? 0 : Math.min(1, (ts - start) / DUR));
      requestAnimationFrame(tick);
    }

    root.querySelector('button').addEventListener('click', function () {
      queue = Math.min(3, queue + 1);
      el.hint.setAttribute('opacity', 0);
    });

    // only auto-run while the graphic is on screen
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; }).observe(root);
    }

    draw(0);
    requestAnimationFrame(tick);
  });
})();
