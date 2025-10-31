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
  import { onDestroy, onMount } from "svelte";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const { sortControls, navigationSidebar, centerPanel } = $props<{
    sortControls: Snippet;
    navigationSidebar: Snippet;
    centerPanel: Snippet;
  }>();

  // ✅ PURE RUNES: Reactive state for portrait detection
  let isPortraitMobile = $state(false);

  // Detect portrait mobile mode (narrow width, portrait orientation)
  function checkPortraitMobile() {
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const isPortrait = viewportHeight > viewportWidth;
    const hasNarrowWidth = viewportWidth < 600;
    isPortraitMobile = isPortrait && hasNarrowWidth;
  }

  // Update on mount and window resize
  onMount(() => {
    checkPortraitMobile();
    window.addEventListener("resize", checkPortraitMobile);
    window.addEventListener("orientationchange", checkPortraitMobile);
  });

  onDestroy(() => {
    window.removeEventListener("resize", checkPortraitMobile);
    window.removeEventListener("orientationchange", checkPortraitMobile);
  });
</script>

<div class="gallery-layout" class:portrait-mobile={isPortraitMobile}>
  <!-- Top Section: Sort Controls + Filter Button -->
  <div class="top-section">
    {@render sortControls()}
  </div>

  <!-- Portrait Mobile: Horizontal Navigation Above Content -->
  {#if isPortraitMobile}
    <div class="horizontal-navigation">
      {@render navigationSidebar()}
    </div>
  {/if}

  <!-- Main Content Area -->
  <div class="main-content">
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
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(10px);
  }

  /* Horizontal Navigation - Portrait mobile only */
  .horizontal-navigation {
    flex-shrink: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
  }

  /* Main Content Area - Left panel + Center panel */
  .main-content {
    display: flex;
    flex: 1;
    overflow: hidden;
  }

  /* Portrait mobile - no sidebar in main content */
  .gallery-layout.portrait-mobile .main-content {
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

    .main-content {
      flex-direction: row;
    }
  }
</style>
