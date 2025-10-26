<!--
LengthCard.svelte - Card for selecting sequence length
Shows current length with +/- stepper controls for quick adjustment
-->
<script lang="ts">
  import StepperCard from "./StepperCard.svelte";

  let {
    currentLength,
    onLengthChange,
    // 🎨 ENHANCED: More pronounced blue gradient with radial overlay for 3D depth
    color = "radial-gradient(ellipse at top left, #60a5fa 0%, #3b82f6 40%, #1d4ed8 100%)",
    shadowColor = "220deg 80% 55%", // Blue-matched shadow
    gridColumnSpan = 2,
    headerFontSize = "9px"
  } = $props<{
    currentLength: number;
    onLengthChange: (length: number) => void;
    color?: string;
    shadowColor?: string;
    gridColumnSpan?: number;
    headerFontSize?: string;
  }>();

  // Length constraints
  const MIN_LENGTH = 4;
  const MAX_LENGTH = 64;
  const STEP = 4; // Increment by 4 beats at a time

  function handleIncrement() {
    const newLength = Math.min(currentLength + STEP, MAX_LENGTH);
    onLengthChange(newLength);
  }

  function handleDecrement() {
    const newLength = Math.max(currentLength - STEP, MIN_LENGTH);
    onLengthChange(newLength);
  }

  function formatValue(value: number): string {
    return value.toString();
  }
</script>

<StepperCard
  title="Length"
  currentValue={currentLength}
  minValue={MIN_LENGTH}
  maxValue={MAX_LENGTH}
  step={STEP}
  onIncrement={handleIncrement}
  onDecrement={handleDecrement}
  formatValue={formatValue}
  {color}
  {shadowColor}
  {gridColumnSpan}
  {headerFontSize}
/>
