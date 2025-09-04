<!--
Turn Intensity Selector - Svelte Version
Simple increment/decrement control for turn intensity values.
-->
<script lang="ts">
  import IncrementAdjusterButton from "./IncrementAdjusterButton.svelte";

  interface Props {
    initialValue?: number;
  }

  let { initialValue = 1.0 }: Props = $props();

  // State
  let currentValue = $state(initialValue);
  const values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0];

  // Methods
  function adjustIntensity(change: number) {
    try {
      const currentIndex = values.indexOf(currentValue);
      const newIndex = currentIndex + change;

      if (newIndex >= 0 && newIndex < values.length) {
        const newValue = values[newIndex];
        if (newValue !== undefined) {
          currentValue = newValue;
        }

        // Dispatch value change
        const event = new CustomEvent("valueChanged", {
          detail: { value: currentValue },
        });
        document.dispatchEvent(event);
      }
    } catch {
      // Find closest value if current value isn't in array
      const closest = values.reduce((prev, curr) =>
        Math.abs(curr - currentValue) < Math.abs(prev - currentValue)
          ? curr
          : prev
      );
      const closestIndex = values.indexOf(closest);
      const newIndex = closestIndex + change;

      if (newIndex >= 0 && newIndex < values.length) {
        const newValue = values[newIndex];
        if (newValue !== undefined) {
          currentValue = newValue;
        }

        const event = new CustomEvent("valueChanged", {
          detail: { value: currentValue },
        });
        document.dispatchEvent(event);
      }
    }
  }

  function increaseIntensity() {
    adjustIntensity(1);
  }

  function decreaseIntensity() {
    adjustIntensity(-1);
  }

  // Public methods
  export function setValue(value: number) {
    if (values.includes(value)) {
      currentValue = value;
    } else {
      // Find closest value
      const closest = values.reduce((prev, curr) =>
        Math.abs(curr - value) < Math.abs(prev - value) ? curr : prev
      );
      currentValue = closest;
    }
  }

  export function getValue() {
    return currentValue;
  }

  // Computed properties
  let canIncrease = $derived(values.indexOf(currentValue) < values.length - 1);
  let canDecrease = $derived(values.indexOf(currentValue) > 0);
</script>

<div class="turn-intensity-selector">
  <div class="selector-label" id="turn-intensity-label">Turn Intensity:</div>

  <IncrementAdjusterButton
    symbol="-"
    disabled={!canDecrease}
    onclick={decreaseIntensity}
  />

  <div
    class="value-display"
    role="status"
    aria-labelledby="turn-intensity-label"
  >
    {currentValue}
  </div>

  <IncrementAdjusterButton
    symbol="+"
    disabled={!canIncrease}
    onclick={increaseIntensity}
  />
</div>

<style>
  .turn-intensity-selector {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 8px 0;
  }

  .selector-label {
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    font-weight: 500;
    margin: 0;
  }

  .value-display {
    color: white;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    padding: 6px 12px;
    min-width: 30px;
    text-align: center;
    font-family: Georgia, serif;
    font-size: 14px;
    font-weight: bold;
  }
</style>
