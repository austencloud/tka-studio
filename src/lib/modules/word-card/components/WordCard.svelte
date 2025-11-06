<!-- WordCard.svelte - Bare bones sequence image matching legacy desktop -->
<script lang="ts">
  import type { IHapticFeedbackService, SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Props
  let { sequence } = $props<{
    sequence: SequenceData;
  }>();

  // State for tracking which image version loads successfully
  let imageVersion = $state<number>(1);
  let imageLoadFailed = $state<boolean>(false);

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Generate sequence image path - try multiple versions like PNG metadata extractor
  let imagePath = $derived.by(() => {
    // Strip " Sequence" suffix from name to get the actual folder/file name
    const word = sequence.name.replace(" Sequence", "");
    return `/gallery/${word}/${word}_ver${imageVersion}.webp`;
  });

  function handleCardClick() {
    // Trigger selection haptic feedback for word card selection
    hapticService?.trigger("selection");

    console.log("Word card clicked:", sequence.name);
  }

  // Handle image load errors by trying next version
  function handleImageError() {
    if (imageVersion < 6) {
      // Try up to version 6
      imageVersion++;
      imageLoadFailed = false;
    } else {
      imageLoadFailed = true;
      console.warn(
        `No WebP image found for sequence: ${sequence.name} (tried versions 1-6)`
      );
    }
  }
</script>

<!-- Bare bones word card - just the image -->
<div
  class="word-card"
  onclick={handleCardClick}
  onkeydown={(e) => e.key === "Enter" && handleCardClick()}
  role="button"
  tabindex="0"
>
  <img
    src={imagePath}
    alt={sequence.name}
    class="sequence-image"
    class:hidden={imageLoadFailed}
    loading="lazy"
    onerror={handleImageError}
  />

  <!-- Simple fallback for missing images -->
  <div class="image-fallback" class:visible={imageLoadFailed}>
    <div class="fallback-content">
      <div class="sequence-name">{sequence.name}</div>
      <div class="beat-count">{sequence.beats.length} beats</div>
      <div class="missing-image-note">Image not found</div>
    </div>
  </div>
</div>

<style>
  .word-card {
    cursor: pointer;
    border-radius: var(--border-radius-md);
    overflow: hidden;
    transition: all var(--transition-normal);
    background: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    /* No forced aspect ratio - let the actual sequence image determine size */
  }

  .word-card:hover {
    transform: scale(1.02) translateY(-2px);
    box-shadow:
      0 4px 16px rgba(0, 0, 0, 0.15),
      0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .word-card:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
  }

  .sequence-image {
    max-width: 100%;
    height: auto;
    display: block;
    /* Let the image maintain its natural aspect ratio */
  }

  .sequence-image.hidden {
    display: none;
  }

  .image-fallback {
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    display: none;
    align-items: center;
    justify-content: center;
    min-height: 120px;
  }

  .image-fallback.visible {
    display: flex;
  }

  .fallback-content {
    text-align: center;
    padding: var(--spacing-lg);
    color: var(--text-color);
  }

  .sequence-name {
    font-size: var(--font-size-sm);
    font-weight: 500;
    margin-bottom: var(--spacing-xs);
    color: var(--text-color);
  }

  .beat-count {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .missing-image-note {
    font-size: var(--font-size-xs);
    color: var(--text-muted);
    font-style: italic;
    margin-top: var(--spacing-xs);
  }
</style>
