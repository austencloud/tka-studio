<!--
  ToggleRow.svelte - Reusable Toggle Switch Component

  A self-contained toggle row with label, optional badge, and toggle switch.
  Used for all visibility controls in the settings panel.
-->
<script lang="ts">
  interface Props {
    label: string;
    checked: boolean;
    disabled?: boolean;
    badgeText?: string | undefined;
    onChange: () => void;
    ariaLabel?: string;
  }

  let {
    label,
    checked,
    disabled = false,
    badgeText,
    onChange,
    ariaLabel,
  }: Props = $props();
</script>

<div class="toggle-row" class:disabled>
  <span class="toggle-label">
    {label}
    {#if badgeText}
      <span class="disabled-badge">{badgeText}</span>
    {/if}
  </span>
  <label class="toggle-switch">
    <input
      type="checkbox"
      {checked}
      {disabled}
      onchange={onChange}
      aria-label={ariaLabel || `Toggle ${label} visibility`}
    />
    <span class="toggle-slider"></span>
  </label>
</div>

<style>
  .toggle-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: clamp(0.5rem, 2vw, 1rem);
    padding: clamp(0.625rem, 1.5vw, 0.875rem) 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    transition: opacity 0.2s;
  }

  .toggle-row:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }

  .toggle-row:first-child {
    padding-top: 0;
  }

  .toggle-row.disabled {
    opacity: 0.5;
  }

  .toggle-label {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    font-size: clamp(0.813rem, 1.5vw + 0.125rem, 1rem);
    font-weight: 500;
    color: rgba(255, 255, 255, 0.95);
    flex: 1;
    min-width: 0;
  }

  .disabled-badge {
    font-size: clamp(0.688rem, 1.25vw, 0.813rem);
    font-weight: 400;
    color: rgba(255, 193, 7, 0.9);
  }

  /* Toggle Switch - Fluid sizing with minimum touch target */
  .toggle-switch {
    flex-shrink: 0;
    position: relative;
    display: inline-block;
    width: clamp(2.75rem, 5vw, 3.25rem);
    height: clamp(1.625rem, 3vw, 2rem);
    cursor: pointer;
  }

  .toggle-switch input {
    position: absolute;
    opacity: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
    margin: 0;
    z-index: 2;
    top: 0;
    left: 0;
  }

  .toggle-slider {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 999px;
    transition: all 0.3s;
  }

  .toggle-slider:before {
    content: "";
    position: absolute;
    height: calc(100% - 6px);
    aspect-ratio: 1;
    left: 3px;
    top: 50%;
    transform: translateY(-50%);
    background: white;
    border-radius: 50%;
    transition: all 0.3s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  input:checked + .toggle-slider {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
  }

  input:checked + .toggle-slider:before {
    left: calc(100% - 3px);
    transform: translate(-100%, -50%);
  }

  input:disabled + .toggle-slider {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .toggle-row,
    .toggle-slider,
    .toggle-slider:before {
      transition: none;
    }
  }
</style>
