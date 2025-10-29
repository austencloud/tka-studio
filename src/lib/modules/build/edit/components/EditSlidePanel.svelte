<!--
EditSlidePanel.svelte - Ultra-modern slide-out edit panel

Features:
- 🎨 Glassmorphism with backdrop blur
- 🌊 Smooth spring animations
- ⌨️ Keyboard shortcuts (Esc to close)
- 📱 Mobile-friendly with swipe gestures
- 🎯 Context-aware editing without leaving the flow
-->
<script lang="ts">
  import type { BeatData } from "$build/workspace-panel";
  import type { IHapticFeedbackService } from "$shared";
  import { BottomSheet, resolve, TYPES } from "$shared";
  import { onDestroy, onMount } from 'svelte';
  import RemoveBeatButton from '../../workspace-panel/shared/components/buttons/RemoveBeatButton.svelte';
  import BatchEditLayout from './BatchEditLayout.svelte';
  import EditPanelLayout from './EditPanelLayout.svelte';

  // Props
  const {
    isOpen = false,
    onClose,
    selectedBeatNumber,
    selectedBeatData,
    selectedBeatsData = null, // NEW: For batch mode
    combinedPanelHeight = 0,
    isSideBySideLayout = false,
    onOrientationChanged,
    onTurnAmountChanged,
    onBatchApply, // NEW: Batch apply callback
    onRemoveBeat, // Remove beat callback
  } = $props<{
    isOpen: boolean;
    onClose: () => void;
    selectedBeatNumber: number | null; // 0=start, 1=first beat, 2=second beat, etc.
    selectedBeatData: BeatData | null;
    selectedBeatsData?: BeatData[] | null; // NEW: Multiple beats for batch edit
    combinedPanelHeight?: number;
    isSideBySideLayout?: boolean;
    onOrientationChanged: (color: string, orientation: string) => void;
    onTurnAmountChanged: (color: string, turnAmount: number) => void;
    onBatchApply?: (changes: Partial<BeatData>) => void; // NEW: Batch mode
    onRemoveBeat?: (beatNumber: number) => void; // Remove beat callback
  }>();

  // Detect batch mode
  const isBatchMode = $derived(
    selectedBeatsData && selectedBeatsData.length > 1
  );

  const shouldUseBottomPlacement = $derived(() => !isSideBySideLayout);

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  // Component refs
  let editPanelLayoutRef: EditPanelLayout | null = $state(null);
  let panelElement: HTMLElement | null = $state(null);

  // Touch gesture state
  let touchStartX = $state(0);
  let touchCurrentX = $state(0);
  let touchStartY = $state(0);
  let touchCurrentY = $state(0);
  let isDragging = $state(false);

  // Device detection for responsive behavior
  let isMobile = $state(false);
  let windowWidth = $state(0);


  // Calculate panel height dynamically to match tool panel + button panel
  const panelHeightStyle = $derived(() => {
    if (combinedPanelHeight > 0) {
      return `height: ${combinedPanelHeight}px;`;
    }
    return 'height: 70vh;';
  });

  // Keyboard handler
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape' && isOpen) {
      event.preventDefault();
      handleClose();
    }
  }

  // Close handler with haptic feedback
  function handleClose() {
    hapticService?.trigger('selection');
    onClose();
  }

  // Note: No backdrop click handler - allow clicking beats to switch editing
  // Users can close via: X button, Escape key, or swipe gesture

  // Touch gesture handlers for swipe-to-dismiss
  // Mobile: Vertical swipe (down to dismiss from bottom)
  // Desktop: Horizontal swipe (right to dismiss from side)
  function handleTouchStart(event: TouchEvent) {
    touchStartX = event.touches[0].clientX;
    touchCurrentX = touchStartX;
    touchStartY = event.touches[0].clientY;
    touchCurrentY = touchStartY;
    isDragging = true;
  }

  function handleTouchMove(event: TouchEvent) {
    if (!isDragging) return;
    touchCurrentX = event.touches[0].clientX;
    touchCurrentY = event.touches[0].clientY;

    if (shouldUseBottomPlacement()) {
      // Bottom placement: Allow dragging downward (to close from bottom)
      const deltaY = touchCurrentY - touchStartY;
      if (deltaY > 0 && panelElement) {
        panelElement.style.transform = `translateY(${deltaY}px)`;
      }
    } else {
      // Side placement: Allow dragging to the right (to close from side)
      const deltaX = touchCurrentX - touchStartX;
      if (deltaX > 0 && panelElement) {
        panelElement.style.transform = `translateX(${deltaX}px)`;
      }
    }
  }

  function handleTouchEnd() {
    if (!isDragging) return;
    isDragging = false;

    const threshold = 100; // Swipe threshold in pixels

    if (panelElement) {
      if (shouldUseBottomPlacement()) {
        // Bottom placement: Check vertical swipe distance
        const deltaY = touchCurrentY - touchStartY;
        if (deltaY > threshold) {
          // Swipe far enough - close the panel
          hapticService?.trigger('warning');
          onClose();
        } else {
          // Snap back
          panelElement.style.transform = 'translateY(0)';
          panelElement.style.transition = 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
          setTimeout(() => {
            if (panelElement) {
              panelElement.style.transition = '';
            }
          }, 300);
        }
      } else {
        // Side placement: Check horizontal swipe distance
        const deltaX = touchCurrentX - touchStartX;
        if (deltaX > threshold) {
          // Swipe far enough - close the panel
          hapticService?.trigger('warning');
          onClose();
        } else {
          // Snap back
          panelElement.style.transform = 'translateX(0)';
          panelElement.style.transition = 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
          setTimeout(() => {
            if (panelElement) {
              panelElement.style.transition = '';
            }
          }, 300);
        }
      }
    }
  }

  // Window resize handler
  function handleResize() {
    if (typeof window !== 'undefined') {
      windowWidth = window.innerWidth;
      isMobile = windowWidth < 768;
    }
  }

  // Lifecycle
  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    handleResize();

    // Add event listeners
    window.addEventListener('keydown', handleKeydown);
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('keydown', handleKeydown);
      window.removeEventListener('resize', handleResize);
    };
  });

  onDestroy(() => {
    window.removeEventListener('keydown', handleKeydown);
    window.removeEventListener('resize', handleResize);
  });

  // Reactive: Trigger haptic when panel opens
  $effect(() => {
    if (isOpen) {
      hapticService?.trigger('selection');
    }
  });

  // Handle remove beat click
  function handleRemoveBeat() {
    if (selectedBeatNumber !== null && selectedBeatNumber >= 1) {
      onRemoveBeat?.(selectedBeatNumber);
      // Close the panel after deletion
      handleClose();
    }
  }

  // Determine if we should show the remove beat button
  const shouldShowRemoveButton = $derived(
    !isBatchMode && selectedBeatNumber !== null && selectedBeatNumber >= 1
  );
</script>

<BottomSheet
  isOpen={isOpen}
  labelledBy="edit-panel-title"
  on:close={handleClose}
  closeOnBackdrop={true}
  focusTrap={false}
  lockScroll={false}
  showHandle={false}
  placement={shouldUseBottomPlacement() ? "bottom" : "right"}
  class="edit-panel-container"
  backdropClass="edit-panel-backdrop"
>
  <div
    bind:this={panelElement}
    class="edit-panel"
    class:mobile={shouldUseBottomPlacement()}
    style={panelHeightStyle()}
    ontouchstart={handleTouchStart}
    ontouchmove={handleTouchMove}
    ontouchend={handleTouchEnd}
  >
    <div class="edit-panel-header">
      <!-- Left: Remove Beat Button -->
      <div class="header-left">
        {#if shouldShowRemoveButton}
          <RemoveBeatButton
            beatNumber={selectedBeatNumber}
            onclick={handleRemoveBeat}
          />
        {/if}
      </div>

      <!-- Center: Title -->
      <h2 id="edit-panel-title" class="edit-panel-title">
        {#if isBatchMode}
          Batch Edit
        {:else if selectedBeatNumber === 0}
          Edit Start Position
        {:else}
          Edit Beat {selectedBeatNumber}
        {/if}
      </h2>

      <!-- Right: Close Button -->
      <div class="header-right">
        <button
          class="close-button"
          onclick={handleClose}
          aria-label="Close edit panel"
          type="button"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>

    {#if !isMobile}
      <div class="keyboard-hint">
        Press <kbd>Esc</kbd> to close
      </div>
    {/if}

    <div class="edit-panel-content">
      {#if isBatchMode && selectedBeatsData}
        <BatchEditLayout
          selectedBeats={selectedBeatsData}
          onApply={(changes) => onBatchApply?.(changes)}
          onCancel={handleClose}
        />
      {:else}
        <EditPanelLayout
          bind:this={editPanelLayoutRef}
          selectedBeatIndex={selectedBeatNumber}
          {selectedBeatData}
          {onOrientationChanged}
          {onTurnAmountChanged}
        />
      {/if}
    </div>
  </div>
</BottomSheet>
<style>
  :global(.bottom-sheet-backdrop.edit-panel-backdrop) {
    background: transparent; /* Fully transparent - no dimming at all */
    backdrop-filter: none !important; /* No blur - keep background fully visible */
    pointer-events: auto;
  }

  :global(.bottom-sheet-backdrop.edit-panel-backdrop[data-placement="right"]) {
    justify-content: flex-end;
    align-items: stretch;
  }

  :global(.bottom-sheet-backdrop.edit-panel-backdrop[data-placement="bottom"]) {
    justify-content: stretch;
    align-items: flex-end;
  }

  :global(.bottom-sheet.edit-panel-container) {
    background: transparent;
    border: none;
    box-shadow: none;
    width: min(600px, 90vw);
    max-height: none;
    padding-bottom: 0;
    pointer-events: auto;
  }

  :global(.bottom-sheet.edit-panel-container[data-placement="bottom"]) {
    width: 100%;
    /* Height controlled by inner .edit-panel div */
  }

  :global(.bottom-sheet.edit-panel-container[data-placement="right"]) {
    height: auto;
    max-height: 90vh;
  }

  /* The slide-out panel itself - OPAQUE, not glass */
  .edit-panel {
    position: relative;
    width: min(600px, 90vw);
    /* Height set dynamically via inline style */

    /* FULLY OPAQUE solid background - dark theme color */
    background: #1a1a2e;
    border-left: 1px solid rgba(255, 255, 255, 0.2);

    /* Premium shadow */
    box-shadow:
      -8px 0 32px rgba(0, 0, 0, 0.3),
      -2px 0 8px rgba(0, 0, 0, 0.2);

    display: flex;
    flex-direction: column;

    /* Re-enable pointer events for the panel itself */
    pointer-events: auto;
  }

  /* Mobile: Full-width bottom panel with beautiful rounded top corners */
  .edit-panel.mobile {
    width: 100vw;
    /* Height set dynamically via inline style to match tool panel height */
    /* Fallback max-height if dynamic height not available */
    max-height: 75vh;

    /* Remove side border, add top border */
    border-left: none;
    border-top: 1px solid hsl(var(--border));

    /* Gorgeous rounded top corners for bottom-slide aesthetic */
    border-radius: 24px 24px 0 0;

    /* Shadow goes UPWARD for bottom panel - stronger for visibility */
    box-shadow:
      0 -8px 32px rgba(0, 0, 0, 0.4),
      0 -4px 16px rgba(0, 0, 0, 0.3),
      0 -2px 8px rgba(0, 0, 0, 0.2);

    /* Entire panel is draggable */
    cursor: grab;
  }

  .edit-panel.mobile:active {
    cursor: grabbing;
  }

  /* Subtle drag indicator at top - doesn't take layout space */
  .edit-panel.mobile::before {
    content: '';
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 4px;
    border-radius: 2px;
    background: rgba(255, 255, 255, 0.3);
    pointer-events: none;
    z-index: 1;
  }

  /* Header - 3-column layout: left (remove button), center (title), right (close button) */
  .edit-panel-header {
    flex-shrink: 0;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    padding: var(--spacing-lg) var(--spacing-xl);

    /* Solid opaque header - matches panel background */
    background: #252540;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .header-left {
    display: flex;
    align-items: center;
    justify-content: flex-start;
  }

  .edit-panel-title {
    margin: 0;
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: var(--foreground);
    text-align: center;
    justify-self: center; /* Center in grid column */

    /* Subtle text shadow for depth */
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .header-right {
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }

  /* Close button - modern and clean */
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
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    font-size: var(--font-size-lg);

    /* Subtle inner shadow */
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .close-button:hover {
    background: hsl(var(--muted) / 0.8);
    transform: scale(1.1) rotate(90deg);
    box-shadow:
      inset 0 1px 2px rgba(0, 0, 0, 0.1),
      0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .close-button:active {
    transform: scale(0.95) rotate(90deg);
  }


  /* Keyboard hint */
  .keyboard-hint {
    padding: var(--spacing-sm) var(--spacing-xl);
    font-size: var(--font-size-sm);
    color: #a0a0b0;
    text-align: right;
    background: #1a1a2e;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .keyboard-hint kbd {
    padding: 2px 6px;
    border-radius: 4px;
    background: hsl(var(--muted));
    border: 1px solid hsl(var(--border));
    font-family: monospace;
    font-size: var(--font-size-xs);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* Content area - IMPORTANT: Remove padding here, let layout component handle it */
  .edit-panel-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;

    /* FULLY OPAQUE - matches panel background exactly */
    background: #1a1a2e;

    /* Ensure full height for container queries to work */
    min-height: 0; /* Critical for flexbox scrolling */

    /* Custom scrollbar for modern look */
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
  }

  .edit-panel-content::-webkit-scrollbar {
    width: 8px;
  }

  .edit-panel-content::-webkit-scrollbar-track {
    background: transparent;
  }

  .edit-panel-content::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    transition: background 0.2s;
  }

  .edit-panel-content::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .edit-panel-header {
      padding: var(--spacing-sm) var(--spacing-md);
      /* Rounded top corners to match panel */
      border-radius: 24px 24px 0 0;
    }

    .edit-panel-title {
      font-size: var(--font-size-lg);
    }


  }

  /* Extra small screens (Z Fold folded) */
  @media (max-width: 320px) {
    .edit-panel-title {
      font-size: var(--font-size-md);
    }

    .close-button {
      width: 36px;
      height: 36px;
    }
  }
</style>
