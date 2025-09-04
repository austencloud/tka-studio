<!--
Level Selector - Svelte Version
Simple 3-level difficulty selector with circular buttons.
-->
<script lang="ts">
  import { DifficultyLevel } from '$domain';

  interface Props {
    initialValue?: DifficultyLevel;
    onvalueChanged?: (value: DifficultyLevel) => void;
  }

  let { initialValue = DifficultyLevel.INTERMEDIATE, onvalueChanged }: Props = $props();

  // State
  let currentValue = $state(initialValue);

  // Level data with exact legacy gradient colors
  const levelData = [
    {
      level: DifficultyLevel.BEGINNER,
      number: "1",
      label: "No Turns",
      gradient: "rgb(245, 245, 245)",
      color: "black",
    },
    {
      level: DifficultyLevel.INTERMEDIATE,
      number: "2",
      label: "Whole Turns",
      gradient: `linear-gradient(135deg,
        rgb(170, 170, 170) 0%,
        rgb(120, 120, 120) 30%,
        rgb(180, 180, 180) 60%,
        rgb(110, 110, 110) 100%)`,
      color: "black",
    },
    {
      level: DifficultyLevel.ADVANCED,
      number: "3",
      label: "Half Turns",
      gradient: `linear-gradient(135deg,
        rgb(255, 215, 0) 0%,
        rgb(238, 201, 0) 20%,
        rgb(218, 165, 32) 40%,
        rgb(184, 134, 11) 60%,
        rgb(139, 69, 19) 80%,
        rgb(85, 107, 47) 100%)`,
      color: "black",
    },
  ];

  // Handle button click
  function selectLevel(level: DifficultyLevel) {
    if (level !== currentValue) {
      currentValue = level;

      // Call callback if provided
      onvalueChanged?.(level);

      // Also dispatch custom event for compatibility
      const event = new CustomEvent("valueChanged", {
        detail: { value: level },
        bubbles: true,
      });
      if (typeof window !== 'undefined') {
        document.dispatchEvent(event);
      }
    }
  }

  // Public methods
  export function setValue(value: DifficultyLevel) {
    if (Object.values(DifficultyLevel).includes(value)) {
      currentValue = value;
    }
  }

  export function getValue(): DifficultyLevel {
    return currentValue;
  }
</script>

<div class="level-selector">
  {#each levelData as { level, number, label, gradient, color }}
  <div class="level-item">
    <button
    class="level-button"
    class:checked={currentValue === level}
    onclick={() => selectLevel(level)}
    style="background: {gradient}; color: {color};"
    type="button"
    >
    {number}
    </button>
    <div class="level-label">{label}</div>
  </div>
  {/each}
</div>

<style>
  .level-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 8px 0;
  }

  .level-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  }

  .level-button {
  width: 60px;
  height: 60px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  font-weight: bold;
  font-size: 18px;
  font-family: Georgia, serif;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  }

  .level-button:hover:not(.checked) {
  border: 3px solid rgba(255, 255, 255, 0.6);
  }

  .level-button.checked {
  border: 4px solid rgba(255, 255, 255, 0.95);
  }

  .level-label {
  color: white;
  font-size: 12px;
  font-weight: bold;
  text-align: center;
  }
</style>
