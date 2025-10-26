<script lang="ts">
  import { UndoOperationType } from "$build/shared/services/contracts/IUndoService";
  import type { IBuildTabState } from "$build/shared/types/build-tab-types";

  // Props
  let {
    buildTabState,
    onUndo = () => {},
    showHistoryDropdown = false
  }: {
    buildTabState: IBuildTabState;
    onUndo?: () => void;
    showHistoryDropdown?: boolean;
  } = $props();

  // Debug logging removed - this creates noise during reactive updates
  // $effect(() => {
  //   console.log('🔍 UndoButton: buildTabState.canUndo =', buildTabState.canUndo);
  // });

  // Derived state
  const undoButtonText = $derived(() => {
    if (!buildTabState.canUndo) return "Nothing to Undo";

    const lastEntry = buildTabState.undoHistory[buildTabState.undoHistory.length - 1];
    if (lastEntry?.metadata?.description) {
      return `Undo ${lastEntry.metadata.description}`;
    }

    // Fallback to type-based descriptions
    const typeDescriptions: Record<UndoOperationType, string> = {
      [UndoOperationType.ADD_BEAT]: 'Add Beat',
      [UndoOperationType.REMOVE_BEATS]: 'Remove Beats',
      [UndoOperationType.CLEAR_SEQUENCE]: 'Clear Sequence',
      [UndoOperationType.SELECT_START_POSITION]: 'Select Start Position',
      [UndoOperationType.UPDATE_BEAT]: 'Update Beat',
      [UndoOperationType.INSERT_BEAT]: 'Insert Beat',
      [UndoOperationType.MIRROR_SEQUENCE]: 'Mirror Sequence',
      [UndoOperationType.ROTATE_SEQUENCE]: 'Rotate Sequence',
      [UndoOperationType.SWAP_COLORS]: 'Swap Colors',
      [UndoOperationType.MODIFY_BEAT_PROPERTIES]: 'Modify Beat Properties',
      [UndoOperationType.GENERATE_SEQUENCE]: 'Generate Sequence',
    };

    return `Undo ${typeDescriptions[lastEntry?.type] || 'Last Action'}`;
  });

  const undoTooltip = $derived(() => {
    if (!buildTabState.canUndo) return "No actions to undo";

    const lastEntry = buildTabState.undoHistory[buildTabState.undoHistory.length - 1];
    if (lastEntry?.metadata?.description) {
      return `Undo: ${lastEntry.metadata.description}`;
    }

    return `Undo last action (${lastEntry?.type || 'Unknown'})`;
  });

  // Functions
  function handleUndo() {
    const success = buildTabState.undo();
    if (success) {
      onUndo();
    }
  }


</script>

<!-- Professional Undo Button matching ButtonPanel style - only show when there's something to undo -->
{#if buildTabState.canUndo}
  <button
    class="undo-button"
    onclick={handleUndo}
    title={undoTooltip()}
    aria-label={undoButtonText()}
  >
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        d="M9 14L4 9L9 4"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <path
        d="M4 9H15A6 6 0 0 1 15 21H13"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
  </button>
{/if}





<style>
  .undo-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 18px;
    color: #ffffff;

    /* Professional glass styling matching ButtonPanel */
    background: rgba(100, 116, 139, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .undo-button:hover {
    transform: scale(1.05);
    background: rgba(100, 116, 139, 0.9);
    border-color: rgba(148, 163, 184, 0.4);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .undo-button:active {
    transform: scale(0.95);
    transition: all 0.1s ease;
  }

  .undo-button:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .undo-button {
      width: 44px;
      height: 44px;
      font-size: 16px;
    }
  }

  @media (max-width: 480px) {
    .undo-button {
      width: 40px;
      height: 40px;
      font-size: 14px;
    }
  }

  @media (max-width: 320px) {
    .undo-button {
      width: 36px;
      height: 36px;
      font-size: 12px;
    }
  }

  /* 🎯 LANDSCAPE MOBILE: Compact buttons for Z Fold 5 horizontal (882x344) */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .undo-button {
      width: 36px;
      height: 36px;
      font-size: 14px;
    }
  }
</style>
