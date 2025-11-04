# Component Architecture Analysis - TKA Studio

## Executive Summary

TKA Studio is a modern SvelteKit application with a well-organized component hierarchy. The codebase contains **300+ Svelte components** organized into modular feature areas. While `bits-ui` v2.14.2 is installed, it's **currently not utilized**. Instead, the app uses a mix of custom-built components and `vaul-svelte` for sheets/drawers.

This presents a significant opportunity to upgrade the component system with **Bits UI + shadcn-svelte**, which would provide:
- Consistent, accessible UI primitives
- Better type safety and composability
- Reduced custom CSS and maintenance burden
- Industry-standard design patterns
- Improved mobile/touch experience with built-in gestures

---

## Current Component Landscape

### 1. **Foundation UI Components** (Core Reusable Layer)
Located in: `/src/lib/shared/foundation/ui/`

#### Status: Mostly Custom-Built
Currently 12 foundation components, with minimal library usage:

| Component | Current Implementation | Status | Migration Potential |
|-----------|----------------------|--------|---------------------|
| **Drawer** | `vaul-svelte` wrapper | Active (Nov 3) | Ready for Bits UI Dialog/Popover |
| **ConfirmDialog** | Custom (glassmorphism) | Active (Oct 30) | Replace with Bits UI Dialog + Button |
| **IOSToggle** | Custom (100% built) | Active | Replace with Bits UI Switch |
| **ErrorBanner** | Custom (100% built) | Active | Keep custom, enhance with Bits Button |
| **ErrorScreen** | Custom (100% built) | Active | Combine with Bits components |
| **FloatingFullscreenButton** | Custom (100% built) | Active | Replace with Bits UI Button + Floating UI |
| **HorizontalSwipeContainer** | Custom (Embla Carousel) | Active | Keep as-is, enhance carousel with Bits Carousel |
| **SkeletonLoader** | Custom (100% built) | Active | Replace with Bits UI Skeleton |
| **SheetDragHandle** | Custom (100% built) | Active | Keep custom (specific UX need) |
| **SimpleGlassScroll** | Custom (100% built) | Active | Can stay custom or enhance with Bits Scroll Area |
| **Splitter** | Custom (100% built) | Active | Replace with Bits UI Splitter |
| **FontAwesomeIcon** | FontAwesome wrapper | Active | Keep as-is |

**Key Insight**: The Drawer component has already been refactored to use `vaul-svelte` v1.0.0-next.7, suggesting openness to adopting better UI libraries.

---

### 2. **Form & Input Components**
Located in: `/src/lib/shared/settings/components/`

| Component | Implementation | Usage Pattern | Migration Target |
|-----------|----------------|----------------|-------------------|
| **TextInput** | Custom `<input>` | Settings forms | Bits UI Input |
| **SelectInput** | Custom `<select>` | Settings dropdowns | Bits UI Select |
| **ToggleSetting** | Custom toggle UI | Settings toggles | Bits UI Switch |

**Current Pattern**: All use haptic feedback service, custom styling with CSS variables, and light/dark mode support.

---

### 3. **Modal/Dialog Components**
Located across multiple modules:

#### Dialog Implementations:
1. **ConfirmDialog** (`/shared/foundation/ui/ConfirmDialog.svelte`)
   - Custom implementation with glassmorphism
   - Features: Icon variants (warning/danger/info), haptic feedback
   - Size: 290 lines of code
   - **Migration**: Replace with Bits UI Dialog

2. **PresetSelectionModal** (`/modules/create/generate/components/modals/`)
   - Custom backdrop + portal pattern
   - Features: Dynamic content, preset grid display
   - **Migration**: Use Bits UI Dialog + Modal primitives

3. **CAPSelectionModal** (`/modules/create/generate/components/modals/`)
   - Similar to PresetSelectionModal
   - **Migration**: Same as above

4. **FilterModal** (`/modules/explore/filtering/components/`)
   - Bottom sheet modal for filters
   - **Migration**: Use Bits UI Popover or Sheet

5. **ResourceModal** (`/modules/about/components/resource-guide/`)
   - Custom modal with navigation
   - Header, footer, close button subcomponents
   - **Migration**: Decompose into Bits components + compositions

6. **SettingsModal** (`/modules/about/components/`)
   - Settings-specific modal
   - **Migration**: Can reuse SettingsSheet pattern

#### Summary:
- **Total Modal/Dialog Components**: 15+
- **Custom Implementations**: 14+ (93% custom)
- **Library Usage**: 0%
- **Opportunity**: High - All can be replaced with Bits UI Dialog/Popover/Drawer

---

### 4. **Sheet/Drawer Components**
Located across modules with bottom sheet behavior:

| Component | Current Tech | Usage |
|-----------|-------------|-------|
| **SettingsSheet** | `vaul-svelte` | Full-screen settings panel (Nov 3 update) |
| **AuthSheet** | Custom | Authentication UI |
| **ProfileSettingsSheet** | Custom | User profile settings |
| **PrivacySheet** | Custom | Privacy/terms display |
| **TermsSheet** | Custom | Terms of service |
| **SharePanelSheet** | `vaul-svelte` | Share functionality |
| **ActSheet** | Custom | Act/content browser |
| **SequenceActionsSheet** | Custom | Quick actions for sequences |

**Key Observations**:
- Transition from custom to `vaul-svelte` indicates library adoption preference
- SettingsSheet recently updated (Nov 3) - most mature example
- Most use glass morphism styling and bottom placement
- All support backdrop dismiss and keyboard (Escape) close

---

### 5. **Button Components**
Located across modules with specialized implementations:

#### Foundation/Navigation:
- **SettingsButton** - Settings gear icon with user avatar
- **ProfileButton** - Profile menu trigger
- **InstallPromptButton** - PWA install prompt

#### Specialized Buttons:
- **SaveSequenceButton** - With state management
- **PlayButton** - Video/animation playback
- **ShareButton** - Share functionality
- **UndoButton** - Undo action
- **FullscreenButton** - Fullscreen toggle
- **ClearSequenceButton** - Sequence clearing
- **AnswerButton** - Quiz answer selection
- **LessonButton** - Lesson navigation

#### Action Buttons:
- **CAPComponentButton** - Grid buttons for CAP selection
- **GenerateButtonCard** - Generate action button
- **OrientationControlButton** - Orientation selector
- **TurnControlButton** - Turn direction selector

**Current Pattern**: Mix of bare `<button>` tags with inline styles and custom wrapper components.

**Migration Opportunity**: Create a reusable Bits UI Button component wrapper with consistent sizing, variants (primary/secondary/outline/ghost), and states (loading/disabled).

---

### 6. **Dropdown/Select Components**
Located across modules:

| Component | Current Implementation | Type |
|-----------|----------------------|------|
| **SelectInput** | Native `<select>` | Form control |
| **MixedValueDropdown** | Custom `<select>` with logic | Batch edit control |
| **BackgroundCategorySelector** | Custom | Settings selector |
| **BackgroundSelector** | Custom | Visual selector |
| **FilterSelectionPanel** | Custom | Filter UI |
| **QuizSelectorView** | Custom | Quiz mode selector |

**Current Pattern**: Mix of native `<select>` and custom implementations with haptic feedback.

**Migration Target**: Bits UI Combobox or Select component with proper accessibility and customization.

---

### 7. **Notification/Toast Components**
Located at: `/src/lib/modules/create/workspace-panel/components/Toast.svelte`
And: `/src/lib/shared/gamification/components/AchievementNotificationToast.svelte`

#### Toast Implementation:
- **Position**: Fixed bottom center (80px from bottom)
- **Auto-dismiss**: 3 second timeout
- **Features**: Icon + message + optional close button
- **Styling**: Uses CSS variables for colors
- **Size**: 120 lines

#### AchievementNotificationToast:
- Achievement-specific notification styling
- Custom animation

**Migration Opportunity**: Replace with Bits UI Toast/Sonner integration for better stacking, dismissal, and variants.

---

### 8. **Form Input Components**

#### Located in `/src/lib/shared/settings/components/`:

| Component | Implementation | Type | Notes |
|-----------|----------------|------|-------|
| **TextInput** | Custom wrapper | Text/Email/Password | 130 lines, uses haptic feedback |
| **SelectInput** | Custom wrapper | Dropdown select | 140 lines, normalized options |
| **ToggleSetting** | Implied | Toggle switch | See IOSToggle for style |

#### Located in `/src/lib/modules/about/components/contact/`:
- **ContactForm** - Custom form with validation

**Current Pattern**: Wrapped native inputs with glassmorphic styling, haptic feedback, and CSS variable theming.

**Migration Target**: Bits UI Form components + shadcn-svelte form validation utilities.

---

### 9. **Grid/List Components**

#### Preset Grid:
- **PresetGrid** - Custom grid for preset display
- **PresetCard** - Individual preset card

#### Icon Grid:
- **IconGrid** - Icon picker grid
- **CAPComponentGrid** - CAP component selection grid

#### Filter/Sort:
- **ExploreGrid** - Explore module grid
- **SequenceGrid** - Write module sequence grid
- **PictographGrid** - Pictograph selection grid

#### Resource Grid:
- **ResourceGrid** - Resource card display
- **ResourceCard** - Individual resource

**Current Pattern**: Custom CSS Grid with Embla Carousel for swiping.

**Migration Opportunity**: Bits UI doesn't provide grid components (use CSS Grid directly), but can enhance with better card primitives.

---

### 10. **Navigation/Tab Components**
Located across modules:

| Component | Type | Location |
|-----------|------|----------|
| **PrimaryNavigation** | Main nav | Shared |
| **ModuleList** | Module switcher | Shared |
| **SettingsSidebar** | Settings nav | Settings |
| **UnifiedNavigationMenu** | Menu drawer | Shared |
| **ExploreTabNavigation** | Tab nav | Explore module |
| **LearnTabHeader** | Section header | Learn module |

**Current Implementation**: Custom CSS with tab-like styling, FontAwesome icons.

**Migration Target**: Bits UI Tabs component for better accessibility and keyboard navigation.

---

## Current Design System

### Styling Approach:
- **System**: CSS Variables + Component-Scoped CSS
- **No Tailwind CSS** (despite being in prettier plugins)
- **Design Pattern**: Glassmorphism (blur, transparency, gradients)
- **Responsive**: Mobile-first with breakpoints at 480px, 768px
- **Accessibility**: ARIA labels, keyboard support, high contrast media queries
- **Motion**: Respects `prefers-reduced-motion`

### Color Palette (from app.css):
```css
--primary-color: #6366f1 (Indigo)
--primary-light: #818cf8
--primary-dark: #4f46e5
--secondary-color: #ec4899 (Pink)
--secondary-light: #f472b6
--secondary-dark: #db2777
--accent-color: #06b6d4 (Cyan)
--accent-light: #22d3ee
--accent-dark: #0891b2
```

### Glass Morphism Effects:
- Consistent use of `backdrop-filter: blur()`
- Semi-transparent backgrounds with rgba
- Subtle borders with `rgba(255, 255, 255, 0.1-0.2)`
- Gradient overlays for depth

---

## Component Usage Patterns

### 1. **Service Injection**
All interactive components follow this pattern:
```typescript
import type { IHapticFeedbackService } from "$shared";
import { resolve, TYPES } from "$shared";

let hapticService: IHapticFeedbackService;

onMount(() => {
  hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
});

// Usage:
hapticService?.trigger("selection"); // or "success", "warning"
```

**Impact**: Any component replacement must integrate with this DI container pattern.

### 2. **Event Handling**
Standard patterns:
```typescript
// Props-based callbacks
export let onchange: (value: T) => void;
export let onClose: () => void;

// Svelte 5 runes
let { value = $bindable() } = $props();
```

### 3. **Styling Composition**
```svelte
<button class="button-base" class:primary={variant === 'primary'}>
  {label}
</button>
```

Uses combined class binding with CSS modules.

### 4. **Accessibility**
- All interactive elements have proper ARIA attributes
- Keyboard event handling (Escape, Enter, Arrow keys)
- Focus management (focus traps in modals)
- High contrast mode support
- Reduced motion support

### 5. **Mobile Optimization**
- Touch-friendly sizing (44px minimum target)
- Safe area insets for notched devices
- Responsive breakpoints
- Swipe gesture support via vaul-svelte

---

## Architecture by Module

### Create Module (`/modules/create/`)
**Most Complex Module** - Heavy use of:
- Modal dialogs (preset selection, CAP selection, GIF export)
- Sheet panels (share panel)
- Custom forms (handpath builder, option picker)
- Toolbar buttons (play, save, export)
- Toast notifications

**Recommendation**: Prioritize Bits UI adoption here for:
- Dialog consistency (PresetSelectionModal, CAPSelectionModal, GifExportDialog)
- Form controls (in edit panels)
- Button variants (SequenceActionsButton)

### Explore Module (`/modules/explore/`)
**Features**:
- Filter panels (FilterModal, CompactFilterPanel)
- Grid display (ExploreGrid)
- Navigation (NavigationSidebar, QuickAccessSection)

**Recommendation**: 
- Filter modal → Bits UI Popover
- Grids → Stay CSS Grid, enhance cards with Bits primitives

### Learn Module (`/modules/learn/`)
**Features**:
- Quiz components (AnswerButton, QuestionGenerator)
- Codex (interactive pictograph grids)
- Progress tracking

**Recommendation**:
- Quiz buttons → Bits UI Button variants
- Progress indicators → Bits UI Progress

### Settings System (`/shared/settings/`)
**Features**:
- Tab navigation (SettingsSidebar)
- Form inputs (TextInput, SelectInput)
- Settings sheet (SettingsSheet)

**Status**: Recently modernized with vaul-svelte
**Next Step**: Replace TextInput/SelectInput with Bits UI equivalents

---

## Dependency Analysis

### Currently Installed UI Libraries:
```json
{
  "bits-ui": "^2.14.2",        // Installed, unused
  "vaul-svelte": "^1.0.0-next.7", // Active (Drawer wrapper)
  "embla-carousel-svelte": "^8.6.0" // Active (grid swiping)
}
```

### Supporting Libraries:
- `@formkit/auto-animate`: Auto-animation on DOM changes
- `xstate`: State machine (for complex flows)
- `zod`: Schema validation
- `@fortawesome/fontawesome-free`: Icons (7.0.1)

### No Usage Of:
- Headless UI libraries
- Radix UI (Bits UI is Radix-based)
- shadcn-svelte (not installed, but pairs well with Bits UI)
- Tailwind CSS (CSS variables only)

---

## Migration Roadmap Overview

### Phase 1: Low-Hanging Fruit (Weeks 1-2)
- Convert IOSToggle → Bits UI Switch
- Convert SelectInput → Bits UI Select  
- Convert TextInput → Bits UI Input
- Add Bits UI Button as standardized button component

**Effort**: ~40 components affected
**Risk**: Low (isolated form controls)

### Phase 2: Core Primitives (Weeks 3-4)
- Convert ConfirmDialog → Bits UI Dialog + Modal
- Enhance other Dialogs with Bits UI Dialog/Modal
- Add Bits UI Tooltip for help text
- Implement Bits UI Popover for dropdowns

**Effort**: ~15 components affected
**Risk**: Medium (state coordination with modals)

### Phase 3: Advanced Components (Weeks 5-6)
- Replace Toast system with Bits UI Toast/Sonner
- Implement Bits UI Combobox for advanced selects
- Add Bits UI Accordion for collapsible sections
- Implement Bits UI DropdownMenu for more menus

**Effort**: ~20 components affected
**Risk**: Medium (requires testing)

### Phase 4: Layout & Navigation (Weeks 7-8)
- Refactor Splitter with Bits UI (already available)
- Enhance navigation with Bits UI NavigationMenu
- Implement Bits UI Breadcrumb navigation
- Add Bits UI Pagination

**Effort**: ~10 components affected
**Risk**: Low (mostly additive)

### Phase 5: Advanced Patterns (Weeks 9+)
- Create shadcn-svelte form components
- Implement advanced validation with Zod + Bits UI
- Add data tables with Bits UI Checkbox/Row selection
- Create reusable form field wrapper

**Effort**: ~30+ new components
**Risk**: Medium-High (new abstraction layer)

---

## Quick Stats

| Metric | Value |
|--------|-------|
| **Total .svelte components** | 300+ |
| **Foundation UI components** | 12 |
| **Modal/Dialog variants** | 15+ |
| **Custom form inputs** | 3+ |
| **Button variants** | 20+ |
| **Dropdown/Select components** | 6+ |
| **Custom CSS LOC** | ~50,000+ |
| **Bits UI adoption** | 0% (installed, unused) |
| **vaul-svelte adoption** | ~5% (Drawer + 2 sheets) |

---

## Key Findings

### Strengths:
1. **Excellent accessibility foundation** - ARIA, keyboard support already implemented
2. **Consistent styling approach** - CSS variables and component patterns
3. **Good separation of concerns** - Modular component structure
4. **DI container pattern** - Service injection enables testability
5. **Mobile-first design** - Touch-friendly, responsive

### Weaknesses:
1. **High custom component burden** - 93% custom modals/dialogs
2. **Unused dependency** - bits-ui@2.14.2 installed but not used
3. **Inconsistent button implementation** - 20+ different button styles
4. **Limited form validation** - Native HTML inputs without validation libs
5. **No unified popover/tooltip system** - No reusable positioning primitives

### Opportunities:
1. **Reduce maintenance burden** - Replace 100+ custom components
2. **Improve type safety** - Bits UI provides TypeScript support
3. **Better accessibility** - Bits UI handles complex ARIA patterns
4. **Faster development** - Standardized component APIs
5. **Mobile experience** - Better gesture handling with vaul-svelte
6. **Design consistency** - Unified component variants

---

## Bits UI + shadcn-svelte Fit Analysis

### Why Bits UI is Perfect for TKA:
1. **Svelte-native**: Built specifically for Svelte
2. **Headless**: Pairs perfectly with existing CSS Variable system
3. **Accessibility**: WCAG AAA compliant out-of-the-box
4. **Type-safe**: Full TypeScript support
5. **Customizable**: Works with any CSS approach
6. **Already installed**: No dependency changes needed

### Why shadcn-svelte Fits:
1. **Extends Bits UI**: Provides styled layer on top
2. **Copy-paste model**: Full control over component code
3. **Theming**: Built-in support for CSS variables
4. **Small bundle**: Only ship what you use
5. **No lock-in**: Pure Svelte components

### Recommended Integration Approach:
1. **Use Bits UI primitives** for core interactive behavior (Dialog, Select, etc.)
2. **Extend with custom styling** to match glassmorphism theme
3. **Optional**: Use shadcn-svelte base components as reference
4. **Maintain CSS variables**: Keep existing design system tokens

---

## Next Steps

1. **Create Bits UI wrapper components** that extend the library with your glassmorphic styling
2. **Set up design tokens** for typography, spacing, colors
3. **Create component documentation** with examples for each Bits UI component used
4. **Plan migration sprints** focusing on high-impact components first
5. **Establish testing strategy** for component replacements
6. **Create storybook** for component showcase and testing

---

## Appendix: Component Directory Structure

```
src/lib/
├── shared/
│   ├── foundation/ui/              # 12 foundation components
│   │   ├── ConfirmDialog.svelte     # Custom modal (HIGH PRIORITY)
│   │   ├── Drawer.svelte            # vaul-svelte wrapper (reference)
│   │   ├── IOSToggle.svelte         # Custom toggle (HIGH PRIORITY)
│   │   ├── ErrorBanner.svelte       # Custom banner
│   │   └── ... (7 more)
│   ├── settings/components/        # Form components
│   │   ├── TextInput.svelte         # Custom input (HIGH PRIORITY)
│   │   ├── SelectInput.svelte       # Custom select (HIGH PRIORITY)
│   │   └── SettingsSheet.svelte     # vaul-svelte sheet (reference)
│   ├── navigation/components/       # Nav components
│   └── ...
├── modules/
│   ├── create/
│   │   ├── generate/components/modals/  # 5+ modal components
│   │   └── ...
│   ├── explore/
│   │   ├── filtering/components/        # FilterModal (HIGH PRIORITY)
│   │   └── ...
│   ├── learn/                          # Quiz components
│   └── ...
└── ...
```

---

## Document Version
- **Created**: 2025-11-04
- **Status**: Ready for Implementation Planning
- **Author**: Component Architecture Analysis
