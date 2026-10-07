/* Rede de sinapses atrás do hero — porte em JS puro do "Interactive Synapse Network" (21st.dev, dhileepkumargm), adaptado:
   canvas do tamanho do hero (não da janela), DPR, conexões recalculadas a cada quadro, excitação automática (celular não tem mouse),
   toque conta como cursor, pausa com aba escondida / fora da tela, respeita prefers-reduced-motion, paleta da Black (#009BBE / #00c4ea). */
(function () {
  "use strict";
  var canvas = document.querySelector("canvas.synapse");
  if (!canvas) return;
  var host = canvas.parentElement;
  var ctx = canvas.getContext("2d");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var mobile = window.matchMedia && window.matchMedia("(max-width: 959px)").matches;

  var CFG = {
    count: mobile ? 34 : 70,
    radius: mobile ? 125 : 170,          // distância máxima de conexão (px CSS)
    speed: mobile ? 0.22 : 0.3,
    node: [0, 196, 234],                 // --blue-2
    line: [0, 155, 190],                 // --blue
    pulseSpeed: 0.028
  };

  var W = 0, H = 0, dpr = 1, nodes = [], pulses = [];
  var pointer = { x: -9999, y: -9999, t: 0 };
  var auto = { x: 0, y: 0 };
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
    nodes = [];
    for (var i = 0; i < CFG.count; i++) {
      var a = Math.random() * Math.PI * 2;
      nodes.push({ x: Math.random() * W, y: Math.random() * H, vx: Math.cos(a) * CFG.speed, vy: Math.sin(a) * CFG.speed, r: Math.random() * 1.8 + (mobile ? 1.5 : 1.8), act: 0, links: [] });
    }
    pulses = [];
  }

  function rgba(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a.toFixed(3) + ")"; }

  function frame(now) {
    if (!running) return;
    var dt = Math.min(2, (now - (frame.last || now)) / 16.7); frame.last = now;
    ctx.clearRect(0, 0, W, H);

    // ponto de excitação: o cursor/toque recente ou, sem ele, um passeio lento pela área (para a rede viver sozinha)
    var ex, ey;
    if (now - pointer.t < 2500) { ex = pointer.x; ey = pointer.y; }
    else {
      var s = (now - t0) / 1000;
      auto.x = W * (0.5 + 0.36 * Math.sin(s * 0.21) * Math.cos(s * 0.07));
      auto.y = H * (0.5 + 0.34 * Math.sin(s * 0.17 + 1.3));
      ex = auto.x; ey = auto.y;
    }

    var R = CFG.radius, R2 = R * R, i, j, n, m;
    // movimento + ativação
    for (i = 0; i < nodes.length; i++) {
      n = nodes[i];
      n.x += n.vx * dt; n.y += n.vy * dt;
      if (n.x < 0 || n.x > W) n.vx *= -1;
      if (n.y < 0 || n.y > H) n.vy *= -1;
      var dx = n.x - ex, dy = n.y - ey, d = Math.hypot(dx, dy);
      var target = Math.max(0, 1 - d / (R * 0.9));
      n.act += (target - n.act) * 0.08 * dt;
      n.links.length = 0;
    }
    // conexões (recalculadas: os nós andam)
    for (i = 0; i < nodes.length; i++) {
      n = nodes[i];
      for (j = i + 1; j < nodes.length; j++) {
        m = nodes[j];
        var ddx = n.x - m.x, ddy = n.y - m.y, d2 = ddx * ddx + ddy * ddy;
        if (d2 < R2) {
          n.links.push(m); m.links.push(n);
          var near = 1 - Math.sqrt(d2) / R;
          var a = (0.09 + Math.max(n.act, m.act) * 0.4) * near;
          ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(m.x, m.y);
          ctx.strokeStyle = rgba(CFG.line, a); ctx.lineWidth = 1; ctx.stroke();
        }
      }
    }
    // pulsos: nó ativo dispara um sinal por uma conexão
    for (i = 0; i < nodes.length; i++) {
      n = nodes[i];
      if (n.act > 0.45 && n.links.length && Math.random() > 0.975 && pulses.length < 40) {
        pulses.push({ a: n, b: n.links[(Math.random() * n.links.length) | 0], p: 0 });
      }
    }
    for (i = pulses.length - 1; i >= 0; i--) {
      var p = pulses[i]; p.p += CFG.pulseSpeed * dt;
      if (p.p >= 1) { p.b.act = Math.min(1, p.b.act + 0.35); pulses.splice(i, 1); continue; }
      var px = p.a.x + (p.b.x - p.a.x) * p.p, py = p.a.y + (p.b.y - p.a.y) * p.p;
      ctx.beginPath(); ctx.arc(px, py, 2.2, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(255,255,255,0.95)"; ctx.shadowColor = rgba(CFG.node, 0.9); ctx.shadowBlur = 10; ctx.fill(); ctx.shadowBlur = 0;
    }
    // nós
    for (i = 0; i < nodes.length; i++) {
      n = nodes[i];
      var al = 0.38 + n.act * 0.62;
      if (n.act > 0.3) { ctx.beginPath(); ctx.arc(n.x, n.y, n.r + 6 * n.act, 0, Math.PI * 2); ctx.fillStyle = rgba(CFG.node, 0.12 * n.act); ctx.fill(); }
      ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2); ctx.fillStyle = rgba(CFG.node, al); ctx.fill();
    }
    raf = requestAnimationFrame(frame);
  }

  function start() { if (running || reduce) return; running = true; frame.last = 0; raf = requestAnimationFrame(frame); }
  function stop() { running = false; cancelAnimationFrame(raf); }

  function toLocal(cx, cy) { var r = host.getBoundingClientRect(); pointer.x = cx - r.left; pointer.y = cy - r.top; pointer.t = performance.now(); }
  window.addEventListener("mousemove", function (e) { toLocal(e.clientX, e.clientY); }, { passive: true });
  window.addEventListener("touchmove", function (e) { var t = e.touches && e.touches[0]; if (t) toLocal(t.clientX, t.clientY); }, { passive: true });
  window.addEventListener("touchstart", function (e) { var t = e.touches && e.touches[0]; if (t) toLocal(t.clientX, t.clientY); }, { passive: true });

  var rsz; window.addEventListener("resize", function () { clearTimeout(rsz); rsz = setTimeout(function () { size(); seed(); }, 150); });
  document.addEventListener("visibilitychange", function () { document.hidden ? stop() : start(); });
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? start() : stop(); }); }, { threshold: 0.02 }).observe(host);
  }

  size(); seed();
  if (reduce) { // quadro estático, sem animação
    running = true; frame(performance.now()); running = false; cancelAnimationFrame(raf);
  } else start();
})();
