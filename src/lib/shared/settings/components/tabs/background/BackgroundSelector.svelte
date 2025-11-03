<!--
  BackgroundSelector.svelte - Clean background selection component

  Handles the selection logic and grid layout of background thumbnails.
  Focused on component coordination and state management.
-->
<script lang="ts">
  import type { BackgroundType } from "$shared";
  import { backgroundsConfig } from "./background-config";
  import BackgroundThumbnail from "./BackgroundThumbnail.svelte";

  const {
    selectedBackground,
    onBackgroundSelect,
    orientation = "square",
  } = $props<{
    selectedBackground: BackgroundType;
    onBackgroundSelect: (type: BackgroundType) => void;
    orientation?: "portrait" | "landscape" | "square";
  }>();

  function handleBackgroundSelect(type: BackgroundType) {
    onBackgroundSelect(type);
  }
</script>

<div class="background-selector">
  <div class="background-grid" data-orientation={orientation}>
    {#each backgroundsConfig as background}
      <BackgroundThumbnail
        {background}
        isSelected={selectedBackground === background.type}
        onSelect={handleBackgroundSelect}
        {orientation}
      />
    {/each}
  </div>
</div>

<style>
  .background-selector {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    container-type: size;
    container-name: background-selector;
    overflow: visible;
  }

  .background-grid {
    display: grid;
    width: 100%;
    height: 100%;
    align-content: center;
    justify-content: center;
    overflow: visible;

    /*
      Intelligent responsive grid for 4 background cards
      - Uses container queries for true container-relative sizing
      - Automatically adapts layout based on available space
      - No reliance on device orientation detection
    */

    /* Default: 2×2 grid for balanced layout */
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: clamp(10px, 2cqi, 20px);
    max-width: min(900px, 95cqw);
    max-height: min(700px, 95cqh);
    margin: auto;
  }

  /*
    Container-based responsive layouts (pure CSS)
    Automatically chooses optimal layout based on container dimensions
  */

  /* Ultra-narrow (< 280px): 1 column with square aspect and minimal spacing */
  @container (max-width: 280px) {
    .background-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, minmax(60px, 1fr));
      gap: clamp(6px, 1.5cqh, 10px);
      max-width: 100%;
      max-height: 100%;
    }

    /* Force square aspect ratio for ultra-compact space */
    .background-grid :global(.background-thumbnail) {
      aspect-ratio: 1;
    }
  }

  /* Very narrow containers (280-400px): 1 column × 4 rows (vertical stack) */
  @container (min-width: 281px) and (max-width: 400px) {
    .background-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, 1fr);
      gap: clamp(8px, 1.5cqh, 14px);
      max-width: min(500px, 90cqw);
      max-height: 100%;
    }
  }

  /* Small-medium (401-500px): 2×2 grid with square aspect for tight space */
  @container (min-width: 401px) and (max-width: 500px) {
    .background-grid {
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: clamp(8px, 2cqi, 14px);
      max-width: min(500px, 92cqw);
      max-height: min(500px, 92cqh);
    }

    /* Square aspect for better space usage */
    .background-grid :global(.background-thumbnail) {
      aspect-ratio: 1;
    }
  }

  /* Medium containers (501-800px): 2×2 grid (optimal for most cases) */
  @container (min-width: 501px) and (max-width: 800px) {
    .background-grid {
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: clamp(12px, 2.5cqi, 18px);
      max-width: min(700px, 92cqw);
      max-height: min(600px, 92cqh);
    }
  }

  /* Wide containers: 4 columns × 1 row (horizontal layout) */
  @container (min-width: 801px) {
    .background-grid {
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: 1fr;
      gap: clamp(14px, 2.8cqi, 24px);
      max-width: 100%;
      max-height: min(350px, 85cqh);
    }
  }

  /*
    Height-constrained containers: Force horizontal layout
    When height is limited but width is available, use 4×1 layout
  */
  @container (max-height: 400px) and (min-width: 600px) {
    .background-grid {
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: 1fr;
      gap: clamp(10px, 2cqi, 16px);
      max-height: min(280px, 90cqh);
      max-width: 100%;
    }
  }

  /*
    Very height-constrained: Use 2×2 with smaller gaps
    Prevents cards from becoming too small in landscape mobile
  */
  @container (max-height: 350px) and (max-width: 599px) {
    .background-grid {
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: clamp(6px, 1.5cqi, 10px);
      max-height: 95cqh;
      max-width: 95cqw;
    }
  }

  /* Accessibility - Maintain usability in all orientations */
  @media (prefers-reduced-motion: reduce) {
    .background-grid {
      transition: none;
    }
  }
</style>
