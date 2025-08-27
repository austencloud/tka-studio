<!-- WriteToolbar.svelte - Top toolbar with file operations -->
<script lang="ts">
  // Props
  interface Props {
    hasUnsavedChanges?: boolean;
    disabled?: boolean;
    onNewActRequested?: () => void;
    onSaveRequested?: () => void;
    onSaveAsRequested?: () => void;
  }

  let {
    hasUnsavedChanges = false,
    disabled = false,
    onNewActRequested,
    onSaveRequested,
    onSaveAsRequested,
  }: Props = $props();

  // Handle toolbar actions
  function handleNewAct() {
    if (disabled) return;
    onNewActRequested?.();
  }

  function handleSave() {
    if (disabled) return;
    onSaveRequested?.();
  }

  function handleSaveAs() {
    if (disabled) return;
    onSaveAsRequested?.();
  }
</script>

<div class="write-toolbar" class:disabled>
  <!-- File operations -->
  <div class="toolbar-section file-operations">
    <button
      class="toolbar-button new-button btn-primary"
      {disabled}
      onclick={handleNewAct}
      title="Create new act"
    >
      📄 New Act
    </button>

    <button
      class="toolbar-button save-button btn-glass"
      class:has-changes={hasUnsavedChanges}
      {disabled}
      onclick={handleSave}
      title="Save current act"
    >
      💾 Save
      {#if hasUnsavedChanges}
        <span class="unsaved-indicator">●</span>
      {/if}
    </button>

    <button
      class="toolbar-button save-as-button btn-glass"
      {disabled}
      onclick={handleSaveAs}
      title="Save act with new name"
    >
      💾 Save As...
    </button>
  </div>

  <!-- Spacer -->
  <div class="toolbar-spacer"></div>
</div>

<style>
  .write-toolbar {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-sm) var(--spacing-md);
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-glass);
    min-height: 48px;
    transition: all var(--transition-normal);
  }

  .write-toolbar.disabled {
    opacity: 0.6;
    pointer-events: none;
  }

  .toolbar-section {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .file-operations {
    flex-shrink: 0;
  }

  .toolbar-spacer {
    flex: 1;
  }

  .toolbar-button {
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: var(--border-radius-md);
    font-size: var(--font-size-sm);
    font-weight: 500;
    font-family: "Segoe UI", sans-serif;
    transition: all var(--transition-normal);
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    position: relative;
    backdrop-filter: blur(8px);
  }

  .toolbar-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  .new-button {
    background: var(--primary-color);
    border: 1px solid var(--primary-light);
    color: white;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
  }

  .new-button:hover:not(:disabled) {
    background: var(--primary-light);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
  }

  .save-button,
  .save-as-button {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-color);
  }

  .save-button:hover:not(:disabled),
  .save-as-button:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
  }

  .save-button.has-changes {
    background: var(--accent-color);
    border-color: var(--accent-light);
    color: white;
    box-shadow: 0 4px 16px rgba(6, 182, 212, 0.3);
  }

  .save-button.has-changes:hover:not(:disabled) {
    background: var(--accent-light);
    box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
  }

  .unsaved-indicator {
    color: var(--secondary-color);
    font-weight: bold;
    font-size: var(--font-size-lg);
    line-height: 1;
    animation: pulse 2s infinite;
    text-shadow: var(--text-shadow-glass);
  }

  @keyframes pulse {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .write-toolbar {
      padding: var(--spacing-xs) var(--spacing-sm);
      gap: var(--spacing-sm);
      min-height: 40px;
    }

    .toolbar-section {
      gap: var(--spacing-xs);
    }

    .toolbar-button {
      padding: var(--spacing-xs) var(--spacing-sm);
      font-size: var(--font-size-xs);
    }

    .unsaved-indicator {
      font-size: var(--font-size-base);
    }
  }

  @media (max-width: 480px) {
    .write-toolbar {
      flex-direction: column;
      align-items: stretch;
      gap: var(--spacing-xs);
      padding: var(--spacing-xs);
    }

    .toolbar-section {
      justify-content: center;
    }

    .toolbar-spacer {
      display: none;
    }

    .file-operations {
      order: 1;
    }

    .toolbar-button {
      flex: 1;
      justify-content: center;
      min-width: 0;
    }
  }

  /* Focus styles for accessibility */
  .toolbar-button:focus-visible {
    outline: 2px solid rgba(255, 255, 255, 0.6);
    outline-offset: 2px;
  }
</style>
