// Hub · service worker mínimo: só torna o app instalável. Nada é guardado em cache
// (as plataformas, principalmente o áudio do Play Passei, nunca passam por aqui).
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => {});
