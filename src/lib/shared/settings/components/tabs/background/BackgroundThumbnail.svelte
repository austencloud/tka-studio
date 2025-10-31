<!--
  BackgroundThumbnail.svelte - Individual background preview thumbnail

  A focused component that renders a single background option with its
  animated preview, metadata, and selection state.
-->
<script lang="ts">
  import type { BackgroundType, IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { BackgroundMetadata } from "./background-config";

  const {
    background,
    isSelected,
    onSelect,
    orientation = "square",
  } = $props<{
    background: BackgroundMetadata;
    isSelected: boolean;
    onSelect: (type: BackgroundType) => void;
    orientation?: "portrait" | "landscape" | "square";
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleClick() {
    // Trigger selection haptic feedback for background selection
    hapticService?.trigger("selection");
    onSelect(background.type);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      // Trigger selection haptic feedback for keyboard selection
      hapticService?.trigger("selection");
      onSelect(background.type);
    }
  }
</script>

<div
  class="background-thumbnail {background.animation}"
  class:selected={isSelected}
  data-orientation={orientation}
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
    <div class="thumbnail-icon">{@html background.icon}</div>
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
  /* ===== ANIMATION STYLES ===== */
  /* Using :global() for dynamically added class names and -global- prefix for keyframes */
  /* This prevents Svelte from stripping these as "unused" at compile time */

  /* Aurora Flow - Colorful flowing gradient */
  .background-thumbnail:global(.aurora-flow) .background-preview {
    background: linear-gradient(
      45deg,
      #667eea,
      #764ba2,
      #f093fb,
      #f5576c,
      #4facfe,
      #00f2fe
    ) !important;
    background-size: 400% 400%;
    animation: -global-aurora-animation 8s ease-in-out infinite;
  }

  @keyframes -global-aurora-animation {
    0%,
    100% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
  }

  /* Snowfall Animation - Dark blue background with falling snow */
  .background-thumbnail:global(.snow-fall) .background-preview {
    background: linear-gradient(
      135deg,
      #1a1a2e 0%,
      #16213e 50%,
      #0f3460 100%
    ) !important;
  }

  .background-thumbnail:global(.snow-fall) .background-preview::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
      radial-gradient(2px 2px at 20px 30px, #ffffff, transparent),
      radial-gradient(1.5px 1.5px at 40px 70px, #f8faff, transparent),
      radial-gradient(1px 1px at 90px 40px, #e8f4f8, transparent),
      radial-gradient(1px 1px at 130px 80px, #f0f8ff, transparent);
    background-size: 320px 160px;
    animation: -global-snowfall 15s ease-in-out infinite;
    opacity: 0.9;
  }

  @keyframes -global-snowfall {
    0% {
      transform: translateY(-30px) translateX(0px);
    }
    100% {
      transform: translateY(220px) translateX(2px);
    }
  }

  /* Night Sky Animation - Deep purple with twinkling stars */
  .background-thumbnail:global(.star-twinkle) .background-preview {
    background: linear-gradient(
      135deg,
      #0a0e2c 0%,
      #1a2040 50%,
      #2a3060 100%
    ) !important;
  }

  .background-thumbnail:global(.star-twinkle) .background-preview::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
      radial-gradient(1px 1px at 25px 25px, #ffffff, transparent),
      radial-gradient(2px 2px at 75px 50px, #ffeb3b, transparent),
      radial-gradient(1px 1px at 125px 75px, #ffffff, transparent),
      radial-gradient(2px 2px at 200px 100px, #ffffff, transparent);
    background-size: 280px 180px;
    animation: -global-star-twinkle-animation 3s ease-in-out infinite;
    opacity: 0.9;
  }

  @keyframes -global-star-twinkle-animation {
    0%,
    100% {
      opacity: 0.9;
    }
    50% {
      opacity: 0.4;
    }
  }

  /* Ocean Animation - Very dark blue with rising bubbles */
  .background-thumbnail:global(.bubble-float) .background-preview {
    background: linear-gradient(
      135deg,
      #001122 0%,
      #000c1e 50%,
      #000511 100%
    ) !important;
  }

  .background-thumbnail:global(.bubble-float) .background-preview::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
      radial-gradient(
        circle at 30px 140px,
        rgba(255, 255, 255, 0.4) 3px,
        transparent 4px
      ),
      radial-gradient(
        circle at 80px 160px,
        rgba(255, 255, 255, 0.3) 5px,
        transparent 6px
      ),
      radial-gradient(
        circle at 120px 120px,
        rgba(255, 255, 255, 0.35) 2px,
        transparent 3px
      );
    background-size: 250px 200px;
    animation: -global-bubble-rise 8s ease-in-out infinite;
    opacity: 0.8;
  }

  @keyframes -global-bubble-rise {
    0% {
      transform: translateY(30px);
    }
    50% {
      transform: translateY(-15px) translateX(-3px);
    }
    100% {
      transform: translateY(30px);
    }
  }

  /* ===== COMPONENT STYLES ===== */

  .background-thumbnail {
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: clamp(6px, 1cqi, 12px);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
    /* Ensure minimum touch target size for mobile */
    min-height: 44px;
    min-width: 44px;
  }

  /* Portrait Mode - Cards are shorter and wider */
  .background-thumbnail[data-orientation="portrait"] {
    aspect-ratio: 3 / 2;
    min-height: 60px;
    max-height: 200px;
  }

  /* Landscape Mode - Cards are taller and narrower */
  .background-thumbnail[data-orientation="landscape"] {
    aspect-ratio: 2 / 3;
    min-width: 80px;
    max-width: 300px;
  }

  /* Square/Default Mode - Balanced aspect ratio */
  .background-thumbnail[data-orientation="square"] {
    aspect-ratio: 16 / 9;
    min-height: 80px;
    max-height: 250px;
  }

  .background-thumbnail:hover {
    transform: translateY(-2px);
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

  /* Make background-preview globally accessible for external animation CSS */
  :global(.background-preview) {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    opacity: 1;
  }

  /* Fallback background for non-animated backgrounds */
  .background-thumbnail:not(:global(.aurora-flow)):not(:global(.snow-fall)):not(
      :global(.star-twinkle)
    ):not(:global(.bubble-float))
    :global(.background-preview) {
    background: var(--bg-gradient);
  }

  .thumbnail-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      180deg,
      rgba(0, 0, 0, 0.15) 0%,
      rgba(0, 0, 0, 0.05) 30%,
      rgba(0, 0, 0, 0.05) 70%,
      rgba(0, 0, 0, 0.3) 100%
    ); /* Much lighter overlay - animations visible! */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: clamp(8px, 2cqi, 16px);
    color: white;
    backdrop-filter: none; /* No blur - crisp animations! */
  }

  .thumbnail-icon {
    font-size: clamp(20px, 4cqi, 32px);
    line-height: 1;
    text-shadow:
      0 2px 8px rgba(0, 0, 0, 0.8),
      0 0 4px rgba(0, 0, 0, 0.9); /* Stronger shadow for readability */
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5));
  }

  .thumbnail-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    background: linear-gradient(
      180deg,
      transparent 0%,
      rgba(0, 0, 0, 0.3) 100%
    ); /* Subtle gradient behind text */
    padding: clamp(8px, 1.5cqi, 12px);
    margin: clamp(-8px, -1.5cqi, -12px);
    border-radius: 0 0 clamp(6px, 1cqi, 12px) clamp(6px, 1cqi, 12px);
  }

  .thumbnail-name {
    font-size: clamp(13px, 2.5cqi, 18px);
    font-weight: 700; /* Bolder for better readability */
    margin: 0 0 clamp(3px, 1cqi, 8px) 0;
    text-shadow:
      0 2px 6px rgba(0, 0, 0, 0.9),
      0 0 3px rgba(0, 0, 0, 1); /* Much stronger shadow */
  }

  .thumbnail-description {
    font-size: clamp(10px, 2cqi, 14px);
    margin: 0;
    opacity: 0.95;
    line-height: 1.3;
    font-weight: 500;
    text-shadow:
      0 2px 6px rgba(0, 0, 0, 0.9),
      0 0 3px rgba(0, 0, 0, 1); /* Much stronger shadow */
  }

  .selection-indicator {
    position: absolute;
    top: clamp(8px, 1.5cqi, 12px);
    right: clamp(8px, 1.5cqi, 12px);
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    padding: 4px;
    backdrop-filter: blur(10px);
  }

  /* Accessibility - Disable all animations for reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .background-thumbnail {
      transition: none;
    }

    .background-thumbnail:hover {
      transform: none;
    }

    .background-thumbnail:global(.aurora-flow) .background-preview,
    .background-thumbnail:global(.snow-fall) .background-preview::before,
    .background-thumbnail:global(.star-twinkle) .background-preview::before,
    .background-thumbnail:global(.bubble-float) .background-preview::before {
      animation: none !important;
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
