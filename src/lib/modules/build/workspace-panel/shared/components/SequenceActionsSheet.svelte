<!-- Slide-up Sheet for Sequence Actions -->
<script lang="ts">
  import { onMount } from "svelte";
  import { BottomSheet } from "$shared";

  let {
    show = false,
    hasSequence = false,
    toolPanelHeight = 0,
    onAnimate,
    onMirror,
    onRotate,
    onColorSwap,
    onEdit,
    onSave,
    onCopyJSON,
    onClose,
  } = $props<{
    show: boolean;
    hasSequence: boolean;
    toolPanelHeight?: number;
    onAnimate?: () => void;
    onMirror?: () => void;
    onRotate?: () => void;
    onColorSwap?: () => void;
    onEdit?: () => void;
    onSave?: () => void;
    onCopyJSON?: () => void;
    onClose?: () => void;
  }>();

  // Dynamically measured navigation bar height
  let bottomNavHeight = $state(0);

  // Measure navigation bar height proactively on mount, so it's ready when panel opens
  onMount(() => {
    const measureNavHeight = () => {
      const bottomNav = document.querySelector('.bottom-navigation');
      if (bottomNav) {
        bottomNavHeight = bottomNav.clientHeight;
      }
    };

    // Initial measure
    measureNavHeight();

    // Measure again after a brief delay to ensure DOM is fully rendered
    const timeout = setTimeout(measureNavHeight, 50);

    // Re-measure on window resize
    const handleResize = () => measureNavHeight();
    window.addEventListener('resize', handleResize);

    return () => {
      clearTimeout(timeout);
      window.removeEventListener('resize', handleResize);
    };
  });

  // Calculate panel height dynamically - exact same logic as InlineAnimatorPanel (matching all panels)
  const panelHeightStyle = $derived(() => {
    // Use tool panel height + navigation bar height + border + gap if available
    if (toolPanelHeight > 0 && bottomNavHeight > 0) {
      // Add 1px for border-top + 4px for grid gap between workspace and tool panel
      const totalHeight = toolPanelHeight + bottomNavHeight + 1 + 4;
      return `height: ${totalHeight}px;`;
    }

    return 'height: 45vh;';
  });

  // Action definitions - Animate and Edit removed (now have dedicated UI)
  const actions: Action[] = [
    {
      id: "mirror",
      label: "Mirror",
      icon: '<i class="fas fa-arrows-alt-h"></i>',
      description: "Flip sequence horizontally",
      color: "#8b5cf6",
      requiresSequence: true,
      handler: onMirror,
    },
    {
      id: "rotate",
      label: "Rotate",
      icon: '<i class="fas fa-redo"></i>',
      description: "Rotate sequence 90°",
      color: "#ec4899",
      requiresSequence: true,
      handler: onRotate,
    },
    {
      id: "colorSwap",
      label: "Color Swap",
      icon: '<i class="fas fa-palette"></i>',
      description: "Swap blue and red",
      color: "#f59e0b",
      requiresSequence: true,
      handler: onColorSwap,
    },
    {
      id: "save",
      label: "Save",
      icon: '<i class="fas fa-save"></i>',
      description: "Save sequence (coming soon)",
      color: "#10b981",
      requiresSequence: true,
      handler: onSave,
      disabled: true, // Not implemented yet
    },
    {
      id: "copyJSON",
      label: "Copy JSON",
      icon: '<i class="fas fa-code"></i>',
      description: "Copy sequence data (debug)",
      color: "#6b7280",
      requiresSequence: true,
      handler: onCopyJSON,
    },
  ];

  // Filter actions based on sequence availability
  const availableActions = $derived(
    actions.filter((action) => !action.requiresSequence || hasSequence)
  );
  // Action type definition
  type Action = {
    id: string;
    label: string;
    icon: string;
    description: string;
    color: string;
    requiresSequence: boolean;
    handler?: () => void;
    disabled?: boolean;
  };

  // Handle action click - keep sheet open to see immediate effects
  function handleActionClick(action: Action): void {
    if (action.disabled) return;
    action.handler?.();
    // Don't close the sheet - user can see the effect and apply more actions
  }

  // Handle close button click
  function handleClose(): void {
    onClose?.();
  }

  // Slide transition
  function handleSheetClose(): void {
    handleClose();
  }
</script>

<BottomSheet
  isOpen={show}
  on:close={handleSheetClose}
  labelledBy="sequence-actions-title"
  closeOnBackdrop={false}
  focusTrap={false}
  lockScroll={false}
  showHandle={false}
  class="actions-sheet-container glass-surface"
  backdropClass="actions-sheet-backdrop"
>
  <div
    class="actions-sheet"
    role="dialog"
    aria-label="Sequence actions"
    style={panelHeightStyle()}
  >
    <button class="close-button" onclick={handleClose} aria-label="Close actions sheet">
      <i class="fas fa-times"></i>
    </button>

    <div class="sheet-header">
      <h2 id="sequence-actions-title">Sequence Actions</h2>
    </div>

    <div class="actions-list">
      {#if availableActions.length === 0}
        <div class="empty-state">
          <i class="fas fa-info-circle"></i>
          <p>Create a sequence to access actions</p>
        </div>
      {:else}
        {#each availableActions as action}
          <button
            class="action-button"
            class:disabled={action.disabled}
            onclick={() => handleActionClick(action)}
            disabled={action.disabled}
            style="--action-color: {action.color}"
          >
            <span class="action-icon">{@html action.icon}</span>
            <div class="action-info">
              <span class="action-label">{action.label}</span>
              <span class="action-description">{action.description}</span>
            </div>
            {#if action.disabled}
              <span class="action-badge">Coming soon</span>
            {/if}
          </button>
        {/each}
      {/if}
    </div>

    <div class="sheet-footer">
      <button class="done-button" onclick={handleClose} aria-label="Close actions sheet">
        Done
      </button>
    </div>
  </div>
</BottomSheet>

<style>
  :global(.actions-sheet-backdrop) {
    background: transparent;
    pointer-events: none;
  }

  :global(.bottom-sheet.actions-sheet-container) {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: var(--glass-backdrop-strong);
    border-top-left-radius: 24px;
    border-top-right-radius: 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    display: flex;
    flex-direction: column;
    min-height: 300px;
    padding-bottom: env(safe-area-inset-bottom);
    pointer-events: auto;
  }

  :global(.bottom-sheet.actions-sheet-container:hover) {
    background: rgba(255, 255, 255, 0.08);
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: none;
  }

  .actions-sheet {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }

  .close-button {
    position: absolute;
    top: 16px;
    right: 16px;
    width: 40px;
    height: 40px;
    border: none;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    z-index: 10;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.05);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .sheet-header {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px 24px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .sheet-header h2 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .actions-list {
    padding: 12px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px;
    color: rgba(255, 255, 255, 0.5);
    gap: 12px;
  }

  .empty-state i {
    font-size: 32px;
  }

  .empty-state p {
    margin: 0;
    font-size: 14px;
  }

  .action-button {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    min-height: 64px;
  }

  .action-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--action-color, rgba(255, 255, 255, 0.2));
  }

  .action-button:active {
    transform: scale(0.98);
  }

  .action-button.disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .action-button.disabled:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
  }

  .action-button.disabled:active {
    transform: none;
  }

  .action-icon {
    font-size: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: var(--action-color, rgba(255, 255, 255, 0.9));
  }

  .action-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
  }

  .action-label {
    font-size: 16px;
    font-weight: 600;
  }

  .action-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
  }

  .action-badge {
    margin-left: auto;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.12);
    color: rgba(255, 255, 255, 0.8);
    font-size: 12px;
    font-weight: 600;
  }

  .sheet-footer {
    padding: 12px 16px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .done-button {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.95);
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
  }

  .done-button:hover {
    background: rgba(255, 255, 255, 0.14);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .done-button:active {
    transform: scale(0.98);
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .actions-sheet {
      background: rgba(0, 0, 0, 0.95);
      border-top: 2px solid white;
    }

    .action-button {
      background: rgba(255, 255, 255, 0.1);
      border: 2px solid rgba(255, 255, 255, 0.3);
    }

    .action-button:hover {
      background: rgba(255, 255, 255, 0.2);
      border-color: white;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .action-button {
      transition: none;
    }

    .action-button:active {
      transform: none;
    }
  }
</style>
