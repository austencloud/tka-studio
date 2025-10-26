<!--
StepperLandscapeLayout.svelte - Landscape/horizontal stepper layout
Left half decrements, right half increments (horizontal layout)
Used when card aspect ratio is wide/landscape
-->
<script lang="ts">
  import CardHeader from "./shared/CardHeader.svelte";

  let {
    title,
    displayValue,
    subtitle = "",
    description = "",
    canIncrement,
    canDecrement,
    handleIncrement,
    handleDecrement,
    handleKeydown,
    headerFontSize = "9px"
  } = $props<{
    title: string;
    displayValue: string;
    subtitle?: string;
    description?: string;
    canIncrement: boolean;
    canDecrement: boolean;
    handleIncrement: () => void;
    handleDecrement: () => void;
    handleKeydown: (event: KeyboardEvent, action: 'increment' | 'decrement') => void;
    headerFontSize?: string;
  }>();
</script>

<!-- Landscape Mode: Touch Zones - Absolutely positioned to overlay entire card -->
<button
  class="touch-zone decrement-zone"
  onclick={handleDecrement}
  onkeydown={(e) => handleKeydown(e, 'decrement')}
  disabled={!canDecrement}
  aria-label="Decrease {title}"
>
  <div class="zone-icon">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round">
      <path d="M5 12h14"/>
    </svg>
  </div>
</button>

<button
  class="touch-zone increment-zone"
  onclick={handleIncrement}
  onkeydown={(e) => handleKeydown(e, 'increment')}
  disabled={!canIncrement}
  aria-label="Increase {title}"
>
  <div class="zone-icon">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round">
      <path d="M12 5v14M5 12h14"/>
    </svg>
  </div>
</button>

<!-- Landscape Mode: Centered Value Display -->
<div class="stepper-value landscape-value" aria-live="polite">
  <span class="value-number">{displayValue}</span>
</div>

<!-- Landscape Mode: Content Layer -->
<div class="content-layer">
  <CardHeader {title} {headerFontSize} />

  {#if subtitle}
    <div class="card-subtitle">{subtitle}</div>
  {/if}
  {#if description}
    <div class="card-description">{description}</div>
  {/if}
</div>

<style>
  /* LANDSCAPE MODE: Horizontal Stepper Layout */

  /* Content layer - sits above touch zones */
  .content-layer {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    height: 100%;
    z-index: 2;
    pointer-events: none;
  }

  /* Landscape mode: Touch zones for left/right buttons */
  .touch-zone {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 50%;

    display: flex;
    align-items: center;

    background: transparent;
    border: none;
    color: color-mix(in srgb, var(--text-color) 40%, transparent);

    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);

    user-select: none;
    -webkit-user-select: none;

    z-index: 1;
  }

  .decrement-zone {
    left: 0;
    justify-content: center;
    padding-right: clamp(14px, 4cqw, 32px);
    padding-left: clamp(2px, 0.5cqw, 4px);
  }

  .increment-zone {
    right: 0;
    justify-content: center;
    padding-left: clamp(14px, 4cqw, 32px);
    padding-right: clamp(2px, 0.5cqw, 4px);
  }

  .touch-zone:hover:not(:disabled) {
    background: color-mix(in srgb, var(--text-color) 15%, transparent);
    color: color-mix(in srgb, var(--text-color) 80%, transparent);
  }

  .touch-zone:active:not(:disabled) {
    background: color-mix(in srgb, var(--text-color) 25%, transparent);
    color: var(--text-color);
  }

  .touch-zone:disabled {
    opacity: 0.2;
    cursor: not-allowed;
  }

  .touch-zone:focus-visible {
    outline: 2px solid color-mix(in srgb, var(--text-color) 70%, transparent);
    outline-offset: -2px;
  }

  .zone-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(28px, 6cqh, 40px);
    height: clamp(28px, 6cqh, 40px);
    flex-shrink: 0;

    background: color-mix(in srgb, var(--text-color) 15%, transparent);
    border: 2px solid color-mix(in srgb, var(--text-color) 30%, transparent);
    border-radius: 50%;
    color: var(--text-color);

    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
  }

  .zone-icon svg {
    width: 60%;
    height: 60%;
  }

  /* Visual feedback when touch zone is hovered/active */
  .touch-zone:hover:not(:disabled) .zone-icon {
    background: color-mix(in srgb, var(--text-color) 25%, transparent);
    border-color: color-mix(in srgb, var(--text-color) 50%, transparent);
    transform: scale(1.05);
  }

  .touch-zone:active:not(:disabled) .zone-icon {
    background: color-mix(in srgb, var(--text-color) 35%, transparent);
    transform: scale(0.95);
  }

  /* Landscape mode: Centered value display */
  .landscape-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    padding: 0 clamp(6px, 1.5cqw, 12px);
    font-size: clamp(18px, 5cqh, 28px);
    font-weight: 700;
    color: var(--text-color);
    text-align: center;
    line-height: 1.2;

    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    pointer-events: none;
    white-space: nowrap;
    z-index: 3;
  }

  /* Landscape mode: Absolutely positioned subtitle and description */
  .card-subtitle {
    position: absolute;
    bottom: clamp(4px, 1cqh, 8px);
    left: clamp(4px, 1cqw, 8px);
    right: clamp(4px, 1cqw, 8px);

    font-size: clamp(9px, 2cqh, 12px);
    font-weight: 500;
    color: color-mix(in srgb, var(--text-color) 80%, transparent);
    text-align: center;
    text-transform: lowercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    pointer-events: none;
  }

  .card-subtitle:has(~ .card-description) {
    bottom: clamp(16px, 3.5cqh, 22px);
  }

  .card-description {
    position: absolute;
    bottom: clamp(4px, 1cqh, 8px);
    left: clamp(4px, 1cqw, 8px);
    right: clamp(4px, 1cqw, 8px);

    font-size: clamp(9px, 2.2cqh, 11px);
    font-weight: 500;
    color: color-mix(in srgb, var(--text-color) 75%, transparent);
    text-align: center;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    pointer-events: none;
  }

  /* Desktop optimization: Larger controls */
  @media (min-width: 1280px) {
    .landscape-value {
      font-size: clamp(32px, 8cqh, 56px);
    }

    .card-description {
      font-size: clamp(11px, 1.8vh, 14px);
    }
  }
</style>
