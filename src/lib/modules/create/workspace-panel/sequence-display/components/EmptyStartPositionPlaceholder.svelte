<!--
EmptyStartPositionPlaceholder.svelte - Empty Start Position Placeholder Component

Displays a glassmorphism-styled placeholder when no start position has been selected yet.
Fills the entire beat cell space with a subtle animated glass effect.
-->
<script lang="ts">
  import { FontAwesomeIcon } from "$shared";

  // No props needed - this is a pure presentation component
</script>

<div class="empty-start-placeholder">
  <!-- Glossy sheen overlay for 3D glass effect -->
  <div class="glass-sheen"></div>

  <!-- Content -->
  <div class="placeholder-content">
    <div class="start-text">Choose your start position!</div>
  </div>
</div>

<style>
  .empty-start-placeholder {
    /* Fill entire container - same size as actual beat cells */
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;

    /* Glassmorphism styling */
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.12) 0%,
      rgba(255, 255, 255, 0.06) 100%
    );
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);

    /* Glass border */
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 0; /* Match pictograph - no border radius */

    /* Glass shadow with inset highlight */
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.12),
      0 4px 16px rgba(0, 0, 0, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.25);

    /* Smooth transitions - but don't transition transform (let animation handle it) */
    transition:
      background 0.3s cubic-bezier(0.4, 0, 0.2, 1),
      border-color 0.3s cubic-bezier(0.4, 0, 0.2, 1),
      box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    overflow: hidden;

    /* More pronounced breathing animation with shimmer */
    animation: glassBreath 2.5s ease-in-out infinite;
  }

  .empty-start-placeholder:hover {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.18) 0%,
      rgba(255, 255, 255, 0.1) 100%
    );
    border-color: rgba(255, 255, 255, 0.35);
    box-shadow:
      0 12px 40px rgba(0, 0, 0, 0.18),
      0 6px 20px rgba(0, 0, 0, 0.12),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  /* Glossy sheen overlay - creates 3D glass effect with shimmer */
  .glass-sheen {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    right: 0;
    height: 100%;
    width: 200%;
    background: linear-gradient(
      90deg,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.3) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    pointer-events: none;
    z-index: 1;
    animation: shimmer 3s ease-in-out infinite;
  }

  .placeholder-content {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 1rem;
  }

  .icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.7);
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
    animation: iconPulse 2.5s ease-in-out infinite;
  }

  .start-text {
    font-family: Georgia, serif;
    font-size: 1.25rem;
    font-weight: bold;
    color: rgba(255, 255, 255, 0.9);
    text-align: center;
    letter-spacing: 1px;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }

  /* Glass breathing animation - more pronounced */
  @keyframes glassBreath {
    0%,
    100% {
      opacity: 0.75;
      box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.12),
        0 4px 16px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }
    50% {
      opacity: 1;
      box-shadow:
        0 12px 40px rgba(0, 0, 0, 0.15),
        0 6px 20px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.35);
    }
  }

  /* Shimmer effect across the glass */
  @keyframes shimmer {
    0% {
      left: -100%;
    }
    50%,
    100% {
      left: 100%;
    }
  }

  /* Icon pulse animation */
  @keyframes iconPulse {
    0%,
    100% {
      transform: scale(1);
      opacity: 0.7;
    }
    50% {
      transform: scale(1.1);
      opacity: 1;
    }
  }

  /* Responsive text sizing */
  @media (max-width: 768px) {
    .start-text {
      font-size: 1.25rem;
    }
  }

  @media (max-width: 480px) {
    .start-text {
      font-size: 1.1rem;
    }
  }
</style>
