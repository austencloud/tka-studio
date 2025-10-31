<!-- SettingCard.svelte - Improved contrast card container with contextual help -->
<script lang="ts">
  import type { Snippet } from "svelte";

  let { title, description, helpText, children } = $props<{
    title?: string;
    description?: string;
    helpText?: string;
    children: Snippet;
  }>();

  let showTooltip = $state(false);
</script>

<div class="setting-section">
  {#if title}
    <div class="title-container">
      <h3 class="section-title">{title}</h3>
      {#if helpText}
        <button
          class="help-button"
          aria-label="Help for {title}"
          onmouseenter={() => (showTooltip = true)}
          onmouseleave={() => (showTooltip = false)}
          onfocus={() => (showTooltip = true)}
          onblur={() => (showTooltip = false)}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="2"
            />
            <path
              d="M12 16v-1a2 2 0 012-2v0a2 2 0 002-2v0a2 2 0 00-2-2h-1a2 2 0 00-2 2"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
            <circle cx="12" cy="18" r="0.5" fill="currentColor" />
          </svg>
          {#if showTooltip}
            <span class="tooltip">{helpText}</span>
          {/if}
        </button>
      {/if}
    </div>
  {/if}
  {#if description}
    <p class="section-description">{description}</p>
  {/if}

  <div class="setting-cards">
    {@render children()}
  </div>
</div>

<style>
  .setting-section {
    container-type: inline-size;
  }

  .title-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-bottom: clamp(8px, 1cqi, 12px);
  }

  .section-title {
    font-size: clamp(20px, 2vw, 24px); /* Further increased for 2025 standards */
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.01em; /* Tighter tracking for modern look */
  }

  .help-button {
    position: relative;
    background: transparent;
    border: none;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color var(--transition-fast);
  }

  .help-button:hover,
  .help-button:focus {
    color: rgba(255, 255, 255, 0.9);
    outline: none;
  }

  .tooltip {
    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.95);
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
    line-height: 1.4;
    white-space: nowrap;
    max-width: 250px;
    white-space: normal;
    text-align: left;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    pointer-events: none;
    animation: fadeIn 0.2s ease-out;
  }

  .tooltip::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: rgba(0, 0, 0, 0.95);
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateX(-50%) translateY(-4px);
    }
    to {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }

  .section-description {
    color: rgba(255, 255, 255, 0.7);
    font-size: clamp(12px, 1.2vw, 16px);
    line-height: 1.4;
    text-align: center;
    margin: 0 0 clamp(16px, 2cqi, 24px) 0;
  }

  .setting-cards {
    display: flex;
    flex-direction: column;
    gap: clamp(8px, 1vw, 16px);
  }

  /* Container queries for setting cards layout */
  @container (min-width: 600px) {
    .setting-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: clamp(12px, 1.5vw, 24px);
    }
  }
</style>
