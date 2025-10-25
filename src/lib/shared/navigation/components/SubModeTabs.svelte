<!--
  Sub-Mode Tabs Component

  Displays navigation tabs for the current module's sub-modes (e.g., Construct, Edit, Generate).
  Adapts to horizontal or vertical layout.
  Intelligently hides labels when tabs overflow the container.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { FontAwesomeIcon, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ModeOption } from "../domain/types";

  // Helper function to extract Font Awesome icon name from HTML string
  function extractIconName(htmlString: string): string | null {
    // Match patterns like: <i class="fas fa-hammer"></i>
    const match = htmlString.match(/fa-([a-z-]+)/);
    return match ? match[1] : null;
  }

  let {
    subModeTabs = [],
    currentSubMode,
    navigationLayout,
    onSubModeChange,
    forceIconOnly = false,
  } = $props<{
    subModeTabs: ModeOption[];
    currentSubMode: string;
    navigationLayout: "top" | "left";
    onSubModeChange?: (subModeId: string) => void;
    forceIconOnly?: boolean;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Overflow detection state (local detection, can be overridden by forceIconOnly)
  let containerElement: HTMLDivElement | null = $state(null);
  let isOverflowing = $state(false);

  // Combined overflow state: either forced from parent or detected locally
  const shouldShowIconOnly = $derived(forceIconOnly || isOverflowing);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    // Set up overflow detection for top layout only
    if (navigationLayout === "top" && containerElement) {
      const resizeObserver = new ResizeObserver(() => {
        checkOverflow();
      });

      resizeObserver.observe(containerElement);

      // Also check on window resize
      window.addEventListener("resize", checkOverflow);

      // Initial check
      checkOverflow();

      return () => {
        resizeObserver.disconnect();
        window.removeEventListener("resize", checkOverflow);
      };
    }
  });

  function checkOverflow() {
    if (!containerElement || navigationLayout !== "top") return;

    // Check if the container's scroll width exceeds its client width
    // This indicates that content is overflowing
    const hasOverflow =
      containerElement.scrollWidth > containerElement.clientWidth;

    // Only update if state actually changed to avoid unnecessary re-renders
    if (hasOverflow !== isOverflowing) {
      isOverflowing = hasOverflow;
    }
  }

  // Handle sub-mode selection
  function handleSubModeSelect(subModeId: string) {
    hapticService?.trigger("navigation");
    onSubModeChange?.(subModeId);
  }
</script>

<div
  bind:this={containerElement}
  class="sub-mode-tabs"
  class:layout-left={navigationLayout === "left"}
  class:icon-only={shouldShowIconOnly && navigationLayout === "top"}
>
  {#each subModeTabs as subMode}
    <button
      class="nav-tab sub-mode-tab"
      class:active={currentSubMode === subMode.id}
      class:disabled={subMode.disabled}
      onclick={() =>
        subMode.disabled ? null : handleSubModeSelect(subMode.id)}
      disabled={subMode.disabled}
      aria-pressed={currentSubMode === subMode.id}
      aria-disabled={subMode.disabled}
      title={subMode.disabled
        ? `${subMode.label} (requires a sequence)`
        : subMode.description || subMode.label}
      style="--tab-color: {subMode.color ||
        'var(--muted-foreground)'}; --tab-gradient: {subMode.gradient ||
        subMode.color ||
        'var(--muted-foreground)'};"
    >
      <span class="tab-icon">
        {#if extractIconName(subMode.icon)}
          <FontAwesomeIcon icon={extractIconName(subMode.icon)!} size="1em" />
        {:else}
          {@html subMode.icon}
        {/if}
      </span>
      {#if navigationLayout === "top"}
        <span class="tab-label">{subMode.label}</span>
      {/if}
    </button>
  {/each}
</div>

<style>
  .sub-mode-tabs {
    display: flex;
    height: 100%; /* Fill full navigation bar height */
  }

  .sub-mode-tabs.layout-left {
    flex-direction: column;
    gap: 0px;
    align-items: center;
    height: 100%; /* Fill the nav-center container */
    justify-content: space-evenly; /* Distribute buttons evenly */
  }

  /* NAVIGATION TAB STYLES */
  .nav-tab {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    /* IMPROVED TOUCH TARGETS: Fill the full navigation bar height for easier tapping */
    padding: 0 var(--spacing-md);
    height: 100%; /* Fill full navigation bar height */
    background: transparent;
    border: none;
    border-radius: 8px;
    color: var(--muted-foreground);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: var(--font-size-sm);
    font-weight: 500;
  }

  /* Left layout tab adjustments - maximize touch targets */
  .layout-left .nav-tab {
    width: 72px; /* Full navigation bar width for maximum touch target */
    flex: 1; /* Expand to fill available vertical space */
    max-height: 80px; /* Prevent buttons from getting too tall */
    min-height: 44px; /* Minimum touch target size */
    padding: 0; /* Remove padding to maximize touch area */
    justify-content: center;
    flex-direction: column;
    gap: 0;
  }

  .nav-tab:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--foreground);
  }

  .nav-tab.active {
    background: rgba(99, 102, 241, 0.2);
    color: var(--primary-light);
    border: 1px solid rgba(99, 102, 241, 0.3);
  }

  .nav-tab.disabled {
    opacity: 0.4;
    cursor: not-allowed;
    color: var(--muted-foreground);
    pointer-events: none;
  }

  .nav-tab.disabled:hover {
    background: transparent;
    color: var(--muted-foreground);
  }

  .tab-icon {
    font-size: 16px;
    transition: all var(--transition-fast);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Style Font Awesome icons with gradient colors */
  .tab-icon :global(i) {
    background: var(--tab-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 8px rgba(0, 0, 0, 0.2));
  }

  /* Fallback for browsers that don't support background-clip */
  @supports not (background-clip: text) {
    .tab-icon :global(i) {
      color: var(--tab-color);
      background: none;
      -webkit-text-fill-color: initial;
    }
  }

  /* Inactive tabs have reduced opacity */
  .nav-tab:not(.active) .tab-icon :global(i) {
    opacity: 0.6;
  }

  .nav-tab:hover .tab-icon :global(i) {
    opacity: 1;
    filter: drop-shadow(0 0 12px rgba(0, 0, 0, 0.3));
  }

  /* Active tab has full color and glow */
  .nav-tab.active .tab-icon :global(i) {
    opacity: 1;
    filter: drop-shadow(0 0 16px var(--tab-color)) brightness(1.1);
  }

  /* Disabled tabs remain grayed out */
  .nav-tab.disabled .tab-icon {
    opacity: 0.3;
    filter: grayscale(1);
  }

  /* Ensure Font Awesome icons inherit color properly when disabled */
  .nav-tab.disabled .tab-icon :global(i) {
    color: var(--muted-foreground);
  }

  /* Larger icons in left layout */
  .layout-left .tab-icon {
    font-size: 20px;
  }

  /* Scale icons down for very short heights */
  @media (max-height: 400px) {
    .layout-left .tab-icon {
      font-size: 16px;
    }
  }

  /* Slightly smaller icons for short heights */
  @media (min-height: 400px) and (max-height: 500px) {
    .layout-left .tab-icon {
      font-size: 18px;
    }
  }

  .tab-label {
    font-weight: 500;
  }

  /* INTELLIGENT OVERFLOW DETECTION - Hide labels when tabs overflow */
  /* When in icon-only mode, maximize touch targets by expanding buttons */
  .sub-mode-tabs.icon-only {
    width: 100%; /* Fill the nav-center container */
    justify-content: space-evenly; /* Distribute buttons evenly */
  }

  .sub-mode-tabs.icon-only .nav-tab {
    flex: 1; /* Expand to fill available space */
    max-width: 80px; /* Prevent buttons from getting too wide */
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-xs);
    justify-content: center; /* Center icon within button */
  }

  .sub-mode-tabs.icon-only .tab-label {
    display: none;
  }

  .sub-mode-tabs.icon-only .tab-icon {
    font-size: 18px;
  }

  /* RESPONSIVE BREAKPOINTS - Removed static media query in favor of intelligent overflow detection */
  /* The NavigationBar component now dynamically detects overflow and applies .icon-only class as needed */

  /* ACCESSIBILITY & MOTION */
  @media (prefers-reduced-motion: reduce) {
    .nav-tab {
      transition: none;
    }
  }

  @media (prefers-contrast: high) {
    .nav-tab {
      border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .nav-tab.active {
      border-color: #667eea;
      background: rgba(102, 126, 234, 0.3);
    }
  }
</style>
