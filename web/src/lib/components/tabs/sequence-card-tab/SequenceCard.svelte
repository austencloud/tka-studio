<!-- SequenceCard.svelte - Bare bones sequence image matching legacy desktop -->
<script lang="ts">
  import type { SequenceData } from "$services/interfaces/domain-types";

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
    console.log("Sequence card clicked:", sequence.name);
  }
</script>

<!-- Bare bones sequence card - just the image -->
<div
  class="sequence-card"
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
  .sequence-card {
    cursor: pointer;
    border-radius: 4px;
    overflow: hidden;
    transition: transform 0.2s ease;
    background: white;
    border: 1px solid #ddd;
    /* No forced aspect ratio - let the actual sequence image determine size */
  }

  .sequence-card:hover {
    transform: scale(1.02);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
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
    background: #f5f5f5;
    border: 1px solid #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .fallback-content {
    text-align: center;
    padding: 16px;
    color: #666;
  }

  .sequence-name {
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 4px;
  }

  .beat-count {
    font-size: 10px;
    color: #999;
  }
</style>
