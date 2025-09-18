<!--
Gallery Layout with Sort Controls

Provides layout matching legacy desktop app:
- Top section with sort controls and filter button
- Left panel with navigation sidebar
- Center panel for content
-->
<script lang="ts">
  import type { Snippet } from "svelte";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sortControls,
    navigationSidebar,
    centerPanel,
  } = $props<{
    sortControls: Snippet;
    navigationSidebar: Snippet;
    centerPanel: Snippet;
  }>();
</script>

<div class="gallery-layout">
  <!-- Top Section: Sort Controls + Filter Button -->
  <div class="top-section">
    {@render sortControls()}
  </div>

  <!-- Main Content Area -->
  <div class="main-content">
    <!-- Navigation Sidebar -->
    {@render navigationSidebar()}

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

  /* Main Content Area - Left panel + Center panel */
  .main-content {
    display: flex;
    flex: 1;
    overflow: hidden;
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

    .main-content {
      flex-direction: row; /* Keep sidebar on mobile for navigation */
      overflow: hidden;
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
