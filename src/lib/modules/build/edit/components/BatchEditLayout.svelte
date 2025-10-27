<!--
BatchEditLayout.svelte - Batch editing interface for multiple beats

Replaces the normal edit panel when multiple beats are selected.
Shows thumbnails and simplified controls without the graph.
-->
<script lang="ts">
  import type { BeatData } from "$shared";
  import PictographThumbnailGrid from './PictographThumbnailGrid.svelte';
  import MixedValueDropdown from './MixedValueDropdown.svelte';

  // Props
  const {
    selectedBeats = [],
    onApply,
    onCancel,
  } = $props<{
    selectedBeats: BeatData[];
    onApply: (changes: Partial<BeatData>) => void;
    onCancel?: () => void;
  }>();

  // Turn value options (0-3 turns)
  const TURN_VALUES = [0, 1, 2, 3];

  // State for edited values
  let leftRedTurn = $state<number | null>(null);
  let rightRedTurn = $state<number | null>(null);
  let leftBlueTurn = $state<number | null>(null);
  let rightBlueTurn = $state<number | null>(null);

  // Analyze current values across selection
  // @ts-ignore - Turn properties accessed dynamically
  const leftRedValues = $derived(new Set<number>(selectedBeats.map((b: any) => b.leftRedTurn ?? 0)));
  // @ts-ignore - Turn properties accessed dynamically
  const rightRedValues = $derived(new Set<number>(selectedBeats.map((b: any) => b.rightRedTurn ?? 0)));
  // @ts-ignore - Turn properties accessed dynamically
  const leftBlueValues = $derived(new Set<number>(selectedBeats.map((b: any) => b.leftBlueTurn ?? 0)));
  // @ts-ignore - Turn properties accessed dynamically
  const rightBlueValues = $derived(new Set<number>(selectedBeats.map((b: any) => b.rightBlueTurn ?? 0)));

  const hasEdits = $derived(
    leftRedTurn !== null ||
    rightRedTurn !== null ||
    leftBlueTurn !== null ||
    rightBlueTurn !== null
  );

  function handleApply() {
    // Build changes object with only edited fields
    const changes: any = {};

    if (leftRedTurn !== null) changes.leftRedTurn = leftRedTurn;
    if (rightRedTurn !== null) changes.rightRedTurn = rightRedTurn;
    if (leftBlueTurn !== null) changes.leftBlueTurn = leftBlueTurn;
    if (rightBlueTurn !== null) changes.rightBlueTurn = rightBlueTurn;

    onApply(changes);
  }

  function handleCancel() {
    // Reset all edits
    leftRedTurn = null;
    rightRedTurn = null;
    leftBlueTurn = null;
    rightBlueTurn = null;

    onCancel?.();
  }
</script>

<div class="batch-edit-layout">
  <!-- Header -->
  <div class="batch-header">
    <h3 class="batch-title">
      <i class="fas fa-edit"></i>
      Editing {selectedBeats.length} Beat{selectedBeats.length !== 1 ? 's' : ''}
    </h3>
  </div>

  <!-- Pictograph Thumbnails -->
  <div class="thumbnails-section">
    <PictographThumbnailGrid {selectedBeats} />
  </div>

  <!-- Turn Controls -->
  <div class="controls-section">
    <h4 class="section-title">Turn Controls</h4>

    <div class="controls-grid">
      <!-- Red Prop Turns -->
      <div class="control-group">
        <div class="group-label">
          <span class="prop-color red"></span>
          Red Prop
        </div>

        <MixedValueDropdown
          label="Left Turn"
          values={TURN_VALUES}
          currentValues={leftRedValues}
          bind:selectedValue={leftRedTurn}
        />

        <MixedValueDropdown
          label="Right Turn"
          values={TURN_VALUES}
          currentValues={rightRedValues}
          bind:selectedValue={rightRedTurn}
        />
      </div>

      <!-- Blue Prop Turns -->
      <div class="control-group">
        <div class="group-label">
          <span class="prop-color blue"></span>
          Blue Prop
        </div>

        <MixedValueDropdown
          label="Left Turn"
          values={TURN_VALUES}
          currentValues={leftBlueValues}
          bind:selectedValue={leftBlueTurn}
        />

        <MixedValueDropdown
          label="Right Turn"
          values={TURN_VALUES}
          currentValues={rightBlueValues}
          bind:selectedValue={rightBlueTurn}
        />
      </div>
    </div>
  </div>

  <!-- Info Banner -->
  <div class="info-banner">
    <i class="fas fa-info-circle"></i>
    <div class="info-text">
      {#if hasEdits}
        <strong>Changes will apply to all {selectedBeats.length} beats.</strong>
        Unchanged fields will keep their current values.
      {:else}
        Select values to change. Only edited fields will be updated.
      {/if}
    </div>
  </div>

  <!-- Action Buttons -->
  <div class="actions">
    <button
      class="action-button cancel-button"
      onclick={handleCancel}
      type="button"
    >
      Cancel
    </button>

    <button
      class="action-button apply-button"
      onclick={handleApply}
      disabled={!hasEdits}
      type="button"
    >
      <i class="fas fa-check"></i>
      Apply to All
    </button>
  </div>
</div>

<style>
  .batch-edit-layout {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg) var(--spacing-xl);
    height: 100%;
    overflow-y: auto;
  }

  /* Header */
  .batch-header {
    flex-shrink: 0;
  }

  .batch-title {
    margin: 0;
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: hsl(var(--foreground));
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .batch-title i {
    color: hsl(var(--primary));
  }

  /* Thumbnails */
  .thumbnails-section {
    flex-shrink: 0;
    border-bottom: 1px solid hsl(var(--border));
    padding-bottom: var(--spacing-md);
  }

  /* Controls */
  .controls-section {
    flex: 1;
    overflow-y: auto;
  }

  .section-title {
    margin: 0 0 var(--spacing-md) 0;
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: hsl(var(--foreground));
  }

  .controls-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }

  @media (min-width: 600px) {
    .controls-grid {
      grid-template-columns: 1fr 1fr;
    }
  }

  .control-group {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
    background: hsl(var(--muted) / 0.3);
    border: 1px solid hsl(var(--border));
    border-radius: 8px;
  }

  .group-label {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    font-size: var(--font-size-md);
    font-weight: 600;
    color: hsl(var(--foreground));
    margin-bottom: var(--spacing-xs);
  }

  .prop-color {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    border: 2px solid currentColor;
  }

  .prop-color.red {
    background: #ef4444;
    border-color: #dc2626;
  }

  .prop-color.blue {
    background: #3b82f6;
    border-color: #2563eb;
  }

  /* Info Banner */
  .info-banner {
    flex-shrink: 0;
    display: flex;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    background: hsl(var(--primary) / 0.1);
    border: 1px solid hsl(var(--primary) / 0.3);
    border-radius: 8px;
  }

  .info-banner i {
    color: hsl(var(--primary));
    flex-shrink: 0;
    margin-top: 2px;
  }

  .info-text {
    flex: 1;
    font-size: var(--font-size-sm);
    color: hsl(var(--foreground));
  }

  /* Actions */
  .actions {
    flex-shrink: 0;
    display: flex;
    gap: var(--spacing-md);
    padding-top: var(--spacing-md);
    border-top: 1px solid hsl(var(--border));
  }

  .action-button {
    flex: 1;
    padding: var(--spacing-md) var(--spacing-lg);
    border: none;
    border-radius: 8px;
    font-size: var(--font-size-md);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
    min-height: 48px;
  }

  .cancel-button {
    background: hsl(var(--muted));
    color: hsl(var(--foreground));
  }

  .cancel-button:hover {
    background: hsl(var(--muted) / 0.8);
  }

  .apply-button {
    background: hsl(var(--primary));
    color: hsl(var(--primary-foreground));
  }

  .apply-button:hover:not(:disabled) {
    background: hsl(var(--primary) / 0.9);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px hsl(var(--primary) / 0.4);
  }

  .apply-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .apply-button:active:not(:disabled) {
    transform: translateY(0);
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .batch-edit-layout {
      padding: var(--spacing-md) var(--spacing-lg);
      gap: var(--spacing-md);
    }

    .batch-title {
      font-size: var(--font-size-lg);
    }

    .section-title {
      font-size: var(--font-size-md);
    }

    .controls-grid {
      grid-template-columns: 1fr;
    }

    .actions {
      flex-direction: column;
    }

    .action-button {
      width: 100%;
    }
  }
</style>
