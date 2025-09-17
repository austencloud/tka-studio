<script lang="ts">
  import { onMount } from "svelte";
  import type { ModeOption } from "../domain/types";

  let {
    modes = [],
    currentMode,
    onModeChange,
    onClose,
    isOpen = false,
    contextLabel = "Mode"
  } = $props<{
    modes: ModeOption[];
    currentMode: string;
    onModeChange: (mode: string) => void;
    onClose: () => void;
    isOpen: boolean;
    contextLabel?: string;
  }>();

  // Handle escape key
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      onClose();
    }
  }

  // Handle mode selection
  function selectMode(mode: ModeOption) {
    onModeChange(mode.id);
    onClose();
  }

  // Prevent body scroll when modal is open
  onMount(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      return () => {
        document.body.style.overflow = '';
      };
    }
  });
</script>

{#if isOpen}
  <!-- Modal backdrop -->
  <div
    class="modal-backdrop"
    onclick={onClose}
    onkeydown={handleKeydown}
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
    tabindex="-1"
  >
    <!-- Modal content -->
    <div
      class="modal-content"
      role="document"
    >
      <!-- Header -->
      <div class="modal-header">
        <h2 id="modal-title">Choose {contextLabel} Mode</h2>
        <button 
          class="close-button"
          onclick={onClose}
          aria-label="Close modal"
        >
          ✕
        </button>
      </div>

      <!-- Mode cards -->
      <div class="mode-cards">
        {#each modes as mode}
          <button
            class="mode-card"
            class:current={mode.id === currentMode}
            onclick={() => selectMode(mode)}
          >
            <div class="mode-icon-large">{mode.icon}</div>
            <div class="mode-info">
              <h3 class="mode-title">{mode.label}</h3>
              {#if mode.description}
                <p class="mode-description">{mode.description}</p>
              {/if}
              {#if mode.id === currentMode}
                <div class="current-badge">Current</div>
              {/if}
            </div>
          </button>
        {/each}
      </div>

      <!-- Cancel button -->
      <div class="modal-footer">
        <button class="cancel-button" onclick={onClose}>
          Cancel
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 9999;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    animation: backdrop-appear 0.3s ease-out;
  }

  @keyframes backdrop-appear {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .modal-content {
    background: linear-gradient(135deg, 
      rgba(255, 255, 255, 0.1) 0%, 
      rgba(255, 255, 255, 0.05) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    max-width: 400px;
    width: 100%;
    max-height: 80vh;
    overflow-y: auto;
    animation: modal-appear 0.3s ease-out;
  }

  @keyframes modal-appear {
    from {
      opacity: 0;
      transform: scale(0.9) translateY(20px);
    }
    to {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }

  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  #modal-title {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: var(--foreground, #ffffff);
  }

  .close-button {
    background: none;
    border: none;
    color: var(--muted-foreground, #a3a3a3);
    font-size: 24px;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--foreground, #ffffff);
  }

  .mode-cards {
    padding: 16px 24px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .mode-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: var(--foreground, #ffffff);
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 72px;
  }

  .mode-card:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  .mode-card.current {
    background: rgba(255, 255, 255, 0.15);
    border-color: var(--accent, #3b82f6);
  }

  .mode-icon-large {
    font-size: 32px;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .mode-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .mode-title {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    line-height: 1.2;
  }

  .mode-description {
    margin: 0;
    font-size: 14px;
    color: var(--muted-foreground, #a3a3a3);
    line-height: 1.3;
  }

  .current-badge {
    display: inline-block;
    padding: 2px 8px;
    background: var(--accent, #3b82f6);
    color: white;
    font-size: 12px;
    font-weight: 600;
    border-radius: 12px;
    align-self: flex-start;
    margin-top: 4px;
  }

  .modal-footer {
    padding: 16px 24px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .cancel-button {
    width: 100%;
    padding: 12px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: var(--foreground, #ffffff);
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .cancel-button:hover {
    background: rgba(255, 255, 255, 0.15);
  }
</style>
