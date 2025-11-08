<!--
  TopBar.svelte - Global Top Navigation Bar

  Features:
  - Profile picture/account dropdown (right)
  - Module-specific content slot (center)
  - Glass morphism styling matching bottom navigation
  - Responsive to portrait/landscape layouts
  - Reactive height measurement via context
-->
<script lang="ts">
  import { onMount, setContext } from "svelte";
  import { resolve, TYPES, type IDeviceDetector } from "$shared";
  import type { ResponsiveSettings } from "$shared/device/domain/models/device-models";
  import ProfileButton from "./ProfileButton.svelte";
  import LandingButton from "../../landing/components/LandingButton.svelte";

  // Props
  let {
    navigationLayout = "top",
    onHeightChange,
    left,
    content,
  } = $props<{
    navigationLayout?: "top" | "left";
    onHeightChange?: (height: number) => void;
    left?: import("svelte").Snippet;
    content?: import("svelte").Snippet;
  }>();

  // Services
  let deviceDetector: IDeviceDetector | null = null;

  // Refs
  let topBarElement = $state<HTMLElement | null>(null);

  // Reactive responsive settings from DeviceDetector
  let responsiveSettings = $state<ResponsiveSettings | null>(null);

  // Reactive responsive values based on device detector
  const isMobile = $derived(responsiveSettings?.isMobile ?? false);
  const computedHeight = $derived(isMobile ? 52 : 56);
  const computedPadding = $derived(
    isMobile ? "var(--spacing-sm)" : "var(--spacing-md)"
  );

  // Reactive height state (actual measured height may differ from computed)
  let topBarHeight = $state(56); // Default fallback

  // Expose height via context for descendant components
  setContext("topBarHeight", {
    get height() {
      return topBarHeight;
    },
  });

  // Initialize services and track height changes
  onMount(() => {
    // Resolve DeviceDetector service
    try {
      deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);

      // Get initial responsive settings
      responsiveSettings = deviceDetector.getResponsiveSettings();

      // Return cleanup function from onCapabilitiesChanged
      return (
        deviceDetector.onCapabilitiesChanged(() => {
          responsiveSettings = deviceDetector!.getResponsiveSettings();
        }) || undefined
      );
    } catch (error) {
      console.warn("TopBar: Failed to resolve DeviceDetector", error);
    }

    return undefined;
  });

  // Measure actual height and track changes
  onMount(() => {
    if (!topBarElement) return;

    // Initial measurement
    const updateHeight = () => {
      if (topBarElement) {
        const rect = topBarElement.getBoundingClientRect();
        const newHeight = rect.height;
        if (newHeight > 0 && newHeight !== topBarHeight) {
          topBarHeight = newHeight;
          onHeightChange?.(newHeight);
        }
      }
    };

    // Measure immediately
    updateHeight();

    // Track resize changes
    const resizeObserver = new ResizeObserver(() => {
      updateHeight();
    });

    resizeObserver.observe(topBarElement);

    return () => {
      resizeObserver.disconnect();
    };
  });
</script>

<div
  bind:this={topBarElement}
  class="top-bar"
  class:layout-top={navigationLayout === "top"}
  class:layout-left={navigationLayout === "left"}
  style:height="{computedHeight}px"
  style:padding="0 {computedPadding}"
>
  <!-- Left: Landing/home button + Module-specific left content (e.g., back button) -->
  <div class="top-bar__left">
    <LandingButton />
    {#if left}
      {@render left()}
    {/if}
  </div>

  <!-- Center: Module-specific content slot -->
  <div class="top-bar__center">
    {#if content}
      {@render content()}
    {/if}
  </div>

  <!-- Right: Profile picture/account button -->
  <div class="top-bar__right">
    <ProfileButton />
  </div>
</div>

<style>
  /* ============================================================================
     BASE TOP BAR STYLES
     ============================================================================ */
  .top-bar {
    position: fixed;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    /* Slightly higher opacity to compensate for darker gradient behind it */
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: var(--glass-backdrop-strong);
    z-index: 100;
    border-radius: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  /* ============================================================================
     TOP LAYOUT (Portrait - Horizontal Bar)
     ============================================================================ */
  .top-bar.layout-top {
    top: 0;
    left: 0;
    right: 0;
    /* Height and padding controlled by reactive inline styles */
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }

  /* ============================================================================
     LEFT LAYOUT (Landscape - Integrated with Side Nav)
     ============================================================================ */
  .top-bar.layout-left {
    top: 0;
    left: 72px; /* Account for side navigation width */
    right: 0;
    height: 56px;
    padding: 0 var(--spacing-md);
  }

  /* ============================================================================
     LAYOUT SECTIONS
     ============================================================================ */
  .top-bar__left {
    display: flex;
    align-items: center;
    justify-content: flex-start;
  }

  .top-bar__center {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 0; /* Allow content to shrink */
    pointer-events: none; /* Allow slot content to control pointer events */
  }

  .top-bar__center :global(*) {
    pointer-events: auto; /* Re-enable for slot content */
  }

  .top-bar__right {
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  @media (prefers-contrast: high) {
    .top-bar {
      background: rgba(0, 0, 0, 0.95);
      border-bottom: 2px solid white;
    }
  }
</style>
