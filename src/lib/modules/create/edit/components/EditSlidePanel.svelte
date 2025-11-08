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
  import { resolve, TYPES } from "$shared";
  import { CreatePanelDrawer } from "$create/shared/components";
  import PanelHeader from "$create/shared/components/PanelHeader.svelte";
  import { onDestroy, onMount } from "svelte";
  import BatchEditLayout from "./BatchEditLayout.svelte";
  import EditPanelLayout from "./EditPanelLayout.svelte";
  import PictographAdjustmentEditorPanel from "./PictographAdjustmentEditorPanel.svelte";

  // Props
  const {
    isOpen: isOpenProp = false,
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

  // Local state for isOpen (bindable to Drawer)
  let isOpen = $state(isOpenProp);

  // Sync local isOpen with prop changes
  $effect(() => {
    isOpen = isOpenProp;
  });

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

  // ============================================================================
  // DERIVED STATE
  // ============================================================================

  // Detect batch mode
  const isBatchMode = $derived(
    selectedBeatsData && selectedBeatsData.length > 1
  );

  // Device detection using service
  const isMobile = $derived(() => deviceDetector?.isMobile() ?? false);

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
    if (event.key === "Escape" && isOpen) {
      event.preventDefault();
      handleClose();
    }
  }

  // Close handler with haptic feedback
  function handleClose() {
    console.log("🟣 EditSlidePanel handleClose called");
    hapticService?.trigger("selection");
    onClose();
    console.log("🟣 EditSlidePanel onClose() completed");
  }

  // NOTE: Backdrop click detection has been removed to prevent accidental panel closure
  // when selecting different pictographs. Panel can only be closed via:
  // - X button in the header
  // - Escape key
  // - Programmatic calls to onClose()

  // Handle remove beat click
  function handleRemoveBeat() {
    if (selectedBeatNumber !== null && selectedBeatNumber >= 1) {
      onRemoveBeat?.(selectedBeatNumber);
      handleClose();
    }
  }

  // Handle adjust arrows click
  function handleAdjustArrows() {
    hapticService?.trigger("selection");
    adjustedBeatData = selectedBeatData;
    isAdjustmentPanelOpen = true;
  }

  // Handle beat data updates from arrow adjustments
  function handleBeatDataUpdate(updatedBeatData: BeatData) {
    console.log(
      "[EditSlidePanel] Beat data updated with manual adjustments:",
      updatedBeatData
    );
    adjustedBeatData = updatedBeatData;
  }

  // ============================================================================
  // LIFECYCLE
  // ============================================================================

  onMount(() => {
    // Resolve services
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
    deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);

    // Add keyboard listener
    window.addEventListener("keydown", handleKeydown);

    return () => {
      window.removeEventListener("keydown", handleKeydown);
    };
  });

  onDestroy(() => {
    window.removeEventListener("keydown", handleKeydown);
  });

  // Trigger haptic when panel opens
  $effect(() => {
    if (isOpen) {
      hapticService?.trigger("selection");
    }
  });
</script>

<CreatePanelDrawer
  bind:isOpen
  panelName="edit"
  {combinedPanelHeight}
  showHandle={true}
  closeOnBackdrop={false}
  focusTrap={false}
  lockScroll={false}
  labelledBy="edit-panel-title"
  onClose={handleClose}
>
  <div class="edit-panel">
    <PanelHeader
      title={isBatchMode
        ? "Edit Selected Beats"
        : `Edit Beat ${selectedBeatNumber}`}
      isMobile={isMobile()}
      onClose={handleClose}
    >
      {#snippet tabButtons()}
        {#if !isBatchMode}
          {#if shouldShowRemoveButton}
            <button
              class="action-button remove-button"
              onclick={handleRemoveBeat}
              aria-label="Remove Beat {selectedBeatNumber} and all following beats"
            >
              <i class="fas fa-trash-alt"></i>
            </button>
          {/if}
          {#if shouldShowAdjustButton}
            <button
              class="action-button adjust-button"
              onclick={handleAdjustArrows}
              aria-label="Adjust arrow positions"
            >
              <i class="fas fa-arrows-alt"></i>
            </button>
          {/if}
        {/if}
      {/snippet}
    </PanelHeader>

    <h2 id="edit-panel-title" class="sr-only">
      {isBatchMode ? "Edit Selected Beats" : `Edit Beat ${selectedBeatNumber}`}
    </h2>

    <div class="edit-panel-content">
      {#if isBatchMode && selectedBeatsData}
        <BatchEditLayout
          selectedBeats={selectedBeatsData}
          onApply={(changes) => onBatchApply?.(changes)}
          onCancel={handleClose}
        />
      {:else}
        <EditPanelLayout
          selectedBeatIndex={selectedBeatNumber}
          {selectedBeatData}
          {onOrientationChanged}
          {onTurnAmountChanged}
        />
      {/if}
    </div>
  </div>
</CreatePanelDrawer>

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
  /* Panel-specific styles */
  :global(.drawer-content.edit-panel-container) {
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(15, 20, 30, 0.95) 100%
    ) !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow:
      0 -8px 32px rgba(0, 0, 0, 0.5),
      0 -2px 8px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.12);
  }

  /* Side-by-side layout - width handled by base Drawer */

  /* Mobile layout - positioning handled by base Drawer */

  /* Backdrop - ensure no blur/interaction */
  :global(.drawer-overlay.edit-panel-backdrop) {
    background: transparent !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    pointer-events: none !important;
  }

  /* Backdrop for side-by-side: only covers right side */
  :global(.drawer-overlay.edit-panel-backdrop.side-by-side-layout) {
    top: var(--create-panel-top, 64px);
    bottom: var(--create-panel-bottom, 0);
    left: var(--create-panel-left, 50%);
    right: 0;
  }

  /* Drag handle in side-by-side mode */
  :global(
    .drawer-content.edit-panel-container.side-by-side-layout .drawer-handle
  ) {
    position: absolute;
    top: 50%;
    left: 18px;
    width: 4px;
    height: 48px;
    margin: 0;
    border-radius: 999px;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.35);
  }

  /* The slide-out panel itself */
  .edit-panel {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: transparent;
  }

  /* Screen reader only heading */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  /* NOTE: Button styles have been moved to PanelHeader.svelte for consistency */

  /* Content area - let layout component handle spacing */
  .edit-panel-content {
    flex: 1; /* Fill remaining space after header */
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0; /* Critical for flexbox scrolling */
    width: 100%;
    display: flex;
    flex-direction: column;

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

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .edit-panel {
      transition: none;
    }

    :global(
      .drawer-content.edit-panel-container.side-by-side-layout[data-placement="right"]
    ) {
      transition: none;
    }
  }
</style>
