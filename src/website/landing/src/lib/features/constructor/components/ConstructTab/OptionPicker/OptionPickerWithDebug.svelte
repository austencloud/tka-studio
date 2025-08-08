<!-- Option Picker -->
<script lang="ts">
  import { onMount } from 'svelte';

  let mounted = false;

  onMount(() => {
    mounted = true;
  });

  // Mock options data
  const options = [
    { id: 1, name: 'Static', description: 'No movement', preview: '●' },
    { id: 2, name: 'Dash', description: 'Quick movement', preview: '→' },
    { id: 3, name: 'Float', description: 'Smooth movement', preview: '~' },
    { id: 4, name: 'Shift', description: 'Position change', preview: '↔' }
  ];
</script>

<div class="option-picker">
  <div class="header">
    <h3>Motion Options</h3>
    <p>Choose the next motion for your sequence</p>
  </div>

  {#if mounted}
    <div class="options-grid">
      {#each options as option (option.id)}
        <div class="option-card" data-option-id={option.id}>
          <div class="option-preview">{option.preview}</div>
          <div class="option-info">
            <span class="option-name">{option.name}</span>
            <span class="option-description">{option.description}</span>
          </div>
        </div>
      {/each}
    </div>

    <div class="actions">
      <button class="action-btn primary">Add Motion</button>
      <button class="action-btn secondary">Clear Sequence</button>
    </div>
  {:else}
    <div class="loading">Loading options...</div>
  {/if}
</div>

<style>
  .option-picker {
    padding: 1rem;
    height: 100%;
    display: flex;
    flex-direction: column;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 0.75rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .header {
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .header h3 {
    color: white;
    margin: 0 0 0.5rem 0;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .header p {
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    font-size: 0.875rem;
  }

  .options-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.75rem;
    flex: 1;
    margin-bottom: 1.5rem;
  }

  .option-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.875rem;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .option-card:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }

  .option-preview {
    width: 2.5rem;
    height: 2.5rem;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 0.375rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 1.25rem;
    flex-shrink: 0;
  }

  .option-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .option-name {
    color: white;
    font-weight: 600;
    font-size: 0.875rem;
  }

  .option-description {
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.75rem;
  }

  .actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .action-btn {
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .action-btn.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .action-btn.primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .action-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.15);
    color: white;
  }

  .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    color: rgba(255, 255, 255, 0.7);
    font-style: italic;
  }

  @media (max-width: 768px) {
    .option-picker {
      padding: 0.75rem;
    }

    .options-grid {
      gap: 0.5rem;
      margin-bottom: 1rem;
    }

    .option-card {
      padding: 0.75rem;
    }

    .option-preview {
      width: 2rem;
      height: 2rem;
      font-size: 1rem;
    }

    .actions {
      gap: 0.5rem;
    }

    .action-btn {
      padding: 0.625rem 0.875rem;
    }
  }
</style>