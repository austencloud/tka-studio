<!-- Primary Navigation - Responsive Bottom/Side Navigation -->
<!-- Automatically adapts between bottom (portrait) and side (landscape) layouts -->
<script lang="ts">
  import {
    resolve,
    TYPES,
    type IDeviceDetector,
    type IHapticFeedbackService,
  } from "$shared";
  import type { ResponsiveSettings } from "$shared/device/domain/models/device-models";
  import { onMount } from "svelte";
  import {
    getShowSettings,
    toggleSettingsDialog,
  } from "../../application/state/app-state.svelte";
  import type { Section } from "../domain/types";

  let {
    sections = [],
    currentSection,
    onSectionChange,
    onModuleSwitcherTap,
    onLayoutChange,
    showModuleSwitcher = true,
    showSettings = true,
  } = $props<{
    sections: Section[];
    currentSection: string;
    onSectionChange?: (sectionId: string) => void;
    onModuleSwitcherTap?: () => void;
    onLayoutChange?: (isLandscape: boolean) => void;
    showModuleSwitcher?: boolean;
    showSettings?: boolean;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;
  let deviceDetector: IDeviceDetector | null = null;

  // Responsive settings from DeviceDetector (single source of truth)
  let responsiveSettings = $state<ResponsiveSettings | null>(null);

  // Layout state - use DeviceDetector instead of duplicating logic
  let isLandscape = $derived(responsiveSettings?.isLandscapeMobile ?? false);

  // Ref to nav element for container query support detection
  let navElement = $state<HTMLElement | null>(null);

  // Abbreviated labels for compact mode
  const abbreviations: Record<string, string> = {
    Construct: "Construct",
    Generate: "Generate",
    Settings: "Settings",
    Menu: "Menu",
  };

  function handleSectionTap(section: Section) {
    if (!section.disabled) {
      hapticService?.trigger("selection");
      onSectionChange?.(section.id);
    }
  }

  function handleModuleSwitcher() {
    hapticService?.trigger("selection");
    onModuleSwitcherTap?.();
  }

  function handleSettingsTap() {
    hapticService?.trigger("selection");
    toggleSettingsDialog();
  }

  // Get abbreviated label if available
  function getCompactLabel(fullLabel: string): string {
    return abbreviations[fullLabel] || fullLabel;
  }

  // Notify parent when layout changes (reactive to isLandscape derived value)
  $effect(() => {
    // Notify parent of current layout state when it changes
    onLayoutChange?.(isLandscape);
    return undefined;
  });

  onMount(() => {
    // Initialize services
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    // Resolve DeviceDetector service
    try {
      deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);

      // Get initial responsive settings
      responsiveSettings = deviceDetector.getResponsiveSettings();

      // Return cleanup function from onCapabilitiesChanged
      const cleanup = deviceDetector.onCapabilitiesChanged(() => {
        responsiveSettings = deviceDetector!.getResponsiveSettings();
      });
      return cleanup || undefined;
    } catch (error) {
      console.warn(
        "PrimaryNavigation: Failed to resolve DeviceDetector",
        error
      );
    }

    // Feature detection for container queries
    if (navElement && !CSS.supports("container-type: inline-size")) {
      console.warn(
        "Container queries not supported - falling back to media queries"
      );
    }

    return undefined;
  });
</script>

<nav
  class="primary-navigation glass-surface"
  class:layout-bottom={!isLandscape}
  class:layout-side={isLandscape}
  bind:this={navElement}
>
  <!-- Module Switcher Button (Left) -->
  {#if showModuleSwitcher}
    <button
      class="nav-button module-switcher"
      onclick={handleModuleSwitcher}
      aria-label="Switch module"
      style="--section-color: rgba(255, 255, 255, 1); --section-gradient: rgba(255, 255, 255, 1);"
    >
      <span class="nav-icon"><i class="fas fa-bars"></i></span>
      <span class="nav-label nav-label-full">Menu</span>
      <span class="nav-label nav-label-compact">{getCompactLabel("Menu")}</span>
    </button>
  {/if}

  <!-- Current Module's Sections -->
  <div class="sections">
    {#each sections as section}
      <button
        class="nav-button"
        class:active={currentSection === section.id}
        class:disabled={section.disabled}
        onclick={() => handleSectionTap(section)}
        disabled={section.disabled}
        aria-label={section.label}
        style="--section-color: {section.color ||
          'var(--muted-foreground)'}; --section-gradient: {section.gradient ||
          section.color ||
          'var(--muted-foreground)'};"
      >
        <span class="nav-icon">{@html section.icon}</span>
        <span class="nav-label nav-label-full">{section.label}</span>
        <span class="nav-label nav-label-compact"
          >{getCompactLabel(section.label)}</span
        >
      </button>
    {/each}
  </div>

  <!-- Settings Button (Right) -->
  {#if showSettings}
    <button
      class="nav-button settings-button"
      class:active={getShowSettings()}
      onclick={handleSettingsTap}
      aria-label="Settings"
      style="--section-color: rgba(255, 255, 255, 1); --section-gradient: rgba(255, 255, 255, 1);"
    >
      <span class="nav-icon"><i class="fas fa-cog"></i></span>
      <span class="nav-label nav-label-full">Settings</span>
      <span class="nav-label nav-label-compact"
        >{getCompactLabel("Settings")}</span
      >
    </button>
  {/if}
</nav>

<style>
  /* ============================================================================
     BASE PRIMARY NAVIGATION STYLES
     ============================================================================ */
  .primary-navigation {
    position: fixed;
    display: flex;
    gap: 4px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: var(--glass-backdrop-strong);
    z-index: 100;
  }

  /* ============================================================================
     BOTTOM LAYOUT (Portrait Mobile)
     ============================================================================ */
  .primary-navigation.layout-bottom {
    bottom: 0;
    left: 0;
    right: 0;
    flex-direction: row;
    align-items: center;
    padding: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    /* Account for iOS safe area */
    padding-bottom: max(8px, env(safe-area-inset-bottom));
    min-height: 64px;
    /* Remove bottom corners border-radius since it comes out of the bottom */
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;

    /* Enable container queries for responsive labels */
    container-type: inline-size;
    container-name: primary-nav;
  }

  /* ============================================================================
     SIDE LAYOUT (Landscape Mobile)
     ============================================================================ */
  .primary-navigation.layout-side {
    left: 0;
    top: 0;
    bottom: 0;
    flex-direction: column;
    align-items: center;
    padding: 8px 4px;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    width: 72px;
    /* Account for safe area on sides */
    padding-left: max(4px, env(safe-area-inset-left));
    min-height: 100vh;
  }

  /* ============================================================================
     SECTIONS CONTAINER
     ============================================================================ */
  /* Bottom layout - horizontal sections */
  .layout-bottom .sections {
    display: flex;
    flex-direction: row;
    gap: 4px;
    flex: 1;
    justify-content: center;
    align-items: center;
    min-width: 0; /* Allow flex shrinking */
  }

  /* Side layout - vertical sections */
  .layout-side .sections {
    display: flex;
    flex-direction: column;
    gap: 6px;
    flex: 1;
    justify-content: center;
    align-items: center;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    /* Hide scrollbar but keep functionality */
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  .layout-side .sections::-webkit-scrollbar {
    display: none;
  }

  /* ============================================================================
     BUTTON STYLES
     ============================================================================ */
  /* Base button styles */
  .nav-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    background: transparent;
    border: none;
    border-radius: 50%;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
  }

  /* Bottom layout - horizontal buttons with labels */
  .layout-bottom .nav-button {
    padding: 6px 8px;
    min-width: 44px;
    min-height: 44px;
    flex: 1 1 auto;
    max-width: 80px;
    border-radius: 12px; /* Section buttons remain rounded rectangles */
  }

  /* Menu and Settings buttons match top bar style - circular */
  .layout-bottom .module-switcher,
  .layout-bottom .settings-button {
    flex: 0 0 auto;
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    padding: 0;
    border-radius: 50%; /* Circular like top bar buttons */
  }

  /* Remove unused selector - keeping this comment for reference */
  /* .module-switcher.active - removed as it was unused */

  /* Side layout - icon-only buttons */
  .layout-side .nav-button {
    padding: 8px;
    min-width: 56px;
    min-height: 56px;
    width: 56px;
    flex: 0 0 auto;
    border-radius: 12px; /* Section buttons remain rounded rectangles */
  }

  /* Menu and Settings buttons match top bar style - circular */
  .layout-side .module-switcher,
  .layout-side .settings-button {
    flex-shrink: 0;
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    padding: 0;
    border-radius: 50%; /* Circular like top bar buttons */
  }

  .nav-button:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.15);
    transform: scale(1.05);
  }

  .nav-button:active {
    transform: scale(0.95);
  }

  .nav-button.active {
    color: rgba(255, 255, 255, 1);
    background: rgba(255, 255, 255, 0.1);
  }

  /* Menu and Settings buttons - match top bar hover behavior */
  .module-switcher:hover:not(.disabled),
  .settings-button:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.15);
    transform: scale(1.05);
  }

  .settings-button.active {
    background: rgba(255, 255, 255, 0.1);
  }

  .nav-button.disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .nav-button.disabled:active {
    transform: none;
  }

  .nav-icon {
    /* Container-aware icon sizing */
    font-size: clamp(18px, 4cqi, 22px);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all var(--transition-fast);
  }

  /* Style Font Awesome icons with gradient colors - matches top navigation */
  .nav-icon :global(i) {
    background: var(--section-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 8px rgba(0, 0, 0, 0.2));
  }

  /* Fallback for browsers that don't support background-clip */
  @supports not (background-clip: text) {
    .nav-icon :global(i) {
      color: var(--section-color);
      background: none;
      -webkit-text-fill-color: initial;
    }
  }

  /* Inactive buttons have reduced opacity */
  .nav-button:not(.active) .nav-icon :global(i) {
    opacity: 0.6;
  }

  .nav-button:hover .nav-icon :global(i) {
    opacity: 1;
    filter: drop-shadow(0 0 12px rgba(0, 0, 0, 0.3));
  }

  /* Active button has full color and glow */
  .nav-button.active .nav-icon :global(i) {
    opacity: 1;
    filter: drop-shadow(0 0 16px var(--section-color)) brightness(1.1);
  }

  /* Disabled buttons remain grayed out */
  .nav-button.disabled .nav-icon {
    opacity: 0.3;
    filter: grayscale(1);
  }

  .nav-button.disabled .nav-icon :global(i) {
    color: var(--muted-foreground);
  }

  /* ============================================================================
     LABEL SYSTEM
     ============================================================================ */
  .nav-label {
    /* Container-aware label sizing */
    font-size: clamp(9px, 2cqi, 11px);
    font-weight: 500;
    text-align: center;
    white-space: nowrap;
    line-height: 1.2;
  }

  /* Labels hidden by default */
  .nav-label-full,
  .nav-label-compact {
    display: none;
  }

  /* Side layout - always hide labels (icon-only) */
  .layout-side .nav-label {
    display: none !important;
  }

  /*
    Bottom Layout Container Query Breakpoints:
    - >= 600px: Full labels (Menu, Construct, Generate, Animate, Share, Settings)
    - 450-599px: Compact labels (Menu, Build, Gen, Play, Share, Set)
    - < 450px: Icons only
  */

  /* Full labels mode (spacious - 600px+) */
  @container primary-nav (min-width: 600px) {
    .layout-bottom .nav-label-full {
      display: block;
    }

    .layout-bottom .nav-button {
      max-width: 90px;
      gap: 4px;
    }

    .layout-bottom .module-switcher,
    .layout-bottom .settings-button {
      max-width: 80px;
    }
  }

  /* Compact labels mode (tight - 450-599px) */
  @container primary-nav (min-width: 450px) and (max-width: 599px) {
    .layout-bottom .nav-label-compact {
      display: block;
    }

    .layout-bottom .nav-button {
      max-width: 70px;
      gap: 2px;
      padding: 6px 4px;
    }

    .layout-bottom .nav-label {
      /* Slightly smaller in compact mode */
      font-size: clamp(8px, 1.8cqi, 10px);
    }
  }

  /* Icons only mode (cramped - < 450px) */
  @container primary-nav (max-width: 449px) {
    .layout-bottom .nav-button {
      max-width: 52px;
      padding: 6px 4px;
    }

    .layout-bottom .nav-icon {
      /* Larger icons when labels are hidden */
      font-size: clamp(20px, 5cqi, 24px);
    }
  }

  /* Fallback for browsers without container query support */
  @supports not (container-type: inline-size) {
    /* Use viewport-based media queries as fallback */

    /* Full labels */
    @media (min-width: 600px) {
      .layout-bottom .nav-label-full {
        display: block;
      }
    }

    /* Compact labels */
    @media (min-width: 450px) and (max-width: 599px) {
      .layout-bottom .nav-label-compact {
        display: block;
      }

      .layout-bottom .nav-button {
        max-width: 70px;
        padding: 6px 4px;
      }
    }

    /* Icons only - default state, labels already hidden */
    @media (max-width: 449px) {
      .layout-bottom .nav-icon {
        font-size: 22px;
      }
    }
  }

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  /* High contrast mode */
  @media (prefers-contrast: high) {
    .primary-navigation {
      background: rgba(0, 0, 0, 0.95);
    }

    .primary-navigation.layout-bottom {
      border-top: 2px solid white;
    }

    .primary-navigation.layout-side {
      border-right: 2px solid white;
    }

    .nav-button.active {
      background: rgba(255, 255, 255, 0.3);
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .nav-button {
      transition: none;
    }

    .nav-button:active {
      transform: none;
    }
  }
</style>
