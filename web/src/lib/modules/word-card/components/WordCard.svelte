<!-- WordCard.svelte - Bare bones sequence image matching legacy desktop -->
<script lang="ts">
  import type { SequenceData } from "$shared/domain";

  // Props
  interface Props {
    sequence: SequenceData;
  }

  let { sequence }: Props = $props();

  // Generate sequence image path - load from dictionary
  let imagePath = $derived(() => {
    // Use the actual dictionary path structure: /dictionary/{word}/{word}_ver1.png
    const word = sequence.name;
    return `/dictionary/${word}/${word}_ver1.png`;
  });

  function handleCardClick() {
    console.log("Word card clicked:", sequence.name);
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
    src={imagePath()}
    alt={sequence.name}
    class="sequence-image"
    loading="lazy"
    onerror={(e) => {
      // Fallback to a simple placeholder if image fails to load
      const target = e.target as HTMLImageElement;
      if (target) {
        target.style.display = "none";
        const fallback = target.nextElementSibling as HTMLElement;
        if (fallback) fallback.style.display = "flex";
      }
    }}
  />

  <!-- Simple fallback for missing images -->
  <div class="image-fallback" style="display: none;">
    <div class="fallback-content">
      <div class="sequence-name">{sequence.name}</div>
      <div class="beat-count">{sequence.beats.length} beats</div>
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

  .image-fallback {
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 120px;
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
</style>
