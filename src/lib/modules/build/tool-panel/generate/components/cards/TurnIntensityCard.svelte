<!--
TurnIntensityCard.svelte - Card for selecting turn intensity
Uses stepper pattern for direct increment/decrement interaction
-->
<script lang="ts">
  import StepperCard from "./StepperCard.svelte";

  let {
    currentIntensity,
    allowedValues,
    onIntensityChange,
    shadowColor = "0deg 0% 0%", // Neutral shadow (adapts to any color)
    gridColumnSpan = 2,
    cardIndex = 0,
    headerFontSize = "9px"
  } = $props<{
    currentIntensity: number;
    allowedValues: number[];
    onIntensityChange: (intensity: number) => void;
    shadowColor?: string;
    gridColumnSpan?: number;
    cardIndex?: number;
    headerFontSize?: string;
  }>();

  // Find current index in allowed values
  const currentIndex = $derived(allowedValues.indexOf(currentIntensity));

  // Check if we can increment/decrement within allowed values
  const canIncrement = $derived(currentIndex < allowedValues.length - 1);
  const canDecrement = $derived(currentIndex > 0);

  // Get min/max from allowed values for stepper
  const minValue = $derived(Math.min(...allowedValues));
  const maxValue = $derived(Math.max(...allowedValues));

  function handleIncrement() {
    if (canIncrement) {
      const nextValue = allowedValues[currentIndex + 1];
      onIntensityChange(nextValue);
    }
  }

  function handleDecrement() {
    if (canDecrement) {
      const prevValue = allowedValues[currentIndex - 1];
      onIntensityChange(prevValue);
    }
  }

  // Format intensity display
  function formatValue(value: number): string {
    return `${value}x`;
  }

  // Generate description based on intensity
  function getDescription(value: number): string {
    if (value <= 0.5) return "Minimal turns";
    if (value <= 1.0) return "Gentle turns";
    if (value <= 1.5) return "Light turns";
    if (value <= 2.0) return "Moderate turns";
    if (value <= 2.5) return "Strong turns";
    return "Intense turns";
  }

  // 🎨 ENHANCED: Dynamic color with RADIAL gradients for 3D depth
  // Green (safe) → Yellow → Orange → Red (dangerous)
  function getColor(value: number): string {
    if (value <= 0.5) {
      // Minimal (0.5x) - Light Fresh Green with radial depth
      return "radial-gradient(ellipse at top left, #a7f3d0 0%, #6ee7b7 40%, #34d399 100%)";
    } else if (value <= 1.0) {
      // Gentle (1.0x) - Solid Green with depth
      return "radial-gradient(ellipse at top left, #4ade80 0%, #22c55e 40%, #16a34a 100%)";
    } else if (value <= 1.5) {
      // Light (1.5x) - Lime Green with vibrant depth
      return "radial-gradient(ellipse at top left, #bef264 0%, #a3e635 40%, #84cc16 100%)";
    } else if (value <= 2.0) {
      // Moderate (2.0x) - Amber with warm depth
      return "radial-gradient(ellipse at top left, #fbbf24 0%, #f59e0b 40%, #d97706 100%)";
    } else if (value <= 2.5) {
      // Strong (2.5x) - Orange-Red with intense depth
      return "radial-gradient(ellipse at top left, #fb923c 0%, #f97316 40%, #ea580c 100%)";
    } else {
      // Intense (3.0x) - Deep Red with danger depth
      return "radial-gradient(ellipse at top left, #f87171 0%, #ef4444 40%, #dc2626 100%)";
    }
  }

  const description = $derived(getDescription(currentIntensity));
  const dynamicColor = $derived(getColor(currentIntensity));
</script>

<StepperCard
  title="Turn Intensity"
  icon="🔄"
  currentValue={currentIntensity}
  {minValue}
  {maxValue}
  step={0.5}
  onIncrement={handleIncrement}
  onDecrement={handleDecrement}
  {formatValue}
  {description}
  color={dynamicColor}
  {shadowColor}
  textColor="white"
  {gridColumnSpan}
  {cardIndex}
  {headerFontSize}
/>
