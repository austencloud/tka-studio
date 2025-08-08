<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let currentBackground = 'deepOcean';

  const backgrounds = [
    { id: 'deepOcean', name: 'Deep Ocean', description: 'Serene underwater environment' },
    { id: 'nightSky', name: 'Night Sky', description: 'Starry cosmic atmosphere' },
    { id: 'snowfall', name: 'Snowfall', description: 'Peaceful winter scene' }
  ];

  function selectBackground(backgroundId: string) {
    currentBackground = backgroundId;
    dispatch('backgroundChange', backgroundId);
  }
</script>

<div class="background-selector">
  <h3>Background Theme</h3>
  <div class="background-options">
    {#each backgrounds as bg}
      <button
        class="background-option"
        class:active={currentBackground === bg.id}
        on:click={() => selectBackground(bg.id)}
      >
        <div class="background-preview" data-background={bg.id}></div>
        <div class="background-info">
          <span class="background-name">{bg.name}</span>
          <span class="background-description">{bg.description}</span>
        </div>
      </button>
    {/each}
  </div>
</div>

<style>
  .background-selector {
    /* Glassmorphism styling */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-glass);
  }

  .background-selector h3 {
    margin: 0 0 var(--spacing-md) 0;
    color: var(--text-color);
    font-size: var(--font-size-lg);
  }

  .background-options {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .background-option {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-sm);
    border: var(--glass-border);
    border-radius: var(--border-radius);
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    cursor: pointer;
    transition: all var(--transition-normal);
    text-align: left;
  }

  .background-option:hover {
    background: var(--surface-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-glass-hover);
  }

  .background-option.active {
    border-color: var(--primary-color);
    background: var(--surface-active);
    box-shadow:
      var(--shadow-glass),
      0 0 0 2px rgba(102, 126, 234, 0.3);
  }

  .background-preview {
    width: 40px;
    height: 30px;
    border-radius: var(--border-radius-sm);
    border: 1px solid var(--border-color);
    position: relative;
    overflow: hidden;
  }

  /* Preview backgrounds */
  .background-preview[data-background="deepOcean"] {
    background: linear-gradient(135deg, #001122 0%, #003366 50%, #004080 100%);
  }

  .background-preview[data-background="nightSky"] {
    background: linear-gradient(135deg, #0A0E2C 0%, #1A2151 50%, #2A3270 100%);
  }

  .background-preview[data-background="snowfall"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  }

  .background-info {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .background-name {
    color: var(--text-color);
    font-weight: 600;
    font-size: var(--font-size-sm);
  }

  .background-description {
    color: var(--text-secondary);
    font-size: var(--font-size-xs);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .background-options {
      gap: var(--spacing-xs);
    }

    .background-option {
      padding: var(--spacing-xs);
      gap: var(--spacing-sm);
    }

    .background-preview {
      width: 30px;
      height: 24px;
    }
  }
</style>
