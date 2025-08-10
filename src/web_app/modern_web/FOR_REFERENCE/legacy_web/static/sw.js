// Service Worker for TKA Legacy Web App
// This will dramatically improve caching and loading performance

const CACHE_NAME = 'tka-legacy-v1';
const ASSET_CACHE = 'tka-assets-v1';

// Critical assets to cache immediately
const CRITICAL_ASSETS = [
  '/',
  '/app.css',
  '/app.js',
  '/favicon.ico'
];

// Install: Cache critical assets
self.addEventListener('install', (event) => {
  console.log('🚀 Service Worker installing...');

  event.waitUntil(
    Promise.all([
      // Cache critical assets
      caches.open(CACHE_NAME).then(cache => {
        console.log('📦 Caching critical assets...');
        return cache.addAll(CRITICAL_ASSETS);
      }),

      // Skip waiting to activate immediately
      self.skipWaiting()
    ])
  );
});

// Activate: Clean up old caches
self.addEventListener('activate', (event) => {
  console.log('✅ Service Worker activated');

  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== CACHE_NAME && cacheName !== ASSET_CACHE) {
              console.log('🗑️ Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),

      // Take control of all pages
      self.clients.claim()
    ])
  );
});

// Fetch: Implement smart caching strategy
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle same-origin requests
  if (url.origin !== location.origin) {
    return;
  }

  // Handle different types of requests
  if (request.url.includes('/images/')) {
    // Images: Cache-first, fail if not found
    event.respondWith(handleImageRequest(request));
  } else if (request.url.includes('.js') || request.url.includes('.css')) {
    // Assets: Cache-first
    event.respondWith(handleAssetRequest(request));
  } else {
    // Pages: Network-first with cache fallback
    event.respondWith(handlePageRequest(request));
  }
});

// Handle image requests - no fallbacks, fail properly
async function handleImageRequest(request) {
  try {
    // Try cache first
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    // Try network
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      // Cache successful response
      const cache = await caches.open(ASSET_CACHE);
      cache.put(request, networkResponse.clone());
      return networkResponse;
    }

    // Network failed, let it fail properly
    console.log('🚨 Image request failed:', request.url, 'Status:', networkResponse.status);
    return networkResponse; // Return the actual error response

  } catch (error) {
    console.log('🚨 Image request failed:', request.url, error);
    throw error; // Let the error propagate properly
  }
}

// Handle asset requests (JS, CSS)
async function handleAssetRequest(request) {
  try {
    // Try cache first
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    // Try network
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      // Cache successful response
      const cache = await caches.open(ASSET_CACHE);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;

  } catch (error) {
    console.log('🚨 Asset request failed:', request.url, error);
    // Return cached version if available
    return caches.match(request);
  }
}

// Handle page requests
async function handlePageRequest(request) {
  try {
    // Try network first for pages
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      // Cache successful response
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;

  } catch (error) {
    console.log('🚨 Page request failed:', request.url, error);
    // Return cached version if available
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    // Return offline page if available
    return caches.match('/');
  }
}



// Listen for messages from the main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

console.log('🎯 TKA Service Worker loaded and ready!');
