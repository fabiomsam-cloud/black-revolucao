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
  var LIVE_AT = new Date("2026-11-10T20:00:00-03:00").getTime();
  var qs = new URLSearchParams(location.search);

  /* ---------- atribuição (mesmo padrão do gerador de páginas: scvp_attr, 30 dias) ---------- */
  var ATTR_KEY = "scvp_attr", ATTR_TTL = 30 * 24 * 3600 * 1000;
  var ATTR_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid"];
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

  /* ---------- pixel ---------- */
  function loadPixel() {
    if (!PIXEL || window.fbq) return;
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", String(PIXEL));
    window.fbq("track", "PageView");
  }
  loadPixel();

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
      var nome = form.nome.value.trim(), email = form.email.value.trim().toLowerCase();
      var digits = form.telefone.value.replace(/\D/g, ""), esc = form.escolaridade.value;
      var ok = true;
      setErr("nome", nome.length < 2); ok = ok && nome.length >= 2;
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); setErr("email", !emailOk); ok = ok && emailOk;
      var telOk = digits.length === 11 && digits[2] === "9"; setErr("telefone", !telOk); ok = ok && telOk;
      setErr("escolaridade", !esc); ok = ok && !!esc;
      if (!ok) return;
      var utm = {};
      ["utm_source", "utm_medium", "utm_campaign", "utm_term"].forEach(function (k) { if (attr[k]) utm[k] = attr[k]; });
      utm.utm_content = attr.utm_content || VERSAO;
      var payload = {
        op: "lead", slug: SLUG, nome: nome, email: email, telefone: digits,
        escolaridade: "", answers: { escolaridade: esc }, utm: utm,
        fbclid: attr.fbclid || qs.get("fbclid") || null, fbclid_ts: attr.ts || Date.now(),
        fbp: cookie("_fbp"), fbc: cookie("_fbc"), page_url: location.href
      };
      var btn = form.querySelector("button[type=submit]"), label = btn.innerHTML;
      btn.disabled = true; btn.innerHTML = "ENVIANDO…";
      form.querySelector(".form-error").classList.remove("show");
      fetch(API, { method: "POST", headers: HEADERS, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { if (!r.ok) throw new Error(d.error || "erro de conexão"); return d; }); })
        .then(function (r) {
          try { if (r.pixel && window.fbq) window.fbq("track", "Lead", {}, { eventID: r.pixel.event_id }); } catch (_) {}
          var dest = r.redirect_url || r.redirect_url_desq || CFG.grupo;
          try { sessionStorage.setItem("black_reg", JSON.stringify({ id: r.registro_id, dest: dest, q: r.qualified })); } catch (_) {}
          var u = new URL(CFG.obrigado || "../obrigado/", location.href);
          u.searchParams.set("reg", r.registro_id || "");
          u.searchParams.set("v", VERSAO);
          location.href = u.toString();
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
