<script lang="ts">
  interface Props {
    text: string;
    link?: string;
    onclick?: () => void | Promise<void>;
    primary?: boolean;
    internal?: boolean;
    disabled?: boolean;
    loading?: boolean;
    onsuccess?: () => void;
    onerror?: (error: any) => void;
    onclicked?: () => void;
  }

  let { 
    text, 
    link, 
    onclick,
    primary = true,
    internal = false,
    disabled = false,
    loading = false,
    onsuccess,
    onerror,
    onclicked
  }: Props = $props();

  async function handleClick(event: MouseEvent) {
    if (disabled || loading) {
      event.preventDefault();
      return;
    }

    // If it's an internal action (like entering app mode)
    if (internal && onclick) {
      event.preventDefault();
      loading = true;
      try {
        await onclick();
        onsuccess?.();
      } catch (error) {
        console.error('Action failed:', error);
        onerror?.(error);
      } finally {
        loading = false;
      }
      return;
    }

    // External link - let browser handle naturally
    if (link && !internal) {
      onclicked?.();
      return;
    }

    // Custom click handler
    if (onclick) {
      event.preventDefault();
      await onclick();
      onclicked?.();
    }
  }
</script>

{#if link && !internal}
  <!-- External link -->
  <a
    href={link}
    target="_blank"
    rel="noopener noreferrer"
    class="cta-button"
    class:primary
    class:secondary={!primary}
    class:disabled
    class:loading
    onclick={handleClick}
    aria-label="{text} (opens in new tab)"
  >
    <span class="button-content">
      <span class="button-text">{text}</span>
      {#if loading}
        <span class="button-spinner" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M12,2 A10,10 0 0,1 22,12" stroke="currentColor" stroke-width="2" fill="none">
              <animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
            </path>
          </svg>
        </span>
      {:else}
        <span class="button-icon" aria-hidden="true">→</span>
      {/if}
    </span>
    <div class="glass-overlay" aria-hidden="true"></div>
  </a>
{:else}
  <!-- Internal button -->
  <button
    type="button"
    class="cta-button"
    class:primary
    class:secondary={!primary}
    class:disabled
    class:loading
    onclick={handleClick}
    {disabled}
    aria-label={text}
  >
    <span class="button-content">
      <span class="button-text">{text}</span>
      {#if loading}
        <span class="button-spinner" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M12,2 A10,10 0 0,1 22,12" stroke="currentColor" stroke-width="2" fill="none">
              <animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
            </path>
          </svg>
        </span>
      {:else if internal}
        <span class="button-icon" aria-hidden="true">⚡</span>
      {:else}
        <span class="button-icon" aria-hidden="true">→</span>
      {/if}
    </span>
    <div class="glass-overlay" aria-hidden="true"></div>
  </button>
{/if}

<style>
  .cta-button {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-md) var(--spacing-xl);
    border: none;
    border-radius: var(--border-radius-lg);
    text-decoration: none;
    text-align: center;
    font-weight: 600;
    font-size: var(--font-size-base);
    font-family: inherit;
    min-width: 220px;
    margin: var(--spacing-xs);
    overflow: hidden;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
    will-change: transform, box-shadow, background-color;
  }

  .button-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
    position: relative;
    z-index: 1;
    transition: transform 0.2s ease;
  }

  .button-text {
    transition: opacity 0.2s ease;
  }

  .button-icon {
    font-size: 1.2em;
    transition: transform 0.2s ease;
  }

  .button-spinner {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  /* Primary button styling */
  .cta-button.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 
      0 8px 32px rgba(118, 75, 162, 0.3),
      0 4px 16px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .cta-button.primary:hover:not(.disabled):not(.loading) {
    transform: translateY(-4px) scale(1.03);
    border-color: rgba(255, 255, 255, 0.4);
    box-shadow:
      0 20px 40px rgba(118, 75, 162, 0.4),
      0 8px 20px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.4);
    filter: brightness(1.05);
  }

  .cta-button.primary:hover:not(.disabled):not(.loading) .button-icon {
    transform: translateX(4px);
  }

  .cta-button.primary:active:not(.disabled):not(.loading) {
    transform: translateY(-2px) scale(1.02);
  }

  /* Secondary button styling */
  .cta-button.secondary {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: var(--text-color, white);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .cta-button.secondary:hover:not(.disabled):not(.loading) {
    background: rgba(255, 255, 255, 0.1);
    color: #667eea;
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-3px) scale(1.02);
    box-shadow: 
      0 16px 32px rgba(0, 0, 0, 0.15),
      0 6px 16px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
    text-shadow: 0 2px 8px rgba(118, 75, 162, 0.3);
  }

  .cta-button.secondary:hover:not(.disabled):not(.loading) .button-icon {
    transform: translateX(3px);
  }

  .cta-button.secondary:active:not(.disabled):not(.loading) {
    transform: translateY(-1px) scale(1.01);
  }

  /* Glassmorphism overlay */
  .glass-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.05) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    opacity: 0;
    transition: opacity 0.2s ease;
    border-radius: inherit;
  }

  .cta-button:hover:not(.disabled):not(.loading) .glass-overlay {
    opacity: 1;
  }

  /* Disabled state */
  .cta-button.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
  }

  .cta-button.disabled .button-text {
    opacity: 0.7;
  }

  /* Loading state */
  .cta-button.loading {
    cursor: wait;
  }

  .cta-button.loading .button-text {
    opacity: 0.7;
  }

  /* Focus styles for accessibility */
  .cta-button:focus-visible {
    outline: 3px solid #667eea;
    outline-offset: 3px;
  }

  /* Mobile responsive design */
  @media (max-width: 768px) {
    .cta-button {
      width: 100%;
      max-width: 300px;
      margin: var(--spacing-xs) 0;
      padding: var(--spacing-md) var(--spacing-lg);
      font-size: var(--font-size-sm);
      min-width: unset;
    }

    .button-content {
      gap: var(--spacing-xs);
    }

    .button-icon {
      font-size: 1em;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .cta-button,
    .button-content,
    .button-icon,
    .glass-overlay {
      transition: none;
    }

    .cta-button:hover {
      transform: none;
    }

    .cta-button:hover .button-icon {
      transform: none;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .cta-button.primary {
      border: 2px solid white;
      background: #4f46e5;
    }

    .cta-button.secondary {
      border: 2px solid #4f46e5;
      background: rgba(255, 255, 255, 0.9);
      color: #4f46e5;
    }
  }
</style>
