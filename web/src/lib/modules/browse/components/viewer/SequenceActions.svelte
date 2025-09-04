<!-- SequenceActions.svelte - Action buttons for sequence operations -->
<script lang="ts">
  interface Props {
    onAction?: (action: string) => void;
  }

  let { onAction }: Props = $props();

  // Action handlers
  function handleEditAction() {
    onAction?.("edit");
  }

  function handleSaveAction() {
    onAction?.("save");
  }

  function handleFullscreenAction() {
    onAction?.("fullscreen");
  }

  function handleDeleteAction() {
    onAction?.("delete");
  }
</script>

<div class="action-buttons">
  <button
    class="action-button primary"
    onclick={handleEditAction}
    type="button"
  >
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path
        d="M12.1465 1.85355C12.3417 1.65829 12.6583 1.65829 12.8536 1.85355L14.1464 3.14645C14.3417 3.34171 14.3417 3.65829 14.1464 3.85355L5.35355 12.6464L2 13L2.35355 9.64645L11.1464 0.853553C11.3417 0.658291 11.6583 0.658291 11.8536 0.853553L12.1465 1.85355Z"
        stroke="currentColor"
        stroke-width="1.5"
      />
    </svg>
    Edit
  </button>

  <button
    class="action-button secondary"
    onclick={handleSaveAction}
    type="button"
  >
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path
        d="M13 2.5V13.5H3V2.5H13Z"
        stroke="currentColor"
        stroke-width="1.5"
      />
      <path d="M10 1V4H6V1" stroke="currentColor" stroke-width="1.5" />
    </svg>
    Save
  </button>

  <button
    class="action-button secondary"
    onclick={handleFullscreenAction}
    type="button"
  >
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path
        d="M2 5V2H5M14 5V2H11M14 11V14H11M2 11V14H5"
        stroke="currentColor"
        stroke-width="1.5"
      />
    </svg>
    Fullscreen
  </button>

  <button
    class="action-button danger"
    onclick={handleDeleteAction}
    type="button"
  >
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path
        d="M2 4H14M6 4V2H10V4M12 4V14H4V4"
        stroke="currentColor"
        stroke-width="1.5"
      />
    </svg>
    Delete
  </button>
</div>

<style>
  /* Action Buttons */
  .action-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-sm);
    flex-shrink: 0;
  }

  .action-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-md);
    border: var(--glass-border);
    border-radius: 8px;
    font-family: inherit;
    font-size: var(--font-size-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
    backdrop-filter: var(--glass-backdrop);
  }

  .action-button.primary {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
  }

  .action-button.primary:hover {
    background: var(--primary-light);
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
  }

  .action-button.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: var(--foreground);
  }

  .action-button.secondary:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: var(--primary-color);
    color: var(--primary-color);
  }

  .action-button.danger {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border-color: rgba(239, 68, 68, 0.3);
  }

  .action-button.danger:hover {
    background: #ef4444;
    color: white;
    border-color: #ef4444;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .action-buttons {
      grid-template-columns: 1fr;
    }
  }
</style>
