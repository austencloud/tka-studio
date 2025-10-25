<!--
CAPComponentButton.svelte - Individual CAP component selection button
Displays a selectable button for a single CAP transformation type
Container-aware and aspect-ratio responsive
-->
<script lang="ts">
  import { FontAwesomeIcon } from "$shared";
  import type { CAPComponentInfo } from "./cap-components";

  let {
    componentInfo,
    isSelected = false,
    onClick
  } = $props<{
    componentInfo: CAPComponentInfo;
    isSelected?: boolean;
    onClick: () => void;
  }>();

  const { component, label, shortLabel, icon, color } = componentInfo;
</script>

<button
  class="cap-component-button"
  class:selected={isSelected}
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

  {#if isSelected}
    <div class="selected-indicator">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
        <polyline points="20,6 9,17 4,12"></polyline>
      </svg>
    </div>
  {/if}
</button>

<style>
  .cap-component-button {
    /* 🎯 Container-aware sizing for intelligent scaling */
    /* container-type: size; */

    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(4px, 2cqi, 10px);
    background: rgba(0, 0, 0, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: clamp(8px, 2cqi, 12px);
    cursor: pointer;
    text-align: center;
    color: white;
    transition: all 0.2s ease;
    width: 100%;
    height: 100%;
    min-height: 0;
    box-sizing: border-box;
  }

  .cap-component-button:hover {
    background: rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
  }

  .cap-component-button.selected {
    background: color-mix(in srgb, var(--component-color) 25%, rgba(0, 0, 0, 0.3));
    border-color: var(--component-color);
    border-width: 2px;
  }

  .cap-component-button.selected:hover {
    background: color-mix(in srgb, var(--component-color) 35%, rgba(0, 0, 0, 0.3));
  }

  .cap-component-icon {
    /* Icon takes ~50-60% of container height, scales proportionally */
    font-size: clamp(24px, 28cqi, 60px);
    line-height: 1;
    flex-shrink: 0;
    max-height: 55cqh;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .cap-component-label {
    /* Text takes ~15-20% of container height, scales with icon */
    font-size: clamp(12px, 10cqi, 24px);
    font-weight: 600;
    color: white;
    line-height: 1.2;
    width: 100%;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-height: 20cqh;
    flex-shrink: 1;
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

  .selected-indicator {
    position: absolute;
    top: clamp(6px, 2.5cqi, 10px);
    right: clamp(6px, 2.5cqi, 10px);
    width: clamp(16px, 8cqi, 28px);
    height: clamp(16px, 8cqi, 28px);
    color: white;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .selected-indicator svg {
    width: 60%;
    height: 60%;
  }
</style>
