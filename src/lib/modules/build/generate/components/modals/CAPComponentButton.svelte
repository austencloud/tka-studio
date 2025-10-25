<!--
CAPComponentButton.svelte - Individual CAP component selection button
Displays a selectable button for a single CAP transformation type
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
  class="component-button"
  class:selected={isSelected}
  onclick={onClick}
  style="--component-color: {color};"
  aria-label="{label} - {isSelected ? 'selected' : 'not selected'}"
>
  <div class="component-icon">
    <FontAwesomeIcon {icon} size="min(8vmin, 32px)" {color} />
  </div>
  <div class="component-label">
    <span class="label-full">{label}</span>
    <span class="label-short">{shortLabel}</span>
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
  .component-button {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(4px, 1vh, 8px);
    padding: clamp(12px, 3vmin, 20px);
    background: rgba(0, 0, 0, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    cursor: pointer;
    text-align: center;
    color: white;
    transition: all 0.2s ease;
    width: 100%;
    aspect-ratio: 1 / 1;
  }

  .component-button:hover {
    background: rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
  }

  .component-button.selected {
    background: color-mix(in srgb, var(--component-color) 25%, rgba(0, 0, 0, 0.3));
    border-color: var(--component-color);
    border-width: 2px;
  }

  .component-button.selected:hover {
    background: color-mix(in srgb, var(--component-color) 35%, rgba(0, 0, 0, 0.3));
  }

  .component-icon {
    font-size: min(8vmin, 32px);
    line-height: 1;
    flex-shrink: 0;
  }

  .component-label {
    font-size: min(3.5vmin, 14px);
    font-weight: 600;
    color: white;
    line-height: 1.2;
    width: 100%;
    max-width: 100%;
    text-align: center;
  }

  /* Show full label by default, hide short label */
  .label-short {
    display: none;
  }

  .label-full {
    display: inline;
  }

  /* On narrow devices (Z Fold, etc.), switch to short labels */
  @media (max-width: 380px) {
    .label-short {
      display: inline;
    }

    .label-full {
      display: none;
    }
  }

  .selected-indicator {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 24px;
    height: 24px;
    color: white;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .selected-indicator svg {
    width: 14px;
    height: 14px;
  }

  /* 💻 DESKTOP & WIDE SCREENS: Cap sizes to prevent oversized content */
  @media (min-width: 1025px) {
    .component-button {
      padding: 16px;
      max-width: 200px;
    }

    .component-icon {
      font-size: 28px;
    }

    .component-label {
      font-size: 14px;
    }

    .selected-indicator {
      width: 24px;
      height: 24px;
    }

    .selected-indicator svg {
      width: 14px;
      height: 14px;
    }
  }

  /* 📱 TABLET & LARGE PHONES: Optimized for bigger screens */
  @media (min-width: 600px) and (max-width: 1024px) and (orientation: portrait) {
    .component-button {
      padding: clamp(16px, 3vw, 24px);
    }

    .component-icon {
      font-size: clamp(28px, 5vw, 40px);
    }

    .component-label {
      font-size: clamp(14px, 2.5vw, 18px);
    }

    .selected-indicator {
      width: 28px;
      height: 28px;
      top: 10px;
      right: 10px;
    }

    .selected-indicator svg {
      width: 16px;
      height: 16px;
    }
  }

  /* 📱 MEDIUM PORTRAIT PHONES */
  @media (max-width: 520px) and (min-height: 700px) and (orientation: portrait) {
    .component-button {
      aspect-ratio: 1 / 1;
      padding: clamp(12px, 2.2vw, 16px);
      gap: clamp(4px, 0.8vh, 6px);
      max-width: min(48vw, 180px);
    }

    .component-icon {
      font-size: clamp(24px, 4.5vw, 30px);
    }

    .component-label {
      font-size: clamp(12px, 2.6vw, 14px);
    }
  }

  /* 🚨 SHORT SCREENS */
  @media (max-height: 850px) and (orientation: portrait) {
    .component-button {
      aspect-ratio: 5 / 4;
      padding: clamp(10px, 2vw, 14px);
      gap: clamp(4px, 0.8vh, 6px);
    }

    .component-icon {
      font-size: clamp(20px, 4vw, 26px);
    }

    .component-label {
      font-size: clamp(11px, 2.5vw, 13px);
    }
  }

  /* 🚨 VERY SHORT SCREENS */
  @media (max-height: 700px) and (orientation: portrait) {
    .component-button {
      aspect-ratio: 5 / 4;
      padding: 10px 8px;
      gap: 4px;
    }

    .component-icon {
      font-size: 22px;
    }

    .component-label {
      font-size: 11px;
      line-height: 1.1;
    }

    .selected-indicator {
      width: 18px;
      height: 18px;
      top: 6px;
      right: 6px;
    }

    .selected-indicator svg {
      width: 10px;
      height: 10px;
    }
  }

  /* 📱 SMALL SCREENS */
  @media (max-width: 400px) and (min-width: 280px) {
    .component-button {
      padding: clamp(8px, 2vw, 12px);
      gap: clamp(3px, 0.8vh, 5px);
      max-width: 100%;
    }

    .component-icon {
      font-size: clamp(20px, 5.5vw, 26px);
    }

    .component-label {
      font-size: clamp(9px, 2.8vw, 11px);
      white-space: normal;
      line-height: 1.1;
    }
  }

  /* 📱 ULTRA-NARROW SCREENS */
  @media (max-width: 279px) {
    .component-button {
      aspect-ratio: 5 / 6;
      padding: 8px 6px;
      gap: 3px;
      max-width: 100%;
      border-radius: 10px;
    }

    .component-icon {
      font-size: 20px;
    }

    .component-label {
      font-size: 9px;
      line-height: 1.1;
      white-space: normal;
      word-break: break-word;
      max-width: 100%;
    }

    .selected-indicator {
      width: 16px;
      height: 16px;
      top: 4px;
      right: 4px;
    }

    .selected-indicator svg {
      width: 9px;
      height: 9px;
    }
  }

  /* 🌅 LANDSCAPE MODE: Compact buttons for wide, short viewports */
  @media (orientation: landscape) and (max-height: 600px) {
    .component-button {
      aspect-ratio: 1 / 1;
      padding: 6px;
      gap: 3px;
    }

    .component-icon {
      font-size: 20px;
    }

    .component-label {
      font-size: 10px;
    }

    .selected-indicator {
      width: 18px;
      height: 18px;
      top: 4px;
      right: 4px;
    }

    .selected-indicator svg {
      width: 10px;
      height: 10px;
    }
  }

  /* 📱 LANDSCAPE + VERY NARROW: Ultra-compact for 344px height */
  @media (orientation: landscape) and (max-height: 400px) {
    .component-button {
      aspect-ratio: 1 / 1;
      padding: 4px;
      gap: 2px;
    }

    .component-icon {
      font-size: 16px;
    }

    .component-label {
      font-size: 8px;
      line-height: 1;
    }

    .selected-indicator {
      width: 14px;
      height: 14px;
      top: 3px;
      right: 3px;
    }

    .selected-indicator svg {
      width: 8px;
      height: 8px;
    }
  }
</style>
