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
  import type { Section } from "../domain/types";

  // Helper function to extract Font Awesome icon name from HTML string
  function extractIconName(htmlString: string): string | null {
    // Match patterns like: <i class="fas fa-hammer"></i>
    const match = htmlString.match(/fa-([a-z-]+)/);
    return match ? match[1] : null;
  }

  let {
    sectionTabs = [],
    currentSection,
    navigationLayout,
    onSectionChange,
    forceIconOnly = false,
  } = $props<{
    sectionTabs: Section[];
    currentSection: string;
    navigationLayout: "top" | "left";
    onSectionChange?: (sectionId: string) => void;
    forceIconOnly?: boolean;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Overflow detection state (local detection, can be overridden by forceIconOnly)
  let containerElement: HTMLDivElement | null = $state(null);

  // Reactive measurements updated by ResizeObserver
  let containerScrollWidth = $state(0);
  let containerClientWidth = $state(0);

  // Derived overflow detection: compares container scroll width against client width
  const isOverflowing = $derived(
    containerScrollWidth > containerClientWidth && navigationLayout === "top"
  );

  // Combined overflow state: either forced from parent or detected locally
  const shouldShowIconOnly = $derived(forceIconOnly || isOverflowing);

  // Measure container dimensions
  function updateContainerMeasurements() {
    if (!containerElement || navigationLayout !== "top") {
      containerScrollWidth = 0;
      containerClientWidth = 0;
      return;
    }

    containerScrollWidth = containerElement.scrollWidth;
    containerClientWidth = containerElement.clientWidth;
  }

  // Reactive effect: Update measurements when sectionTabs array changes
  // This ensures overflow detection reacts to dynamic tab additions/removals
  $effect(() => {
    // Track the sectionTabs array length to trigger on changes
    const tabCount = sectionTabs.length;

    // Schedule measurement update after DOM updates complete
    // This allows the new tabs to render before we measure
    if (tabCount > 0 && containerElement) {
      // Use requestAnimationFrame to wait for layout
      requestAnimationFrame(() => {
        updateContainerMeasurements();
      });
    }
  });

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    // Set up overflow detection for top layout only
    if (navigationLayout === "top" && containerElement) {
      const resizeObserver = new ResizeObserver(() => {
        updateContainerMeasurements();
      });

      resizeObserver.observe(containerElement);

      // Also check on window resize
      window.addEventListener("resize", updateContainerMeasurements);

      // Initial measurement
      updateContainerMeasurements();

      return () => {
        resizeObserver.disconnect();
        window.removeEventListener("resize", updateContainerMeasurements);
      };
    }
  });

  // Handle sub-mode selection
  function handleSectionSelect(sectionId: string) {
    hapticService?.trigger("selection");
    onSectionChange?.(sectionId);
  }
</script>

<div
  bind:this={containerElement}
  class="sub-mode-tabs"
  class:layout-left={navigationLayout === "left"}
  class:icon-only={shouldShowIconOnly && navigationLayout === "top"}
>
  {#each sectionTabs as section}
    <button
      class="nav-tab sub-mode-tab"
      class:active={currentSection === section.id}
      class:disabled={section.disabled}
      onclick={() =>
        section.disabled ? null : handleSectionSelect(section.id)}
      disabled={section.disabled}
      aria-pressed={currentSection === section.id}
      aria-disabled={section.disabled}
      title={section.disabled
        ? `${section.label} (requires a sequence)`
        : section.description || section.label}
      style="--tab-color: {section.color ||
        'var(--muted-foreground)'}; --tab-gradient: {section.gradient ||
        section.color ||
        'var(--muted-foreground)'};"
    >
      <span class="tab-icon">
        {#if extractIconName(section.icon)}
          <FontAwesomeIcon icon={extractIconName(section.icon)!} size="1em" />
        {:else}
          {@html section.icon}
        {/if}
      </span>
      <span class="tab-label">{section.label}</span>
    </button>
  {/each}
</div>

<style>
  .sub-mode-tabs {
    display: flex;
    height: 100%; /* Fill full navigation bar height */
    /* Allow tabs to overflow for proper overflow detection */
    overflow: visible;
    flex-shrink: 0; /* Don't allow container to shrink */
    min-width: max-content; /* Container must be at least as wide as its content */
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
    flex-direction: column; /* Consistent vertical layout: icon above label */
    align-items: center;
    justify-content: center;
    gap: 2px; /* Tighter gap for vertical layout */
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
    /* CRITICAL FOR OVERFLOW DETECTION: Prevent tabs from shrinking */
    flex-shrink: 0;
    white-space: nowrap;
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
    font-size: 10px;
    font-weight: 500;
    text-align: center;
    white-space: nowrap;
    line-height: 1.2;
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
