<!--
PictographAdjustmentEditorPanel.svelte - Arrow Adjustment Editor

Full-screen panel for adjusting arrow positions with WASD keyboard controls.
Features:
- Clickable, selectable arrows with visual feedback
- WASD keyboard controls for arrow movement
- Modifier keys: Shift (20px), Shift+Ctrl (200px)
- Adjustment value display
- Hotkey legend
-->
<script lang="ts">
  import type { IKeyboardArrowAdjustmentService } from "$create/shared/services/contracts/IKeyboardArrowAdjustmentService";
  import { selectedArrowState } from "$create/shared/state/selected-arrow-state.svelte";
  import type { BeatData } from "$create/workspace-panel";
  import type { IHapticFeedbackService } from "$shared";
  import { Drawer, Pictograph, resolve, TYPES } from "$shared";
  import { onMount } from 'svelte';

  // Props
  const {
    isOpen = false,
    onClose,
    selectedBeatData,
    onBeatDataUpdate,
  } = $props<{
    isOpen: boolean;
    onClose: () => void;
    selectedBeatData: BeatData | null;
    onBeatDataUpdate?: (updatedBeatData: BeatData) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = null;
  let keyboardAdjustmentService: IKeyboardArrowAdjustmentService | null = null;

  // State
  let currentIncrement = $state(5); // 5, 20, or 200
  let lastAdjustment = $state({ x: 0, y: 0 });

  // Keyboard handler
  function handleKeydown(event: KeyboardEvent) {
    if (!isOpen) {
      console.log('[Keydown] Panel not open, ignoring');
      return;
    }

    const key = event.key.toLowerCase();
    console.log('[Keydown] Key pressed:', key, 'Panel open:', isOpen);

    // Close on Escape
    if (key === 'escape') {
      event.preventDefault();
      handleClose();
      return;
    }

    // Calculate increment based on modifiers
    const shiftHeld = event.shiftKey;
    const ctrlHeld = event.ctrlKey;

    if (shiftHeld && ctrlHeld) {
      currentIncrement = 200;
    } else if (shiftHeld) {
      currentIncrement = 20;
    } else {
      currentIncrement = 5;
    }

    // Handle WASD movement
    if (['w', 'a', 's', 'd'].includes(key)) {
      console.log('[Keydown] WASD key detected:', key, 'increment:', currentIncrement);
      event.preventDefault();
      handleWASDMovement(key as 'w' | 'a' | 's' | 'd');
    }
  }

  function handleWASDMovement(key: 'w' | 'a' | 's' | 'd') {
    if (!selectedArrowState.selectedArrow) {
      console.warn('[WASD] No arrow selected');
      return;
    }

    if (!selectedBeatData) {
      console.warn('[WASD] No beat data available');
      return;
    }

    if (!keyboardAdjustmentService) {
      console.warn('[WASD] Keyboard adjustment service not initialized');
      return;
    }

    // Calculate adjustment for display
    const adjustment = keyboardAdjustmentService.calculateAdjustment(key, currentIncrement);
    lastAdjustment = adjustment;

    // Apply the adjustment using the service
    const updatedBeatData = keyboardAdjustmentService.handleWASDMovement(
      key,
      currentIncrement,
      selectedArrowState.selectedArrow,
      selectedBeatData
    );

    // Notify parent component of the update
    if (onBeatDataUpdate) {
      onBeatDataUpdate(updatedBeatData);
    }

    // Haptic feedback
    hapticService?.trigger('selection');
  }

  function handleClose() {
    selectedArrowState.clearSelection();
    hapticService?.trigger('selection');
    onClose();
  }

  // Lifecycle
  onMount(() => {
    try {
      hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
      keyboardAdjustmentService = resolve<IKeyboardArrowAdjustmentService>(TYPES.IKeyboardArrowAdjustmentService);
    } catch (error) {
      console.error('[PictographAdjustment] Failed to initialize services:', error);
    }

    return undefined;
  });

  // Add/remove keyboard listener when panel opens/closes
  $effect(() => {
    if (isOpen) {
      window.addEventListener('keydown', handleKeydown);
      return () => {
        window.removeEventListener('keydown', handleKeydown);
      };
    }
    return undefined;
  });

  // Clear selection when panel closes
  $effect(() => {
    if (!isOpen) {
      selectedArrowState.clearSelection();
    }
  });

  // Derived state
  const selectedArrow = $derived(selectedArrowState.selectedArrow);
</script>

<Drawer
  isOpen={isOpen}
  labelledBy="adjustment-panel-title"
  on:close={handleClose}
  closeOnBackdrop={true}
  focusTrap={true}
  lockScroll={true}
  showHandle={false}
  placement="bottom"
  class="adjustment-editor-container"
>
  <div class="adjustment-panel">
    <!-- Header -->
    <div class="panel-header">
      <h2 id="adjustment-panel-title" class="panel-title">
        <i class="fas fa-crosshairs"></i>
        Adjust Arrows
      </h2>
      <button
        class="close-button"
        onclick={handleClose}
        aria-label="Close adjustment panel"
        type="button"
      >
        <i class="fas fa-times"></i>
      </button>
    </div>

    <!-- Main content area -->
    <div class="panel-content">
      <!-- Pictograph display with clickable arrows -->
      <div class="pictograph-section">
        {#if selectedBeatData && !selectedBeatData.isBlank}
          <Pictograph
            pictographData={selectedBeatData}
            arrowsClickable={true}
            disableContentTransitions={true}
          />
        {:else}
          <div class="no-pictograph">
            <div class="placeholder-icon">🎯</div>
            <p>No pictograph selected</p>
          </div>
        {/if}
      </div>

      <!-- Controls and info panel -->
      <div class="controls-section">
        <!-- Selected arrow info -->
        {#if selectedArrow}
          <div class="info-card">
            <h3 class="info-title">Selected Arrow</h3>
            <div class="info-content">
              <div class="info-item">
                <span class="info-label">Color:</span>
                <span class="info-value" class:blue={selectedArrow.color === 'blue'} class:red={selectedArrow.color === 'red'}>
                  {selectedArrow.color}
                </span>
              </div>
              <div class="info-item">
                <span class="info-label">Type:</span>
                <span class="info-value">{selectedArrow.motionData.motionType}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Last Adjustment:</span>
                <span class="info-value">
                  X: {lastAdjustment.x > 0 ? '+' : ''}{lastAdjustment.x}px,
                  Y: {lastAdjustment.y > 0 ? '+' : ''}{lastAdjustment.y}px
                </span>
              </div>
            </div>
          </div>
        {:else}
          <div class="info-card empty">
            <p class="hint">Click an arrow to select it</p>
          </div>
        {/if}

        <!-- Increment indicator -->
        <div class="increment-card">
          <h3 class="info-title">Movement Increment</h3>
          <div class="increment-display">
            <span class="increment-value">{currentIncrement}px</span>
            <div class="increment-hint">
              {#if currentIncrement === 5}
                <span>Default</span>
              {:else if currentIncrement === 20}
                <span><kbd>Shift</kbd> held</span>
              {:else}
                <span><kbd>Shift</kbd> + <kbd>Ctrl</kbd> held</span>
              {/if}
            </div>
          </div>
        </div>

        <!-- Hotkey legend -->
        <div class="hotkey-legend">
          <h3 class="info-title">Keyboard Controls</h3>
          <div class="hotkey-list">
            <div class="hotkey-item">
              <div class="hotkeys">
                <kbd>W</kbd>
                <kbd>A</kbd>
                <kbd>S</kbd>
                <kbd>D</kbd>
              </div>
              <span class="hotkey-desc">Move arrow</span>
            </div>
            <div class="hotkey-item">
              <kbd>Shift</kbd>
              <span class="hotkey-desc">Large increment (20px)</span>
            </div>
            <div class="hotkey-item">
              <kbd>Shift</kbd> + <kbd>Ctrl</kbd>
              <span class="hotkey-desc">Huge increment (200px)</span>
            </div>
            <div class="hotkey-item">
              <kbd>Esc</kbd>
              <span class="hotkey-desc">Close panel</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</Drawer>

<style>
  :global(.bottom-sheet.adjustment-editor-container) {
    --sheet-width: 100%;
    --sheet-max-height: 90vh;
    --sheet-bg: var(--sheet-bg-solid);
    --sheet-border: var(--sheet-border-strong);
  }

  .adjustment-panel {
    display: flex;
    flex-direction: column;
    height: 90vh;
    background: var(--sheet-bg-solid);
  }

  /* Header */
  .panel-header {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-lg) var(--spacing-xl);
    background: #252540;
    border-bottom: var(--sheet-border-strong);
  }

  .panel-title {
    margin: 0;
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: var(--foreground);
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .close-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background: hsl(var(--muted));
    color: hsl(var(--foreground));
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: hsl(var(--muted) / 0.8);
    transform: scale(1.1) rotate(90deg);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  /* Content */
  .panel-content {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 400px;
    gap: 0;
    min-height: 0;
    overflow: hidden;
  }

  .pictograph-section {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xl);
    background: rgba(255, 255, 255, 0.02);
  }

  .no-pictograph {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--muted-foreground);
    gap: var(--spacing-md);
  }

  .placeholder-icon {
    font-size: 4rem;
    opacity: 0.5;
  }

  .controls-section {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
    padding: var(--spacing-xl);
    background: #1a1a2e;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    overflow-y: auto;
  }

  /* Info cards */
  .info-card {
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .info-card.empty {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100px;
  }

  .info-title {
    margin: 0 0 var(--spacing-md) 0;
    font-size: var(--font-size-md);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
  }

  .info-content {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .info-label {
    font-size: var(--font-size-sm);
    color: rgba(255, 255, 255, 0.6);
  }

  .info-value {
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
  }

  .info-value.blue {
    color: #60a5fa;
  }

  .info-value.red {
    color: #f87171;
  }

  .hint {
    font-size: var(--font-size-sm);
    color: rgba(255, 255, 255, 0.5);
    margin: 0;
  }

  /* Increment display */
  .increment-card {
    padding: var(--spacing-lg);
    background: rgba(251, 191, 36, 0.1);
    border-radius: var(--border-radius);
    border: 1px solid rgba(251, 191, 36, 0.3);
  }

  .increment-display {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .increment-value {
    font-size: 2rem;
    font-weight: 700;
    color: #fbbf24;
  }

  .increment-hint {
    font-size: var(--font-size-sm);
    color: rgba(255, 255, 255, 0.7);
  }

  /* Hotkey legend */
  .hotkey-legend {
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .hotkey-list {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .hotkey-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .hotkeys {
    display: flex;
    gap: var(--spacing-xs);
  }

  kbd {
    padding: 4px 8px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-family: monospace;
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.9);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .hotkey-desc {
    font-size: var(--font-size-sm);
    color: rgba(255, 255, 255, 0.7);
  }

  /* Mobile responsive */
  @media (max-width: 1024px) {
    .panel-content {
      grid-template-columns: 1fr;
      grid-template-rows: 1fr auto;
    }

    .controls-section {
      border-left: none;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      max-height: 50vh;
    }
  }
</style>
