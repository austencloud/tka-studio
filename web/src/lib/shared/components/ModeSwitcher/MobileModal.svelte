<script lang="ts">
  import type { ModeOption } from "./ModeSwitcher.svelte";
  
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
    >
      <div class="mode-modal" onclick|stopPropagation>
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
