<!--
  ElementVisibilityControls.svelte - Element Visibility Controls

  Controls for toggling visibility of various pictograph elements:
  - Glyphs (TKA, VTG, Elemental, Positions, Reversals)
  - Grid elements (Non-radial Points)
-->
<script lang="ts">
  import ToggleRow from "./ToggleRow.svelte";

  interface Props {
    tkaVisible: boolean;
    vtgVisible: boolean;
    elementalVisible: boolean;
    positionsVisible: boolean;
    reversalsVisible: boolean;
    nonRadialVisible: boolean;
    onToggleTKA: () => void;
    onToggleVTG: () => void;
    onToggleElemental: () => void;
    onTogglePositions: () => void;
    onToggleReversals: () => void;
    onToggleNonRadial: () => void;
  }

  let {
    tkaVisible,
    vtgVisible,
    elementalVisible,
    positionsVisible,
    reversalsVisible,
    nonRadialVisible,
    onToggleTKA,
    onToggleVTG,
    onToggleElemental,
    onTogglePositions,
    onToggleReversals,
    onToggleNonRadial,
  }: Props = $props();
</script>

<div class="element-controls">
  <h4 class="group-title">Element Visibility</h4>

  <!-- Glyphs -->
  <ToggleRow
    label="TKA"
    checked={tkaVisible}
    onChange={onToggleTKA}
    ariaLabel="Toggle TKA glyph visibility"
  />

  <ToggleRow
    label="VTG"
    checked={vtgVisible}
    onChange={onToggleVTG}
    ariaLabel="Toggle VTG glyph visibility"
  />

  <ToggleRow
    label="Elemental"
    checked={elementalVisible}
    onChange={onToggleElemental}
    ariaLabel="Toggle elemental glyph visibility"
  />

  <ToggleRow
    label="Positions"
    checked={positionsVisible}
    onChange={onTogglePositions}
    ariaLabel="Toggle position glyph visibility"
  />

  <ToggleRow
    label="Reversals"
    checked={reversalsVisible}
    onChange={onToggleReversals}
    ariaLabel="Toggle reversal indicators visibility"
  />

  <!-- Grid Elements -->
  <ToggleRow
    label="Non-radial Points"
    checked={nonRadialVisible}
    onChange={onToggleNonRadial}
    ariaLabel="Toggle non-radial points visibility"
  />
</div>

<style>
  .element-controls {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: clamp(0.5rem, 1vw, 0.75rem);
    padding: clamp(1rem, 2.5vw, 1.5rem);
  }

  .group-title {
    font-size: clamp(0.938rem, 1.5vw + 0.25rem, 1.125rem);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 clamp(0.75rem, 2vw, 1.25rem) 0;
  }

  /* Accessibility */
  @media (prefers-contrast: high) {
    .element-controls {
      border-width: 2px;
      border-color: rgba(255, 255, 255, 0.3);
    }
  }
</style>
