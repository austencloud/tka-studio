<!--
  BackgroundSelector.svelte - Clean background selection component
  
  Handles the selection logic and grid layout of background thumbnails.
  Focused on component coordination and state management.
-->
<script lang="ts">
  import type { BackgroundType } from "$domain";
  import { backgroundsConfig } from "./background-config";
  import "./background-thumbnail-animations.css";
  import BackgroundThumbnail from "./BackgroundThumbnail.svelte";

  interface Props {
    selectedBackground: BackgroundType;
    onBackgroundSelect: (type: BackgroundType) => void;
  }

  const { selectedBackground, onBackgroundSelect }: Props = $props();

  function handleBackgroundSelect(type: BackgroundType) {
    onBackgroundSelect(type);
  }
</script>

<div class="background-selector">
  <div class="background-grid">
    {#each backgroundsConfig as background}
      <BackgroundThumbnail
        {background}
        isSelected={selectedBackground === background.type}
        onSelect={handleBackgroundSelect}
      />
    {/each}
  </div>
</div>

<style>
  .background-selector {
    width: 100%;
  }

  .background-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: clamp(16px, 2vw, 24px);
    margin-top: clamp(12px, 1.5vw, 20px);
  }

  /* Container Queries for Responsive Layout */
  @container (max-width: 600px) {
    .background-grid {
      grid-template-columns: 1fr;
    }
  }

  @container (min-width: 900px) {
    .background-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @container (min-width: 1200px) {
    .background-grid {
      grid-template-columns: repeat(2, 1fr);
      max-width: 800px;
      margin: 0 auto;
    }
  }
</style>
