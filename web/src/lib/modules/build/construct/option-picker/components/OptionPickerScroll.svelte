<!--
OptionPickerScroll.svelte - Clean scroll component using service architecture

Migrated to use OptionPickerServiceAdapter directly:
- Pure service-based architecture
- Minimal state for UI concerns only
- Clean separation of concerns
-->
<script lang="ts">
  import SimpleGlassScroll from "$shared/components/ui/SimpleGlassScroll.svelte";
  import type {
    OptionPickerLayoutCalculationResult,
    PictographData,
  } from "$shared/domain";
  import OptionPickerSection from "./OptionPickerSection.svelte";

  // ===== Props =====
  const {
    pictographs = [],
    onPictographSelected = () => {},
    containerWidth = 800,
    containerHeight = 600,
    layout = null,
  } = $props<{
    pictographs?: PictographData[];
    onPictographSelected?: (pictograph: PictographData) => void;
    containerWidth?: number;
    containerHeight?: number;
    layout?: OptionPickerLayoutCalculationResult | null;
  }>();

  // ===== Organized Pictographs =====
  // Group pictographs by category for clean section rendering
  let organizedPictographs = $derived.by(() => {
    if (!pictographs?.length) return [];

    // Simple grouping by pictograph type/category
    const groups = new Map<string, PictographData[]>();

    for (const pictograph of pictographs) {
      const category = pictograph.tags?.[0] || "Other";
      if (!groups.has(category)) {
        groups.set(category, []);
      }
      groups.get(category)!.push(pictograph);
    }

    return Array.from(groups.entries()).map(([category, items]) => ({
      title: category,
      pictographs: items,
    }));
  });

  // ===== Style Properties =====
  let scrollStyle = $derived(() => {
    if (!layout) return {};

    return {
      "--grid-columns": layout.gridConfig.columns,
      "--option-size": layout.gridConfig.itemSize + "px",
      "--grid-gap": layout.gridConfig.gap + "px",
    };
  });
</script>

<div
  class="option-picker-scroll"
  class:mobile={layout?.deviceType === "mobile"}
  class:tablet={layout?.deviceType === "tablet"}
  style={Object.entries(scrollStyle)
    .map(([key, value]) => `${key}: ${value}`)
    .join("; ")}
>
  <SimpleGlassScroll>
    {#each organizedPictographs as section (section.title)}
      <OptionPickerSection
        letterType={section.title}
        pictographs={section.pictographs}
        {onPictographSelected}
        {containerWidth}
      />
    {/each}
  </SimpleGlassScroll>
</div>

<style>
  .option-picker-scroll {
    width: 100%;
    height: 100%;
  }

  .option-picker-scroll.mobile {
    --grid-columns: 2;
    --option-size: 80px;
    --grid-gap: 6px;
  }

  .option-picker-scroll.tablet {
    --grid-columns: 3;
    --option-size: 100px;
    --grid-gap: 8px;
  }
</style>
