<!-- src/lib/components/GenerateTab/controls/GeneratorOptionsSection.svelte -->
<script lang="ts">
  import { settingsStore, generatorType as activeGeneratorType } from '../store/settings';
  import { sequenceSelectors } from '$lib/state/machines/sequenceMachine';
  import CircularSequencer from '../components/CircularSequencer.svelte';
  import FreeformSequencer from '../components/FreeformSequencer.svelte';

  // Use both old and new state management during migration
  export let useNewStateManagement = true;

  // Get state from sequence machine
  $: newGeneratorType = sequenceSelectors.generationType();
</script>

<section class="control-section generator-options-section">
  <div class="panel-header compact">
    <h3>Generator Options</h3>
  </div>

  <div class="generator-content">
    {#if (useNewStateManagement ? newGeneratorType : $activeGeneratorType) === 'circular'}
      <CircularSequencer />
    {:else}
      <FreeformSequencer />
    {/if}
  </div>
</section>

<style>
  .control-section {
    margin-bottom: 1rem;
    background: var(--color-surface-700, rgba(30, 40, 60, 0.5));
    border-radius: 0.5rem;
    overflow: visible; /* Changed from hidden to allow tooltips to show */
    border: 1px solid rgba(255, 255, 255, 0.05);
    position: relative; /* Ensure proper stacking context */
    animation: fadeIn 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    opacity: 0;
  }

  .generator-options-section {
    margin-bottom: 1rem;
    animation-delay: 0.5s;
  }

  .panel-header {
    padding: 1rem 1rem 0.75rem 1rem;
    position: relative;
    background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  .panel-header.compact {
    padding: 0.75rem 1rem;
  }

  .panel-header::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 1rem;
    width: 2rem;
    height: 2px;
    background: linear-gradient(to right, var(--color-accent, #3a7bd5), transparent);
    border-radius: 2px;
  }

  .panel-header h3 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--color-text-primary, white);
    letter-spacing: -0.01em;
  }

  .generator-content {
    padding: 0 1rem 1rem;
    overflow: auto;
    max-height: 300px; /* Reduced from 400px */
    scrollbar-width: thin;
    scrollbar-color: var(--color-accent, #3a7bd5) transparent;
  }

  .generator-content::-webkit-scrollbar {
    width: 6px;
  }

  .generator-content::-webkit-scrollbar-track {
    background: transparent;
  }

  .generator-content::-webkit-scrollbar-thumb {
    background-color: var(--color-accent, #3a7bd5);
    border-radius: 3px;
  }

  /* Animation for panel transitions */
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
      filter: blur(5px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
      filter: blur(0);
    }
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .generator-content {
      padding: 1rem;
    }

    .panel-header {
      padding: 1rem 1rem 0.5rem 1rem;
    }

    .control-section {
      margin-bottom: 1rem;
    }
  }
</style>
