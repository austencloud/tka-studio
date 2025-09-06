<script lang="ts">
  // TODO: Fix missing SVGGenerator import
  // import { SVGGenerator } from "$components/tabs/browse-tab/animator/utils/canvas/SVGGenerator";
  // import { svgStringToImage } from "./svgStringToImage";

  // Modern Svelte 5 props
  let {
    canvasSize = 500,
    onGridImageLoad,
  }: {
    canvasSize?: number;
    onGridImageLoad: (image: HTMLImageElement) => void;
  } = $props();

  let gridImage: HTMLImageElement | null = null;
  let isLoading = $state(false);

  // Load grid image when component mounts or size changes
  $effect(() => {
    loadGridImage();
  });

  async function loadGridImage(): Promise<void> {
    if (isLoading) return;

    isLoading = true;

    try {
      // TODO: Fix SVGGenerator import
      // const svgString = SVGGenerator.generateGridSvg();
      // gridImage = await svgStringToImage(svgString, canvasSize, canvasSize);
      console.warn(
        "GridManager: SVGGenerator not available, skipping grid generation"
      );

      // Notify parent component
      if (gridImage) {
        onGridImageLoad(gridImage);
      }
    } catch (error) {
      console.error("Failed to load grid image:", error);
    } finally {
      isLoading = false;
    }
  }
</script>

<!-- GridManager is invisible - it just manages grid image loading -->
<div style="display: none;">
  {#if isLoading}
    Loading grid...
  {/if}
</div>
