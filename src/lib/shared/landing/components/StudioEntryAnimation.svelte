<script lang="ts">
  /**
   * Studio Entry Animation Component
   *
   * Beautiful transition animation shown when entering the studio for the first time.
   * Features opening doors, golden sparkles, and a welcoming message.
   */

  import { fade } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { onMount } from "svelte";

  // Generate random sparkles
  let sparkles = $state<
    Array<{
      id: number;
      left: number;
      top: number;
      delay: number;
      size: number;
    }>
  >([]);

  onMount(() => {
    // Generate 30 random sparkles
    sparkles = Array.from({ length: 30 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      delay: Math.random() * 800,
      size: 4 + Math.random() * 8,
    }));
  });
</script>

<!-- Full screen overlay with doors opening animation -->
<div
  class="studio-entry-overlay"
  transition:fade={{ duration: 600, easing: cubicOut }}
>
  <!-- Left Door -->
  <div class="door door-left"></div>

  <!-- Right Door -->
  <div class="door door-right"></div>

  <!-- Welcome Message -->
  <div class="welcome-message">
    <div class="welcome-icon">
      <i class="fas fa-door-open"></i>
    </div>
    <h2 class="welcome-text">Welcome to the Studio</h2>
    <div class="welcome-subtitle">Your creative journey begins...</div>
  </div>

  <!-- Golden Sparkles -->
  <div class="sparkles-container">
    {#each sparkles as sparkle (sparkle.id)}
      <div
        class="sparkle"
        style="
          left: {sparkle.left}%;
          top: {sparkle.top}%;
          animation-delay: {sparkle.delay}ms;
          width: {sparkle.size}px;
          height: {sparkle.size}px;
        "
      ></div>
    {/each}
  </div>
</div>

<style>
  /* ============================================================================
     OVERLAY BASE
     ============================================================================ */
  .studio-entry-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 10002; /* Above landing modal */
    overflow: hidden;
    pointer-events: none;
    background: linear-gradient(
      135deg,
      rgba(20, 20, 30, 0.98) 0%,
      rgba(30, 30, 40, 0.98) 100%
    );
  }

  /* ============================================================================
     DOORS
     ============================================================================ */
  .door {
    position: absolute;
    top: 0;
    width: 50%;
    height: 100%;
    background: linear-gradient(
      135deg,
      rgba(102, 126, 234, 0.15) 0%,
      rgba(118, 75, 162, 0.15) 100%
    );
    border: 2px solid rgba(255, 215, 0, 0.3);
    box-shadow:
      inset 0 0 60px rgba(255, 215, 0, 0.1),
      0 0 40px rgba(102, 126, 234, 0.2);
    animation: door-open 1200ms cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
  }

  .door-left {
    left: 0;
    transform-origin: left center;
    border-right: 4px solid rgba(255, 215, 0, 0.4);
  }

  .door-right {
    right: 0;
    transform-origin: right center;
    border-left: 4px solid rgba(255, 215, 0, 0.4);
  }

  @keyframes door-open {
    0% {
      transform: perspective(1200px) rotateY(0deg);
      opacity: 1;
    }
    100% {
      transform: perspective(1200px) rotateY(90deg);
      opacity: 0;
    }
  }

  .door-left {
    animation-name: door-open-left;
  }

  .door-right {
    animation-name: door-open-right;
  }

  @keyframes door-open-left {
    0% {
      transform: perspective(1200px) rotateY(0deg);
      opacity: 1;
    }
    100% {
      transform: perspective(1200px) rotateY(-90deg);
      opacity: 0;
    }
  }

  @keyframes door-open-right {
    0% {
      transform: perspective(1200px) rotateY(0deg);
      opacity: 1;
    }
    100% {
      transform: perspective(1200px) rotateY(90deg);
      opacity: 0;
    }
  }

  /* ============================================================================
     WELCOME MESSAGE
     ============================================================================ */
  .welcome-message {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 10;
    opacity: 0;
    animation: welcome-fade-in 800ms ease-out 400ms forwards;
  }

  @keyframes welcome-fade-in {
    0% {
      opacity: 0;
      transform: translate(-50%, -50%) scale(0.9);
    }
    100% {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
    }
  }

  .welcome-icon {
    font-size: clamp(3rem, 8vw, 5rem);
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 4px 12px rgba(255, 215, 0, 0.4));
    animation: icon-glow 2s ease-in-out infinite;
  }

  @keyframes icon-glow {
    0%,
    100% {
      filter: drop-shadow(0 4px 12px rgba(255, 215, 0, 0.4));
    }
    50% {
      filter: drop-shadow(0 6px 20px rgba(255, 215, 0, 0.6));
    }
  }

  .welcome-text {
    font-size: clamp(1.75rem, 5vw, 3rem);
    font-weight: 900;
    margin: 0 0 0.75rem 0;
    background: linear-gradient(
      90deg,
      #667eea 0%,
      #764ba2 25%,
      #f43f5e 50%,
      #38bdf8 75%,
      #667eea 100%
    );
    background-size: 200% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-flow 3s linear infinite;
  }

  @keyframes gradient-flow {
    0% {
      background-position: 0% 50%;
    }
    100% {
      background-position: 200% 50%;
    }
  }

  .welcome-subtitle {
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    color: rgba(255, 255, 255, 0.8);
    font-weight: 500;
    letter-spacing: 0.05em;
  }

  /* ============================================================================
     SPARKLES
     ============================================================================ */
  .sparkles-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
  }

  .sparkle {
    position: absolute;
    opacity: 0;
    animation: sparkle-twinkle 2s ease-in-out infinite;
  }

  /* Create cross/star shape */
  .sparkle::before,
  .sparkle::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 2px;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 215, 0, 1),
      transparent
    );
    transform: translate(-50%, -50%);
    box-shadow: 0 0 6px rgba(255, 215, 0, 0.8);
  }

  .sparkle::before {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  .sparkle::after {
    transform: translate(-50%, -50%) rotate(90deg);
  }

  @keyframes sparkle-twinkle {
    0%,
    100% {
      opacity: 0;
      transform: scale(0) rotate(0deg);
    }
    50% {
      opacity: 1;
      transform: scale(1) rotate(180deg);
    }
  }

  /* ============================================================================
     ACCESSIBILITY & REDUCED MOTION
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .door,
    .welcome-message,
    .sparkle,
    .welcome-icon,
    .welcome-text {
      animation: none !important;
    }

    .door {
      opacity: 0;
    }

    .welcome-message {
      opacity: 1;
      transform: translate(-50%, -50%);
    }

    .sparkle {
      display: none;
    }
  }

  /* High Contrast Mode */
  @media (prefers-contrast: high) {
    .studio-entry-overlay {
      background: black;
      border: 2px solid white;
    }

    .door {
      background: rgba(255, 255, 255, 0.1);
      border-color: white;
    }

    .welcome-text {
      background: white;
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }
</style>
