<!--
Length Selector Component - Svelte Version
Simple increment/decrement control for sequence length.
-->
<script lang="ts">
  import IncrementAdjusterButton from "./IncrementAdjusterButton.svelte";

  interface Props {
    initialValue?: number;
    minValue?: number;
    maxValue?: number;
    adjustmentAmount?: number;
  }

  let {
    initialValue = 16,
    minValue = 4,
    maxValue = 64,
    adjustmentAmount = 2,
  }: Props = $props();

  // State
  let currentValue = $state(initialValue);

  // Create custom event dispatcher
  const dispatch = (value: number) => {
    // Dispatch custom event that parent can listen to
    const event = new CustomEvent("valueChanged", {
      detail: { value },
    });
    document.dispatchEvent(event);
  };

  // Methods
  function increaseLength() {
    if (currentValue < maxValue) {
      currentValue += adjustmentAmount;
      dispatch(currentValue);
    }
  }

  function decreaseLength() {
    if (currentValue > minValue) {
      currentValue -= adjustmentAmount;
      dispatch(currentValue);
    }
  }

  // Public methods for parent component
  export function setValue(value: number) {
    if (minValue <= value && value <= maxValue) {
      currentValue = value;
    }
  }

  export function getValue() {
    return currentValue;
  }

  // Computed properties
  let canIncrease = $derived(currentValue < maxValue);
  let canDecrease = $derived(currentValue > minValue);
</script>

<div class="length-selector">
  <label class="selector-label" for="length-value">Length:</label>

  <IncrementAdjusterButton
    symbol="-"
    disabled={!canDecrease}
    onclick={decreaseLength}
    aria-label="Decrease sequence length"
  />

  <div
    class="value-display"
    id="length-value"
    role="spinbutton"
    aria-valuenow={currentValue}
    aria-valuemin={minValue}
    aria-valuemax={maxValue}
    aria-label="Sequence length"
  >
    {currentValue}
  </div>

  <IncrementAdjusterButton
    symbol="+"
    disabled={!canIncrease}
    onclick={increaseLength}
    aria-label="Increase sequence length"
  />
</div>

<style>
  .length-selector {
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
