<!--
MotionTypeButtons.svelte - Visual motion type selector

Replaces dropdown with styled button group showing motion types
with intuitive icons and better visual feedback.
-->
<script lang="ts">
  import { MotionType } from "$lib/domain/enums";

  interface Props {
    selectedMotionType: MotionType;
    onMotionTypeChange: (motionType: MotionType) => void;
    onTurnsChange?: (turns: number | "fl") => void; // For setting turns to "fl" when float is selected
    color: string;
    availableMotionTypes?: string[]; // Optional prop for filtering
    currentTurns?: number | "fl"; // To know if we're currently in float
  }

  let {
    selectedMotionType,
    onMotionTypeChange,
    onTurnsChange,
    color,
    availableMotionTypes,
    currentTurns,
  }: Props = $props();

  const allMotionTypes = [
    {
      id: MotionType.PRO,
      label: "Pro",
      description: "Pronation - Natural circular motion",
    },
    {
      id: MotionType.ANTI,
      label: "Anti",
      description: "Anti-pronation - Reverse circular motion",
    },
    {
      id: MotionType.FLOAT,
      label: "Float",
      description: "Float motion - Negative turns",
    },
    {
      id: MotionType.DASH,
      label: "Dash",
      description: "Dash motion - Opposite locations",
    },
    {
      id: MotionType.STATIC,
      label: "Static",
      description: "Static motion - Same location",
    },
  ];

  // Filter motion types based on available types, or show all if not specified
  let motionTypes = $derived.by(() => {
    if (!availableMotionTypes || availableMotionTypes.length === 0) {
      return allMotionTypes;
    }
    return allMotionTypes.filter((type) =>
      availableMotionTypes.includes(type.id)
    );
  });

  // Calculate grid columns based on number of buttons
  let gridColumns = $derived(`repeat(${motionTypes.length}, 1fr)`);

  // Determine if buttons are interactive (more than one option available)
  let isInteractive = $derived(motionTypes.length > 1);

  function handleMotionTypeClick(motionTypeId: string) {
    const motionType = motionTypeId as MotionType;
    onMotionTypeChange(motionType);

    // If user selects float, automatically set turns to "fl"
    if (motionType === MotionType.FLOAT && onTurnsChange) {
      onTurnsChange("fl");
    }

    // If user selects pro or anti while currently in float, set turns to 0
    if (
      (motionType === MotionType.PRO || motionType === MotionType.ANTI) &&
      currentTurns === "fl" &&
      onTurnsChange
    ) {
      onTurnsChange(0);
    }
  }

  function isSelected(motionTypeId: string): boolean {
    return motionTypeId.toLowerCase() === selectedMotionType.toLowerCase();
  }
</script>

<div class="motion-type-container">
  <div class="motion-label">Motion Type</div>
  <div
    class="motion-type-buttons"
    style="--accent-color: {color}; grid-template-columns: {gridColumns}"
  >
    {#each motionTypes as motionType}
      <button
        class="motion-btn"
        class:selected={isSelected(motionType.id)}
        class:interactive={isInteractive}
        class:display-only={!isInteractive}
        onclick={() =>
          isInteractive ? handleMotionTypeClick(motionType.id) : null}
        disabled={!isInteractive}
        aria-label={isInteractive
          ? `Select ${motionType.label} motion type`
          : `Current motion type: ${motionType.label}`}
        title={motionType.description}
      >
        <span class="motion-label-text">{motionType.label}</span>
      </button>
    {/each}
  </div>
</div>

<style>
  .motion-type-container {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .motion-label {
    font-size: 11px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: center;
  }

  .motion-type-buttons {
    display: grid;
    /* grid-template-columns set dynamically via style attribute */
    gap: 6px;
    padding: 8px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .motion-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px 12px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 56px;
    flex: 1;
  }

  .motion-btn.interactive:hover {
    background: rgba(var(--accent-color), 0.2);
    border-color: rgba(var(--accent-color), 0.4);
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .motion-btn.display-only {
    background: rgba(var(--accent-color), 0.15);
    border-color: rgba(var(--accent-color), 0.3);
    color: rgba(255, 255, 255, 0.9);
    cursor: default;
    transform: none;
    opacity: 0.8;
  }

  .motion-btn.display-only:hover {
    transform: none;
    background: rgba(var(--accent-color), 0.15);
    border-color: rgba(var(--accent-color), 0.3);
    box-shadow: none;
  }

  .motion-btn.selected {
    background: linear-gradient(
      135deg,
      rgba(var(--accent-color), 0.3),
      rgba(var(--accent-color), 0.2)
    );
    border-color: rgba(var(--accent-color), 0.6);
    color: white;
    box-shadow:
      0 0 8px rgba(var(--accent-color), 0.3),
      inset 0 1px 2px rgba(255, 255, 255, 0.1);
  }

  .motion-label-text {
    font-size: 11px;
    line-height: 1;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* Focus styles for accessibility */
  .motion-btn:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(var(--accent-color), 0.5);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    /* Grid columns are set dynamically, no override needed */

    .motion-btn {
      padding: 10px 6px;
      min-height: 42px;
    }

    .motion-label-text {
      font-size: 10px;
    }
  }

  @media (max-width: 480px) {
    .motion-type-buttons {
      gap: 3px;
      padding: 3px;
    }

    .motion-btn {
      padding: 8px 4px;
      min-height: 38px;
    }

    .motion-label-text {
      font-size: 9px;
    }
  }
</style>
