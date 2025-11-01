# App Name Update: "TKA Studio"

## Summary

Updated all references from "The Kinetic Constructor", "The Kinetic Alphabet" (as app name), and standalone "TKA" (as app name) to **"TKA Studio"**.

**Important distinction:**
- **"TKA Studio"** = The application/software tool
- **"The Kinetic Alphabet"** = The notation system/methodology (still used when referring to the system itself)

## Files Changed

### Core Configuration Files

1. **`static/manifest.webmanifest`**
   - `name`: "The Kinetic Alphabet" → "TKA Studio"
   - `short_name`: "TKA" → "TKA Studio"

2. **`package.json`**
   - `name`: "@tka/web-app" → "@tka/studio"
   - `description`: Updated to mention "TKA Studio"

3. **`README.md`**
   - Title: "TKA Web Application" → "TKA Studio"
   - Subtitle: "The Kinetic Alphabet" → "TKA Studio"
   - Description: Updated to clarify TKA Studio is built on The Kinetic Alphabet notation system

4. **`src/app.html`**
   - `apple-mobile-web-app-title`: "TKA" → "TKA Studio"

### Application Files

5. **`src/lib/shared/application/components/MainApplication.svelte`**
   - `<title>`: "TKA Constructor - The Kinetic Alphabet" → "TKA Studio - Flow Arts Choreography Tool"
   - Meta description: Updated to mention TKA Studio using The Kinetic Alphabet notation system

6. **`src/lib/shared/foundation/services/implementations/SeoService.ts`**
   - Default title: "TKA Constructor - The Kinetic Alphabet" → "TKA Studio - Flow Arts Choreography Tool"
   - Default description: Updated to mention TKA Studio and The Kinetic Alphabet notation system

7. **`src/routes/+page.svelte`**
   - `<title>`: "TKA - The Kinetic Constructor" → "TKA Studio - Flow Arts Choreography Tool"

8. **`src/config/domains.ts`**
   - `siteName`: "TKA - The Kinetic Alphabet" → "TKA Studio"

9. **`src/routes/sitemap.xml/+server.ts`**
   - Description: "TKA - The Kinetic Constructor | Home" → "TKA Studio | Home"

### About Module

10. **`src/lib/modules/about/components/Home.svelte`**
    - Page title: "The Kinetic Alphabet - Flow Arts..." → "TKA Studio - Flow Arts..."
    - Hero title: "The Kinetic Alphabet" → "TKA Studio"
    - Features heading: "The Kinetic Alphabet Features" → "TKA Studio Features"
    - Feature description: "The Kinetic Constructor enables..." → "TKA Studio enables..."
    - Meta description: Updated to mention TKA Studio and The Kinetic Alphabet notation system

11. **`src/lib/modules/about/components/HeroSection.svelte`**
    - Hero title: "About The Kinetic Alphabet" → "About TKA Studio"

12. **`src/lib/modules/about/components/Features.svelte`**
    - Features heading: "The Kinetic Alphabet Features" → "TKA Studio Features"
    - Feature description: "The Kinetic Constructor enables..." → "TKA Studio enables..."

13. **`src/lib/modules/about/components/Contact.svelte`**
    - Page title: "Contact - The Kinetic Alphabet" → "Contact - TKA Studio"
    - Meta description: "...The Kinetic Alphabet team..." → "...the creator of TKA Studio..."

14. **`src/lib/modules/about/components/Links.svelte`**
    - Page title: "Links & Resources - The Kinetic Alphabet" → "Links & Resources - TKA Studio"
    - Meta description: Updated to mention TKA Studio

15. **`src/lib/modules/about/components/LandingNavBar.svelte`**
    - Logo subtitle: "The Kinetic Alphabet" → "TKA Studio"

### Share Module

16. **`src/lib/modules/build/share/domain/models/ShareOptions.ts`**
    - Print preset notes: "Created with The Kinetic Alphabet" → "Created with TKA Studio"

17. **`src/lib/modules/build/share/services/implementations/ShareService.ts`**
    - Default notes (2 locations): "Created with The Kinetic Alphabet" → "Created with TKA Studio"

### Learn Module

18. **`src/lib/modules/learn/domain/concepts.ts`**
    - File header: "The Kinetic Alphabet - Complete Learning Path" → "TKA Studio - Complete Learning Path for The Kinetic Alphabet"
    - Note: "The Kinetic Alphabet" as the notation system name remains in curriculum references

19. **`src/lib/modules/learn/IMPLEMENTATION_SUMMARY.md`**
    - Description: "...for The Kinetic Alphabet..." → "...for TKA Studio (The Kinetic Alphabet)..."

### Documentation

20. **`docs/ios-pwa-optimization.md`**
    - Manifest example: Updated to show "TKA Studio" as app name

## What Was NOT Changed

The following references to "The Kinetic Alphabet" were **intentionally kept** because they refer to the notation system/methodology, not the app:

- **VTG relationship**: "The Kinetic Alphabet was built from VTG poi theory"
- **Curriculum references**: "Based on The Kinetic Alphabet Level 1 curriculum"
- **System descriptions**: "The Kinetic Alphabet uses a 4-point grid system"
- **Methodology references**: "Core building blocks of The Kinetic Alphabet"
- **Educational content**: References to The Kinetic Alphabet as a notation system

## Naming Convention Going Forward

### Use "TKA Studio" when referring to:
- The application/software
- The web app
- The tool/platform
- User-facing branding
- App titles and metadata
- Download/share attribution

### Use "The Kinetic Alphabet" when referring to:
- The notation system
- The methodology
- The curriculum
- The theoretical framework
- Historical context (VTG relationship)
- Educational concepts

### Examples:

✅ **Correct:**
- "TKA Studio is a web application for creating movement sequences"
- "TKA Studio uses The Kinetic Alphabet notation system"
- "Created with TKA Studio"
- "The Kinetic Alphabet is based on a 4-point grid"
- "The Kinetic Alphabet was built from VTG poi theory"

❌ **Incorrect:**
- "The Kinetic Alphabet is a web application" (should be "TKA Studio")
- "TKA Studio is based on a 4-point grid" (should be "The Kinetic Alphabet")
- "Created with The Kinetic Alphabet" (should be "TKA Studio")

## Impact

### User-Facing Changes:
- App name on home screen (iOS): "TKA Studio"
- Browser tab titles: "TKA Studio - ..."
- Shared images: "Created with TKA Studio"
- About page: "About TKA Studio"

### Developer-Facing Changes:
- Package name: `@tka/studio`
- Documentation references updated
- Code comments clarified

### SEO Impact:
- All meta titles/descriptions updated
- Sitemap updated
- Consistent branding across all pages

## Testing Checklist

- [ ] Verify PWA install shows "TKA Studio" on home screen
- [ ] Check all page titles in browser tabs
- [ ] Test shared image attribution text
- [ ] Verify About page displays correctly
- [ ] Check manifest.webmanifest is valid
- [ ] Confirm SEO meta tags are correct
- [ ] Test that educational content still references "The Kinetic Alphabet" appropriately

## Related Files

- iOS PWA optimization guide: `docs/ios-pwa-optimization.md`
- PWA vs App Store analysis: `docs/pwa-vs-app-store-2025.md`
- Main README: `README.md`
