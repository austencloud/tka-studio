# EnhancedPWAInstallGuide Architecture Documentation

## Component Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│ EnhancedPWAInstallGuide.svelte (Main Component)             │
│ • Manages visibility state                                   │
│ • Orchestrates platform detection                            │
│ • Handles viewport measurement                               │
│ • Renders backdrop and sheet container                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Uses
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PlatformInstructions.svelte (Instruction Orchestrator)      │
│ • Receives instruction configuration                         │
│ • Renders steps and benefits sections                        │
│ • Manages compact mode styling                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Renders
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ InstructionStep.svelte (Step Display)                       │
│ • Displays single instruction step                           │
│ • Shows step number and text                                 │
│ • Handles image/placeholder rendering                        │
│ • Adapts to compact mode                                     │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────────────┐
│  User Agent      │
│  (Browser Info)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│ platform-detection.service.ts            │
│ detectPlatformAndBrowser()               │
└────────┬─────────────────────────────────┘
         │ Returns: { platform, browser }
         ▼
┌──────────────────────────────────────────┐
│ pwa-install-instructions.ts              │
│ getInstallInstructions(platform, browser)│
└────────┬─────────────────────────────────┘
         │ Returns: InstallInstructions
         ▼
┌──────────────────────────────────────────┐
│ PlatformInstructions.svelte              │
│ Renders instructions                      │
└──────────────────────────────────────────┘
```

## Separation of Concerns

### 1. Detection Layer
**File**: `utils/platform-detection.service.ts`

**Responsibility**: Detect user's platform and browser

```typescript
// Input: navigator.userAgent
// Output: { platform: Platform, browser: Browser }

detectPlatformAndBrowser() → {
  platform: "ios" | "android" | "desktop",
  browser: "chrome" | "safari" | "edge" | "firefox" | "samsung" | "other"
}
```

### 2. Configuration Layer
**File**: `config/pwa-install-instructions.ts`

**Responsibility**: Store all instruction variations

```typescript
// Input: platform, browser
// Output: InstallInstructions

getInstallInstructions(platform, browser) → {
  title: string,
  icon: string,
  steps: InstructionStep[],
  benefits: string[]
}
```

### 3. Measurement Layer
**File**: `utils/viewport-measurement.svelte.ts`

**Responsibility**: Measure viewport and determine compact mode

```typescript
// Input: sheet element, content element
// Output: needsCompactMode: boolean

createViewportMeasurement() → {
  sheetElement: HTMLElement | null,
  contentElement: HTMLElement | null,
  needsCompactMode: boolean,
  measure(): void
}
```

### 4. Display Layer
**Files**:
- `components/EnhancedPWAInstallGuide.svelte` (Main container)
- `components/PlatformInstructions.svelte` (Instruction orchestrator)
- `components/InstructionStep.svelte` (Step display)

**Responsibility**: Render UI based on data

## State Management

### Main Component State
```typescript
// Platform/Browser detection
let platform = $state<Platform>("desktop");
let browser = $state<Browser>("other");

// Viewport measurement
const viewport = createViewportMeasurement({ initialDelay: 100 });

// Derived instructions
const instructions = $derived(getInstallInstructions(platform, browser));
```

### Reactive Dependencies
```
platform + browser
    │
    ▼
getInstallInstructions()
    │
    ▼
instructions (derived)
    │
    ▼
PlatformInstructions component re-renders
    │
    ▼
InstructionStep components update
```

## File Structure

```
src/lib/shared/mobile/
│
├── components/
│   ├── EnhancedPWAInstallGuide.svelte   (281 lines)
│   │   └── Main component, orchestrates everything
│   │
│   ├── PlatformInstructions.svelte      (154 lines)
│   │   └── Displays full instruction set
│   │
│   └── InstructionStep.svelte            (146 lines)
│       └── Displays single instruction step
│
├── config/
│   └── pwa-install-instructions.ts       (309 lines)
│       └── All instruction configurations
│
└── utils/
    ├── platform-detection.service.ts     (123 lines)
    │   └── Platform/browser detection logic
    │
    └── viewport-measurement.svelte.ts    (132 lines)
        └── Viewport measurement and ResizeObserver
```

## Platform/Browser Matrix

| Platform | Browser | Supported | Instructions Config |
|----------|---------|-----------|-------------------|
| iOS | Safari | ✅ Yes | `ios-safari` |
| iOS | Chrome | ⚠️ Limited | `ios-other` (redirects to Safari) |
| iOS | Firefox | ⚠️ Limited | `ios-other` (redirects to Safari) |
| iOS | Edge | ⚠️ Limited | `ios-other` (redirects to Safari) |
| Android | Chrome | ✅ Yes | `android-chrome` |
| Android | Edge | ✅ Yes | `android-chrome` |
| Android | Samsung Internet | ✅ Yes | `android-samsung` |
| Android | Firefox | ❌ No | Fallback |
| Desktop | Chrome | ✅ Yes | `desktop-chrome` |
| Desktop | Edge | ✅ Yes | `desktop-chrome` |
| Desktop | Firefox | ❌ No | Fallback |
| Desktop | Safari | ❌ No | Fallback |

## Configuration Schema

### InstructionStep
```typescript
interface InstructionStep {
  text: string;          // HTML string with <strong> tags
  icon: string;          // Font Awesome icon class
  image: string | null;  // Path to screenshot or null for placeholder
}
```

### InstallInstructions
```typescript
interface InstallInstructions {
  title: string;              // Main title for this platform/browser
  icon: string;               // Font Awesome icon class
  steps: InstructionStep[];   // Array of instruction steps
  benefits: string[];         // Array of benefit strings
}
```

## Styling Architecture

### CSS Organization
1. **Main Component**: Container, backdrop, header, footer styles
2. **PlatformInstructions**: Section layout, grid, spacing
3. **InstructionStep**: Card styling, step number, image placeholder

### Compact Mode Strategy
- Detected by viewport measurement utility
- Passed as prop through component hierarchy
- Applied via CSS classes: `class:compact={needsCompactMode}`
- Reduces padding, font sizes, margins using `clamp()` and CSS container queries

### Responsive Design
- Uses CSS container queries for adaptive layouts
- Fluid typography with `clamp()`
- Dynamic viewport height (`95dvh`)
- Safe area insets for mobile devices

## Testing Strategy

### Unit Tests

#### 1. Platform Detection Service
```typescript
describe('platform-detection.service', () => {
  describe('detectPlatformAndBrowser', () => {
    test('iOS Safari', () => {...});
    test('Android Chrome', () => {...});
    test('Desktop Edge', () => {...});
  });

  describe('supportsPWAInstall', () => {
    test('iOS Safari returns true', () => {...});
    test('iOS Chrome returns false', () => {...});
  });
});
```

#### 2. Instructions Configuration
```typescript
describe('pwa-install-instructions', () => {
  describe('getInstallInstructions', () => {
    test('returns correct config for iOS Safari', () => {...});
    test('falls back for unsupported browsers', () => {...});
  });
});
```

#### 3. Viewport Measurement
```typescript
describe('viewport-measurement', () => {
  test('detects when compact mode is needed', () => {...});
  test('updates on viewport resize', () => {...});
});
```

### Component Tests

#### 1. InstructionStep
```typescript
describe('InstructionStep', () => {
  test('renders step number and text', () => {...});
  test('shows placeholder when no image', () => {...});
  test('hides image in compact mode', () => {...});
});
```

#### 2. PlatformInstructions
```typescript
describe('PlatformInstructions', () => {
  test('renders all steps', () => {...});
  test('renders all benefits', () => {...});
  test('applies compact mode styles', () => {...});
});
```

#### 3. EnhancedPWAInstallGuide
```typescript
describe('EnhancedPWAInstallGuide', () => {
  test('detects platform on mount', () => {...});
  test('shows correct instructions for detected platform', () => {...});
  test('closes when backdrop clicked', () => {...});
});
```

### Integration Tests
1. **E2E flow**: Open guide → Detect platform → Show instructions → Close
2. **Platform switching**: Mock different user agents, verify instructions change
3. **Responsive behavior**: Resize viewport, verify compact mode triggers

## Performance Considerations

### Initial Load
- Detection runs once on mount
- Instructions retrieved via pure function (fast lookup)
- No heavy computations

### Runtime
- ResizeObserver efficiently tracks viewport changes
- Svelte's reactivity minimizes re-renders
- Compact mode detection is debounced

### Bundle Size
- Config file: ~10KB uncompressed
- Services/utilities: ~8KB uncompressed
- Components: ~15KB uncompressed
- Total: ~33KB (compresses well with gzip)

### Code Splitting Opportunities
```typescript
// Lazy load instructions config
const instructions = await import('./config/pwa-install-instructions');

// Lazy load detection service
const { detectPlatformAndBrowser } = await import('./utils/platform-detection.service');
```

## Extensibility Patterns

### Adding New Platform
```typescript
// 1. Add to type definition
type Platform = "ios" | "android" | "desktop" | "chromeos"; // Add chromeos

// 2. Add detection logic
function detectPlatform(ua: string): Platform {
  if (/cros/.test(ua)) return "chromeos"; // Add detection
  // ... existing code
}

// 3. Add instructions config
const INSTRUCTIONS_MAP = {
  "chromeos-chrome": { /* config */ },
  // ... existing configs
};
```

### Adding Localization
```typescript
// 1. Create locale-specific configs
export function getInstallInstructions(
  platform: Platform,
  browser: Browser,
  locale: string = 'en'
): InstallInstructions {
  const key = `${platform}-${browser}`;
  const localeKey = `${key}-${locale}`;

  return INSTRUCTIONS_MAP_LOCALIZED[localeKey] || INSTRUCTIONS_MAP[key];
}
```

### Adding Analytics
```typescript
// 1. Track instruction views
onMount(() => {
  const detected = detectPlatformAndBrowser();
  analytics.track('pwa_guide_opened', {
    platform: detected.platform,
    browser: detected.browser
  });
});

// 2. Track step interactions
function handleStepClick(stepIndex: number) {
  analytics.track('pwa_guide_step_viewed', { stepIndex });
}
```

## Best Practices Applied

1. ✅ **Single Responsibility**: Each file has one clear purpose
2. ✅ **DRY**: No duplicated code
3. ✅ **Composition**: Built from small, focused components
4. ✅ **Configuration**: Data-driven, not hardcoded
5. ✅ **Type Safety**: Full TypeScript coverage
6. ✅ **Testability**: Pure functions, isolated components
7. ✅ **Maintainability**: Easy to understand and modify
8. ✅ **Reusability**: Utilities can be used elsewhere
9. ✅ **Accessibility**: ARIA labels, semantic HTML
10. ✅ **Performance**: Efficient rendering, minimal re-renders

## Migration Guide

### For Developers Using This Component

**No changes required!** The refactored component is a drop-in replacement:

```svelte
<!-- Before and After - Exact same API -->
<EnhancedPWAInstallGuide bind:showGuide={showPWAGuide} />
```

### For Developers Extending This Component

**New utilities available for reuse:**

```typescript
// Use detection service elsewhere
import { detectPlatformAndBrowser } from '$lib/shared/mobile/utils/platform-detection.service';
const { platform, browser } = detectPlatformAndBrowser();

// Use viewport measurement for other sheets
import { createViewportMeasurement } from '$lib/shared/mobile/utils/viewport-measurement.svelte';
const viewport = createViewportMeasurement();

// Reuse instruction step component
import InstructionStep from '$lib/shared/mobile/components/InstructionStep.svelte';
```

---

**Last Updated**: 2025-10-30
**Maintainer**: Development Team
**Version**: 2.0 (Refactored)
