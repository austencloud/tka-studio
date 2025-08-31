<!--
	Pictograph Renderer Component

	Simple pictograph display for learning components.
-->

<script lang="ts">
  import type { PictographData } from "$domain";

  // Props using Svelte 5 runes
  let {
    pictographData,
    size = "medium",
  }: {
    pictographData: PictographData;
    size?: "small" | "medium" | "large";
  } = $props();
</script>

<div class="pictograph-renderer {size}">
  <!-- Simple letter display if available -->
  {#if pictographData?.letter}
    <div class="letter-display">
      {pictographData.letter}
    </div>
  {/if}

  <!-- Placeholder for actual pictograph content -->
  <div class="pictograph-placeholder">
    <!-- This will eventually be replaced with actual pictograph SVG rendering -->
    <span class="placeholder-text">Pictograph</span>
  </div>
</div>

<style>
  .pictograph-renderer {
    position: relative;
    display: inline-block;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
    width: 120px;
    height: 120px;
  }

  .pictograph-renderer.small {
    width: 80px;
    height: 80px;
  }

  .pictograph-renderer.large {
    width: 160px;
    height: 160px;
  }

  .letter-display {
    position: absolute;
    top: 8px;
    right: 8px;
    font-size: 0.8rem;
    font-weight: bold;
    color: #ffffff;
    background: rgba(0, 0, 0, 0.6);
    padding: 2px 6px;
    border-radius: 4px;
    z-index: 2;
  }

  .pictograph-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.6);
  }

  .placeholder-text {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
</style>
