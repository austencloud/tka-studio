<script lang="ts">
  import { fade } from "svelte/transition";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    size = "medium",
    color = "var(--primary-color)",
    overlay = false,
    message = "Loading...",
    detail = "",
    show = true,
  } = $props<{
    size?: "small" | "medium" | "large";
    color?: string;
    overlay?: boolean;
    message?: string;
    detail?: string;
    show?: boolean;
  }>();
</script>

{#if show}
  {#if overlay}
    <!-- Loading overlay mode -->
    <div class="loading-overlay" transition:fade>
      <div class="loading-content">
        <div
          class="loading-spinner"
          class:small={size === "small"}
          class:medium={size === "medium"}
          class:large={size === "large"}
          style="--spinner-color: {color}"
        >
          <div class="spinner-ring">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
          </div>
        </div>
        <p class="loading-message">{message}</p>
        {#if detail}
          <p class="loading-detail">{detail}</p>
        {/if}
      </div>
    </div>
  {:else}
    <!-- Inline spinner mode -->
    <div
      class="loading-spinner"
      class:small={size === "small"}
      class:medium={size === "medium"}
      class:large={size === "large"}
      style="--spinner-color: {color}"
    >
      <div class="spinner-ring">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  {/if}
{/if}

<style>
  /* Overlay styles */
  .loading-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .loading-content {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    padding: var(--spacing-xl);
    text-align: center;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    max-width: 300px;
    backdrop-filter: blur(10px);
  }

  .loading-message {
    margin: var(--spacing-md) 0 0 0;
    color: #374151;
    font-weight: 600;
  }

  .loading-detail {
    font-size: var(--font-size-sm);
    color: #6b7280;
    font-weight: 400;
    margin: var(--spacing-xs) 0 0 0;
  }

  /* Spinner styles */
  .loading-spinner {
    display: inline-block;
    position: relative;
  }

  .spinner-ring {
    display: inline-block;
    position: relative;
  }

  .spinner-ring div {
    box-sizing: border-box;
    display: block;
    position: absolute;
    border-radius: 50%;
    animation: spinner-ring-animation 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    border-color: var(--spinner-color) transparent transparent transparent;
  }

  .spinner-ring div:nth-child(1) {
    animation-delay: -0.45s;
  }

  .spinner-ring div:nth-child(2) {
    animation-delay: -0.3s;
  }

  .spinner-ring div:nth-child(3) {
    animation-delay: -0.15s;
  }

  /* Size variants */
  .small .spinner-ring {
    width: 24px;
    height: 24px;
  }

  .small .spinner-ring div {
    width: 20px;
    height: 20px;
    margin: 2px;
    border-width: 2px;
  }

  .medium .spinner-ring {
    width: 40px;
    height: 40px;
  }

  .medium .spinner-ring div {
    width: 32px;
    height: 32px;
    margin: 4px;
    border-width: 3px;
  }

  .large .spinner-ring {
    width: 64px;
    height: 64px;
  }

  .large .spinner-ring div {
    width: 52px;
    height: 52px;
    margin: 6px;
    border-width: 4px;
  }

  @keyframes spinner-ring-animation {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>