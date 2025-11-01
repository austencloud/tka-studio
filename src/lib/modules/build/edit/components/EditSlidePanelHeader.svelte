<!--
EditSlidePanelHeader.svelte - Header for the edit slide panel

Contains:
- Action buttons (Remove Beat, Adjust Arrows)
- Panel title
- Close button
- Keyboard hint
-->
<script lang="ts">
  import RemoveBeatButton from '../../workspace-panel/shared/components/buttons/RemoveBeatButton.svelte';

  // Props
  const {
    isBatchMode = false,
    selectedBeatNumber,
    isMobile = false,
    onRemove,
    onAdjustArrows,
    onClose,
    shouldShowRemoveButton = false,
    shouldShowAdjustButton = false,
  } = $props<{
    isBatchMode?: boolean;
    selectedBeatNumber: number | null;
    isMobile?: boolean;
    onRemove: () => void;
    onAdjustArrows: () => void;
    onClose: () => void;
    shouldShowRemoveButton?: boolean;
    shouldShowAdjustButton?: boolean;
  }>();

  // Derived title
  const title = $derived(() => {
    if (isBatchMode) return 'Batch Edit';
    if (selectedBeatNumber === 0) return 'Edit Start Position';
    return `Edit Beat ${selectedBeatNumber}`;
  });
</script>

<div class="edit-panel-header">
  <!-- Left: Action Buttons -->
  <div class="header-left">
    {#if shouldShowRemoveButton}
      <RemoveBeatButton
        beatNumber={selectedBeatNumber}
        onclick={onRemove}
      />
    {/if}
    {#if shouldShowAdjustButton}
      <button
        class="adjust-arrows-button"
        onclick={onAdjustArrows}
        aria-label="Adjust arrow positions"
        title="Adjust arrow positions with WASD"
        type="button"
      >
        <i class="fas fa-crosshairs"></i>
      </button>
    {/if}
  </div>

  <!-- Center: Title -->
  <h2 id="edit-panel-title" class="edit-panel-title">
    {title()}
  </h2>

  <!-- Right: Close Button -->
  <div class="header-right">
    <button
      class="close-button"
      onclick={onClose}
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

<style>
  /* Header - 3-column layout: left (remove button), center (title), right (close button) */
  .edit-panel-header {
    flex-shrink: 0;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    padding: var(--spacing-lg) var(--spacing-xl);

    /* Modern glassmorphism - matches design system */
    background: var(--sheet-header-bg);
    backdrop-filter: blur(12px);
    border-bottom: var(--sheet-header-border);
  }

  .header-left {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: var(--spacing-md);
  }

  /* Adjust Arrows Button */
  .adjust-arrows-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1));
    font-size: 18px;
    color: #ffffff;

    /* Gradient background for adjustment button */
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  .adjust-arrows-button:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.6);
    transform: scale(1.05);
  }

  .adjust-arrows-button:active {
    transform: scale(0.95);
  }

  .adjust-arrows-button:focus-visible {
    outline: 2px solid var(--primary-light, #818cf8);
    outline-offset: 2px;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .adjust-arrows-button {
      width: 44px;
      height: 44px;
      font-size: 16px;
    }

    .edit-panel-header {
      padding: var(--spacing-sm) var(--spacing-md);
      /* Rounded top corners to match panel */
      border-radius: var(--sheet-radius-large) var(--sheet-radius-large) 0 0;
    }

    .edit-panel-title {
      font-size: var(--font-size-lg);
    }
  }

  @media (max-width: 480px) {
    .adjust-arrows-button {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
      font-size: 14px;
    }
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
    width: var(--sheet-close-size-small);
    height: var(--sheet-close-size-small);
    border-radius: 50%;
    border: none;
    background: var(--sheet-close-bg);
    backdrop-filter: blur(10px);
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all var(--sheet-transition-spring);
    font-size: var(--font-size-lg);

    /* Subtle shadow for depth */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .close-button:hover {
    background: var(--sheet-close-bg-hover);
    transform: scale(1.1) rotate(90deg);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  }

  .close-button:active {
    transform: scale(0.95) rotate(90deg);
  }

  /* Keyboard hint */
  .keyboard-hint {
    padding: var(--spacing-sm) var(--spacing-xl);
    font-size: var(--font-size-sm);
    color: rgba(255, 255, 255, 0.6);
    text-align: right;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(12px);
    border-bottom: var(--sheet-header-border);
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

  /* Extra small screens (Z Fold folded) */
  @media (max-width: 320px) {
    .edit-panel-title {
      font-size: var(--font-size-md);
    }

    .close-button {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
    }
  }
</style>
