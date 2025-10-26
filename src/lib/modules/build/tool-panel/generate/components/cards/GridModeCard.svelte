<!--
GridModeCard.svelte - Card for toggling grid mode
Shows BOTH grid mode options vertically with clear active/inactive states
-->
<script lang="ts">
  import { GridMode } from "$shared";
  import ToggleCard from "./ToggleCard.svelte";

  let {
    currentMode,
    onModeChange,
    color = "linear-gradient(135deg, #10b981 0%, #059669 100%)", // Emerald green gradient
    shadowColor = "160deg 75% 45%", // Green-matched shadow
    gridColumnSpan = 2,
    cardIndex = 0,
    headerFontSize = "9px"
  } = $props<{
    currentMode: GridMode;
    onModeChange: (mode: GridMode) => void;
    color?: string;
    shadowColor?: string;
    gridColumnSpan?: number;
    cardIndex?: number;
    headerFontSize?: string;
  }>();
</script>

<ToggleCard
  title="Grid"
  option1={{ value: GridMode.DIAMOND, label: "Diamond", icon: "gem" }}
  option2={{ value: GridMode.BOX, label: "Box", icon: "square" }}
  activeOption={currentMode}
  onToggle={onModeChange}
  {color}
  {shadowColor}
  {gridColumnSpan}
  {cardIndex}
  {headerFontSize}
/>
