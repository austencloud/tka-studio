# PWA Installation Guide Screenshots

This directory contains platform-specific screenshots for the PWA installation guide.

## Required Screenshots

### iOS Safari

- `ios-safari-step1.png` - Safari with Share button highlighted
- `ios-safari-step2.png` - Share menu with "Add to Home Screen" highlighted
- `ios-safari-step3.png` - "Add to Home Screen" dialog with "Add" button

**Recommended size:** 375x667px (iPhone SE) or 390x844px (iPhone 13)

### Android Chrome/Edge

- `android-chrome-step1.png` - Chrome menu (⋮) highlighted
- `android-chrome-step2.png` - Menu with "Add to Home screen" highlighted
- `android-chrome-step3.png` - Install confirmation dialog

**Recommended size:** 360x640px or 412x915px

### Android Samsung Internet

- `android-samsung-step1.png` - Samsung Internet menu (☰) highlighted
- `android-samsung-step2.png` - "Add page to" → "Home screen" menu

**Recommended size:** 360x640px or 412x915px

### Desktop Chrome/Edge

- `desktop-chrome-step1.png` - Address bar with install icon (⊕) highlighted
- `desktop-chrome-step2.png` - Install dialog

**Recommended size:** 1280x720px (scaled down)

## Creating Screenshots

### Tools

- **iOS:** Use iOS Simulator screenshots or real device screenshots
- **Android:** Use Android Emulator or real device screenshots
- **Desktop:** Use browser DevTools device mode or regular screenshots

### Tips

1. **Annotations:** Add arrows, highlights, or circles to key UI elements
2. **Quality:** Use PNG format for clarity
3. **Consistency:** Use the same device size for all screenshots in a category
4. **Branding:** Ensure TKA is loaded in each screenshot
5. **Compression:** Optimize images (aim for <200KB each)

### Annotation Tools

- **Skitch** (Mac/iOS) - Free, easy annotations
- **Snagit** (Windows/Mac) - Professional annotations
- **Figma** - Design custom arrows and highlights
- **Photopea** (Web) - Free Photoshop alternative

## Fallback Behavior

If a screenshot is missing, the guide will show a placeholder with a camera icon. The installation steps will still be readable without images.

## Example Workflow

1. Load TKA in target browser/device
2. Navigate to the install screen
3. Take screenshot at each step
4. Annotate the screenshot to highlight the relevant UI element
5. Optimize/compress the image
6. Save to this directory with the correct filename
7. Test the guide to ensure images load

## Future Enhancements

Consider adding:

- Animated GIFs showing the full installation process
- Video tutorials for each platform
- Dark mode variants of screenshots
- Localized screenshots for different languages
