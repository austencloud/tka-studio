# SEO Hybrid System Testing Guide

## Testing Strategy Overview

We need to test 3 main scenarios:

1. **Search Engine Bot Behavior** - Bots see static content
2. **User Redirection** - Users get redirected to SPA
3. **SPA Navigation** - In-app navigation stays smooth

## 1. Bot Testing (Search Engine Perspective)

### Manual Bot Simulation

```bash
# Test with curl (simulates bot behavior)
curl -H "User-Agent: Googlebot/2.1" http://localhost:5173/about
curl -H "User-Agent: Bingbot/2.0" http://localhost:5173/features
curl -H "User-Agent: facebookexternalhit/1.1" http://localhost:5173/browse
```

**Expected Results:**

- Should return full HTML content
- No JavaScript redirects should occur
- Meta tags and structured data should be present

### Using Browser Dev Tools

1. Open Chrome DevTools
2. Go to Network tab > User Agent dropdown
3. Select "Googlebot"
4. Navigate to `/about`, `/features`, `/browse`
5. **Expected:** Pages load normally without redirects

## 2. User Redirection Testing

### Test Search Engine Referrals

```javascript
// Simulate coming from Google search
// In browser console, set fake referrer:
Object.defineProperty(document, "referrer", {
  value: "https://www.google.com/search?q=TKA+animation",
  configurable: true,
});

// Then navigate to /about - should redirect to /?tab=about
```

### Test Direct Navigation

1. **Direct URL access:** Go to `http://localhost:5173/about`
   - **Expected:** Redirect to `/?tab=about` after brief delay
2. **Features page:** Go to `http://localhost:5173/features`
   - **Expected:** Redirect to `/?tab=about&section=features`
3. **Browse page:** Go to `http://localhost:5173/browse`
   - **Expected:** Redirect to `/?tab=browse`

## 3. SPA Navigation Testing

### Tab Navigation

1. Load main app at `/`
2. Click each tab in navigation
3. **Expected:** Smooth transitions, no page reloads, URL stays at `/`

### Logo Click

1. From any tab, click the TKA logo
2. **Expected:** Switches to About tab, no page reload

## 4. SEO Infrastructure Testing

### Sitemap Testing

```bash
curl http://localhost:5173/sitemap.xml
```

**Expected:** Valid XML with all pages listed

### Robots.txt Testing

```bash
curl http://localhost:5173/robots.txt
```

**Expected:** Proper directives for bots

### Meta Tags Testing

```bash
# Check meta tags are present
curl -s http://localhost:5173/about | grep -i "meta\|title\|og:"
```

## 5. Automated Testing Script

Let me create a comprehensive test script:
