<!--
EditSlidePanel.svelte - Ultra-modern slide-out edit panel

Features:
- 🎨 Glassmorphism with backdrop blur
- 🌊 Smooth spring animations
- ⌨️ Keyboard shortcuts (Esc to close)
- 📱 Mobile-friendly with swipe gestures
- 🎯 Context-aware editing without leaving the flow

HMR Test: Nested component change test
-->
<script lang="ts">
  import type { BeatData } from "$create/workspace-panel";
  import type { IDeviceDetector, IHapticFeedbackService } from "$shared";
  import { Drawer, resolve, TYPES } from "$shared";
  import { onDestroy, onMount } from 'svelte';
  import BatchEditLayout from './BatchEditLayout.svelte';
  import EditPanelLayout from './EditPanelLayout.svelte';
  import EditSlidePanelHeader from './EditSlidePanelHeader.svelte';
  import PictographAdjustmentEditorPanel from './PictographAdjustmentEditorPanel.svelte';

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

  // ============================================================================
  // SERVICES
  // ============================================================================

  let hapticService: IHapticFeedbackService | null = null;
  let deviceDetector: IDeviceDetector | null = null;

  // ============================================================================
  // STATE
  // ============================================================================

  // Adjustment panel state
  let isAdjustmentPanelOpen = $state(false);
  let adjustedBeatData = $state<BeatData | null>(null);

  // Component refs
  let editPanelLayoutRef: EditPanelLayout | null = $state(null);

  // ============================================================================
  // DERIVED STATE
  // ============================================================================

  // Detect batch mode
  const isBatchMode = $derived(
    selectedBeatsData && selectedBeatsData.length > 1
  );

  const shouldUseBottomPlacement = $derived(() => !isSideBySideLayout);

  // Device detection using service
  const isMobile = $derived(() => deviceDetector?.isMobile() ?? false);


  // Calculate panel height dynamically to match tool panel + button panel
  const panelHeightStyle = $derived(() => {
    if (combinedPanelHeight > 0) {
      return `height: ${combinedPanelHeight}px;`;
    }
    return 'height: 70vh;';
  });

  // Determine if we should show the remove beat button
  const shouldShowRemoveButton = $derived(
    !isBatchMode && selectedBeatNumber !== null && selectedBeatNumber >= 1
  );

  // Determine if we should show the adjust arrows button
  const shouldShowAdjustButton = $derived(
    !isBatchMode && selectedBeatData && !selectedBeatData.isBlank
  );

  // ============================================================================
  // EVENT HANDLERS
  // ============================================================================

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


  // Handle remove beat click
  function handleRemoveBeat() {
    if (selectedBeatNumber !== null && selectedBeatNumber >= 1) {
      onRemoveBeat?.(selectedBeatNumber);
      handleClose();
    }
  }

  // Handle adjust arrows click
  function handleAdjustArrows() {
    hapticService?.trigger('selection');
    adjustedBeatData = selectedBeatData;
    isAdjustmentPanelOpen = true;
  }

  // Handle beat data updates from arrow adjustments
  function handleBeatDataUpdate(updatedBeatData: BeatData) {
    console.log('[EditSlidePanel] Beat data updated with manual adjustments:', updatedBeatData);
    adjustedBeatData = updatedBeatData;
  }

  // ============================================================================
  // LIFECYCLE
  // ============================================================================

  onMount(() => {
    // Resolve services
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);

    // Add keyboard listener
    window.addEventListener('keydown', handleKeydown);

    return () => {
      window.removeEventListener('keydown', handleKeydown);
    };
  });

  onDestroy(() => {
    window.removeEventListener('keydown', handleKeydown);
  });

  // Trigger haptic when panel opens
  $effect(() => {
    if (isOpen) {
      hapticService?.trigger('selection');
    }
  });
</script>

<Drawer
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
    class="edit-panel"
    class:mobile={shouldUseBottomPlacement()}
    style={panelHeightStyle()}
  >
    <EditSlidePanelHeader
      {isBatchMode}
      {selectedBeatNumber}
      isMobile={isMobile()}
      {shouldShowRemoveButton}
      {shouldShowAdjustButton}
      onRemove={handleRemoveBeat}
      onAdjustArrows={handleAdjustArrows}
      onClose={handleClose}
    />

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
</Drawer>

<!-- Pictograph Adjustment Editor Panel -->
<PictographAdjustmentEditorPanel
  isOpen={isAdjustmentPanelOpen}
  onClose={() => {
    isAdjustmentPanelOpen = false;
    adjustedBeatData = null;
  }}
  selectedBeatData={adjustedBeatData || selectedBeatData}
  onBeatDataUpdate={handleBeatDataUpdate}
/>

<style>
  /* Use unified sheet system variables - transparent backdrop to allow workspace interaction */
  :global(.bottom-sheet.edit-panel-container) {
    --sheet-backdrop-bg: transparent;
    --sheet-backdrop-filter: none;
    --sheet-backdrop-pointer-events: none;
    --sheet-bg: var(--sheet-bg-transparent);
    --sheet-border: none;
    --sheet-shadow: none;
    --sheet-pointer-events: auto;
    --sheet-width: min(600px, 90vw);
    --sheet-max-height: none;
  }

  /* Make backdrop completely invisible and non-interactive */
  :global(.bottom-sheet.edit-panel-container .bottom-sheet-backdrop) {
    background: transparent !important;
    backdrop-filter: none !important;
    pointer-events: none !important;
  }

  :global(.bottom-sheet.edit-panel-container[data-placement="bottom"]) {
    --sheet-width: 100%;
  }

  :global(.bottom-sheet.edit-panel-container[data-placement="right"]) {
    --sheet-max-height: 90vh;
  }

  /* The slide-out panel itself - Modern gradient background */
  .edit-panel {
    position: relative;
    width: min(600px, 90vw);
    /* Height set dynamically via inline style */

    /* Modern gradient background matching design system */
    background: var(--sheet-bg-gradient);
    border-left: var(--sheet-border-strong);

    /* Premium shadow */
    box-shadow: var(--sheet-shadow-right);

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
    border-radius: var(--sheet-radius-large) var(--sheet-radius-large) 0 0;

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

  /* Content area - IMPORTANT: Remove padding here, let layout component handle it */
  .edit-panel-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;

    /* Modern subtle gradient background */
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(26, 26, 46, 0.98) 50%,
      rgba(20, 25, 35, 0.98) 100%
    );

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
</style>
