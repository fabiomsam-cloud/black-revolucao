/* "Aether Flow" atrás do hero — porte em JS puro do "Aether Flow Hero" (21st.dev, dhileepkumargm), adaptado:
   canvas do tamanho do hero (não da janela), DPR, fundo transparente (a textura metálica fica por baixo), paleta da Black,
   o cursor/toque empurra as partículas (redemoinho) e, sem cursor, um ponto automático passeia para o éter nunca ficar parado;
   pausa com aba escondida / fora da tela; prefers-reduced-motion = quadro estático. */
(function () {
  "use strict";
  var canvas = document.querySelector("canvas.aether");
  if (!canvas) return;
  var host = canvas.parentElement;
  var ctx = canvas.getContext("2d");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var mobile = window.matchMedia && window.matchMedia("(max-width: 959px)").matches;

  var CFG = {
    density: mobile ? 9000 : 9500,     // px² por partícula (original: 9000)
    cap: mobile ? 60 : 150,
    link: mobile ? 110 : 150,           // distância máxima de ligação (px CSS)
    reach: mobile ? 120 : 200,          // raio de influência do cursor (original: 200)
    push: mobile ? 2.2 : 4.5,           // força de repulsão (original: 5)
    drift: 0.22,                        // velocidade das partículas (original: ±0.2)
    dot: [150, 222, 240],               // partículas: ciano claro
    line: [0, 170, 210],                // ligações: azul da marca
    hot: [255, 255, 255]                // ligações perto do cursor: branco
  };

  var W = 0, H = 0, dpr = 1, parts = [];
  var pointer = { x: -9999, y: -9999, t: 0 };
  var running = false, raf = 0, t0 = performance.now();

  function size() {
    var r = host.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height));
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    canvas.style.width = W + "px"; canvas.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function seed() {
    parts = [];
    var n = Math.min(CFG.cap, Math.round((W * H) / CFG.density));
    for (var i = 0; i < n; i++) {
      var s = Math.random() * 1.6 + 0.9;
      parts.push({ x: s * 2 + Math.random() * (W - s * 4), y: s * 2 + Math.random() * (H - s * 4),
        vx: (Math.random() - 0.5) * CFG.drift * 2, vy: (Math.random() - 0.5) * CFG.drift * 2, s: s });
    }
  }
  function rgba(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a.toFixed(3) + ")"; }

  function frame(now) {
    if (!running) return;
    var dt = Math.min(2, (now - (frame.last || now)) / 16.7); frame.last = now;
    ctx.clearRect(0, 0, W, H);

    // cursor real recente ou passeio automático (celular / ninguém mexendo)
    var ex, ey, autoMode = false;
    if (now - pointer.t < 2500) { ex = pointer.x; ey = pointer.y; }
    else {
      autoMode = true; var s = (now - t0) / 1000;
      ex = W * (0.5 + 0.38 * Math.sin(s * 0.19) * Math.cos(s * 0.06));
      ey = H * (0.5 + 0.36 * Math.sin(s * 0.14 + 0.9));
    }
    var reach = CFG.reach, push = autoMode ? CFG.push * 0.45 : CFG.push;
    var L = CFG.link, L2 = L * L, i, j, p, q;

    for (i = 0; i < parts.length; i++) {
      p = parts[i];
      if (p.x > W || p.x < 0) p.vx = -p.vx;
      if (p.y > H || p.y < 0) p.vy = -p.vy;
      var dx = ex - p.x, dy = ey - p.y, d = Math.hypot(dx, dy);
      if (d < reach + p.s && d > 0.001) {           // repulsão = o "redemoinho no éter"
        var f = (reach - d) / reach;
        p.x -= (dx / d) * f * push * dt; p.y -= (dy / d) * f * push * dt;
      }
      p.x += p.vx * dt; p.y += p.vy * dt;
    }
    // ligações
    ctx.lineWidth = 1;
    for (i = 0; i < parts.length; i++) {
      p = parts[i];
      var nearA = Math.hypot(p.x - ex, p.y - ey) < reach;
      for (j = i + 1; j < parts.length; j++) {
        q = parts[j];
        var ddx = p.x - q.x, ddy = p.y - q.y, d2 = ddx * ddx + ddy * ddy;
        if (d2 < L2) {
          var a = (1 - d2 / L2) * 0.55;
          ctx.strokeStyle = nearA && !autoMode ? rgba(CFG.hot, a) : rgba(CFG.line, a);
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
        }
      }
    }
    // partículas
    for (i = 0; i < parts.length; i++) {
      p = parts[i];
      ctx.beginPath(); ctx.arc(p.x, p.y, p.s, 0, Math.PI * 2); ctx.fillStyle = rgba(CFG.dot, 0.85); ctx.fill();
    }
    raf = requestAnimationFrame(frame);
  }

  function start() { if (running || reduce) return; running = true; frame.last = 0; raf = requestAnimationFrame(frame); }
  function stop() { running = false; cancelAnimationFrame(raf); }
  function toLocal(cx, cy) { var r = host.getBoundingClientRect(); pointer.x = cx - r.left; pointer.y = cy - r.top; pointer.t = performance.now(); }
  window.addEventListener("mousemove", function (e) { toLocal(e.clientX, e.clientY); }, { passive: true });
  window.addEventListener("mouseout", function () { pointer.t = 0; }, { passive: true });
  window.addEventListener("touchstart", function (e) { var t = e.touches && e.touches[0]; if (t) toLocal(t.clientX, t.clientY); }, { passive: true });
  window.addEventListener("touchmove", function (e) { var t = e.touches && e.touches[0]; if (t) toLocal(t.clientX, t.clientY); }, { passive: true });
  var rsz; window.addEventListener("resize", function () { clearTimeout(rsz); rsz = setTimeout(function () { size(); seed(); }, 150); });
  document.addEventListener("visibilitychange", function () { document.hidden ? stop() : start(); });
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? start() : stop(); }); }, { threshold: 0.02 }).observe(host);
  }

  size(); seed();
  if (reduce) { running = true; frame(performance.now()); running = false; cancelAnimationFrame(raf); } else start();
})();
