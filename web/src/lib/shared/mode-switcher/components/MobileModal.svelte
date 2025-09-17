<script lang="ts">
  import type { ModeOption } from "../domain";
  
  let {
    contextLabel,
    currentModeData,
    modes,
    onModeChange
  } = $props<{
    contextLabel: string;
    currentModeData: ModeOption;
    modes: ModeOption[];
    onModeChange: (mode: string) => void;
  }>();
  
  let showModal = $state(false);
  
  function handleModeSelect(modeId: string) {
    showModal = false;
    onModeChange(modeId);
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      showModal = false;
    }
  }
</script>

<div class="mobile-modal-container">
  <button 
    class="mode-button mobile"
    onclick={() => showModal = true}
  >
    <span class="current-mode">
      <span class="mode-icon">{currentModeData.icon}</span>
      <span class="mode-label">{currentModeData.label}</span>
    </span>
    <span class="tap-hint">Tap to change</span>
  </button>
  
  {#if showModal}
    <div 
      class="modal-overlay" 
      onclick={() => showModal = false}
      onkeydown={handleKeydown}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      tabindex="-1"
    >
      <div class="mode-modal" onclick={(e) => e.stopPropagation()}>
        <h3 id="modal-title">Choose {contextLabel} Mode</h3>
        <div class="mode-grid">
          {#each modes as mode}
            <button 
              class="mode-card"
              class:active={mode.id === currentModeData.id}
              onclick={() => handleModeSelect(mode.id)}
            >
              <span class="mode-icon large">{mode.icon}</span>
              <span class="mode-label">{mode.label}</span>
              {#if mode.description}
                <span class="mode-description">{mode.description}</span>
              {/if}
            </button>
          {/each}
        </div>
        <button class="close-button" onclick={() => showModal = false}>
          Cancel
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .mobile-modal-container {
    width: 100%;
  }
  
  .mode-button.mobile {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    background: var(--surface-glass);
    border: var(--glass-border);
    border-radius: 12px;
    color: var(--foreground);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: var(--font-size-base);
    width: 100%;
    height: 56px; /* Larger touch target */
  }
  
  .mode-button.mobile:hover {
    background: var(--surface-hover);
    transform: translateY(-1px);
  }
  
  .current-mode {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
  }
  
  .tap-hint {
    font-size: var(--font-size-xs);
    color: var(--muted-foreground);
    opacity: 0.8;
  }
  
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
    padding: var(--spacing-lg);
  }
  
  .mode-modal {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop-strong);
    border: var(--glass-border);
    border-radius: 20px;
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-modal);
    max-width: 400px;
    width: 100%;
    max-height: 80vh;
    overflow-y: auto;
  }
  
  .mode-modal h3 {
    margin: 0 0 var(--spacing-lg) 0;
    text-align: center;
    color: var(--foreground);
    font-size: var(--font-size-lg);
  }
  
  .mode-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
  }
  
  .mode-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: var(--spacing-lg);
    background: var(--surface-glass);
    border: var(--glass-border);
    border-radius: 16px;
    cursor: pointer;
    transition: all var(--transition-fast);
    text-align: center;
    gap: var(--spacing-sm);
    min-height: var(--min-touch-target);
    color: var(--foreground);
  }
  
  .mode-card:hover {
    background: var(--surface-hover);
    transform: translateY(-2px);
  }
  
  .mode-card.active {
    background: var(--surface-active);
    border-color: var(--primary-light);
    color: var(--primary-light);
  }
  
  .mode-icon.large {
    font-size: 2.5rem;
    margin-bottom: var(--spacing-xs);
  }
  
  .mode-description {
    font-size: var(--font-size-sm);
    color: var(--muted-foreground);
    text-align: center;
    line-height: 1.4;
  }
  
  .close-button {
    width: 100%;
    padding: var(--spacing-md);
    background: var(--surface-glass);
    border: var(--glass-border);
    border-radius: 12px;
    color: var(--muted-foreground);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: var(--font-size-base);
  }
  
  .close-button:hover {
    background: var(--surface-hover);
    color: var(--foreground);
  }
</style>
