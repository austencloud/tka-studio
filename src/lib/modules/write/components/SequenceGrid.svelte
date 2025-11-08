<!-- SequenceGrid.svelte - Grid display of sequences in an act -->
<script lang="ts">
  import type { IHapticFeedbackService, SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Props
  let {
    sequences = [],
    onSequenceClicked,
    onSequenceRemoveRequested,
  } = $props<{
    sequences?: SequenceData[];
    onSequenceClicked?: (position: number) => void;
    onSequenceRemoveRequested?: (position: number) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Handle sequence click
  function handleSequenceClick(sequence: SequenceData, index: number) {
    hapticService?.trigger("selection");
    onSequenceClicked?.(index);
  }

  // Handle sequence remove
  function handleSequenceRemove(
    sequence: SequenceData,
    index: number,
    event: Event
  ) {
    event.stopPropagation();
    hapticService?.trigger("selection");
    onSequenceRemoveRequested?.(index);
  }

  // Generate thumbnail URL for sequence
  function getThumbnailUrl(sequence: SequenceData): string {
    if (sequence.thumbnails && sequence.thumbnails.length > 0) {
      return (
        sequence.thumbnails[0] || "/static/thumbnails/default-sequence.png"
      );
    }
    // Generate based on sequence content or use placeholder
    return `/static/thumbnails/default-sequence.png`;
  }

  // Format sequence duration
  function formatDuration(duration?: number): string {
    if (!duration) return "0:00";
    const minutes = Math.floor(duration / 60);
    const seconds = Math.floor(duration % 60);
    return `${minutes}:${seconds.toString().padStart(2, "0")}`;
  }
</script>

<div class="sequence-grid" class:empty={sequences.length === 0}>
  {#if sequences.length > 0}
    <div class="grid-header">
      <h3>Sequences ({sequences.length})</h3>
      <div class="grid-actions">
        <!-- Future: Add sequence management actions -->
      </div>
    </div>

    <div class="grid-container">
      {#each sequences as sequence, index}
        <div
          class="word-card"
          onclick={() => handleSequenceClick(sequence, index)}
          tabindex="0"
          role="button"
          onkeydown={(e) =>
            (e.key === "Enter" || e.key === " ") &&
            handleSequenceClick(sequence, index)}
        >
          <!-- Sequence thumbnail -->
          <div class="sequence-thumbnail">
            <img
              src={getThumbnailUrl(sequence)}
              alt={sequence.name || `Sequence ${index + 1}`}
              loading="lazy"
            />
            <div class="sequence-position">
              {index + 1}
            </div>
          </div>

          <!-- Sequence info -->
          <div class="sequence-info">
            <div class="sequence-title">
              {sequence.name || `Sequence ${index + 1}`}
            </div>
            <div class="sequence-details">
              <span class="sequence-duration">
                {formatDuration(sequence.sequenceLength)}
              </span>
              {#if sequence.beats && sequence.beats.length > 0}
                <span class="sequence-beats">
                  {sequence.beats.length} beats
                </span>
              {/if}
            </div>
          </div>

          <!-- Sequence actions -->
          <div class="sequence-actions">
            <button
              class="remove-btn"
              onclick={(e) => handleSequenceRemove(sequence, index, e)}
              title="Remove sequence from act"
              aria-label="Remove sequence"
            >
              ✕
            </button>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <!-- Empty state -->
    <div class="empty-state">
      <div class="empty-icon">🎬</div>
      <h3>No Sequences</h3>
      <p>
        This act doesn't have any sequences yet.<br />
        Add sequences from the sequence builder or import them.
      </p>
    </div>
  {/if}
</div>

<style>
  .sequence-grid {
    display: flex;
    flex-direction: column;
    height: 100%;
    gap: var(--spacing-md);
  }

  .sequence-grid.empty {
    justify-content: center;
    align-items: center;
  }

  .grid-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: var(--spacing-sm);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .grid-header h3 {
    margin: 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: var(--font-size-lg);
    font-weight: 500;
  }

  .grid-actions {
    display: flex;
    gap: var(--spacing-sm);
  }

  .grid-container {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--spacing-md);
    overflow-y: auto;
    padding: var(--spacing-xs);
  }

  .word-card {
    display: flex;
    flex-direction: column;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transition: all var(--transition-fast);
    position: relative;
  }

  .word-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .word-card:focus {
    outline: 2px solid rgba(74, 144, 226, 0.8);
    outline-offset: 2px;
  }

  .sequence-thumbnail {
    position: relative;
    width: 100%;
    height: 160px;
    overflow: hidden;
    background: rgba(0, 0, 0, 0.3);
  }

  .sequence-thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform var(--transition-fast);
  }

  .word-card:hover .sequence-thumbnail img {
    transform: scale(1.05);
  }

  .sequence-position {
    position: absolute;
    top: var(--spacing-xs);
    left: var(--spacing-xs);
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: 4px;
    font-size: var(--font-size-sm);
    font-weight: 500;
  }

  .sequence-info {
    padding: var(--spacing-md);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    flex: 1;
  }

  .sequence-title {
    color: rgba(255, 255, 255, 0.9);
    font-size: var(--font-size-base);
    font-weight: 500;
    line-height: 1.3;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .sequence-details {
    display: flex;
    gap: var(--spacing-sm);
    align-items: center;
    font-size: var(--font-size-sm);
    color: rgba(255, 255, 255, 0.6);
  }

  .sequence-duration {
    font-weight: 500;
  }

  .sequence-beats {
    opacity: 0.8;
  }

  .sequence-actions {
    position: absolute;
    top: var(--spacing-xs);
    right: var(--spacing-xs);
    opacity: 0;
    transition: opacity var(--transition-fast);
  }

  .word-card:hover .sequence-actions {
    opacity: 1;
  }

  .remove-btn {
    background: rgba(220, 38, 38, 0.8);
    border: none;
    border-radius: 4px;
    color: white;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: var(--font-size-sm);
    transition: all var(--transition-fast);
  }

  .remove-btn:hover {
    background: rgba(220, 38, 38, 1);
    transform: scale(1.1);
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: var(--spacing-lg);
    max-width: 400px;
    padding: var(--spacing-xl);
  }

  .empty-icon {
    font-size: 4rem;
    opacity: 0.4;
  }

  .empty-state h3 {
    color: rgba(255, 255, 255, 0.8);
    font-size: var(--font-size-xl);
    margin: 0;
  }

  .empty-state p {
    color: rgba(255, 255, 255, 0.6);
    font-size: var(--font-size-base);
    margin: 0;
    line-height: 1.5;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .grid-container {
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: var(--spacing-sm);
    }

    .sequence-thumbnail {
      height: 140px;
    }

    .sequence-info {
      padding: var(--spacing-sm);
    }

    .empty-state {
      padding: var(--spacing-lg);
      gap: var(--spacing-md);
    }

    .empty-icon {
      font-size: 3rem;
    }
  }

  @media (max-width: 480px) {
    .grid-container {
      grid-template-columns: 1fr;
      gap: var(--spacing-sm);
    }

    .sequence-thumbnail {
      height: 120px;
    }

    .grid-header {
      flex-direction: column;
      align-items: stretch;
      gap: var(--spacing-sm);
    }

    .empty-state {
      padding: var(--spacing-md);
    }

    .empty-icon {
      font-size: 2.5rem;
    }
  }

  /* Ensure proper scrolling */
  @media (max-height: 600px) {
    .sequence-thumbnail {
      height: 100px;
    }

    .empty-state {
      gap: var(--spacing-sm);
    }

    .empty-icon {
      font-size: 2.5rem;
    }
  }
</style>
