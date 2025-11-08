<!--
CAPComponentButton.svelte - Individual CAP component selection button
Displays a selectable button for a single CAP transformation type
Container-aware and aspect-ratio responsive
-->
<script lang="ts">
  import { FontAwesomeIcon } from "$shared";
  import type { CAPComponentInfo } from "$create/generate/shared/domain/constants/cap-components";

  let {
    componentInfo,
    isMultiSelectMode = false,
    isSelected = false,
    onClick,
  } = $props<{
    componentInfo: CAPComponentInfo;
    isMultiSelectMode?: boolean;
    isSelected?: boolean;
    onClick: () => void;
  }>();

  const { component, label, shortLabel, icon, color } = componentInfo;
</script>

<button
  class="cap-component-button"
  class:selected={isSelected}
  class:multi-select={isMultiSelectMode}
  onclick={onClick}
  style="--component-color: {color};"
  aria-label="{label} - {isSelected ? 'selected' : 'not selected'}"
>
  <div class="cap-component-icon">
    <FontAwesomeIcon {icon} size="1em" />
  </div>
  <div class="cap-component-label">
    <span class="cap-label-full">{label}</span>
    <span class="cap-label-short">{shortLabel}</span>
  </div>

  {#if isMultiSelectMode}
    <!-- Multi-select mode: Show checkbox -->
    <div class="selection-indicator checkbox" class:checked={isSelected}>
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
      >
        <rect x="3" y="3" width="18" height="18" rx="3"></rect>
        {#if isSelected}
          <polyline points="6,12 10,16 18,8" stroke-width="3"></polyline>
        {/if}
      </svg>
    </div>
  {/if}
</button>

<style>
  .cap-component-button {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px;
    background: rgba(0, 0, 0, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    cursor: pointer;
    text-align: center;
    color: white;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    width: 100%;
    height: 100%;
    box-sizing: border-box;
  }

  /* Single-select mode: Strong hover (immediate action) */
  .cap-component-button:not(.multi-select):hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.7);
    box-shadow:
      0 0 16px rgba(255, 255, 255, 0.3),
      0 4px 12px rgba(0, 0, 0, 0.2);
    transform: translateY(-2px) scale(1.02);
  }

  /* Single-select mode: Active state (clicking feedback) */
  .cap-component-button:not(.multi-select):active {
    transform: translateY(0) scale(0.98);
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
  }

  /* Multi-select mode: Subtle hover (state building) */
  .cap-component-button.multi-select:hover {
    background: rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
  }

  .cap-component-button.selected {
    background: color-mix(
      in srgb,
      var(--component-color) 25%,
      rgba(0, 0, 0, 0.3)
    );
    border-color: var(--component-color);
    border-width: 2px;
  }

  .cap-component-button.selected:hover {
    background: color-mix(
      in srgb,
      var(--component-color) 35%,
      rgba(0, 0, 0, 0.3)
    );
  }

  .cap-component-icon {
    font-size: 40px;
    line-height: 1;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .cap-component-label {
    font-size: 15px;
    font-weight: 600;
    color: white;
    line-height: 1.3;
    width: 100%;
    text-align: center;
    white-space: nowrap;
    overflow: visible;
    text-overflow: ellipsis;
    flex-shrink: 0;
  }

  /* Show full label by default, hide short label */
  .cap-label-short {
    display: none;
  }

  .cap-label-full {
    display: inline;
  }

  /* Switch to short label when container is narrow */
  @container (max-width: 120px) {
    .cap-label-short {
      display: inline;
    }

    .cap-label-full {
      display: none;
    }
  }

  .selection-indicator {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s ease;
    pointer-events: none;
  }

  .selection-indicator svg {
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  }

  /* Checkbox style (multi-select mode only) */
  .selection-indicator.checkbox svg rect {
    fill: rgba(255, 255, 255, 0.15);
  }

  .selection-indicator.checkbox.checked svg rect {
    fill: white;
  }

  .selection-indicator.checkbox.checked svg polyline {
    stroke: rgba(0, 0, 0, 0.8);
  }
</style>
