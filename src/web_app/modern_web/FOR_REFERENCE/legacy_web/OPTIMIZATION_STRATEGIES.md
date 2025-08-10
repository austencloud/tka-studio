# Caching and Optimization Strategies

## 🎯 Strategic Overview

Based on the performance analysis, here are specific, actionable strategies to improve the legacy web app's performance from 16 seconds to under 3 seconds load time.

## 🗄️ Caching Strategies

### 1. Service Worker Implementation (Priority 1)

Create a comprehensive service worker for aggressive caching:

```javascript
// src/service-worker.js
const CACHE_NAME = "tka-legacy-v1";
const CRITICAL_ASSETS = [
  "/",
  "/app.js",
  "/app.css",
  "/images/critical-icons.svg",
];

const ASSET_CACHE = "tka-assets-v1";
const API_CACHE = "tka-api-v1";

// Install: Cache critical assets immediately
self.addEventListener("install", (event) => {
  event.waitUntil(
    Promise.all([
      caches.open(CACHE_NAME).then((cache) => cache.addAll(CRITICAL_ASSETS)),
      self.skipWaiting(),
    ])
  );
});

// Fetch: Implement cache-first strategy for assets
self.addEventListener("fetch", (event) => {
  const { request } = event;

  // Cache-first for static assets
  if (request.url.includes("/images/") || request.url.includes(".svg")) {
    event.respondWith(
      caches.match(request).then((response) => {
        if (response) return response;

        return fetch(request)
          .then((fetchResponse) => {
            const responseClone = fetchResponse.clone();
            caches.open(ASSET_CACHE).then((cache) => {
              cache.put(request, responseClone);
            });
            return fetchResponse;
          })
          .catch((error) => {
            // Let asset loading fail properly - no fallbacks
            console.log("Asset failed to load:", request.url, error);
            throw error;
          });
      })
    );
  }
});
```

### 2. Browser Caching Headers

Configure server to send proper cache headers:

```nginx
# nginx.conf
location ~* \.(js|css|png|jpg|jpeg|gif|svg|woff|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Vary "Accept-Encoding";
}

location ~* \.(html)$ {
    expires 1h;
    add_header Cache-Control "public, must-revalidate";
}
```

### 3. Asset Versioning Strategy

```javascript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // Content-based hashing for cache busting
        assetFileNames: "assets/[name].[hash][extname]",
        chunkFileNames: "chunks/[name].[hash].js",
        entryFileNames: "entries/[name].[hash].js",
      },
    },
  },
});
```

## ⚡ Code Splitting Strategies

### 1. Route-Based Splitting

```javascript
// src/routes/+layout.svelte
import { onMount } from "svelte";

// Lazy load tab components
const loadTab = async (tabName) => {
  const modules = {
    write: () => import("./WriteTab.svelte"),
    generate: () => import("./GenerateTab.svelte"),
    construct: () => import("./ConstructTab.svelte"),
    browse: () => import("./BrowseTab.svelte"),
    learn: () => import("./LearnTab.svelte"),
  };

  return modules[tabName]?.();
};

// Preload next likely tab
const preloadTab = (tabName) => {
  loadTab(tabName).catch(() => {}); // Silent preload
};
```

### 2. Component-Level Splitting

```javascript
// src/lib/components/LazyComponent.svelte
<script>
  import { onMount } from 'svelte';

  export let componentLoader;
  export let fallback = null;

  let Component = null;
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const module = await componentLoader();
      Component = module.default;
    } catch (e) {
      error = e;
    } finally {
      loading = false;
    }
  });
</script>

{#if loading}
  {#if fallback}
    <svelte:component this={fallback} />
  {:else}
    <div class="loading-skeleton">Loading...</div>
  {/if}
{:else if error}
  <div class="error-state">Failed to load component</div>
{:else if Component}
  <svelte:component this={Component} {...$$props} />
{/if}
```

### 3. Asset Bundling Strategy

```javascript
// Bundle critical SVGs into a sprite
// scripts/build-svg-sprite.js
const fs = require("fs");
const path = require("path");

const criticalSvgs = [
  "arrow-up.svg",
  "arrow-down.svg",
  "play.svg",
  "pause.svg",
];

const buildSvgSprite = () => {
  let sprite = '<svg style="display: none;">';

  criticalSvgs.forEach((filename) => {
    const content = fs.readFileSync(`src/images/${filename}`, "utf8");
    const id = filename.replace(".svg", "");
    sprite += `<symbol id="${id}">${content.replace(/<\/?svg[^>]*>/g, "")}</symbol>`;
  });

  sprite += "</svg>";
  fs.writeFileSync("static/critical-sprites.svg", sprite);
};
```

## 🚀 Asset Optimization

### 1. SVG Optimization

```bash
# Install SVGO
npm install -g svgo

# Optimize all SVGs
find static/images -name "*.svg" -exec svgo {} \;

# Batch optimization with custom config
svgo --config svgo.config.js --folder static/images --recursive
```

```javascript
// svgo.config.js
module.exports = {
  plugins: [
    "removeDoctype",
    "removeXMLProcInst",
    "removeComments",
    "removeMetadata",
    "removeUselessDefs",
    "removeEditorsNSData",
    "removeEmptyAttrs",
    "removeHiddenElems",
    "removeEmptyText",
    "removeEmptyContainers",
    "minifyStyles",
    "convertStyleToAttrs",
  ],
};
```

### 2. Image Format Optimization

```javascript
// vite.config.ts - Add image optimization
import { defineConfig } from "vite";
import { imageOptimize } from "vite-plugin-imagemin";

export default defineConfig({
  plugins: [
    imageOptimize({
      gifsicle: { optimizationLevel: 7 },
      mozjpeg: { quality: 80 },
      pngquant: { quality: [0.65, 0.8] },
      svgo: {
        plugins: [
          { name: "removeViewBox", active: false },
          { name: "removeEmptyAttrs", active: false },
        ],
      },
    }),
  ],
});
```

### 3. Critical CSS Extraction

```javascript
// Extract critical CSS for above-the-fold content
// scripts/extract-critical-css.js
const critical = require("critical");

critical.generate({
  inline: true,
  base: "dist/",
  src: "index.html",
  dest: "index-critical.html",
  width: 1300,
  height: 900,
  minify: true,
});
```

## 🔄 Loading Strategies

### 1. Progressive Loading

```svelte
<!-- src/lib/components/ProgressiveImage.svelte -->
<script>
  export let src;
  export let alt;
  export let placeholder = '/images/placeholder.svg';

  let loaded = false;
  let error = false;

  const handleLoad = () => loaded = true;
  const handleError = () => error = true;
</script>

<div class="progressive-image">
  {#if !loaded && !error}
    <img src={placeholder} alt="" class="placeholder" />
  {/if}

  <img
    {src}
    {alt}
    class:loaded
    class:error
    on:load={handleLoad}
    on:error={handleError}
  />
</div>

<style>
  .progressive-image {
    position: relative;
    overflow: hidden;
  }

  img {
    transition: opacity 0.3s ease;
    opacity: 0;
  }

  img.loaded {
    opacity: 1;
  }

  .placeholder {
    position: absolute;
    opacity: 0.3;
    filter: blur(2px);
  }
</style>
```

### 2. Intersection Observer for Lazy Loading

```javascript
// src/lib/utils/lazyLoad.js
export const lazyLoad = (node, src) => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          node.src = src;
          observer.unobserve(node);
        }
      });
    },
    {
      rootMargin: "50px",
    }
  );

  observer.observe(node);

  return {
    destroy() {
      observer.unobserve(node);
    },
  };
};
```

### 3. Resource Hints Implementation

```html
<!-- Add to app.html -->
<head>
  <!-- Preload critical assets -->
  <link rel="preload" href="/app.css" as="style" />
  <link rel="preload" href="/app.js" as="script" />

  <!-- Prefetch likely next resources -->
  <link rel="prefetch" href="/write-tab.js" />
  <link rel="prefetch" href="/generate-tab.js" />

  <!-- DNS prefetch for external resources -->
  <link rel="dns-prefetch" href="//fonts.googleapis.com" />

  <!-- Preconnect to critical origins -->
  <link rel="preconnect" href="//api.example.com" />
</head>
```

## 📊 Performance Monitoring

### 1. Real User Monitoring

```javascript
// src/lib/utils/performance.js
export class PerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.setupObservers();
  }

  setupObservers() {
    // Web Vitals monitoring
    new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        if (entry.entryType === "largest-contentful-paint") {
          this.metrics.lcp = entry.startTime;
        }
      });
    }).observe({ entryTypes: ["largest-contentful-paint"] });

    // Custom timing
    this.markStart("app-init");
  }

  markStart(name) {
    performance.mark(`${name}-start`);
  }

  markEnd(name) {
    performance.mark(`${name}-end`);
    performance.measure(name, `${name}-start`, `${name}-end`);
  }

  reportMetrics() {
    // Send to analytics
    console.log("Performance Metrics:", this.metrics);
  }
}
```

### 2. Bundle Analysis Automation

```javascript
// package.json scripts
{
  "scripts": {
    "analyze": "vite build --mode analyze",
    "perf-test": "lighthouse http://localhost:5175 --output json --output-path ./perf-report.json",
    "size-check": "bundlesize"
  },
  "bundlesize": [
    {
      "path": "./dist/assets/*.js",
      "maxSize": "250kb"
    },
    {
      "path": "./dist/assets/*.css",
      "maxSize": "50kb"
    }
  ]
}
```

## 🎯 Implementation Priority

### Week 1 (Critical)

1. ✅ Fix missing asset paths
2. ✅ Implement service worker
3. ✅ Add loading states

### Week 2 (High Impact)

1. ✅ Route-based code splitting
2. ✅ SVG optimization
3. ✅ Critical CSS extraction

### Week 3 (Polish)

1. ✅ Progressive loading
2. ✅ Performance monitoring
3. ✅ Bundle size optimization

## 📈 Expected Results

- **Load Time**: 16s → 2-3s (85% improvement)
- **First Paint**: 14.7s → 1.5s (90% improvement)
- **Asset Count**: 250 → 50 (80% reduction)
- **Bundle Size**: 3.6MB → 1.5MB (58% reduction)
- **Cache Hit Rate**: 78% → 95% (22% improvement)

These strategies will transform the legacy web app from an unusably slow application to a fast, modern web experience that users will actually want to use.
