<!--
  BackgroundSelector.svelte - Clean background selection component

  Handles the selection logic and grid layout of background thumbnails.
  Focused on component coordination and state management.
-->
<script lang="ts">
  import type { BackgroundType } from "$shared";
  import { backgroundsConfig } from "./background-config";
  import "./background-thumbnail-animations.css";
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
  }

  .background-grid {
    display: grid;
    width: 100%;
    height: 100%;
    align-content: center;
    justify-content: center;
  }

  /* Portrait Mode - Single column, all 4 cards vertically */
  .background-grid[data-orientation="portrait"] {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(4, 1fr);
    gap: clamp(8px, 1.5cqh, 16px);
    max-width: min(600px, 90cqw);
    max-height: 100%;
    margin: 0 auto;
  }

  /* Landscape Mode - Single row, all 4 cards horizontally */
  .background-grid[data-orientation="landscape"] {
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: 1fr;
    gap: clamp(8px, 1.5cqw, 20px);
    max-height: min(300px, 90cqh);
    max-width: 100%;
    margin: auto 0;
  }

  /* Square/Default Mode - 2x2 grid */
  .background-grid[data-orientation="square"] {
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: clamp(12px, 2cqi, 24px);
    max-width: min(900px, 90cqw);
    max-height: min(600px, 90cqh);
    margin: auto;
  }

  /* Ensure grid doesn't overflow container */
  .background-grid {
    overflow: hidden;
  }

  /* Accessibility - Maintain usability in all orientations */
  @media (prefers-reduced-motion: reduce) {
    .background-grid {
      transition: none;
    }
  }
</style>
