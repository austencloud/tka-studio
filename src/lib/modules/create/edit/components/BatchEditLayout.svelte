<!--
BatchEditLayout.svelte - Batch editing interface for multiple beats

Replaces the normal edit panel when multiple beats are selected.
Uses simplified stepper controls matching the single-beat edit pattern.
-->
<script lang="ts">
  import type { BeatData, IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

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

  // Services
  let hapticService: IHapticFeedbackService;

  // Available turn values (0 to 3 in 0.5 increments)
  const TURN_OPTIONS = [0, 0.5, 1, 1.5, 2, 2.5, 3];

  // State for edited values (null means unchanged)
  // Left = Blue prop, Right = Red prop
  let blueTurn = $state<number | null>(null);
  let redTurn = $state<number | null>(null);

  // Container size awareness using runes + ResizeObserver
  let containerElement = $state<HTMLDivElement | null>(null);
  let containerHeight = $state(0);
  let containerWidth = $state(0);

  // Derived layout mode based on actual container size
  const layoutMode = $derived.by(() => {
    if (containerHeight === 0) return "default";
    if (containerHeight < 400) return "ultra-compact";
    if (containerHeight < 500) return "very-compact";
    if (containerHeight < 600) return "compact";
    return "default";
  });

  // Derived: Should we show header based on available space?
  const showHeader = $derived(containerHeight === 0 || containerHeight > 400);

  // Derived: Optimal button count based on space
  const visibleTurnOptions = $derived.by(() => {
    if (containerHeight < 400) {
      // Ultra-compact: Show fewer options for critical space
      return [0, 0.5, 1, 1.5, 2, 2.5, 3];
    }
    return TURN_OPTIONS;
  });

  // Derived: Smart button text based on available space
  const applyButtonText = $derived.by(() => {
    if (containerHeight < 400) return "Apply";
    if (containerHeight < 500) return `Apply to ${selectedBeats.length}`;
    return `Apply to ${selectedBeats.length} beat${selectedBeats.length !== 1 ? "s" : ""}`;
  });

  // Get current turn values from beat data
  function getTurnValue(beat: BeatData, color: "red" | "blue"): number {
    const motion = beat.motions?.[color];
    if (!motion) return 0;
    const turns = motion.turns ?? 0;
    // Handle "fl" (float) case - convert to 0
    return typeof turns === "number" ? turns : 0;
  }

  // Analyze current values across selection
  const blueValues = $derived(
    new Set<number>(selectedBeats.map((b: BeatData) => getTurnValue(b, "blue")))
  );
  const redValues = $derived(
    new Set<number>(selectedBeats.map((b: BeatData) => getTurnValue(b, "red")))
  );

  const hasEdits = $derived(blueTurn !== null || redTurn !== null);

  // Value selection handlers
  function handleSelectValue(field: "blue" | "red", value: number) {
    hapticService?.trigger("selection");

    if (field === "blue") {
      blueTurn = value;
    } else {
      redTurn = value;
    }
  }

  // Check if a value is currently selected
  function isValueSelected(field: "blue" | "red", value: number): boolean {
    if (field === "blue") {
      return blueTurn === value;
    } else {
      return redTurn === value;
    }
  }

  function handleApply() {
    // Build changes object with only edited fields
    const changes: any = {};

    if (blueTurn !== null) changes.blueTurn = blueTurn;
    if (redTurn !== null) changes.redTurn = redTurn;

    onApply(changes);

    // Reset after applying
    blueTurn = null;
    redTurn = null;
  }

  function handleCancel() {
    // Reset all edits
    blueTurn = null;
    redTurn = null;

    onCancel?.();
  }

  // Effect: Observe container size for reactive layout decisions
  $effect(() => {
    if (!containerElement) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        // Use content box for more accurate measurements
        const { blockSize, inlineSize } = entry.contentBoxSize[0] || {};
        containerHeight = blockSize || entry.contentRect.height;
        containerWidth = inlineSize || entry.contentRect.width;

        // Debug logging (can remove in production)
        console.log(
          `📏 Batch edit container: ${containerWidth}x${containerHeight}px (${layoutMode})`
        );
      }
    });

    resizeObserver.observe(containerElement);

    return () => {
      resizeObserver.disconnect();
    };
  });

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });
</script>

<div
  class="batch-edit-layout"
  bind:this={containerElement}
  data-layout-mode={layoutMode}
>
  <!-- Header - conditionally shown based on available space -->
  {#if showHeader}
    <div class="batch-header">
      <h3 class="batch-title">
        <i class="fas fa-edit"></i>
        {selectedBeats.length} Beat{selectedBeats.length !== 1 ? "s" : ""}
      </h3>
    </div>
  {/if}

  <!-- Turn Controls - Value selection buttons -->
  <div class="controls-section">
    <!-- Left (Blue Prop) -->
    <div class="turn-control blue">
      <div class="control-header">
        <span class="label">Left</span>
        <span class="prop-badge blue">Blue</span>
      </div>
      <div class="value-buttons">
        {#each visibleTurnOptions as value}
          <button
            class="value-btn"
            class:selected={isValueSelected("blue", value)}
            onclick={() => handleSelectValue("blue", value)}
            aria-label={`Set left (blue) turn to ${value}`}
            type="button"
          >
            {value}
          </button>
        {/each}
      </div>
    </div>

    <!-- Right (Red Prop) -->
    <div class="turn-control red">
      <div class="control-header">
        <span class="label">Right</span>
        <span class="prop-badge red">Red</span>
      </div>
      <div class="value-buttons">
        {#each visibleTurnOptions as value}
          <button
            class="value-btn"
            class:selected={isValueSelected("red", value)}
            onclick={() => handleSelectValue("red", value)}
            aria-label={`Set right (red) turn to ${value}`}
            type="button"
          >
            {value}
          </button>
        {/each}
      </div>
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
      {#if containerHeight >= 500}
        <i class="fas fa-check"></i>
      {/if}
      {applyButtonText}
    </button>
  </div>
</div>

<style>
  .batch-edit-layout {
    /* Container query context - responds to both width AND height */
    container-type: size;
    container-name: batch-edit;

    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 16px;
    height: 100%;
    overflow-y: auto;
  }

  /* Header */
  .batch-header {
    flex-shrink: 0;
  }

  .batch-title {
    margin: 0;
    font-size: 18px;
    font-weight: 700;
    color: hsl(var(--foreground));
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .batch-title i {
    color: hsl(var(--primary));
  }

  /* Controls Section */
  .controls-section {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  /* Turn Control - Value selection pattern */
  .turn-control {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 12px;
    border-radius: 12px;
    border: 2px solid;
    background: white;
  }

  .turn-control.blue {
    border-color: #3b82f6;
    background: linear-gradient(
      135deg,
      rgba(59, 130, 246, 0.05) 0%,
      white 100%
    );
  }

  .turn-control.red {
    border-color: #ef4444;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, white 100%);
  }

  /* Control Header - Label and badge on same row */
  .control-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  /* Label (Left/Right) */
  .label {
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 0.5px;
  }

  .turn-control.blue .label {
    color: #3b82f6;
  }

  .turn-control.red .label {
    color: #ef4444;
  }

  /* Value Buttons Grid - 7 buttons in a row */
  .value-buttons {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 6px;
  }

  /* Individual Value Button */
  .value-btn {
    padding: 10px 4px;
    border-radius: 8px;
    border: 2px solid;
    background: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .turn-control.blue .value-btn {
    border-color: #3b82f6;
    color: #3b82f6;
  }

  .turn-control.red .value-btn {
    border-color: #ef4444;
    color: #ef4444;
  }

  /* Selected state */
  .turn-control.blue .value-btn.selected {
    background: #3b82f6;
    color: white;
    border-color: #2563eb;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  }

  .turn-control.red .value-btn.selected {
    background: #ef4444;
    color: white;
    border-color: #dc2626;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
  }

  .value-btn:hover:not(.selected) {
    transform: scale(1.05);
  }

  .value-btn:active {
    transform: scale(0.95);
  }

  .turn-control.blue .value-btn:active:not(.selected) {
    background: rgba(59, 130, 246, 0.1);
  }

  .turn-control.red .value-btn:active:not(.selected) {
    background: rgba(239, 68, 68, 0.1);
  }

  /* Prop Badge (Red/Blue) */
  .prop-badge {
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
    min-width: 50px;
    text-align: center;
    justify-self: center;
  }

  .prop-badge.blue {
    background: rgba(59, 130, 246, 0.15);
    color: #3b82f6;
  }

  .prop-badge.red {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
  }

  /* Action Buttons */
  .actions {
    flex-shrink: 0;
    display: flex;
    gap: 12px;
    padding-top: 12px;
    border-top: 1px solid hsl(var(--border));
  }

  .action-button {
    flex: 1;
    padding: 14px 20px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
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

  /* Container Queries - Responsive to actual available space */

  /* Compact mode - for constrained height (Z Fold with URL bar, etc.) */
  @container batch-edit (max-height: 600px) {
    .batch-edit-layout {
      padding: 8px;
      gap: 8px;
    }

    .batch-title {
      font-size: 14px;
    }

    .turn-control {
      gap: 6px;
      padding: 8px;
      border-width: 2px;
    }

    .control-header {
      margin-bottom: 4px;
    }

    .label {
      font-size: 13px;
    }

    .value-buttons {
      gap: 3px;
    }

    .value-btn {
      padding: 6px 2px;
      font-size: 12px;
      min-height: 36px;
      border-width: 1.5px;
    }

    .prop-badge {
      font-size: 9px;
      padding: 3px 6px;
    }

    .actions {
      padding-top: 8px;
      gap: 8px;
    }

    .action-button {
      padding: 10px 16px;
      font-size: 14px;
      min-height: 40px;
    }
  }

  /* Very compact mode - for very constrained height */
  @container batch-edit (max-height: 500px) {
    .batch-edit-layout {
      padding: 6px;
      gap: 6px;
    }

    .batch-title {
      font-size: 13px;
    }

    .turn-control {
      gap: 4px;
      padding: 6px;
      border-width: 1.5px;
    }

    .label {
      font-size: 12px;
    }

    .value-buttons {
      gap: 2px;
    }

    .value-btn {
      padding: 4px 1px;
      font-size: 11px;
      min-height: 32px;
      border-width: 1px;
    }

    .prop-badge {
      font-size: 8px;
      padding: 2px 4px;
    }

    .actions {
      padding-top: 6px;
      gap: 6px;
    }

    .action-button {
      padding: 8px 12px;
      font-size: 13px;
      min-height: 36px;
    }
  }

  /* Ultra-compact mode - for extremely constrained height (Z Fold folded with URL bar) */
  @container batch-edit (max-height: 400px) {
    .batch-edit-layout {
      padding: 4px;
      gap: 4px;
    }

    .batch-title {
      font-size: 12px;
    }

    .turn-control {
      gap: 3px;
      padding: 4px;
      border-width: 1px;
      border-radius: 8px;
    }

    .label {
      font-size: 11px;
    }

    .value-buttons {
      gap: 2px;
    }

    .value-btn {
      padding: 3px 1px;
      font-size: 10px;
      min-height: 28px;
      border-width: 1px;
      border-radius: 6px;
    }

    .prop-badge {
      font-size: 7px;
      padding: 2px 3px;
      min-width: 35px;
    }

    .actions {
      padding-top: 4px;
      gap: 4px;
      border-top-width: 0.5px;
    }

    .action-button {
      padding: 6px 10px;
      font-size: 12px;
      min-height: 32px;
      border-radius: 6px;
    }
  }

  /* Narrow width adjustments (in addition to height) */
  @container batch-edit (max-width: 400px) {
    .value-btn {
      font-size: clamp(10px, 2.5vw, 12px);
    }

    .label,
    .prop-badge {
      font-size: clamp(10px, 2.5vw, 13px);
    }
  }
</style>
