/* BLACK · A Revolução do Estudo — JS compartilhado (captação v1/v2 + obrigado) */
(function () {
  "use strict";
  var CFG = window.BLACK_CFG || {};
  var API = "https://dqpxugdhlgafvddavzzp.supabase.co/functions/v1/gerador-paginas";
  var ANON = CFG.anon || "";
  var HEADERS = { "Content-Type": "application/json", "Authorization": "Bearer " + ANON, "apikey": ANON };
  var SLUG = CFG.slug || "black-revolucao-nao-alunos";
  var PIXEL = CFG.pixel || "";
  var VERSAO = CFG.versao || "";
  var LIVE_AT = new Date(CFG.live || "2026-11-10T20:00:00-03:00").getTime();   /* 18/10: alunos = 27/10 */
  var qs = new URLSearchParams(location.search);

  /* ---------- atribuição (mesmo padrão do gerador de páginas: scvp_attr, 30 dias) ---------- */
  var ATTR_KEY = "scvp_attr", ATTR_TTL = 30 * 24 * 3600 * 1000;
  var ATTR_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid", "gbraid", "wbraid"];   /* 18/10: ids de clique do Google p/ conversão offline (EntrouGrupo) */
  function loadAttr() {
    var fromUrl = {}, stored = null;
    ATTR_KEYS.forEach(function (k) { if (qs.get(k)) fromUrl[k] = qs.get(k); });
    try {
      var s = JSON.parse(localStorage.getItem(ATTR_KEY) || "null");
      if (s && s.ts && Date.now() - s.ts < ATTR_TTL) stored = s;
    } catch (_) {}
    if (Object.keys(fromUrl).length) {
      stored = Object.assign({}, fromUrl, { ts: Date.now() });
      try { localStorage.setItem(ATTR_KEY, JSON.stringify(stored)); } catch (_) {}
    }
    return stored || {};
  }
  function cookie(name) {
    var m = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
    return m ? decodeURIComponent(m[1]) : null;
  }
  var attr = loadAttr();
  /* 18/10: página com UTM padrão (ex.: /bio) — vale só quando a URL não trouxe nenhuma UTM */
  if (CFG.utm && !attr.utm_source && !attr.utm_campaign) attr = Object.assign({}, CFG.utm, attr);

  /* ---------- pixel ---------- */
  function loadPixel() {
    if (!PIXEL || window.fbq) return;
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", String(PIXEL));
    window.fbq("track", "PageView");
  }
  // pixel na 1ª interação (toque, clique, roda do mouse, tecla — "scroll" não: dispara sozinho na restauração de rolagem) ou 3 s após o load, o que vier antes: os ~260 KB do fbevents
  // ficam fora da janela do LCP no PageSpeed. PageView continua; o Lead chama loadPixel() antes de disparar.
  (function () {
    var evs = ["pointerdown", "touchstart", "wheel", "keydown"], done = false;
    function go() { if (done) return; done = true; evs.forEach(function (e) { window.removeEventListener(e, go, true); }); loadPixel(); loadGtag(); }
    evs.forEach(function (e) { window.addEventListener(e, go, { capture: true, passive: true, once: true }); });
    function arm() { setTimeout(go, 3000); }
    if (document.readyState === "complete") arm(); else window.addEventListener("load", arm);
  })();

  /* ---------- Google Ads (18/10): gtag carrega junto com o pixel (fora da janela do LCP); conversão no Lead ---------- */
  var GADS = CFG.gads || null;
  function loadGtag() {
    if (!GADS || window.gtag) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GADS.id, { allow_enhanced_conversions: true });
    var t = document.createElement("script"); t.async = true; t.src = "https://www.googletagmanager.com/gtag/js?id=" + GADS.id;
    document.head.appendChild(t);
  }
  // espera a tag do Google confirmar (ou 1,2 s) antes de sair da página — senão o redirect corta o envio
  function gadsLead(qualificado, regId, email, digits, done) {
    if (!GADS) return done();
    var fired = false; function go() { if (!fired) { fired = true; done(); } }
    try {
      loadGtag();
      window.gtag("set", "user_data", { email: email, phone_number: "+55" + digits });
      window.gtag("event", "conversion", { send_to: qualificado ? GADS.sup : GADS.med, value: qualificado ? 30 : 10, currency: "BRL",
        transaction_id: regId || undefined, event_callback: go });
    } catch (_) {}
    setTimeout(go, 1200);
  }

  /* ---------- contador ---------- */
  function pad(n) { return String(n).padStart(2, "0"); }
  function tick() {
    var els = document.querySelectorAll("[data-cd]");
    if (!els.length) return;
    var diff = Math.max(0, LIVE_AT - Date.now());
    var d = Math.floor(diff / 86400000), h = Math.floor(diff / 3600000) % 24, m = Math.floor(diff / 60000) % 60, s = Math.floor(diff / 1000) % 60;
    var v = { d: pad(d), h: pad(h), m: pad(m), s: pad(s) };
    els.forEach(function (el) { var k = el.getAttribute("data-cd"); if (el.textContent !== v[k]) el.textContent = v[k]; });
  }
  tick(); setInterval(tick, 1000);

  /* ---------- reveal ---------- */
  var rv = document.querySelectorAll(".rv");
  // o hero está sempre acima da dobra: entra já, com o escalonamento do --d, sem depender do observer
  document.querySelectorAll(".hero .rv, .thanks .rv").forEach(function (el) { requestAnimationFrame(function () { el.classList.add("in"); }); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px", threshold: .08 });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add("in"); }); }
  // rede de segurança: navegador embutido (Instagram/Facebook) ou aba em segundo plano às vezes não entrega o observer → nada pode ficar invisível
  setTimeout(function () { rv.forEach(function (el) { el.classList.add("in"); }); }, 2500);

  /* ---------- scroll para o formulário ---------- */
  document.querySelectorAll("[data-goto-form]").forEach(function (a) {
    a.addEventListener("click", function (ev) {
      var f = document.getElementById("form");
      if (!f) return;
      ev.preventDefault();
      f.scrollIntoView({ behavior: "smooth", block: "center" });
      setTimeout(function () { var i = f.querySelector("input"); if (i) i.focus({ preventScroll: true }); }, 500);
    });
  });

  /* ---------- vídeo em loop no topo (/bio): só depois do load + folga, nunca com economia de dados ou "reduzir movimento" ---------- */
  var hv = document.querySelector(".hero-video video");
  if (hv) {
    var saveData = navigator.connection && navigator.connection.saveData;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!saveData && !reduce) {
      var startVideo = function () {
        var src = hv.canPlayType("video/webm") ? hv.getAttribute("data-webm") : hv.getAttribute("data-mp4");
        hv.src = src;
        hv.addEventListener("playing", function () { hv.parentNode.classList.add("on"); }, { once: true });
        hv.play().catch(function () {});
      };
      var kick = function () { setTimeout(startVideo, 1200); };
      if (document.readyState === "complete") kick(); else window.addEventListener("load", kick, { once: true });
    }
  }

  /* ---------- formulário ---------- */
  var form = document.getElementById("form");
  if (form) {
    var sel = form.querySelector("select[name=escolaridade]");
    if (sel) sel.addEventListener("change", function () { sel.classList.toggle("placeholder", !sel.value); });
    var tel = form.querySelector("[name=telefone]");
    tel.addEventListener("input", function () {
      var d = tel.value.replace(/\D/g, "").slice(0, 11), out = "";
      if (d.length > 0) out = "(" + d.slice(0, 2);
      if (d.length >= 3) out += ") " + d.slice(2, 7);
      if (d.length >= 8) out += "-" + d.slice(7);
      tel.value = out;
    });
    function setErr(name, on) {
      var f = form.querySelector("[name=" + name + "]").closest(".field");
      if (f) f.classList.toggle("err", !!on);
    }
    function showErr(msg) {
      var e = form.querySelector(".form-error");
      e.textContent = msg; e.classList.add("show");
    }
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var email = form.email.value.trim().toLowerCase();
      // o motor exige nome: deriva da parte local do e-mail ("maria.silva" → "Maria Silva"); a Anne pega o nome real depois
      var nome = (email.split("@")[0] || "").replace(/[0-9]+/g, " ").replace(/[._\-+]+/g, " ").trim()
        .split(/\s+/).filter(Boolean).map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); }).join(" ").slice(0, 60);
      if (nome.length < 2) nome = "Concurseiro(a)";
      var digits = form.telefone.value.replace(/\D/g, ""), esc = form.escolaridade ? form.escolaridade.value : "";   /* 18/10: página de alunos não tem escolaridade */
      var ok = true;
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); setErr("email", !emailOk); ok = ok && emailOk;
      var telOk = digits.length === 11 && digits[2] === "9"; setErr("telefone", !telOk); ok = ok && telOk;
      if (form.escolaridade) { setErr("escolaridade", !esc); ok = ok && !!esc; }
      if (!ok) return;
      var utm = {};
      ["utm_source", "utm_medium", "utm_campaign", "utm_term"].forEach(function (k) { if (attr[k]) utm[k] = attr[k]; });
      utm.utm_content = attr.utm_content || VERSAO;
      var payload = {
        op: "lead", slug: SLUG, nome: nome, email: email, telefone: digits,
        escolaridade: "", answers: Object.assign(esc ? { escolaridade: esc, versao: VERSAO } : { versao: VERSAO },
          attr.gclid ? { gclid: attr.gclid } : {}, attr.gbraid ? { gbraid: attr.gbraid } : {}, attr.wbraid ? { wbraid: attr.wbraid } : {}), utm: utm,   /* 18/10: versão da página sempre gravada (utm_content passa a ser o criativo) */
        fbclid: attr.fbclid || qs.get("fbclid") || null, fbclid_ts: attr.ts || Date.now(),
        fbp: cookie("_fbp"), fbc: cookie("_fbc"), page_url: location.href
      };
      var btn = form.querySelector("button[type=submit]"), label = btn.innerHTML;
      btn.disabled = true; btn.innerHTML = "ENVIANDO…";
      form.querySelector(".form-error").classList.remove("show");
      fetch(API, { method: "POST", headers: HEADERS, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { if (!r.ok) throw new Error(d.error || "erro de conexão"); return d; }); })
        .then(function (r) {
          try { loadPixel(); if (r.pixel && window.fbq) window.fbq("track", "Lead", { escolaridade: esc, qualificado: r.qualified ? "sim" : "nao" }, { eventID: r.pixel.event_id }); } catch (_) {}   /* 18/10: Lead p/ todo cadastro (edge lead_todos); escolaridade vai como parâmetro p/ conversão personalizada */
          var dest = r.redirect_url || r.redirect_url_desq || CFG.grupo;
          try { sessionStorage.setItem("black_reg", JSON.stringify({ id: r.registro_id, dest: dest, q: r.qualified })); } catch (_) {}
          var u = new URL(CFG.obrigado || "../obrigado/", location.href);
          u.searchParams.set("reg", r.registro_id || "");
          u.searchParams.set("v", VERSAO);
          gadsLead(!!r.qualified, r.registro_id, email, digits, function () { location.href = u.toString(); });
        })
        .catch(function (e) {
          btn.disabled = false; btn.innerHTML = label;
          showErr(e.message === "whatsapp inválido — use DDD + número" ? "Confira o WhatsApp: DDD + número com 9 dígitos." : "Não conseguimos enviar agora. Tente de novo em instantes.");
        });
    });
  }

  /* ---------- obrigado ---------- */
  var thanks = document.querySelector(".thanks");
  if (thanks) {
    var reg = qs.get("reg") || "";
    var saved = null; try { saved = JSON.parse(sessionStorage.getItem("black_reg") || "null"); } catch (_) {}
    var dest = (saved && saved.dest) || CFG.grupo;
    var bar = thanks.querySelector(".bar i"), pct = thanks.querySelector(".bar b");
    setTimeout(function () { if (bar) bar.style.width = "84%"; }, 250);
    if (pct) { var n = 0, iv = setInterval(function () { n += 3; if (n >= 84) { n = 84; clearInterval(iv); } pct.textContent = n + "%"; }, 60); }
    thanks.querySelectorAll("[data-grupo]").forEach(function (a) {
      a.href = dest;
      a.addEventListener("click", function () {
        var id = reg || (saved && saved.id);
        if (!id) return;
        try { fetch(API, { method: "POST", headers: HEADERS, body: JSON.stringify({ op: "grupo_click", registro_id: id, modo: "obrigado" }), keepalive: true }).catch(function () {}); } catch (_) {}
      });
    });
  }
})();
