<!-- src/lib/components/GenerateTab/ui/LevelSelector/LevelButton.svelte -->
<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    // Props
    export let level: number;
    export let selected = false;

    // Create event dispatcher
    const dispatch = createEventDispatcher();

    // Handle click
    function handleClick() {
      dispatch('click');
    }

    // Get color based on level
    function getLevelColor(level: number): string {
      const colors = [
        'var(--color-level-1, #4CAF50)', // Green
        'var(--color-level-2, #8BC34A)', // Light Green
        'var(--color-level-3, #FFC107)', // Amber
        'var(--color-level-4, #FF9800)', // Orange
        'var(--color-level-5, #F44336)'  // Red
      ];

      return colors[level - 1] || colors[0];
    }

    // Dynamic color
    $: levelColor = getLevelColor(level);
  </script>

  <button
    class="level-button"
    class:selected={selected}
    style="--level-color: {levelColor}"
    on:click={handleClick}
    aria-label="Level {level}"
    aria-pressed={selected}
  >
    <div class="level-indicator">
      <div class="level-dots">
        {#each Array(level) as _}
          <div class="dot"></div>
        {/each}
      </div>
    </div>
    <span class="level-number">{level}</span>
  </button>

  <style>
    .level-button {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 0.25rem;
      padding: 0.5rem;
      background: var(--color-surface, rgba(30, 40, 60, 0.85));
      border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
      border-radius: 0.25rem;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .level-button:hover {
      background: var(--color-surface-hover, rgba(255, 255, 255, 0.1));
    }

    .level-button.selected {
      border-color: var(--level-color);
      background: rgba(var(--level-color-rgb, 30, 40, 60), 0.2);
    }

    .level-indicator {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .level-dots {
      display: flex;
      gap: 0.125rem;
    }

    .dot {
      width: 0.25rem;
      height: 0.25rem;
      border-radius: 50%;
      background-color: var(--level-color);
    }

    .level-number {
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--color-text-primary, white);
    }
  </style>
