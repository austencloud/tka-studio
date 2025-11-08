<!--
SliceSizeCard.svelte - Card for selecting slice size (circular mode)
Shows BOTH slice size options vertically with clear active/inactive states
-->
<script lang="ts">
  import { SliceSize } from "../../circular/domain";
  import ToggleCard from "./ToggleCard.svelte";

  let {
    currentSliceSize,
    onSliceSizeChange,
    // 🎨 EXTREME: Super vibrant pink gradient with HUGE contrast
    color = "radial-gradient(ellipse at top left, #fce7f3 0%, #fbcfe8 20%, #f9a8d4 40%, #f472b6 60%, #ec4899 80%, #be185d 100%)",
    shadowColor = "330deg 75% 55%", // Pink-matched shadow
    gridColumnSpan = 2,
    cardIndex = 0,
    headerFontSize = "9px",
  } = $props<{
    currentSliceSize: SliceSize;
    onSliceSizeChange: (sliceSize: SliceSize) => void;
    color?: string;
    shadowColor?: string;
    gridColumnSpan?: number;
    cardIndex?: number;
    headerFontSize?: string;
  }>();
</script>

<ToggleCard
  title="Slice"
  option1={{
    value: SliceSize.QUARTERED,
    label: "Quartered",
    icon: "chart-pie",
  }}
  option2={{
    value: SliceSize.HALVED,
    label: "Halved",
    icon: "circle-half-stroke",
  }}
  activeOption={currentSliceSize}
  onToggle={onSliceSizeChange}
  {color}
  {shadowColor}
  {gridColumnSpan}
  {cardIndex}
  {headerFontSize}
/>
