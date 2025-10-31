<!--
ThumbnailActions Component - Action Buttons

Handles favorite, delete, and edit actions for sequence thumbnails.
Fullscreen functionality moved to direct thumbnail click.
Extracted from SequenceThumbnail.svelte for better separation of concerns.
-->
<script lang="ts">
  import type { SequenceData } from "$shared";
  import { onMount } from "svelte";
  import type { IHapticFeedbackService } from "../../../../shared/application/services/contracts";
  import { resolve, TYPES } from "../../../../shared/inversify";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sequence,
    isFavorite = false,
    onFavoriteToggle = () => {},
    onAction = () => {},
  } = $props<{
    sequence: SequenceData;
    isFavorite?: boolean;
    onFavoriteToggle?: (sequenceId: string) => void;
    onAction?: (action: string, sequence: SequenceData) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Event handlers
  function handleFavoriteClick(event: Event) {
    hapticService?.trigger("selection");
    event.stopPropagation();
    onFavoriteToggle(sequence.id);
  }

  function handleActionClick(action: string, event: Event) {
    hapticService?.trigger("selection");
    event.stopPropagation();
    onAction(action, sequence);
  }
</script>

<!-- Favorite indicator/button -->
<button
  class="favorite-button"
  class:is-favorite={isFavorite}
  onclick={handleFavoriteClick}
  aria-label={isFavorite ? "Remove from favorites" : "Add to favorites"}
>
  {isFavorite ? "⭐" : "☆"}
</button>

<!-- Action buttons (show on hover) -->
<div class="action-buttons">
  <button
    class="action-button animate-button"
    onclick={(e) => handleActionClick("animate", e)}
    aria-label="Animate sequence"
    title="Animate sequence"
  >
    ▶️
  </button>
  <button
    class="action-button delete-button"
    onclick={(e) => handleActionClick("delete", e)}
    aria-label="Delete sequence"
    title="Delete sequence"
  >
    🗑️
  </button>
  <button
    class="action-button edit-button"
    onclick={(e) => handleActionClick("edit", e)}
    aria-label="Edit sequence"
    title="Edit sequence"
  >
    ✏️
  </button>
</div>

<style>
  .favorite-button {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(200, 200, 200, 0.5);
    border-radius: 50%;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s ease;
    z-index: 2;
  }

  .favorite-button:hover {
    background: rgba(255, 255, 255, 1);
    border-color: rgba(100, 100, 100, 0.3);
    transform: scale(1.1);
  }

  .favorite-button.is-favorite {
    background: rgba(255, 215, 0, 0.9);
    border-color: rgba(255, 193, 7, 0.8);
    color: #fff;
  }

  .action-buttons {
    position: absolute;
    bottom: 8px;
    right: 8px;
    display: flex;
    gap: 4px;
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.2s ease;
    z-index: 2;
  }

  :global(.sequence-thumbnail:hover) .action-buttons {
    opacity: 1;
    transform: translateY(0);
  }

  .action-button {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(200, 200, 200, 0.5);
    border-radius: 6px;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 0.75rem;
    transition: all 0.2s ease;
  }

  .action-button:hover {
    background: rgba(255, 255, 255, 1);
    transform: scale(1.1);
  }

  .animate-button:hover {
    background: rgba(16, 185, 129, 0.1);
    border-color: rgba(16, 185, 129, 0.3);
  }

  .delete-button:hover {
    background: rgba(239, 68, 68, 0.1);
    border-color: rgba(239, 68, 68, 0.3);
  }

  .edit-button:hover {
    background: rgba(59, 130, 246, 0.1);
    border-color: rgba(59, 130, 246, 0.3);
  }

  /* Mobile-first responsive design with proper touch targets */
  @media (max-width: 480px) {
    .favorite-button {
      width: 44px;
      height: 44px;
      font-size: 1.125rem;
      top: 4px;
      right: 4px;
    }

    .action-button {
      width: 44px;
      height: 44px;
      font-size: 0.875rem;
    }

    .action-buttons {
      opacity: 1;
      transform: translateY(0);
      bottom: 4px;
      right: 4px;
      gap: 8px;
    }
  }

  /* Tablet responsive design */
  @media (min-width: 481px) and (max-width: 768px) {
    .favorite-button {
      width: 36px;
      height: 36px;
      font-size: 1rem;
    }

    .action-button {
      width: 36px;
      height: 36px;
      font-size: 0.75rem;
    }

    .action-buttons {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
