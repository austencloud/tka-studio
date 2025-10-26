<!--
TurnEditModal.svelte - Turn Editing Modal (Desktop App Pattern)

Implements the proven DirectSetTurnsDialog pattern from the legacy desktop app:
- Horizontal button layout with turn values [0, 0.5, 1, 1.5, 2, 2.5, 3]
- Color-coded styling with blue/red borders
- Positioned relative to trigger element
- Immediate value selection and feedback
-->
<script lang="ts">
  import type { BeatData } from "$shared";
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";

  // Service resolution
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Props following desktop app pattern
  let {
    isOpen = false,
    currentBeatData = null,
    onClose,
    onTurnAmountChanged
  } = $props<{
    isOpen?: boolean;
    currentBeatData?: BeatData | null;
    onClose?: () => void;
    onTurnAmountChanged?: (color: string, turnAmount: number) => void;
  }>();

  // Turn values exactly matching desktop app
  const turnValues = [0, 0.5, 1, 1.5, 2, 2.5, 3];

  // Extract current turn values from motions
  let blueTurnAmount = $derived(currentBeatData?.motions?.blue?.turns ?? 0);
  let redTurnAmount = $derived(currentBeatData?.motions?.red?.turns ?? 0);

  // Modal state
  let modalElement = $state<HTMLElement>();

  // Handle turn selection (desktop app pattern)
  function handleTurnSelect(color: 'blue' | 'red', value: number) {
    hapticService?.trigger('selection');
    onTurnAmountChanged?.(color, value);
    console.log(`Turn selected: ${color} = ${value}`);
  }

  // Handle escape key and backdrop clicks
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      hapticService?.trigger('selection');
      onClose?.();
    }
  }

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      hapticService?.trigger('selection');
      onClose?.();
    }
  }

  // Focus management for accessibility
  $effect(() => {
    if (isOpen && modalElement) {
      modalElement.focus();
    }
  });

  // Body scroll management
  $effect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }

    return () => {
      document.body.style.overflow = "";
    };
  });
</script>

<!-- Desktop App Pattern: DirectSetTurnsDialog -->
{#if isOpen}
  <div
    class="modal-overlay"
    bind:this={modalElement}
    onclick={handleBackdropClick}
    onkeydown={handleKeydown}
    role="dialog"
    aria-modal="true"
    tabindex="-1"
  >
    <!-- Blue Turn Section -->
    <div class="turn-dialog blue-dialog">
      <div class="dialog-header">
        <h4>Blue Turns</h4>
        <span class="current-value">{blueTurnAmount}</span>
      </div>
      <div class="turn-buttons">
        {#each turnValues as value}
          <button
            class="turn-btn"
            class:selected={blueTurnAmount === value}
            onclick={() => handleTurnSelect('blue', value)}
            type="button"
          >
            {value}
          </button>
        {/each}
      </div>
    </div>

    <!-- Red Turn Section -->
    <div class="turn-dialog red-dialog">
      <div class="dialog-header">
        <h4>Red Turns</h4>
        <span class="current-value">{redTurnAmount}</span>
      </div>
      <div class="turn-buttons">
        {#each turnValues as value}
          <button
            class="turn-btn"
            class:selected={redTurnAmount === value}
            onclick={() => handleTurnSelect('red', value)}
            type="button"
          >
            {value}
          </button>
        {/each}
      </div>
    </div>

    <!-- Close Button -->
    <button class="close-btn" onclick={onClose} type="button">
      Close
    </button>
  </div>
{/if}

<style>
  /* Desktop App Pattern: DirectSetTurnsDialog Styling */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    gap: 16px;
  }

  .turn-dialog {
    background: rgba(30, 30, 30, 0.95);
    border-radius: 8px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    padding: 16px;
    min-width: 400px;
  }

  .blue-dialog {
    border: 2px solid #3b82f6;
  }

  .red-dialog {
    border: 2px solid #ef4444;
  }

  .dialog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .dialog-header h4 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
  }

  .current-value {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
  }

  .turn-buttons {
    display: flex;
    gap: 0;
    border-radius: 6px;
    overflow: hidden;
  }

  .turn-btn {
    flex: 1;
    padding: 12px 8px;
    border: none;
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border-right: 1px solid rgba(255, 255, 255, 0.2);
  }

  .turn-btn:last-child {
    border-right: none;
  }

  .turn-btn:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  .turn-btn.selected {
    background: #6366f1;
    color: #ffffff;
  }

  .blue-dialog .turn-btn.selected {
    background: #3b82f6;
  }

  .red-dialog .turn-btn.selected {
    background: #ef4444;
  }

  .close-btn {
    padding: 12px 24px;
    background: #6366f1;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .close-btn:hover {
    background: #4f46e5;
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .turn-dialog {
      min-width: 300px;
      max-width: 90vw;
    }

    .turn-btn {
      padding: 10px 6px;
      font-size: 12px;
    }
  }
</style>
