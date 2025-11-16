<!--
  PreviewSection.svelte - Interactive Pictograph Preview

  Displays an interactive pictograph that reflects current visibility settings.
  Users can click elements in the preview to toggle their visibility.
-->
<script lang="ts">
  import Pictograph from "$lib/shared/pictograph/shared/components/Pictograph.svelte";
  import type { PictographData } from "$lib/shared/pictograph/shared/domain/models/PictographData";

  interface Props {
    pictographData: PictographData;
    size?: number;
  }

  let { pictographData, size = 300 }: Props = $props();

  // Container element to measure for responsive sizing
  let containerElement: HTMLDivElement | null = $state(null);
  let responsiveSize = $state(300);

  $effect(() => {
    if (!containerElement) return;

    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        // Use 80% of the smaller dimension, with min/max bounds
        const targetSize = Math.min(width, height) * 0.8;
        responsiveSize = Math.max(200, Math.min(600, targetSize));
      }
    });

    observer.observe(containerElement);

    return () => observer.disconnect();
  });
</script>

<div class="preview-section">
  <h4 class="preview-title">Interactive Preview</h4>
  <p class="preview-note">
    Click elements in the preview to toggle their visibility
  </p>

  <div class="preview-container" bind:this={containerElement}>
    <Pictograph {pictographData} />
  </div>
</div>

<style>
  .preview-section {
    display: flex;
    flex-direction: column;
    gap: clamp(0.75rem, 2vw, 1.25rem);
    height: 100%;
    min-height: 0;
  }

  .preview-title {
    font-size: clamp(0.938rem, 1.5vw + 0.25rem, 1.125rem);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
    text-align: center;
  }

  .preview-note {
    font-size: clamp(0.75rem, 1.25vw + 0.125rem, 0.938rem);
    color: rgba(255, 255, 255, 0.6);
    font-style: italic;
    margin: 0;
    text-align: center;
  }

  .preview-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(0.5rem, 1vw, 0.75rem);
    padding: clamp(1rem, 3vw, 2.5rem);
    min-height: clamp(15rem, 40vh, 30rem);
    container-type: size;
  }
</style>
