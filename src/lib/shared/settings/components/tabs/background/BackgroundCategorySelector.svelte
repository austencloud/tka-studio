<!--
  BackgroundCategorySelector.svelte - Filter chips for background category selection

  Material Design 3 filter chips pattern for selecting between Animated and Simple backgrounds.
  Mobile-first, touch-friendly, with haptic feedback.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";

  const { selectedCategory, onCategorySelect } = $props<{
    selectedCategory: "animated" | "simple";
    onCategorySelect: (category: "animated" | "simple") => void;
  }>();

  // Services
  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  function handleCategorySelect(category: "animated" | "simple") {
    if (category !== selectedCategory) {
      hapticService?.trigger("selection");
      onCategorySelect(category);
    }
  }
</script>

<div class="category-selector">
  <div class="chip-container">
    <button
      class="filter-chip"
      class:selected={selectedCategory === "animated"}
      onclick={() => handleCategorySelect("animated")}
      aria-pressed={selectedCategory === "animated"}
      aria-label="Select animated backgrounds"
    >
      <span class="chip-icon"><i class="fas fa-film"></i></span>
      <span class="chip-label">Animated</span>
      {#if selectedCategory === "animated"}
        <span class="chip-checkmark"><i class="fas fa-check"></i></span>
      {/if}
    </button>

    <button
      class="filter-chip"
      class:selected={selectedCategory === "simple"}
      onclick={() => handleCategorySelect("simple")}
      aria-pressed={selectedCategory === "simple"}
      aria-label="Select simple backgrounds"
    >
      <span class="chip-icon"><i class="fas fa-palette"></i></span>
      <span class="chip-label">Simple</span>
      {#if selectedCategory === "simple"}
        <span class="chip-checkmark"><i class="fas fa-check"></i></span>
      {/if}
    </button>
  </div>
</div>

<style>
  .category-selector {
    width: 100%;
    padding: clamp(12px, 2cqh, 20px) clamp(16px, 3cqw, 24px);
    display: flex;
    justify-content: center;
    container-type: inline-size;
    container-name: category-selector;
  }

  .chip-container {
    display: flex;
    gap: clamp(8px, 1.5cqw, 12px);
    flex-wrap: wrap;
    justify-content: center;
  }

  .filter-chip {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 20px;
    border-radius: 10px; /* More rounded */
    border: 1.5px solid rgba(255, 255, 255, 0.25);
    background: rgba(255, 255, 255, 0.06);
    color: #ffffff;
    font-size: clamp(15px, 1.5cqw, 17px); /* Slightly larger */
    font-weight: 500;
    line-height: 1.5;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    min-height: 46px; /* Slightly larger touch target */
    min-width: 130px;
  }

  .filter-chip:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(99, 102, 241, 0.6);
    transform: scale(1.02); /* Subtle scale */
  }

  .filter-chip:active {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(0.98);
  }

  .filter-chip.selected {
    background: rgba(99, 102, 241, 0.25); /* Indigo theme */
    border-color: #6366f1;
    color: #ffffff;
    font-weight: 600;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.3); /* Subtle glow */
  }

  .filter-chip.selected:hover {
    background: rgba(99, 102, 241, 0.3);
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
  }

  .chip-icon {
    font-size: 16px;
    line-height: 1;
    transition: transform 0.2s ease;
  }

  .filter-chip:hover .chip-icon {
    transform: scale(1.1); /* Icon emphasis */
  }

  .chip-label {
    font-size: 15px;
    font-weight: inherit;
  }

  .chip-checkmark {
    font-size: 14px;
    color: #6366f1; /* Indigo checkmark */
    font-weight: bold;
    animation: checkmarkPop 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  @keyframes checkmarkPop {
    0% {
      transform: scale(0);
      opacity: 0;
    }
    50% {
      transform: scale(1.2);
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  /* Focus styles for accessibility */
  .filter-chip:focus-visible {
    outline: 2px solid var(--mio-theme-color-primary, #6442d6);
    outline-offset: 2px;
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .filter-chip {
      transition: none;
    }

    .filter-chip:active {
      transform: none;
    }
  }

  /* Container query for smaller spaces */
  @container category-selector (max-width: 300px) {
    .chip-container {
      flex-direction: column;
      width: 100%;
    }

    .filter-chip {
      width: 100%;
      justify-content: center;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .filter-chip {
      border-width: 2px;
    }

    .filter-chip.selected {
      border-width: 3px;
    }
  }
</style>
