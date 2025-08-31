<!-- SequenceImageViewer.svelte - Image viewer with variation navigation -->
<script lang="ts">
  import type { SequenceData } from "$domain";
  import { GridMode } from "$domain";

  interface Props {
    sequence?: SequenceData & {
      variations?: unknown[];
      gridMode?: string;
      startPosition?: string;
      isFavorite?: boolean;
      word?: string;
    };
    currentVariation?: { imageUrl?: string } | undefined;
    currentVariationIndex?: number;
    onNextVariation?: () => void;
    onPrevVariation?: () => void;
  }

  let {
    sequence,
    currentVariation,
    currentVariationIndex = 0,
    onNextVariation,
    onPrevVariation,
  }: Props = $props();

  // Image loading state
  let isImageLoading = $state(false);
  let imageElement = $state<HTMLImageElement | null>(null);
  let containerElement = $state<HTMLDivElement | null>(null);

  // Dynamic sizing state
  let calculatedWidth = $state(0);
  let calculatedHeight = $state(0);

  // Handle image loading events
  function handleImageLoad() {
    isImageLoading = false;
    calculateOptimalSize();
  }

  function handleImageError() {
    isImageLoading = false;
  }

  // Calculate optimal size based on legacy desktop logic
  function calculateOptimalSize() {
    if (!imageElement || !containerElement) return;

    const containerWidth = containerElement.clientWidth;
    const containerHeight = containerElement.clientHeight;

    // Legacy desktop logic: Use full width with padding, constrain height to 60% of container
    const padding = 20;
    const availableWidth = Math.max(200, containerWidth - padding);
    const maxHeightRatio = 0.6;
    const maxHeight = Math.max(200, containerHeight * maxHeightRatio);

    // Get image natural dimensions
    const imageNaturalWidth = imageElement.naturalWidth;
    const imageNaturalHeight = imageElement.naturalHeight;

    if (imageNaturalWidth > 0 && imageNaturalHeight > 0) {
      // Calculate aspect ratio
      const aspectRatio = imageNaturalWidth / imageNaturalHeight;

      // Start with full available width
      let targetWidth = availableWidth;
      let targetHeight = targetWidth / aspectRatio;

      // If height would exceed max, constrain width to fit height limit
      if (targetHeight > maxHeight) {
        targetHeight = maxHeight;
        targetWidth = targetHeight * aspectRatio;
      }

      calculatedWidth = Math.round(targetWidth);
      calculatedHeight = Math.round(targetHeight);
    } else {
      // Fallback for images without natural dimensions
      calculatedWidth = availableWidth;
      calculatedHeight = Math.min(availableWidth, maxHeight);
    }
  }

  // Set up resize observer for container
  $effect(() => {
    if (containerElement) {
      const resizeObserver = new ResizeObserver(() => {
        calculateOptimalSize();
      });
      resizeObserver.observe(containerElement);

      return () => {
        resizeObserver.disconnect();
      };
    }
    return undefined;
  });

  // Navigation handlers
  function handleNextVariation() {
    onNextVariation?.();
  }

  function handlePrevVariation() {
    onPrevVariation?.();
  }

  // Check if navigation is available
  let hasMultipleVariations = $derived(
    sequence?.variations && sequence.variations.length > 1
  );

  let canGoPrev = $derived(currentVariationIndex > 0);
  let canGoNext = $derived(
    hasMultipleVariations &&
      sequence &&
      sequence.variations &&
      currentVariationIndex < sequence.variations.length - 1
  );
</script>

<div class="image-viewer-section">
  <div class="image-container" bind:this={containerElement}>
    {#if currentVariation?.imageUrl}
      <img
        bind:this={imageElement}
        src={currentVariation.imageUrl}
        alt="{sequence?.word || 'Sequence'} - Variation {currentVariationIndex +
          1}"
        class:loading={isImageLoading}
        style="width: {calculatedWidth}px; height: {calculatedHeight}px;"
        onload={handleImageLoad}
        onerror={handleImageError}
      />
    {:else}
      <!-- Placeholder -->
      <div class="image-placeholder">
        <div class="placeholder-content">
          <div class="sequence-icon">🔄</div>
          <h3>{sequence?.word || "Sequence"}</h3>
          <p>Pictograph visualization</p>
          <div class="placeholder-details">
            <span>{sequence?.gridMode || GridMode.DIAMOND} grid</span>
            <span>{sequence?.startPosition || "center"} start</span>
          </div>
        </div>
      </div>
    {/if}

    {#if sequence?.isFavorite}
      <div class="favorite-indicator">⭐</div>
    {/if}
  </div>

  <!-- Navigation Controls -->
  {#if hasMultipleVariations}
    <div class="image-navigation">
      <button
        class="nav-button"
        class:disabled={!canGoPrev}
        onclick={handlePrevVariation}
        disabled={!canGoPrev}
        type="button"
      >
        ◀
      </button>

      <span class="variation-info">
        {currentVariationIndex + 1} / {sequence?.variations?.length || 1}
      </span>

      <button
        class="nav-button"
        class:disabled={!canGoNext}
        onclick={handleNextVariation}
        disabled={!canGoNext}
        type="button"
      >
        ▶
      </button>
    </div>
  {/if}
</div>

<style>
  /* Image Viewer */
  .image-viewer-section {
    flex-shrink: 0;
  }

  .image-container {
    position: relative;
    width: 100%;
    min-height: 200px;
    max-height: 60vh; /* Legacy desktop: 60% of viewport height */
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.1),
      rgba(168, 85, 247, 0.1),
      rgba(6, 182, 212, 0.1)
    );
    border: var(--glass-border);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: var(--spacing-md);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .image-container img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    transition: opacity var(--transition-fast);
    display: block;
  }

  .image-container img.loading {
    opacity: 0.5;
  }

  .image-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }

  .placeholder-content {
    text-align: center;
    padding: var(--spacing-lg);
  }

  .sequence-icon {
    font-size: 2rem;
    margin-bottom: var(--spacing-sm);
  }

  .placeholder-content h3 {
    font-size: var(--font-size-lg);
    margin: 0 0 var(--spacing-xs) 0;
    color: white;
  }

  .placeholder-content p {
    color: rgba(255, 255, 255, 0.8);
    margin: 0 0 var(--spacing-sm) 0;
    font-size: var(--font-size-sm);
  }

  .placeholder-details {
    display: flex;
    gap: var(--spacing-sm);
    justify-content: center;
    font-size: var(--font-size-xs);
    opacity: 0.7;
  }

  .placeholder-details span {
    padding: 2px 6px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    text-transform: capitalize;
  }

  .favorite-indicator {
    position: absolute;
    top: var(--spacing-sm);
    right: var(--spacing-sm);
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(10px);
    font-size: var(--font-size-base);
  }

  .image-navigation {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-md);
    padding: var(--spacing-sm);
  }

  .nav-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: rgba(255, 255, 255, 0.1);
    border: var(--glass-border);
    border-radius: 50%;
    color: var(--foreground);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: var(--font-size-base);
  }

  .nav-button:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.2);
    border-color: var(--primary-color);
    color: var(--primary-color);
  }

  .nav-button.disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .variation-info {
    font-size: var(--font-size-sm);
    color: var(--muted-foreground);
    min-width: 60px;
    text-align: center;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .image-container {
      min-height: 150px;
      max-height: 50vh; /* Smaller max height on mobile */
    }
  }
</style>
