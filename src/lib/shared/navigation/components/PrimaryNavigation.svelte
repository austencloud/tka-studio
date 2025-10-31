<!-- Primary Navigation - Responsive Bottom/Side Navigation -->
<!-- Automatically adapts between bottom (portrait) and side (landscape) layouts -->
<script lang="ts">
  import { onMount } from "svelte";
  import {
    getShowSettings,
    toggleSettingsDialog,
  } from "../../application/state/app-state.svelte";
  import type { ModeOption } from "../domain/types";
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";

  let {
    subModeTabs = [],
    currentSubMode,
    onSubModeChange,
    onModuleSwitcherTap,
    onLayoutChange,
  } = $props<{
    subModeTabs: ModeOption[];
    currentSubMode: string;
    onSubModeChange?: (subModeId: string) => void;
    onModuleSwitcherTap?: () => void;
    onLayoutChange?: (isLandscape: boolean) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Window dimensions for reactive layout detection
  let innerWidth = $state(0);
  let innerHeight = $state(0);

  // Layout state - determines if we show bottom or side navigation
  // Computed reactively from window dimensions using the same logic as DeviceDetector.isLandscapeMobile()
  //
  // Criteria for landscape mobile navigation:
  // - Currently in landscape orientation (width > height)
  // - Very wide aspect ratio (> 1.7:1) indicating phone-like proportions
  // - Low height (<= 600px) indicating phone/small tablet, not desktop
  let isLandscape = $derived.by(() => {
    if (innerWidth === 0 || innerHeight === 0) return false;

    const isLandscapeOrientation = innerWidth > innerHeight;
    const aspectRatio = innerWidth / innerHeight;
    const isWideAspectRatio = aspectRatio > 1.7; // Includes most phone landscape orientations
    const isLowHeight = innerHeight <= 600; // Phone and small tablet height (increased from 500)

    return isLandscapeOrientation && isWideAspectRatio && isLowHeight;
  });

  // Ref to nav element for container query support detection
  let navElement = $state<HTMLElement | null>(null);

  // Abbreviated labels for compact mode
  const abbreviations: Record<string, string> = {
    Construct: "Build",
    Generate: "Gen",
    Animate: "Play",
    Share: "Share",
    Settings: "Set",
    Menu: "Menu",
  };

  function handleSubModeTap(subMode: ModeOption) {
    if (!subMode.disabled) {
      hapticService?.trigger("selection");
      onSubModeChange?.(subMode.id);
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
    // Access innerWidth and innerHeight to trigger reactivity
    // when window dimensions change
    innerWidth;
    innerHeight;

    // Notify parent of current layout state
    onLayoutChange?.(isLandscape);
  });

  onMount(() => {
    // Initialize services
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    // Initialize window dimensions immediately if not already set by binding
    if (innerWidth === 0 || innerHeight === 0) {
      innerWidth = window.innerWidth;
      innerHeight = window.innerHeight;
    }

    // Feature detection for container queries
    if (navElement && !CSS.supports("container-type: inline-size")) {
      console.warn(
        "Container queries not supported - falling back to media queries"
      );
    }
  });
</script>

<!-- Bind to window dimensions for reactive layout detection -->
<svelte:window bind:innerWidth bind:innerHeight />

<nav
  class="primary-navigation glass-surface"
  class:layout-bottom={!isLandscape}
  class:layout-side={isLandscape}
  bind:this={navElement}
>
  <!-- Module Switcher Button (Left) -->
  <button
    class="nav-button module-switcher"
    onclick={handleModuleSwitcher}
    aria-label="Switch module"
    style="--tab-color: rgba(255, 255, 255, 1); --tab-gradient: rgba(255, 255, 255, 1);"
  >
    <span class="nav-icon"><i class="fas fa-bars"></i></span>
    <span class="nav-label nav-label-full">Menu</span>
    <span class="nav-label nav-label-compact">{getCompactLabel("Menu")}</span>
  </button>

  <!-- Current Module's Sub-Mode Tabs -->
  <div class="sub-mode-tabs">
    {#each subModeTabs as subMode}
      <button
        class="nav-button"
        class:active={currentSubMode === subMode.id}
        class:disabled={subMode.disabled}
        onclick={() => handleSubModeTap(subMode)}
        disabled={subMode.disabled}
        aria-label={subMode.label}
        style="--tab-color: {subMode.color ||
          'var(--muted-foreground)'}; --tab-gradient: {subMode.gradient ||
          subMode.color ||
          'var(--muted-foreground)'};"
      >
        <span class="nav-icon">{@html subMode.icon}</span>
        <span class="nav-label nav-label-full">{subMode.label}</span>
        <span class="nav-label nav-label-compact"
          >{getCompactLabel(subMode.label)}</span
        >
      </button>
    {/each}
  </div>

  <!-- Settings Button (Right) -->
  <button
    class="nav-button settings-button"
    class:active={getShowSettings()}
    onclick={handleSettingsTap}
    aria-label="Settings"
    style="--tab-color: rgba(255, 255, 255, 1); --tab-gradient: rgba(255, 255, 255, 1);"
  >
    <span class="nav-icon"><i class="fas fa-cog"></i></span>
    <span class="nav-label nav-label-full">Settings</span>
    <span class="nav-label nav-label-compact"
      >{getCompactLabel("Settings")}</span
    >
  </button>
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
     SUB-MODE TABS CONTAINER
     ============================================================================ */
  /* Bottom layout - horizontal tabs */
  .layout-bottom .sub-mode-tabs {
    display: flex;
    flex-direction: row;
    gap: 4px;
    flex: 1;
    justify-content: center;
    align-items: center;
    min-width: 0; /* Allow flex shrinking */
  }

  /* Side layout - vertical tabs */
  .layout-side .sub-mode-tabs {
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

  .layout-side .sub-mode-tabs::-webkit-scrollbar {
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
    border-radius: 12px;
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
  }

  .layout-bottom .module-switcher,
  .layout-bottom .settings-button {
    flex: 0 0 auto;
    min-width: 56px;
    max-width: 72px;
  }

  /* Side layout - icon-only square buttons */
  .layout-side .nav-button {
    padding: 8px;
    min-width: 56px;
    min-height: 56px;
    width: 56px;
    flex: 0 0 auto;
  }

  .layout-side .module-switcher,
  .layout-side .settings-button {
    flex-shrink: 0;
  }

  .nav-button:active {
    transform: scale(0.95);
  }

  .nav-button.active {
    color: rgba(255, 255, 255, 1);
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
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all var(--transition-fast);
  }

  /* Style Font Awesome icons with gradient colors - matches top navigation */
  .nav-icon :global(i) {
    background: var(--tab-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 8px rgba(0, 0, 0, 0.2));
  }

  /* Fallback for browsers that don't support background-clip */
  @supports not (background-clip: text) {
    .nav-icon :global(i) {
      color: var(--tab-color);
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
    filter: drop-shadow(0 0 16px var(--tab-color)) brightness(1.1);
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
    font-size: 10px;
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
      font-size: 9px;
    }
  }

  /* Icons only mode (cramped - < 450px) */
  @container primary-nav (max-width: 449px) {
    .layout-bottom .nav-button {
      max-width: 52px;
      padding: 6px 4px;
    }

    .layout-bottom .nav-icon {
      font-size: 22px;
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
