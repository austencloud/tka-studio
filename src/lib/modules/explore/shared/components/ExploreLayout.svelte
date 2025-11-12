<!--
Gallery Layout with Sort Controls

Provides responsive layout:
- Top section with sort controls and filter button
- Portrait mobile: Horizontal navigation above content
- Wider screens: Vertical navigation sidebar on left
- Center panel for content
-->
<script lang="ts">
  import type { Snippet } from "svelte";
  import { onMount } from "svelte";
  import { resolve, TYPES, type IDeviceDetector } from "$shared";
  import type { ResponsiveSettings } from "$shared/device/domain/models/device-models";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sortControls,
    navigationSidebar,
    centerPanel,
    isUIVisible = true,
  } = $props<{
    sortControls: Snippet;
    navigationSidebar: Snippet;
    centerPanel: Snippet;
    isUIVisible?: boolean;
  }>();

  // Services
  let deviceDetector: IDeviceDetector | null = null;

  // Reactive responsive settings from DeviceDetector
  let responsiveSettings = $state<ResponsiveSettings | null>(null);

  // ✅ PURE RUNES: Portrait mode detection using DeviceDetector
  const isPortraitMobile = $derived(
    responsiveSettings?.isMobile &&
      responsiveSettings?.orientation === "portrait"
  );

  // Initialize DeviceDetector service
  onMount(() => {
    try {
      deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
      responsiveSettings = deviceDetector.getResponsiveSettings();

      // Return cleanup function from onCapabilitiesChanged
      return deviceDetector.onCapabilitiesChanged(() => {
        responsiveSettings = deviceDetector!.getResponsiveSettings();
      });
    } catch (error) {
      console.warn("ExploreLayout: Failed to resolve DeviceDetector", error);
    }

    return undefined;
  });
</script>

<div class="gallery-layout" class:portrait-mobile={isPortraitMobile}>
  <!-- Top Section: Sort Controls + Filter Button -->
  <div class="top-section" class:hidden={!isUIVisible}>
    {@render sortControls()}
  </div>

  <!-- Portrait Mobile: Horizontal Navigation Above Content -->
  {#if isPortraitMobile}
    <div class="horizontal-navigation">
      {@render navigationSidebar()}
    </div>
  {/if}

  <!-- Main Content Area -->
  <div class="explore-content">
    <!-- Wider Screens: Vertical Navigation Sidebar -->
    {#if !isPortraitMobile}
      {@render navigationSidebar()}
    {/if}

    <!-- Center Panel: Content -->
    <div class="center-panel">
      {@render centerPanel()}
    </div>
  </div>
</div>

<style>
  .gallery-layout {
    display: flex;
    flex-direction: column;
    flex: 1;
    height: 100%;
    overflow: hidden;
    background: transparent;
    color: white;
  }

  /* Top Section - Sort controls and filter button */
  .top-section {
    flex-shrink: 0;
    padding: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    max-height: 200px; /* Adjust based on your actual content height */
    overflow: hidden;
    transform: translateY(0);
    transition:
      transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
      max-height 0.3s cubic-bezier(0.4, 0, 0.2, 1),
      padding 0.3s cubic-bezier(0.4, 0, 0.2, 1),
      margin 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .top-section.hidden {
    transform: translateY(-100%);
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    margin-bottom: 0;
    border-bottom-width: 0;
  }

  /* Horizontal Navigation - Portrait mobile only */
  .horizontal-navigation {
    flex-shrink: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
  }

  /* Main Content Area - Left panel + Center panel */
  .explore-content {
    display: flex;
    flex: 1;
    overflow: hidden;
  }

  /* Portrait mobile - no sidebar in main content */
  .gallery-layout.portrait-mobile .explore-content {
    flex-direction: column;
  }

  /* Center Panel - Content area */
  .center-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-width: 0;
    background: rgba(255, 255, 255, 0.01);
  }

  /* Mobile-first responsive design */
  @media (max-width: 480px) {
    .gallery-layout {
      height: 100vh;
      height: 100dvh; /* Dynamic viewport height for mobile */
    }

    .top-section {
      padding: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.15);
      max-height: 150px; /* Smaller max-height for mobile */
    }

    .center-panel {
      padding: 0;
    }
  }

  /* Tablet responsive design */
  @media (min-width: 481px) and (max-width: 768px) {
    .top-section {
      padding: 14px;
    }

    .explore-content {
      flex-direction: row;
    }
  }
</style>
