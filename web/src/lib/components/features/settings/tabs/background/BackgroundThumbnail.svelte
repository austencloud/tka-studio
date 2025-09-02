<!--
  BackgroundThumbnail.svelte - Individual background preview thumbnail
  
  A focused component that renders a single background option with its
  animated preview, metadata, and selection state.
-->
<script lang="ts">
  import type { BackgroundType } from "$domain";
  import type { BackgroundMetadata } from "./background-config";

  interface Props {
    background: BackgroundMetadata;
    isSelected: boolean;
    onSelect: (type: BackgroundType) => void;
  }

  const { background, isSelected, onSelect }: Props = $props();

  function handleClick() {
    onSelect(background.type);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onSelect(background.type);
    }
  }
</script>

<div
  class="background-thumbnail {background.animation}"
  class:selected={isSelected}
  style="--bg-gradient: {background.gradient}"
  onclick={handleClick}
  onkeydown={handleKeydown}
  role="button"
  tabindex="0"
  aria-label={`Select ${background.name} background`}
>
  <!-- Animated background preview -->
  <div class="background-preview"></div>

  <!-- Overlay with background info -->
  <div class="thumbnail-overlay">
    <div class="thumbnail-icon">{background.icon}</div>
    <div class="thumbnail-info">
      <h4 class="thumbnail-name">{background.name}</h4>
      <p class="thumbnail-description">{background.description}</p>
    </div>

    <!-- Selection indicator -->
    {#if isSelected}
      <div class="selection-indicator">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <circle
            cx="12"
            cy="12"
            r="10"
            fill="rgba(99, 102, 241, 0.2)"
            stroke="#6366f1"
            stroke-width="2"
          />
          <path
            d="M8 12l2 2 4-4"
            stroke="#6366f1"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>
    {/if}
  </div>
</div>

<style>
  .background-thumbnail {
    position: relative;
    height: 180px;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
  }

  .background-thumbnail:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  }

  .background-thumbnail.selected {
    border-color: #6366f1;
    box-shadow:
      0 0 0 1px #6366f1,
      0 4px 20px rgba(99, 102, 241, 0.3);
  }

  .background-thumbnail:focus-visible {
    outline: 2px solid #6366f1;
    outline-offset: 2px;
  }

  .background-preview {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--bg-gradient);
    opacity: 0.8;
  }

  .thumbnail-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(0, 0, 0, 0.3) 0%,
      rgba(0, 0, 0, 0.1) 50%,
      rgba(0, 0, 0, 0.4) 100%
    );
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 16px;
    color: white;
    backdrop-filter: blur(1px);
  }

  .thumbnail-icon {
    font-size: 32px;
    line-height: 1;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }

  .thumbnail-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }

  .thumbnail-name {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 8px 0;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.7);
  }

  .thumbnail-description {
    font-size: 14px;
    margin: 0;
    opacity: 0.9;
    line-height: 1.3;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.7);
  }

  .selection-indicator {
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    padding: 4px;
    backdrop-filter: blur(10px);
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .background-thumbnail {
      transition: none;
    }

    .background-thumbnail:hover {
      transform: none;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .background-thumbnail {
      border-color: white;
    }

    .background-thumbnail.selected {
      border-color: #6366f1;
      background: rgba(99, 102, 241, 0.1);
    }

    .thumbnail-overlay {
      background: rgba(0, 0, 0, 0.8);
    }
  }
</style>
