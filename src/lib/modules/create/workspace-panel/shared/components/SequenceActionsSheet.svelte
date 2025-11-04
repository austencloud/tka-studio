<!-- Slide-up Sheet for Sequence Actions -->
<script lang="ts">
  import { Drawer, SheetDragHandle } from "$shared";

  let {
    show = false,
    hasSequence = false,
    combinedPanelHeight = 0,
    onMirror,
    onRotate,
    onColorSwap,
    onCopyJSON,
    onClose,
  } = $props<{
    show: boolean;
    hasSequence: boolean;
    combinedPanelHeight?: number;
    onMirror?: () => void;
    onRotate?: () => void;
    onColorSwap?: () => void;
    onCopyJSON?: () => void;
    onClose?: () => void;
  }>();

  // Calculate panel height dynamically to match tool panel + button panel
  // This ensures the panel slides up exactly to not cover the sequence
  const panelHeightStyle = $derived(() => {
    if (combinedPanelHeight > 0) {
      return `height: ${combinedPanelHeight}px;`;
    }
    return 'height: 70vh;';
  });

  // Action type definition
  type Action = {
    id: string;
    label: string;
    icon: string;
    description: string;
    color: string;
    requiresSequence: boolean;
    handler?: () => void;
  };

  // Action definitions - Save removed, mirror icon updated
  const actions: Action[] = [
    {
      id: "mirror",
      label: "Mirror",
      icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="action-svg">
        <path d="M11 2v20H9V2h2zm5 3v14c-2.5 0-4.5-2-4.5-4.5v-5C11.5 7 13.5 5 16 5zm0 2c-1.4 0-2.5.9-2.5 2.5v5c0 1.6 1.1 2.5 2.5 2.5V7zM8 5v14c-2.5 0-4.5-2-4.5-4.5v-5C3.5 7 5.5 5 8 5zm0 2c-1.4 0-2.5.9-2.5 2.5v5C5.5 16.1 6.6 17 8 17V7zm12-2v14c2.5 0 4.5-2 4.5-4.5v-5C24.5 7 22.5 5 20 5zm0 2c1.4 0 2.5.9 2.5 2.5v5c0 1.6-1.1 2.5-2.5 2.5V7zm-4-2v14c2.5 0 4.5-2 4.5-4.5v-5C20.5 7 18.5 5 16 5zm0 2c1.4 0 2.5.9 2.5 2.5v5c0 1.6-1.1 2.5-2.5 2.5V7z"/>
      </svg>`,
      description: "Flip horizontally",
      color: "#8b5cf6",
      requiresSequence: true,
      handler: onMirror,
    },
    {
      id: "rotate",
      label: "Rotate",
      icon: '<i class="fas fa-redo"></i>',
      description: "Rotate 90°",
      color: "#ec4899",
      requiresSequence: true,
      handler: onRotate,
    },
    {
      id: "colorSwap",
      label: "Color Swap",
      icon: '<i class="fas fa-palette"></i>',
      description: "Swap blue/red",
      color: "#f59e0b",
      requiresSequence: true,
      handler: onColorSwap,
    },
    {
      id: "copyJSON",
      label: "Copy JSON",
      icon: '<i class="fas fa-code"></i>',
      description: "Debug data",
      color: "#6b7280",
      requiresSequence: true,
      handler: onCopyJSON,
    },
  ];

  // Filter actions based on sequence availability
  const availableActions = $derived(
    actions.filter((action) => !action.requiresSequence || hasSequence)
  );

  // Handle action click - keep sheet open to see immediate effects
  function handleActionClick(action: Action): void {
    action.handler?.();
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

<Drawer
  isOpen={show}
  on:close={handleSheetClose}
  labelledBy="sequence-actions-title"
  closeOnBackdrop={false}
  focusTrap={false}
  lockScroll={false}
  showHandle={false}
  class="actions-sheet-container"
  backdropClass="actions-sheet-backdrop"
>
  <div
    class="actions-panel"
    style={panelHeightStyle()}
    role="dialog"
    aria-labelledby="sequence-actions-title"
  >
    <SheetDragHandle />
    <button
      class="close-button"
      onclick={handleClose}
      aria-label="Close actions sheet"
    >
      <i class="fas fa-times"></i>
    </button>

    <h3 id="sequence-actions-title" class="sr-only">Sequence Actions</h3>

    <div class="actions-panel__header">
      <h4>Sequence Actions</h4>
    </div>

    <div class="actions-panel__content">
      {#if availableActions.length === 0}
        <div class="empty-state">
          <i class="fas fa-info-circle"></i>
          <p>Create a sequence to access actions</p>
        </div>
      {:else}
        <div class="actions-grid">
          {#each availableActions as action}
            <button
              class="action-button"
              onclick={() => handleActionClick(action)}
              style="--action-color: {action.color}"
              title={action.description}
              aria-label={`${action.label}: ${action.description}`}
            >
              <span class="action-icon">{@html action.icon}</span>
              <span class="action-label">{action.label}</span>
            </button>
          {/each}
        </div>
      {/if}
    </div>
  </div>
</Drawer>

<style>
  /* Use unified sheet system variables - transparent backdrop to allow workspace interaction */
  :global(.bottom-sheet.actions-sheet-container) {
    --sheet-backdrop-bg: var(--backdrop-transparent);
    --sheet-backdrop-filter: var(--backdrop-blur-none);
    --sheet-backdrop-pointer-events: none;
    --sheet-bg: var(--sheet-bg-gradient);
    --sheet-border: var(--sheet-border-medium);
    --sheet-shadow: none;
    --sheet-pointer-events: auto;
    min-height: 300px;
  }

  :global(.bottom-sheet.actions-sheet-container:hover) {
    box-shadow: none;
  }

  /* Container */
  .actions-panel {
    container-type: inline-size;
    display: flex;
    flex-direction: column;
    width: 100%;
    position: relative;
    overflow: hidden;
    padding-bottom: env(safe-area-inset-bottom);
  }

  /* Screen reader only */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }

  /* Close button */
  .close-button {
    position: absolute;
    top: 16px;
    right: 16px;
    width: var(--sheet-close-size-small);
    height: var(--sheet-close-size-small);
    border: none;
    border-radius: 50%;
    background: var(--sheet-close-bg);
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all var(--sheet-transition-smooth);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    z-index: 10;
  }

  .close-button:hover {
    background: var(--sheet-close-bg-hover);
    transform: scale(1.05);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .close-button:focus-visible {
    outline: 2px solid rgba(191, 219, 254, 0.7);
    outline-offset: 2px;
  }

  /* Header */
  .actions-panel__header {
    padding: 16px 20px;
    padding-top: 56px; /* Extra padding at top for close button */
    border-bottom: var(--sheet-header-border);
    background: var(--sheet-header-bg);
    text-align: center;
  }

  .actions-panel__header h4 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  /* Content area */
  .actions-panel__content {
    padding: 16px;
    padding-bottom: 24px;
    flex: 1;
    overflow-y: auto;
  }

  /* Empty state */
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 16px;
    color: rgba(255, 255, 255, 0.5);
    gap: 12px;
  }

  .empty-state i {
    font-size: 28px;
  }

  .empty-state p {
    margin: 0;
    font-size: 14px;
    text-align: center;
  }

  /* Actions grid - responsive with container queries */
  .actions-grid {
    display: grid;
    gap: 12px;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }

  /* Container query for larger spaces - horizontal layout */
  @container (min-width: 500px) {
    .actions-grid {
      grid-template-columns: repeat(4, 1fr);
    }
  }

  /* Container query for medium spaces */
  @container (min-width: 350px) and (max-width: 499px) {
    .actions-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  /* Container query for small spaces */
  @container (max-width: 349px) {
    .actions-grid {
      grid-template-columns: 1fr;
    }
  }

  /* Action buttons - 2026 Level Brain Candy Effects */
  .action-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 16px 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--sheet-radius-small);
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    min-height: 90px;
    position: relative;
    overflow: hidden;

    /* Smooth spring animation like BeatCell */
    transition: all var(--sheet-transition-spring);

    /* Subtle initial shadow */
    box-shadow:
      0 2px 8px rgba(0, 0, 0, 0.15),
      0 0 0 1px rgba(255, 255, 255, 0.05);
  }

  /* Gradient overlay that appears on hover */
  .action-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      var(--action-color, rgba(255, 255, 255, 0.1)) 0%,
      transparent 50%,
      var(--action-color, rgba(255, 255, 255, 0.1)) 100%
    );
    opacity: 0;
    transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
  }

  .action-button:hover {
    /* Elevated state with color-coded glow */
    background: rgba(255, 255, 255, 0.12);
    border-color: var(--action-color, rgba(255, 255, 255, 0.4));

    /* Spring pop transform - signature 2026 effect */
    transform: scale(1.05) translateY(-3px);

    /* Layered luxury shadows with action color glow */
    box-shadow:
      0 0 20px color-mix(in srgb, var(--action-color) 40%, transparent),
      0 8px 24px rgba(0, 0, 0, 0.25),
      0 4px 12px color-mix(in srgb, var(--action-color) 25%, transparent),
      0 0 0 1px var(--action-color, rgba(255, 255, 255, 0.3));
  }

  .action-button:hover::before {
    opacity: 0.15;
  }

  /* Active/press state - satisfying feedback */
  .action-button:active {
    transform: scale(0.97) translateY(0);
    transition: all 0.1s cubic-bezier(0.4, 0, 0.2, 1);

    /* Intensify on press */
    box-shadow:
      0 0 15px color-mix(in srgb, var(--action-color) 50%, transparent),
      0 2px 8px rgba(0, 0, 0, 0.3),
      0 0 0 2px var(--action-color, rgba(255, 255, 255, 0.4));
  }

  .action-button:focus-visible {
    outline: 3px solid rgba(191, 219, 254, 0.7);
    outline-offset: 3px;
  }

  /* Action icon */
  .action-icon {
    font-size: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--action-color, rgba(255, 255, 255, 0.9));
    flex-shrink: 0;
  }

  .action-icon :global(.action-svg) {
    width: 24px;
    height: 24px;
  }

  /* Action label */
  .action-label {
    font-size: 14px;
    font-weight: 500;
    text-align: center;
    line-height: 1.3;
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .actions-panel {
      background: rgba(0, 0, 0, 0.98);
      border-top: 2px solid white;
    }

    .actions-panel__header {
      border-bottom: 2px solid white;
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
    .close-button,
    .action-button {
      transition: none;
    }

    .close-button:hover,
    .close-button:active,
    .action-button:hover,
    .action-button:active {
      transform: none;
    }
  }

  /* Mobile responsiveness for very small screens */
  @media (max-width: 380px) {
    .close-button {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
      font-size: 16px;
      top: 12px;
      right: 12px;
    }

    .actions-panel__header {
      padding: 12px 16px;
      padding-top: 52px;
    }

    .actions-panel__header h4 {
      font-size: 16px;
    }

    .actions-panel__content {
      padding: 12px;
      padding-bottom: 20px;
    }

    .action-button {
      min-height: 80px;
      padding: 12px 8px;
      gap: 8px;
    }

    .action-icon {
      font-size: 20px;
    }

    .action-icon :global(.action-svg) {
      width: 20px;
      height: 20px;
    }

    .action-label {
      font-size: 13px;
    }
  }
</style>
