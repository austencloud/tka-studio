<script lang="ts">
  import type { ModeOption } from "../domain";
  
  let {
    contextLabel,
    currentModeData,
    modes,
    onModeChange,
    showBreadcrumb
  } = $props<{
    contextLabel: string;
    currentModeData: ModeOption;
    modes: ModeOption[];
    onModeChange: (mode: string) => void;
    showBreadcrumb: boolean;
  }>();
  
  let showDropdown = $state(false);
  let dropdownRef: HTMLDivElement;
  
  function handleModeSelect(modeId: string) {
    showDropdown = false;
    onModeChange(modeId);
  }
  
  function handleClickOutside(event: MouseEvent) {
    if (dropdownRef && !dropdownRef.contains(event.target as Node)) {
      showDropdown = false;
    }
  }
  
  $effect(() => {
    if (showDropdown) {
      document.addEventListener('click', handleClickOutside);
      return () => document.removeEventListener('click', handleClickOutside);
    }
  });
  
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      showDropdown = false;
    }
  }
</script>

<div class="desktop-dropdown" bind:this={dropdownRef}>
  <button 
    class="mode-button"
    onclick={() => showDropdown = !showDropdown}
    onkeydown={handleKeydown}
    aria-expanded={showDropdown}
    aria-haspopup="true"
  >
    {#if showBreadcrumb}
      <span class="context">{contextLabel} →</span>
    {/if}
    <span class="current-mode">
      <span class="mode-icon">{currentModeData.icon}</span>
      <span class="mode-label">{currentModeData.label}</span>
    </span>
    <span class="chevron" class:rotated={showDropdown}>▼</span>
  </button>
  
  {#if showDropdown}
    <div class="dropdown-menu">
      {#each modes as mode}
        <button 
          class="dropdown-item"
          class:active={mode.id === currentModeData.id}
          onclick={() => handleModeSelect(mode.id)}
          onkeydown={(e) => e.key === 'Enter' && handleModeSelect(mode.id)}
        >
          <span class="mode-icon">{mode.icon}</span>
          <span class="mode-label">{mode.label}</span>
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  .desktop-dropdown {
    position: relative;
    width: 100%;
  }
  
  .mode-button {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    background: var(--surface-glass);
    border: var(--glass-border);
    border-radius: 8px;
    color: var(--foreground);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: var(--font-size-sm);
    width: 100%;
    height: 40px;
  }
  
  .mode-button:hover {
    background: var(--surface-hover);
    border-color: rgba(255, 255, 255, 0.25);
  }
  
  .context {
    color: var(--muted-foreground);
    font-size: var(--font-size-xs);
  }
  
  .current-mode {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    flex: 1;
  }
  
  .chevron {
    transition: transform var(--transition-fast);
    opacity: 0.7;
  }
  
  .chevron.rotated {
    transform: rotate(180deg);
  }
  
  .dropdown-menu {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    right: 0;
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: 8px;
    box-shadow: var(--shadow-modal);
    z-index: 1000;
    overflow: hidden;
  }
  
  .dropdown-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    background: transparent;
    border: none;
    color: var(--foreground);
    cursor: pointer;
    transition: background var(--transition-fast);
    text-align: left;
  }
  
  .dropdown-item:hover,
  .dropdown-item:focus {
    background: var(--surface-hover);
    outline: none;
  }
  
  .dropdown-item.active {
    background: var(--surface-active);
    color: var(--primary-light);
  }
  
  .mode-icon {
    flex-shrink: 0;
  }
  
  .mode-label {
    flex: 1;
  }
</style>
