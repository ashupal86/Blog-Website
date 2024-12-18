const CACHE_NAME = 'tech-blog-cache-v1';
const CACHE_URLS = [
    '/',
    '/index.html',
    '/styles.css',
    '/scripts.js',
    '/offline.html',
];

// Install Event: Cache the files
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Opened cache');
            return cache.addAll(CACHE_URLS);
        })
    );
});

// Activate Event: Remove outdated caches
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch Event: Serve cached files when offline
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }

            return fetch(event.request).catch(() => {
                // If the network is unavailable, show the offline page
                if (event.request.url.endsWith('.html')) {
                    return caches.match('/offline.html');
                }
            });
        })
    );
});
