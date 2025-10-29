<!-- Enhanced Navigation Bar with Module-based Navigation -->
<script lang="ts">
  import { onMount } from "svelte";
  import { ModuleMenuSection, SettingsButton, SubModeTabs } from ".";
  import type { IAnimationService } from "../../application/services/contracts";
  import type { IDeviceDetector } from "../../device/services/contracts/IDeviceDetector";
  import { resolve, TYPES } from "../../inversify";
  import type { ModeOption, ModuleDefinition, ModuleId } from "../domain/types";

  let {
    // Module-based props
    currentModule,
    currentModuleName,
    currentSubMode,
    subModeTabs = [],
    onSubModeChange,
    onModuleChange,
    modules = [],
    // Layout props
    navigationLayout,
    // Legacy props for backward compatibility
    onBackgroundChange,
  } = $props<{
    // New module-based props
    currentModule: ModuleId;
    currentModuleName: string;
    currentSubMode: string;
    subModeTabs: ModeOption[];
    onSubModeChange?: (subMode: string) => void;
    onModuleChange?: (moduleId: ModuleId) => void;
    modules: ModuleDefinition[];
    // Layout props
    navigationLayout: "top" | "left" | "bottom";
    // Legacy props
    onBackgroundChange?: (background: string) => void;
  }>();

  // Resolve services asynchronously to avoid container initialization errors
  let animationService: IAnimationService | null = null;
  let deviceDetector: IDeviceDetector | null = null;

  // Landscape mobile state for responsive behavior
  let isLandscapeMobile = $state(false);

  // Overflow detection state
  let navBarElement: HTMLElement | null = $state(null);
  let navCenterElement: HTMLElement | null = $state(null);

  // Reactive measurements updated by ResizeObserver
  let navScrollWidth = $state(0);
  let navClientWidth = $state(0);

  // Overflow state (updated by effect with hysteresis logic)
  let isNavOverflowing = $state(false);

  // Update landscape mobile state based on device detection
  function updateLandscapeMobileState() {
    if (!deviceDetector) return;

    // Get landscape mobile state immediately to avoid timing issues
    isLandscapeMobile = deviceDetector.isLandscapeMobile();
  }

  // Effect: Update overflow state with hysteresis when measurements change
  // This prevents infinite toggle loops
  $effect(() => {
    if (!navCenterElement || navigationLayout !== "top") {
      isNavOverflowing = false;
      return;
    }

    // Current overflow state based on measurements
    const hasOverflow = navScrollWidth > navClientWidth;

    // HYSTERESIS: To prevent infinite toggle loop, we need different thresholds
    // for turning icon-only mode ON vs OFF
    //
    // The problem: When we detect overflow and switch to icon-only, the tabs shrink,
    // which makes scrollWidth === clientWidth, which would immediately switch back to
    // full labels, causing an infinite loop.
    //
    // Solution: When in icon-only mode, measure with full labels to check if they fit

    let shouldBeIconOnly = isNavOverflowing; // Keep current state by default

    if (!isNavOverflowing && hasOverflow) {
      // Currently showing full labels, but content is overflowing → switch to icon-only
      shouldBeIconOnly = true;
    } else if (isNavOverflowing && !hasOverflow) {
      // Currently showing icons and no overflow detected
      // Temporarily remove icon-only class to measure if full labels would fit
      const subModeTabs = navCenterElement.querySelector(".sub-mode-tabs");
      if (subModeTabs) {
        subModeTabs.classList.remove("icon-only");

        // Force layout recalculation and measure
        const fullLabelScrollWidth = navCenterElement.scrollWidth;
        const fullLabelClientWidth = navCenterElement.clientWidth;
        const wouldOverflowWithFullLabels =
          fullLabelScrollWidth > fullLabelClientWidth;

        // Restore icon-only class immediately
        subModeTabs.classList.add("icon-only");

        // Only switch to full labels if they would fit
        if (!wouldOverflowWithFullLabels) {
          shouldBeIconOnly = false;
        }
      }
    }

    // Update state if changed
    if (shouldBeIconOnly !== isNavOverflowing) {
      isNavOverflowing = shouldBeIconOnly;
    }
  });

  // Measure nav center dimensions (where tabs overflow) whenever they change
  function updateNavMeasurements() {
    if (!navCenterElement || navigationLayout !== "top") {
      navScrollWidth = 0;
      navClientWidth = 0;
      return;
    }

    navScrollWidth = navCenterElement.scrollWidth;
    navClientWidth = navCenterElement.clientWidth;
  }

  // Reactive effect: Update measurements when subModeTabs array changes
  // This ensures overflow detection reacts to dynamic tab additions/removals
  $effect(() => {
    // Track the subModeTabs array length to trigger on changes
    const tabCount = subModeTabs.length;

    // Schedule measurement update after DOM updates complete
    // This allows the new tabs to render before we measure
    if (tabCount > 0 && navCenterElement) {
      // Use requestAnimationFrame to wait for layout
      requestAnimationFrame(() => {
        updateNavMeasurements();
      });
    }
  });

  // Initialize services when container is ready
  onMount(() => {
    // Use sync resolution (container already initialized)
    animationService = resolve<IAnimationService>(TYPES.IAnimationService);
    deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);

    // Initialize landscape mobile state immediately
    updateLandscapeMobileState();

    // Listen for resize and orientation changes
    const handleResize = () => {
      updateLandscapeMobileState();
      // Use requestAnimationFrame to ensure layout has completed before measuring
      requestAnimationFrame(() => {
        updateNavMeasurements();
      });
    };

    window.addEventListener("resize", handleResize);
    window.addEventListener("orientationchange", handleResize);

    // Set up overflow detection for top layout only
    let resizeObserver: ResizeObserver | null = null;
    if (navigationLayout === "top" && navCenterElement) {
      resizeObserver = new ResizeObserver(() => {
        // Use requestAnimationFrame to ensure layout has completed before measuring
        requestAnimationFrame(() => {
          updateNavMeasurements();
        });
      });

      resizeObserver.observe(navCenterElement);

      // Initial measurements with multiple attempts to ensure DOM is fully rendered
      setTimeout(() => {
        requestAnimationFrame(() => updateNavMeasurements());
      }, 0);
      setTimeout(() => {
        requestAnimationFrame(() => updateNavMeasurements());
      }, 100);
      setTimeout(() => {
        requestAnimationFrame(() => updateNavMeasurements());
      }, 500);
    }

    // Cleanup listeners
    return () => {
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("orientationchange", handleResize);
      resizeObserver?.disconnect();
    };
  });

  // Device detection - handle null service gracefully
  const isMobile = $derived(() => deviceDetector?.isMobile() ?? false);

  // Create fold transition - handle null service gracefully
  const foldTransition = (node: Element, params: any) => {
    if (!animationService) {
      // Fallback transition if service not ready
      return {
        duration: 300,
        css: (t: number) => `opacity: ${t}`,
      };
    }
    return animationService.createFoldTransition({
      direction: "fold-in",
      duration: 300,
      ...params,
    });
  };
</script>

<!-- App Navigation -->
<nav
  bind:this={navBarElement}
  class="app-navigation-bar glass-surface"
  class:layout-top={navigationLayout === "top"}
  class:layout-left={navigationLayout === "left"}
  in:foldTransition={{ direction: "fold-in", duration: 300 }}
>
  <!-- Left: Hamburger Menu Button with Module Selector -->
  <div class="nav-left">
    <ModuleMenuSection
      {modules}
      {currentModule}
      {currentModuleName}
      isMobile={isMobile()}
      {onModuleChange}
    />
  </div>

  <!-- Center: Sub-mode Tabs -->
  <div
    bind:this={navCenterElement}
    class="nav-center"
    class:icon-only-mode={isNavOverflowing}
  >
    {#if currentModule !== "build"}
      <SubModeTabs
        {subModeTabs}
        {currentSubMode}
        {navigationLayout}
        {onSubModeChange}
        forceIconOnly={isNavOverflowing}
      />
    {/if}
  </div>

  <!-- Right: App Actions -->
  <div class="nav-right">
    <SettingsButton {navigationLayout} />
  </div>
</nav>

<style>
  /* ============================================================================
     BASE NAVIGATION BAR STYLES
     ============================================================================ */
  .app-navigation-bar {
    backdrop-filter: var(--glass-backdrop-strong);
    background: rgba(255, 255, 255, 0.05);
    position: relative;
    z-index: 100;
    /* Remove transition to prevent focus lightening effect */
  }

  /* Remove focus outline from navigation bar itself */
  .app-navigation-bar:focus,
  .app-navigation-bar:focus-within {
    outline: none;
  }

  /* Override glass-surface hover effect - navigation bar should not change on hover/click */
  .app-navigation-bar:hover {
    background: rgba(255, 255, 255, 0.05); /* Keep same as default */
    border: 1px solid rgba(255, 255, 255, 0.1); /* Keep same as default */
    box-shadow: var(--shadow-glass); /* Keep same as default */
  }

  /* ============================================================================
     TOP LAYOUT (Default - Horizontal Navigation)
     ============================================================================ */
  .app-navigation-bar.layout-top {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: stretch; /* Changed from center to stretch for full-height touch targets */
    padding: 0 var(--spacing-xs); /* Remove vertical padding for maximum touch targets */
    min-height: 60px; /* Ensure navigation bar has sufficient height for touch targets */
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .layout-top .nav-left {
    display: flex;
    align-items: stretch; /* Changed from center to stretch */
    justify-self: start;
    margin-left: calc(var(--spacing-xs) * -1); /* Push hamburger to corner */
    padding-left: 0;
  }

  .layout-top .nav-center {
    display: flex;
    gap: var(--spacing-lg); /* Increased from sm to lg to spread tabs out */
    justify-self: stretch; /* Fill available space in center column */
    justify-content: center; /* Center content within the space */
    align-items: stretch; /* Changed from default to stretch */
    /* CRITICAL FOR OVERFLOW DETECTION: Use auto to allow scrollWidth measurement */
    overflow: auto;
    min-width: 0; /* Allow flex item to shrink below content size */
  }

  .layout-top .nav-right {
    display: flex;
    align-items: stretch; /* Changed from center to stretch */
    justify-self: end;
  }

  /* ============================================================================
     LEFT LAYOUT (Landscape Mobile - Vertical Navigation)
     ============================================================================ */
  .app-navigation-bar.layout-left {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 72px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: var(--spacing-xs) var(--spacing-xs);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: none;
  }

  /* Tighter spacing for very short heights */
  @media (max-height: 400px) {
    .app-navigation-bar.layout-left {
      padding: 4px 4px;
    }
  }

  .layout-left .nav-left {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 72px;
    margin-bottom: var(--spacing-sm);
    flex-shrink: 0;
  }

  /* Reduce margins for short heights */
  @media (max-height: 400px) {
    .layout-left .nav-left {
      margin-bottom: 4px;
    }
  }

  .layout-left .nav-center {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    align-items: center;
    justify-content: space-evenly; /* Distribute buttons evenly in vertical space */
    flex: 1;
    width: 100%;
    max-width: 72px;
    overflow-y: auto;
    overflow-x: hidden;
    padding: var(--spacing-xs) 0;
    /* Hide scrollbar but keep functionality */
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  /* Tighter gaps for very short heights */
  @media (max-height: 400px) {
    .layout-left .nav-center {
      gap: 2px;
      padding: 2px 0;
    }
  }

  .layout-left .nav-center::-webkit-scrollbar {
    display: none;
  }

  .layout-left .nav-right {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 72px;
    margin-top: var(--spacing-sm);
    flex-shrink: 0;
  }

  /* Reduce margins for short heights */
  @media (max-height: 400px) {
    .layout-left .nav-right {
      margin-top: 4px;
    }
  }

  /* ============================================================================
     RESPONSIVE BREAKPOINTS
     ============================================================================ */
  @media (max-width: 500px) {
    .app-navigation-bar.layout-top {
      padding: var(--spacing-xs) var(--spacing-xs);
    }

    .layout-top .nav-center {
      gap: var(--spacing-xs);
    }
  }

  /* ============================================================================
     ACCESSIBILITY & MOTION
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .app-navigation-bar {
      transition: none;
    }
  }

  @media (prefers-contrast: high) {
    .app-navigation-bar {
      background: rgba(0, 0, 0, 0.9);
      border-bottom: 2px solid white;
    }

    .app-navigation-bar.layout-left {
      border-right: 2px solid white;
      border-bottom: none;
    }
  }
</style>
