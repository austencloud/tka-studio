# iOS PWA Optimization Guide

## Overview

TKA Studio is optimized as a Progressive Web App (PWA) with first-class iOS support. This guide covers iOS-specific optimizations and best practices.

## Why PWA Instead of Native iOS App?

### Current Reality

- ✅ **No Mac required** - Build and deploy from any platform
- ✅ **No App Store approval** - Deploy updates instantly
- ✅ **No $99/year fee** - Free to distribute
- ✅ **Single codebase** - Same code works on iOS, Android, desktop
- ✅ **Already works** - Users can install via "Add to Home Screen"

### Limitations We Accept

- ⚠️ **No push notifications** - TKA Studio doesn't need them
- ⚠️ **No background sync** - TKA Studio is offline-first already
- ⚠️ **Storage limits** - 50MB-1GB (sufficient for TKA Studio)
- ⚠️ **Not in App Store** - But users can still install it

## iOS-Specific Optimizations Implemented

### 1. Meta Tags (`src/app.html`)

```html
<!-- Viewport with safe area support -->
<meta
  name="viewport"
  content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover"
/>

<!-- iOS PWA Configuration -->
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta
  name="apple-mobile-web-app-status-bar-style"
  content="black-translucent"
/>
<meta name="apple-mobile-web-app-title" content="TKA Studio" />

<!-- Apple Touch Icon -->
<link rel="apple-touch-icon" href="/pwa/icon-180x180.png" />
```

**What this does:**

- `viewport-fit=cover` - Extends to notch/Dynamic Island on iPhone
- `apple-mobile-web-app-capable` - Runs fullscreen without Safari UI
- `black-translucent` - Status bar blends with app background
- `apple-mobile-web-app-title` - Short name on home screen

### 2. Splash Screens

iOS shows a white screen during PWA launch unless you provide splash screens. We generate them for all device sizes:

```bash
npm run optimize:ios
```

This creates splash screens for:

- iPhone SE (640x1136)
- iPhone 8/7/6s (750x1334)
- iPhone 8 Plus (1242x2208)
- iPhone 14 (828x1792)
- iPhone 14 Plus (1242x2688)
- iPhone 14 Pro (1125x2436)
- iPhone 15 Pro (1179x2556)
- iPhone 15 Pro Max (1290x2796)
- iPad 10.2" (1536x2048)
- iPad Pro 11" (1668x2388)
- iPad Pro 12.9" (2048x2732)

### 3. Manifest Configuration (`static/manifest.webmanifest`)

```json
{
  "name": "TKA Studio",
  "short_name": "TKA Studio",
  "display": "standalone",
  "theme_color": "#0b1d2a",
  "background_color": "#0b1d2a"
}
```

**Key changes:**

- `display: "standalone"` instead of `"fullscreen"` - Better iOS compatibility
- Proper `short_name` - Shows as "TKA Studio" on home screen
- Matching theme/background colors - Prevents color flash

### 4. Touch Handling

All interactive elements use iOS-optimized touch handling:

```typescript
// Haptic feedback on iOS
hapticService?.trigger("selection"); // Uses navigator.vibrate()

// Touch gesture support
const gesture = gestureService.createSwipeGestureHandler({
  threshold: 100,
  onSwipeLeft: () => {
    /* ... */
  },
  onSwipeRight: () => {
    /* ... */
  },
});
```

**Features:**

- Haptic feedback for buttons, toggles, sliders
- Swipe gestures for navigation
- Proper touch event handling (prevents double-tap zoom)
- iOS-style toggle switches

### 5. Viewport Height Handling

iOS Safari has a dynamic viewport (URL bar hides/shows). We handle this:

```typescript
// Track actual viewport height including Safari chrome
const height = window.visualViewport?.height ?? window.innerHeight;
document.documentElement.style.setProperty("--viewport-height", `${height}px`);
```

**CSS usage:**

```css
.full-height {
  height: var(--viewport-height); /* Not 100vh! */
}
```

### 6. Install Prompts

Smart install prompts that detect iOS Safari:

```typescript
// Detects iOS Safari and shows appropriate instructions
const { platform, browser } = platformService.detectPlatformAndBrowser();

if (platform === "ios" && browser === "safari") {
  // Show "Add to Home Screen" instructions
  showIOSInstallGuide();
}
```

**Features:**

- Platform/browser detection
- iOS-specific install instructions
- Screenshots showing exact steps
- Dismissible with smart re-prompting

## Testing on iOS

### Without Physical Device

**Option 1: BrowserStack** (Recommended)

- $39/month for real iOS devices in cloud
- Test on actual iPhones/iPads
- https://www.browserstack.com

**Option 2: iOS Simulator** (Requires Mac)

- Free with Xcode
- Limited PWA testing (no "Add to Home Screen")

### With Physical Device

1. **Deploy to Netlify** (or any HTTPS host)
2. **Open in Safari** on iPhone/iPad
3. **Tap Share button** (square with up arrow)
4. **Scroll down** and tap "Add to Home Screen"
5. **Tap "Add"** in top-right
6. **Test the installed app**

### What to Test

- ✅ Splash screen appears (not white flash)
- ✅ Icon looks good on home screen
- ✅ App opens fullscreen (no Safari UI)
- ✅ Status bar blends with app
- ✅ Touch gestures work smoothly
- ✅ Haptic feedback works
- ✅ Canvas rendering performs well
- ✅ Offline mode works
- ✅ Data persists (Dexie/IndexedDB)

## Performance Optimization

### Canvas Rendering on iOS

iOS Safari has excellent canvas performance, but:

```typescript
// Use fabric.js with iOS-optimized settings
const canvas = new Canvas(element, {
  renderOnAddRemove: false, // Manual rendering
  skipTargetFind: true, // Faster hit detection
  enableRetinaScaling: true, // Sharp on Retina displays
});
```

### Memory Management

iOS has stricter memory limits than desktop:

```typescript
// Clear unused canvases
canvas.dispose();

// Limit cached images
const MAX_CACHED_SEQUENCES = 50; // Lower on mobile

// Use IndexedDB efficiently
await db.sequences.bulkPut(sequences); // Batch operations
```

### Network Optimization

```typescript
// Service worker caches critical assets
const STATIC_CACHE = [
  "/",
  "/app.css",
  "/manifest.webmanifest",
  "/pwa/icon-512x512.png",
];
```

## Common iOS Issues & Solutions

### Issue: White flash on launch

**Solution:** Generate splash screens with `npm run optimize:ios`

### Issue: App doesn't go fullscreen

**Solution:** Check `apple-mobile-web-app-capable` meta tag is present

### Issue: Status bar wrong color

**Solution:** Set `apple-mobile-web-app-status-bar-style` to `black-translucent`

### Issue: Viewport height jumps when scrolling

**Solution:** Use `window.visualViewport.height` instead of `window.innerHeight`

### Issue: Double-tap zooms in

**Solution:** Add `user-scalable=no` to viewport meta tag

### Issue: Touch events feel laggy

**Solution:** Use `touch-action: manipulation` CSS and add haptic feedback

### Issue: Canvas looks blurry

**Solution:** Enable `enableRetinaScaling: true` in Fabric.js

## Marketing iOS PWA

### Messaging

**Don't say:**

- ❌ "It's not a real app"
- ❌ "It's just a website"
- ❌ "It's not in the App Store"

**Do say:**

- ✅ "Works on iPhone & iPad - no App Store needed"
- ✅ "Install directly from Safari in seconds"
- ✅ "Full offline support, works like a native app"
- ✅ "Always up-to-date, no manual updates required"

### Tutorial Content

Create short videos showing:

1. Opening TKA Studio in Safari
2. Tapping Share button
3. Selecting "Add to Home Screen"
4. The installed app launching

**Platforms:**

- YouTube Shorts (60 seconds)
- Instagram Reels
- TikTok
- Embedded on your website

## Future iOS Improvements

### When iOS Adds Features

Apple is slowly improving PWA support. Watch for:

- **Push Notifications** - Coming to iOS PWAs (maybe)
- **Background Sync** - Requested by developers
- **File System Access** - Would enable better exports
- **Web Bluetooth** - For hardware integration

### If You Ever Need App Store

If business requirements change:

1. **Hire iOS contractor** on Upwork ($500-1000)
2. **Give them Capacitor build** (wraps your PWA)
3. **They handle Xcode/submission**
4. **You keep maintaining web code**

## Resources

- [iOS PWA Best Practices](https://web.dev/progressive-web-apps/)
- [Apple PWA Documentation](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)
- [Can I Use - PWA Features](https://caniuse.com/?search=pwa)
- [BrowserStack - iOS Testing](https://www.browserstack.com/test-on-iphone)

## Conclusion

TKA's PWA approach is the right choice for a solo developer:

- ✅ No Mac/iPhone required for development
- ✅ No App Store gatekeeping
- ✅ Instant updates
- ✅ Works great on iOS Safari
- ✅ Future-proof as PWAs improve

Focus on making the web app amazing, and iOS users will love it just as much as Android/desktop users.
