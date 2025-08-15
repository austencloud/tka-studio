<!-- BackgroundTab.svelte - Redesigned with CSS-animated thumbnail selection -->
<script lang="ts">
  import type { BackgroundType } from "$lib/components/backgrounds/types/types";
  import SettingCard from "../SettingCard.svelte";

  interface Props {
    settings: {
      backgroundType?: BackgroundType;
    };
  }

  let { settings, ...events } = $props();

  // Current selection state
  let selectedBackground = $state<BackgroundType>(
    settings.backgroundType || "aurora"
  );

  // Available backgrounds with metadata
  const backgrounds = [
    {
      type: "aurora" as BackgroundType,
      name: "Aurora",
      description: "Colorful flowing aurora with animated blobs",
      icon: "🌌",
      gradient:
        "linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)",
      animation: "aurora-flow",
    },
    {
      type: "snowfall" as BackgroundType,
      name: "Snowfall",
      description: "Gentle falling snowflakes with shooting stars",
      icon: "❄️",
      gradient:
        "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
      animation: "snow-fall",
    },
    {
      type: "nightSky" as BackgroundType,
      name: "Night Sky",
      description: "Starry night with twinkling celestial bodies",
      icon: "🌙",
      gradient:
        "linear-gradient(135deg, #0a0e2c 0%, #1a2040 50%, #2a3060 100%)",
      animation: "star-twinkle",
    },
    {
      type: "bubbles" as BackgroundType,
      name: "Bubbles",
      description: "Underwater scene with floating bubbles",
      icon: "🫧",
      gradient:
        "linear-gradient(135deg, #143250 0%, #0a1e3c 50%, #050f28 100%)",
      animation: "bubble-float",
    },
  ];

  // Handle thumbnail selection
  function selectBackground(backgroundType: BackgroundType) {
    selectedBackground = backgroundType;

    // Update settings - backgrounds are always enabled, quality is auto-managed
    if (events.onupdate) {
      events.onupdate({ key: "backgroundType", value: backgroundType });
    }

    console.log(`🌌 Background changed to: ${backgroundType}`);
  }
</script>

<div class="tab-content">
  <SettingCard
    title="Background Selection"
    description="Choose your preferred animated background"
  >
    <div class="background-grid">
      {#each backgrounds as background}
        <div
          class="background-thumbnail {background.animation}"
          class:selected={selectedBackground === background.type}
          style="--bg-gradient: {background.gradient}"
          onclick={() => selectBackground(background.type)}
          role="button"
          tabindex="0"
          onkeydown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              selectBackground(background.type);
            }
          }}
          aria-label={`Select ${background.name} background`}
        >
          <!-- Animated background preview -->
          <div class="thumbnail-background"></div>

          <!-- Overlay with background info -->
          <div class="thumbnail-overlay">
            <div class="thumbnail-icon">{background.icon}</div>
            <div class="thumbnail-info">
              <h4 class="thumbnail-name">{background.name}</h4>
              <p class="thumbnail-description">{background.description}</p>
            </div>

            <!-- Selection indicator -->
            {#if selectedBackground === background.type}
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
      {/each}
    </div>
  </SettingCard>

  <!-- Current Selection Info -->
  <SettingCard title="Selected Background">
    <div class="current-selection">
      <div
        class="selection-preview"
        style="--bg-gradient: {backgrounds.find(
          (bg) => bg.type === selectedBackground
        )?.gradient}"
      >
        <div
          class="preview-background {backgrounds.find(
            (bg) => bg.type === selectedBackground
          )?.animation}"
        ></div>
        <div class="preview-overlay">
          <div class="preview-icon">
            {backgrounds.find((bg) => bg.type === selectedBackground)?.icon}
          </div>
        </div>
      </div>
      <div class="selection-info">
        <h3>
          {backgrounds.find((bg) => bg.type === selectedBackground)?.name}
        </h3>
        <p>
          {backgrounds.find((bg) => bg.type === selectedBackground)
            ?.description}
        </p>
        <div class="selection-note">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="2"
            />
            <path
              d="M12 6v6l4 2"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
          <span>Background quality automatically optimizes for performance</span
          >
        </div>
      </div>
    </div>
  </SettingCard>
</div>

<style>
  .tab-content {
    width: 100%;
    max-width: var(--max-content-width, 100%);
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: clamp(20px, 3vw, 32px);
    container-type: inline-size;
  }

  .background-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: clamp(16px, 2vw, 24px);
    margin-top: clamp(12px, 1.5vw, 20px);
  }

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

  .thumbnail-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--bg-gradient);
    opacity: 0.8;
  }

  /* Animated CSS backgrounds */
  .aurora-flow .thumbnail-background {
    background: linear-gradient(
      45deg,
      #667eea,
      #764ba2,
      #f093fb,
      #f5576c,
      #4facfe,
      #00f2fe
    );
    background-size: 400% 400%;
    animation: aurora-animation 8s ease-in-out infinite;
  }

  .snow-fall .thumbnail-background {
    background: var(--bg-gradient);
    position: relative;
  }

  .snow-fall .thumbnail-background::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
      radial-gradient(2px 2px at 20px 30px, white, transparent),
      radial-gradient(2px 2px at 40px 70px, white, transparent),
      radial-gradient(1px 1px at 90px 40px, white, transparent),
      radial-gradient(1px 1px at 130px 80px, white, transparent),
      radial-gradient(2px 2px at 160px 30px, white, transparent),
      radial-gradient(1px 1px at 200px 60px, white, transparent),
      radial-gradient(2px 2px at 240px 90px, white, transparent),
      radial-gradient(1px 1px at 280px 40px, white, transparent);
    background-repeat: repeat;
    background-size: 300px 150px;
    animation: snowfall 12s linear infinite;
    opacity: 0.8;
  }

  .snow-fall .thumbnail-background::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      45deg,
      transparent 30%,
      rgba(255, 255, 255, 0.3) 50%,
      transparent 70%
    );
    background-size: 400px 400px;
    animation: shooting-star 15s ease-in-out infinite;
    opacity: 0.4;
  }

  .star-twinkle .thumbnail-background {
    background: var(--bg-gradient);
    position: relative;
  }

  .star-twinkle .thumbnail-background::before {
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
      radial-gradient(1px 1px at 175px 25px, #81c784, transparent),
      radial-gradient(2px 2px at 200px 100px, #ffffff, transparent),
      radial-gradient(1px 1px at 50px 120px, #ffcdd2, transparent),
      radial-gradient(1px 1px at 150px 140px, #ffffff, transparent),
      radial-gradient(2px 2px at 250px 60px, #e1bee7, transparent);
    background-repeat: repeat;
    background-size: 280px 180px;
    animation: star-twinkle-animation 3s ease-in-out infinite;
    opacity: 0.9;
  }

  .star-twinkle .thumbnail-background::after {
    content: "";
    position: absolute;
    top: 20px;
    right: 30px;
    width: 40px;
    height: 40px;
    background: radial-gradient(
      circle,
      #ffd54f 30%,
      rgba(255, 213, 79, 0.3) 70%,
      transparent
    );
    border-radius: 50%;
    animation: moon-glow 6s ease-in-out infinite;
    opacity: 0.8;
  }

  .bubble-float .thumbnail-background {
    background: var(--bg-gradient);
    position: relative;
    overflow: hidden;
  }

  .bubble-float .thumbnail-background::before {
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
      ),
      radial-gradient(
        circle at 170px 180px,
        rgba(255, 255, 255, 0.4) 4px,
        transparent 5px
      ),
      radial-gradient(
        circle at 220px 140px,
        rgba(255, 255, 255, 0.25) 3px,
        transparent 4px
      ),
      radial-gradient(
        circle at 60px 100px,
        rgba(255, 255, 255, 0.3) 2px,
        transparent 3px
      ),
      radial-gradient(
        circle at 200px 60px,
        rgba(255, 255, 255, 0.4) 6px,
        transparent 7px
      );
    background-size: 250px 200px;
    animation: bubble-rise 8s ease-in-out infinite;
    opacity: 0.8;
  }

  .bubble-float .thumbnail-background::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
      linear-gradient(
        120deg,
        transparent 0%,
        rgba(64, 224, 208, 0.1) 30%,
        transparent 50%
      ),
      linear-gradient(
        60deg,
        transparent 20%,
        rgba(135, 206, 250, 0.15) 60%,
        transparent 80%
      );
    background-size:
      200px 100%,
      300px 100%;
    animation: underwater-light 10s ease-in-out infinite;
    opacity: 0.6;
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
    justify-content: center;
    text-align: center;
    gap: 8px;
  }

  .thumbnail-name {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.7);
    letter-spacing: 0.5px;
  }

  .thumbnail-description {
    margin: 0;
    font-size: 13px;
    opacity: 0.9;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
    line-height: 1.3;
    max-width: 220px;
    margin-left: auto;
    margin-right: auto;
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

  /* Current Selection Styles */
  .current-selection {
    display: flex;
    gap: clamp(16px, 2vw, 24px);
    align-items: center;
    margin-top: clamp(12px, 1.5vw, 20px);
  }

  .selection-preview {
    position: relative;
    width: 120px;
    height: 80px;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.2);
    flex-shrink: 0;
  }

  .preview-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--bg-gradient);
    opacity: 0.8;
  }

  .preview-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.2);
  }

  .preview-icon {
    font-size: 24px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }

  .selection-info {
    flex: 1;
    min-width: 0;
  }

  .selection-info h3 {
    margin: 0 0 8px 0;
    font-size: 18px;
    font-weight: 600;
    color: white;
  }

  .selection-info p {
    margin: 0 0 12px 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.4;
  }

  .selection-note {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    font-style: italic;
  }

  .selection-note svg {
    flex-shrink: 0;
    opacity: 0.7;
  }

  /* Animations */
  @keyframes aurora-animation {
    0%,
    100% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
  }

  @keyframes snowfall {
    0% {
      transform: translateY(-20px);
    }
    100% {
      transform: translateY(200px);
    }
  }

  @keyframes shooting-star {
    0% {
      transform: translateX(-400px) translateY(-100px);
      opacity: 0;
    }
    10% {
      opacity: 1;
    }
    90% {
      opacity: 1;
    }
    100% {
      transform: translateX(400px) translateY(100px);
      opacity: 0;
    }
  }

  @keyframes star-twinkle-animation {
    0%,
    100% {
      opacity: 0.9;
    }
    25% {
      opacity: 0.4;
    }
    50% {
      opacity: 0.9;
    }
    75% {
      opacity: 0.6;
    }
  }

  @keyframes moon-glow {
    0%,
    100% {
      box-shadow: 0 0 20px rgba(255, 213, 79, 0.3);
      transform: scale(1);
    }
    50% {
      box-shadow: 0 0 30px rgba(255, 213, 79, 0.6);
      transform: scale(1.1);
    }
  }

  @keyframes bubble-rise {
    0% {
      transform: translateY(30px);
    }
    25% {
      transform: translateY(-5px) translateX(5px);
    }
    50% {
      transform: translateY(-15px) translateX(-3px);
    }
    75% {
      transform: translateY(-8px) translateX(8px);
    }
    100% {
      transform: translateY(30px);
    }
  }

  @keyframes underwater-light {
    0% {
      transform: translateX(-200px) rotate(0deg);
    }
    50% {
      transform: translateX(200px) rotate(180deg);
    }
    100% {
      transform: translateX(-200px) rotate(360deg);
    }
  }

  /* Container Queries for Responsive Layout */
  @container (max-width: 600px) {
    .background-grid {
      grid-template-columns: 1fr;
    }

    .current-selection {
      flex-direction: column;
      text-align: center;
    }

    .selection-preview {
      width: 100%;
      max-width: 300px;
      height: 120px;
    }
  }

  @container (min-width: 900px) {
    .background-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @container (min-width: 1200px) {
    .background-grid {
      grid-template-columns: repeat(2, 1fr);
      max-width: 800px;
      margin: 0 auto;
    }
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .background-thumbnail,
    .thumbnail-background,
    .preview-background {
      animation: none !important;
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
