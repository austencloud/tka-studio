# Navigation Components Usage Analysis

## Executive Summary

The SvelteKit application has settled on a simple, clean navigation architecture with:
- **Single Top Bar** - Global header with profile/gamification buttons and module-specific content
- **Single Bottom/Side Navigation** - Adaptive primary navigation that switches between bottom bar (portrait) and side bar (landscape)
- **Unified Navigation Menu** - Slide-up panel for module switching (keyboard-accessible via Menu button in nav)

This replaces previous complex multi-component navigation patterns.

---

## Active Navigation Components (IN USE)

### 1. TopBar.svelte
- **Location**: c:\_TKA-STUDIO\src\lib\shared\navigation\components\TopBar.svelte
- **Imported In**: 
  - c:\_TKA-STUDIO\src\lib\shared\MainInterface.svelte (main entry point)
  - c:\_TKA-STUDIO\src\lib\modules\learn\quiz\components\QuizWorkspaceView.svelte (quiz-specific override)
- **Purpose**: Global top navigation bar with profile button, gamification, and module-specific content
- **Features**: Glass morphism, height 52px (mobile) / 56px (desktop)

### 2. PrimaryNavigation.svelte
- **Location**: c:\_TKA-STUDIO\src\lib\shared\navigation\components\PrimaryNavigation.svelte
- **Imported In**: c:\_TKA-STUDIO\src\lib\shared\MainInterface.svelte (conditionally)
- **Purpose**: Adaptive bottom/side navigation for section switching
- **Features**: Bottom layout (portrait) / Side layout (landscape), module switcher, section buttons, settings

### 3. UnifiedNavigationMenu.svelte
- **Location**: c:\_TKA-STUDIO\src\lib\shared\navigation\components\UnifiedNavigationMenu.svelte
- **Imported In**: c:\_TKA-STUDIO\src\lib\shared\MainInterface.svelte (always)
- **Purpose**: Slide-up panel for module switching and PWA installation
- **Features**: Bottom sheet, swipe gestures, keyboard shortcuts, module list

### 4. ModuleList.svelte
- **Location**: c:\_TKA-STUDIO\src\lib\shared\navigation\components\ModuleList.svelte
- **Imported In**: c:\_TKA-STUDIO\src\lib\shared\navigation\components\UnifiedNavigationMenu.svelte
- **Purpose**: Displays available modules with selection UI
- **Features**: Main and developer modules sections

### 5. ProfileButton.svelte
- **Location**: c:\_TKA-STUDIO\src\lib\shared\navigation\components\ProfileButton.svelte
- **Imported In**: c:\_TKA-STUDIO\src\lib\shared\navigation\components\TopBar.svelte
- **Purpose**: Global profile/account button in top bar
- **Features**: Avatar display, sign-in, opens ProfileSettingsSheet

### 6. Sheet Components (Supporting Navigation)

#### ProfileSettingsSheet.svelte
- Location: c:\_TKA-STUDIO\src\lib\shared\navigation\components\ProfileSettingsSheet.svelte
- Imported In: c:\_TKA-STUDIO\src\lib\shared\application\components\MainApplication.svelte
- Purpose: Profile settings modal sheet with Account, Subscription, Developer tabs

#### AuthSheet.svelte, TermsSheet.svelte, PrivacySheet.svelte
- Purpose: Authentication and legal documentation sheets

#### GamificationButton.svelte & AchievementsPanel.svelte
- Location: c:\_TKA-STUDIO\src\lib\shared\gamification\components\
- Imported In: TopBar.svelte
- Purpose: Achievements/gamification UI in top bar

---

## Dead Code Navigation Components (NOT IN USE)

### Components with No References:
1. **ModuleSelector.svelte** - Replaced by ModuleList + UnifiedNavigationMenu
2. **ModuleMenuSection.svelte** - Old wrapper component, never imported
3. **HamburgerMenuButton.svelte** - Only referenced by ModuleMenuSection (dead)
4. **ModuleDropdown.svelte** - Desktop dropdown pattern, only used by ModuleSelector (dead)
5. **ModuleMobileModal.svelte** - Mobile modal pattern, only used by ModuleSelector (dead)
6. **DesktopDropdown.svelte** - Desktop pattern, never imported
7. **ModulePicker.svelte** - Unknown purpose, never imported
8. **ProfileDropdown.svelte** - Old profile menu pattern, never imported
9. **SectionSheet.svelte** - Old section switching, never imported
10. **SectionTabs.svelte** - Old tab-based sections, never imported
11. **SettingsButton.svelte** - Integrated into PrimaryNavigation, never standalone imported
12. **MobileModal.svelte** - Generic modal, never imported

---

## Module-to-Primary Navigation Mapping

Modules with primary navigation (determined by moduleHasPrimaryNav() in layout-state.svelte.ts):
- build
- learn
- explore
- library
- admin

Module 'about' does NOT have primary navigation (special page).

---

## Navigation Entry Points

**Main Application Flow:**
- c:\_TKA-STUDIO\src\routes\+layout.svelte (root layout)
- c:\_TKA-STUDIO\src\lib\shared\MainInterface.svelte (renders active navigation)
- c:\_TKA-STUDIO\src\lib\shared\application\components\MainApplication.svelte (supports sheets)

---

## Key State Files

- Layout State: c:\_TKA-STUDIO\src\lib\shared\layout\layout-state.svelte.ts
- Navigation State: c:\_TKA-STUDIO\src\lib\shared\navigation\state\navigation-state.svelte.ts
- Sheet Router: c:\_TKA-STUDIO\src\lib\shared\navigation\utils\sheet-router.ts

