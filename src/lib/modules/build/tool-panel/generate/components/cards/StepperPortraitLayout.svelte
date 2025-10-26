<!--
StepperPortraitLayout.svelte - Portrait/vertical stepper layout
Top half increments, bottom half decrements (vertical layout)
Used when card aspect ratio is tall/portrait
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

<div class="vertical-stepper">
  <!-- Portrait touch zones - top/bottom halves -->
  <button
    class="portrait-touch-zone portrait-increment-zone"
    onclick={handleIncrement}
    onkeydown={(e) => handleKeydown(e, 'increment')}
    disabled={!canIncrement}
    aria-label="Increase {title}"
  ></button>

  <button
    class="portrait-touch-zone portrait-decrement-zone"
    onclick={handleDecrement}
    onkeydown={(e) => handleKeydown(e, 'decrement')}
    disabled={!canDecrement}
    aria-label="Decrease {title}"
  ></button>

  <CardHeader {title} {headerFontSize} />

  <div class="stepper-controls">
    <div class="stepper-button-visual increment-visual">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round">
        <path d="M12 5v14M5 12h14"/>
      </svg>
    </div>

    <div class="stepper-value portrait-value" aria-live="polite">
      <span class="value-number">{displayValue}</span>
    </div>

    <div class="stepper-button-visual decrement-visual">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round">
        <path d="M5 12h14"/>
      </svg>
    </div>
  </div>

  <div class="card-footer">
    {#if subtitle}
      <div class="card-subtitle">{subtitle}</div>
    {/if}
    {#if description}
      <div class="card-description">{description}</div>
    {/if}
  </div>
</div>

<style>
  /* PORTRAIT MODE: Vertical Stepper Layout */
  .vertical-stepper {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    z-index: 2;
  }

  /* Portrait mode: Stepper controls - absolutely centered */
  .stepper-controls {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(6px, 1.5cqh, 8px);
    width: 100%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 3;
    pointer-events: none;
  }

  /* Portrait mode: Footer - absolutely positioned at bottom */
  .card-footer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: clamp(2px, 0.5cqh, 4px);
    z-index: 3;
    pointer-events: none;
  }

  /* Portrait mode: Touch zones - invisible overlay for top/bottom halves */
  .portrait-touch-zone {
    position: absolute;
    left: 0;
    right: 0;
    height: 50%;
    z-index: 1;

    background: transparent;
    border: none;
    cursor: pointer;
    transition: background 0.2s cubic-bezier(0.4, 0, 0.2, 1);

    user-select: none;
    -webkit-user-select: none;
  }

  .portrait-increment-zone {
    top: 0;
  }

  .portrait-decrement-zone {
    bottom: 0;
  }

  .portrait-touch-zone:hover:not(:disabled) {
    background: color-mix(in srgb, var(--text-color) 8%, transparent);
  }

  .portrait-touch-zone:active:not(:disabled) {
    background: color-mix(in srgb, var(--text-color) 15%, transparent);
  }

  .portrait-touch-zone:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .portrait-touch-zone:focus-visible {
    outline: 2px solid color-mix(in srgb, var(--text-color) 70%, transparent);
    outline-offset: -2px;
  }

  /* Portrait mode: Visual button indicators (non-interactive) */
  .stepper-button-visual {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(32px, 8cqh, 48px);
    height: clamp(32px, 8cqh, 48px);
    flex-shrink: 0;

    background: color-mix(in srgb, var(--text-color) 15%, transparent);
    border: 2px solid color-mix(in srgb, var(--text-color) 30%, transparent);
    border-radius: 50%;
    color: var(--text-color);

    pointer-events: none;
    z-index: 2;

    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .stepper-button-visual svg {
    width: 60%;
    height: 60%;
  }

  /* Visual feedback when parent touch zone is interacted with */
  .portrait-increment-zone:hover:not(:disabled) ~ .stepper-controls .increment-visual,
  .portrait-decrement-zone:hover:not(:disabled) ~ .stepper-controls .decrement-visual {
    background: color-mix(in srgb, var(--text-color) 25%, transparent);
    border-color: color-mix(in srgb, var(--text-color) 50%, transparent);
    transform: scale(1.05);
  }

  .portrait-increment-zone:active:not(:disabled) ~ .stepper-controls .increment-visual,
  .portrait-decrement-zone:active:not(:disabled) ~ .stepper-controls .decrement-visual {
    background: color-mix(in srgb, var(--text-color) 35%, transparent);
    transform: scale(0.95);
  }

  /* Portrait mode: Value display */
  .portrait-value {
    font-size: clamp(32px, 12cqh, 64px);
    font-weight: 700;
    color: var(--text-color);
    text-align: center;
    line-height: 1;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    white-space: nowrap;
    flex-shrink: 0;
  }

  /* Portrait mode: Subtitle and description */
  .card-subtitle {
    font-size: clamp(10px, 2.5cqh, 14px);
    font-weight: 500;
    color: color-mix(in srgb, var(--text-color) 85%, transparent);
    text-align: center;
    text-transform: lowercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
    flex-shrink: 0;
  }

  .card-description {
    font-size: clamp(8px, 2cqh, 11px);
    font-weight: 500;
    color: color-mix(in srgb, var(--text-color) 75%, transparent);
    text-align: center;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
    flex-shrink: 0;
  }

  /* Desktop optimization: Larger controls */
  @media (min-width: 1280px) {
    .stepper-button-visual {
      width: clamp(42px, 10cqh, 60px);
      height: clamp(42px, 10cqh, 60px);
    }

    .portrait-value {
      font-size: clamp(36px, 12cqh, 60px);
    }
  }
</style>
