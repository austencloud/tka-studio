<!--
ToggleOption.svelte - Individual toggle option display component
Presentational component for a single toggle option with icon and label
-->
<script lang="ts">
  import { FontAwesomeIcon } from "$shared";

  let {
    label,
    icon,
    isActive,
    isLandscapeMobile
  } = $props<{
    label: string;
    icon?: string;
    isActive: boolean;
    isLandscapeMobile: boolean;
  }>();

  // Helper function to detect if icon is a Font Awesome icon name
  function isFontAwesomeIcon(iconStr: string | undefined): boolean {
    if (!iconStr) return false;
    // Font Awesome icon names are lowercase with hyphens only
    return /^[a-z-]+$/.test(iconStr);
  }
</script>

<div
  class="toggle-option"
  class:active={isActive}
  class:inactive={!isActive}
  class:landscape-mobile={isLandscapeMobile}
  role="presentation"
  title={label}
  aria-label={label}
>
  {#if icon && !isLandscapeMobile}
    <span class="option-icon">
      {#if isFontAwesomeIcon(icon)}
        <FontAwesomeIcon icon={icon} size="1em" />
      {:else}
        {icon}
      {/if}
    </span>
  {/if}
  <span class="option-label">{label}</span>
</div>

<style>
  .toggle-option {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    flex: 1;
    min-height: 0;
    border-radius: 10px;
    background: transparent;
    border: 1.5px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.6);
    font-weight: 600;
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    user-select: none;
    -webkit-user-select: none;
    pointer-events: none;
  }
  .toggle-option.active {
    background: rgba(255, 255, 255, 0.2);
    border-color: white;
    border-width: 3px;
    color: white;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    transform: scale(1.02);
  }
  .toggle-option.inactive {
    background: rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.25);
    color: rgba(255, 255, 255, 0.7);
  }
  .option-icon {
    font-size: clamp(12px, 4cqw, 20px);
    line-height: 1;
    flex-shrink: 0;
  }
  .option-label {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: center;
    line-height: 1.2;
    padding: 0 2px;
    font-size: clamp(10px, 4.5cqw, 16px);
  }
  .toggle-option.landscape-mobile {
    padding: clamp(2px, 0.5vw, 4px);
  }
  .toggle-option.landscape-mobile .option-label {
    font-size: clamp(9px, 3.5cqw, 12px);
    white-space: nowrap;
  }
  @media (max-width: 320px) {
    .option-label {
      font-size: clamp(9px, 4cqw, 12px);
    }
  }
</style>
