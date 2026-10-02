/* Service worker de la Videoteca · Arduino en el aula.
   Ámbito: la carpeta de esta app (scope './'). No interfiere con otras
   aplicaciones del mismo dominio porque solo controla las páginas bajo
   este directorio. */
const CACHE = 'videoteca-arduino-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './favicon.svg',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/apple-touch-icon.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE && k.startsWith('videoteca-arduino-')).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;

  // Navegaciones y recursos propios: red primero con respaldo en caché (offline).
  if (sameOrigin || req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() =>
          caches.match(req, { ignoreSearch: true }).then((hit) => hit || caches.match('./index.html'))
        )
    );
    return;
  }

  // Recursos de terceros (fuentes, vídeos…): no se cachean aquí; se sirve
  // la caché del navegador o la red directamente.
});
