<!--
Prop Continuity Toggle - Svelte Version
Toggle between random and continuous prop behavior using modern segmented control.
-->
<script lang="ts">
  import IOSToggle from "../../../ui/IOSToggle.svelte";
  import { PropContinuity } from "$lib/domain";

  interface Props {
    initialValue?: PropContinuity;
    onvalueChanged?: (value: PropContinuity) => void;
  }

  let { initialValue = PropContinuity.CONTINUOUS, onvalueChanged }: Props =
    $props();

  // State
  let currentValue = $state(initialValue);

  // Options for the segmented control
  const continuityOptions = [
    { value: PropContinuity.RANDOM, label: "Random", icon: "🎲" },
    { value: PropContinuity.CONTINUOUS, label: "Continuous", icon: "🔗" },
  ];

  // Handle value change
  function handleValueChange(newValue: string) {
    const value = newValue as PropContinuity;
    currentValue = value;
    onvalueChanged?.(value);
  }

  // Public methods
  export function setValue(value: PropContinuity) {
    currentValue = value;
  }

  export function getValue(): PropContinuity {
    return currentValue;
  }
</script>

<IOSToggle
  value={currentValue}
  options={continuityOptions}
  label="Prop Continuity"
  onchange={handleValueChange}
  size="medium"
/>
