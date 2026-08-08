/* Service worker di Giovi Yoga: rete prima, cache come riserva.
   Dopo la prima visita l'app funziona anche offline; quando c'è rete
   la cache viene rinfrescata ad ogni richiesta, quindi gli
   aggiornamenti pubblicati arrivano da soli. */
const CACHE = 'giovi-yoga';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './icona-180.png', './icona-192.png', './icona-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then(r => {
        const copy = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return r;
      })
      .catch(() =>
        caches.match(e.request, { ignoreSearch: true })
          .then(r => r || caches.match('./index.html'))
      )
  );
});
