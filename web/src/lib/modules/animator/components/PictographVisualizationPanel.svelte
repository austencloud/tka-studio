<!--
PictographVisualizationPanel.svelte - Restructured layout

New layout: 2fr (static section with controls) : 1fr (animated section)
No headers or labels, clean minimal design as requested.
-->
<script lang="ts">
  import type { AnimatorState } from "$shared/state";

  // Import the new restructured components
  import AnimatedSection from "./AnimatedSection.svelte";
  import StaticSection from "./StaticSection.svelte";

  interface Props {
    state: AnimatorState;
  }

  let { state: motionState }: Props = $props();
</script>

<div class="pictograph-visualization-panel">
  <!-- Static Section with Controls (2fr) -->
  <div class="static-section">
    <StaticSection {motionState} />
  </div>

  <!-- Animated Section (1fr) -->
  <div class="animated-section">
    <AnimatedSection {motionState} />
  </div>
</div>

<style>
  .pictograph-visualization-panel {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px;
    height: 100%;
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.02),
      rgba(139, 92, 246, 0.01)
    );
    border-radius: 8px;
    padding: 8px;
    min-height: 0;
  }

  .static-section,
  .animated-section {
    display: flex;
    flex-direction: column;
    min-height: 0;
    overflow: hidden;
  }

  /* Responsive Design */
  @media (max-width: 1200px) {
    .pictograph-visualization-panel {
      grid-template-columns: 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 12px;
    }
  }

  @media (max-width: 768px) {
    .pictograph-visualization-panel {
      padding: 6px;
      gap: 8px;
    }
  }
</style>
