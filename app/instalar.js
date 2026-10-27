// Hub · folha "Instale o app" (27/10/2026) — compartilhada por /app, /dominei e /clube do revolucaodoestudo.com.br.
// Instala UM app só (o do hub, manifesto /app/manifest.webmanifest) a partir de qualquer uma das três telas.
// O navegador não instala sozinho: exige um toque da pessoa. Então a folha insiste em todo acesso pelo celular
// até o app estar instalado (aberto pelo ícone = tela "standalone" = a folha nunca aparece).
// Conferir sem celular: ?instalar=android|ios|navegador (&nav=chrome|firefox|edge|opera no iPhone).
(function () {
  if (window.__pwaFolha) return; window.__pwaFolha = true;
  var H = location.hostname;
  if (H !== 'revolucaodoestudo.com.br' && H !== 'localhost' && H !== '127.0.0.1') return; // fora do domínio do hub não há app do hub para instalar
  var UA = navigator.userAgent, q = new URLSearchParams(location.search), debug = q.get('instalar') || '';
  var standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  var ios = /iPhone|iPad|iPod/.test(UA) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var inApp = /Instagram|FBAN|FBAV|FB_IAB|Line\//i.test(UA);
  var mobile = ios || /Android/i.test(UA);
  var navIos = q.get('nav') || (/CriOS/.test(UA) ? 'chrome' : /FxiOS/.test(UA) ? 'firefox' : /EdgiOS/.test(UA) ? 'edge' : /OPiOS|OPT\//.test(UA) ? 'opera' : 'safari');
  var ONDE = { safari: 'na barra de baixo do Safari', chrome: 'no canto da barra de endereço do Chrome', firefox: 'no menu ≡ do Firefox', edge: 'no menu ⋯ do Edge', opera: 'no menu do Opera' };
  var head = document.head;
  function tag(nome, attrs) { var el = document.createElement(nome); for (var k in attrs) el.setAttribute(k, attrs[k]); head.appendChild(el); return el; }
  // 1) fora do /app, a página passa a "ser" o app do hub: manifesto, ícone e metas do /app (senão o Chrome instalaria um app por plataforma)
  if (location.pathname.indexOf('/app') !== 0) {
    Array.prototype.forEach.call(document.querySelectorAll('link[rel="manifest"], link[rel="apple-touch-icon"]'), function (l) { l.parentNode.removeChild(l); });
    tag('link', { rel: 'manifest', href: '/app/manifest.webmanifest' });
    tag('link', { rel: 'apple-touch-icon', href: '/app/img/apple-touch-icon.png' });
    if (!document.querySelector('meta[name="apple-mobile-web-app-capable"]')) tag('meta', { name: 'apple-mobile-web-app-capable', content: 'yes' });
    if (!document.querySelector('meta[name="mobile-web-app-capable"]')) tag('meta', { name: 'mobile-web-app-capable', content: 'yes' });
    if (!document.querySelector('meta[name="apple-mobile-web-app-title"]')) tag('meta', { name: 'apple-mobile-web-app-title', content: 'Revolução' });
  }
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('/app/sw.js', { scope: '/app/' }).catch(function () {});
  if (!debug && (standalone || !mobile)) return;
  // 2) a folha
  var CSS = '.pwa{position:fixed;inset:0;z-index:2147483000;background:rgba(7,8,11,.78);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);display:flex;align-items:flex-end;justify-content:center;font-family:Figtree,Atkinson Hyperlegible,Manrope,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#f4f5f7;-webkit-font-smoothing:antialiased}' +
    '.pwa[hidden],.pwa-box [hidden]{display:none!important}' +
    '.pwa-box{width:100%;max-width:520px;background:#0f1217;border:1px solid #1f2530;border-radius:26px 26px 0 0;padding:24px 20px calc(22px + env(safe-area-inset-bottom));text-align:center;animation:pwaUp .35s cubic-bezier(.2,.9,.3,1) both;box-sizing:border-box}' +
    '@media(min-width:640px){.pwa{align-items:center;padding:16px}.pwa-box{border-radius:26px;padding-bottom:22px}}' +
    '@keyframes pwaUp{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}' +
    '.pwa-box img{width:64px;height:64px;border-radius:16px;margin:0 auto 10px;display:block;box-shadow:0 8px 28px rgba(0,196,234,.25)}' +
    '.pwa-t{font-family:Saira,inherit;font-weight:700;font-size:1.25rem;line-height:1.25}' +
    '.pwa-s{color:#8b919b;font-size:.95rem;margin:6px 0 14px;line-height:1.45}' +
    '.pwa-btn{display:block;width:100%;margin-top:4px;background:linear-gradient(180deg,#00c4ea,#009BBE);color:#001820;border:0;border-radius:999px;padding:15px 18px;font:inherit;font-weight:700;font-size:1.02rem;cursor:pointer;box-shadow:0 8px 28px rgba(0,196,234,.28)}' +
    '.pwa-ios{text-align:left;margin:0;padding:0 0 0 22px;color:#c8ccd3;font-size:.95rem;line-height:1.5}.pwa-ios li{margin:6px 0}.pwa-ios b{color:#f4f5f7}' +
    '.pwa-ios svg{width:18px;height:18px;vertical-align:-3px;color:#00c4ea}' +
    '.pwa-nav{color:#c8ccd3;font-size:.95rem;line-height:1.5;margin:0}' +
    '.pwa-alt{color:#8b919b;font-size:.88rem;line-height:1.5;margin:12px 0 0}.pwa-alt b{color:#c8ccd3}.pwa-alt button{background:none;border:0;color:#00c4ea;font:inherit;text-decoration:underline;text-underline-offset:3px;cursor:pointer;padding:0}' +
    '.pwa-skip{display:block;margin:16px auto 0;background:none;border:0;color:#8b919b;font:inherit;font-size:.86rem;text-decoration:underline;text-underline-offset:3px;cursor:pointer}' +
    'body.pwa-on{overflow:hidden}';
  var HTML = '<div class="pwa-box" role="dialog" aria-labelledby="pwaT">' +
    '<img src="/app/img/icon-192.png" alt="" width="64" height="64">' +
    '<div class="pwa-t" id="pwaT">Instale o app no seu celular</div>' +
    '<p class="pwa-s" id="pwaS">Abre com um toque, sem digitar endereço, com suas plataformas juntas.</p>' +
    '<button class="pwa-btn" id="pwaBtn" type="button" hidden>Instalar o app</button>' +
    '<ol class="pwa-ios" id="pwaIos" hidden>' +
    '<li>Toque em <b>Compartilhar</b> <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 12v7a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-7"/></svg> <span id="pwaOnde"></span></li>' +
    '<li>Role a lista e toque em <b>Adicionar à Tela de Início</b></li>' +
    '<li>Toque em <b>Adicionar</b>. O ícone fica junto dos seus apps.</li></ol>' +
    '<p class="pwa-alt" id="pwaAlt" hidden>Não achou? Abra este endereço no <b>Safari</b> e instale por lá: <button type="button" id="pwaCopiar">copiar o link</button></p>' +
    '<p class="pwa-nav" id="pwaNav" hidden>Este navegador não instala apps. Toque nos três pontos (ou em <b>⋯</b>) e escolha <b>Abrir no navegador</b>. Lá, instale pelo botão.</p>' +
    '<button class="pwa-skip" id="pwaSkip" type="button">Continuar no navegador por agora</button></div>';
  var evt = null, box = null;
  function $(id) { return document.getElementById(id); }
  function montar() {
    if (box) return box;
    var st = document.createElement('style'); st.textContent = CSS; head.appendChild(st);
    box = document.createElement('div'); box.className = 'pwa'; box.id = 'pwa'; box.hidden = true; box.innerHTML = HTML; document.body.appendChild(box);
    $('pwaBtn').onclick = function () { if (!evt) return; evt.prompt(); evt.userChoice.then(function (r) { evt = null; if (!r || r.outcome !== 'accepted') esconder(); }, function () { evt = null; esconder(); }); };
    $('pwaSkip').onclick = function () { try { sessionStorage.setItem('pwa-depois', '1'); } catch (e) {} esconder(); };
    $('pwaCopiar').onclick = function () { var url = location.origin + '/app/'; var b = $('pwaCopiar');
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { b.textContent = 'link copiado ✓'; }, function () { prompt('Copie o endereço:', url); }); else prompt('Copie o endereço:', url); };
    return box;
  }
  function mostrar(modo) {
    var run = function () { montar();
      $('pwaBtn').hidden = modo !== 'android'; $('pwaIos').hidden = modo !== 'ios'; $('pwaNav').hidden = modo !== 'navegador';
      $('pwaOnde').textContent = ONDE[navIos] || ONDE.safari; $('pwaAlt').hidden = !(modo === 'ios' && navIos !== 'safari');
      $('pwaS').textContent = modo === 'navegador' ? 'Para instalar, abra esta página no navegador do celular.' : 'Abre com um toque, sem digitar endereço, com suas plataformas juntas.';
      box.hidden = false; document.body.classList.add('pwa-on'); };
    if (document.body) run(); else document.addEventListener('DOMContentLoaded', run);
  }
  function esconder() { if (box) { box.hidden = true; } document.body.classList.remove('pwa-on'); }
  function decidir() {
    if (debug) return mostrar(debug);
    try { if (sessionStorage.getItem('pwa-depois')) return; } catch (e) {}
    if (inApp) return mostrar('navegador');
    if (ios) return mostrar('ios');
    if (evt) return mostrar('android'); // Android: só quando o Chrome avisa que dá para instalar (já instalado = não avisa)
  }
  window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); evt = e; decidir(); });
  window.addEventListener('appinstalled', function () { evt = null; esconder(); });
  decidir();
})();
