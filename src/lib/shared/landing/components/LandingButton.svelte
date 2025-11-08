<script lang="ts">
  /**
   * Landing Button Component
   *
   * Opens the full-screen landing page modal.
   * Provides access to resources, community links, and support options.
   */

  import { toggleLanding } from "../state/landing-state.svelte";

  // Props
  let { onclick = () => {} }: { onclick?: () => void } = $props();

  function handleClick() {
    toggleLanding();
    onclick();
  }
</script>

<button
  class="landing-button glass-surface"
  onclick={handleClick}
  title="Home & Resources"
  aria-label="Open landing page"
>
  <i class="fas fa-home icon-minimal"></i>
</button>

<style>
  .landing-button {
    /* Match existing button sizing - WCAG AAA minimum touch target */
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    border-radius: 50%;
    border: 1px solid rgba(56, 189, 248, 0.3);
    background: linear-gradient(
      135deg,
      rgba(56, 189, 248, 0.15) 0%,
      rgba(6, 182, 212, 0.1) 100%
    );
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
  }

  .landing-button:hover {
    background: linear-gradient(
      135deg,
      rgba(56, 189, 248, 0.25) 0%,
      rgba(6, 182, 212, 0.2) 100%
    );
    border-color: rgba(56, 189, 248, 0.5);
    transform: scale(1.05);
  }

  .landing-button:active {
    transform: scale(0.95);
  }

  /* Icon styling - White to match other buttons */
  .icon-minimal {
    font-size: 20px;
    color: rgba(255, 255, 255, 0.9);
  }

  /* Accessibility */
  .landing-button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .landing-button {
      transition: none;
    }

    .landing-button:hover,
    .landing-button:active {
      transform: none;
    }
  }

  /* High Contrast */
  @media (prefers-contrast: high) {
    .landing-button {
      background: rgba(255, 255, 255, 0.2);
      border: 2px solid white;
    }

    .icon-minimal {
      color: white;
      filter: none;
    }
  }
</style>
