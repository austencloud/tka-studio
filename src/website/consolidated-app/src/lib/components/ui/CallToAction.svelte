<script lang="ts">
  interface Props {
    text: string;
    link: string;
    primary?: boolean;
  }

  let { text, link, primary = true }: Props = $props();
</script>

<a
  href={link}
  target="_blank"
  rel="noopener noreferrer"
  class="cta-button"
  class:primary
  class:secondary={!primary}
  aria-label="{text} (opens in new tab)"
>
  <span class="button-content">
    <span class="button-text">{text}</span>
    <span class="button-icon" aria-hidden="true">→</span>
  </span>

  <!-- Glassmorphism overlay -->
  <div class="glass-overlay" aria-hidden="true"></div>
</a>

<style>
  /*
   * Enhanced Call-to-Action with Glassmorphism and Micro-interactions
   *
   * Features:
   * - Glassmorphism effects with backdrop-blur
   * - Loading states with spinner animation
   * - Enhanced hover effects and micro-interactions
   * - Accessibility-compliant design
   * - Reduced motion support
   */

  .cta-button {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-md) var(--spacing-xl);
    border-radius: var(--border-radius-lg);
    text-decoration: none;
    text-align: center;
    font-weight: 600;
    font-size: var(--font-size-base);
    min-width: 220px;
    margin: var(--spacing-xs);
    overflow: hidden;

    /* Enhanced transitions */
    transition: all var(--transition-normal);
    will-change: transform, box-shadow, background-color;

    /* Prevent text selection during interactions */
    user-select: none;
    -webkit-user-select: none;
  }

  .button-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
    position: relative;
    z-index: 1;
    transition: transform var(--transition-fast);
  }

  .button-icon {
    font-size: 1.2em;
    transition: transform var(--transition-fast);
  }

  .cta-button:hover .button-icon {
    transform: translateX(4px);
  }

  /* Primary button with advanced glassmorphism */
  .cta-button.primary {
    background: var(--gradient-primary);
    color: var(--text-inverse);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: var(--shadow-glass-colored);
  }

  .cta-button.primary:hover {
    transform: translateY(-4px) scale(1.03);
    border-color: rgba(255, 255, 255, 0.4);
    box-shadow:
      0 20px 40px var(--shadow-colored),
      0 8px 20px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.4);
    text-decoration: none;
    filter: brightness(1.1);
  }

  .cta-button.primary:active {
    transform: translateY(-2px) scale(1.02);
  }

  /* Secondary button with advanced glassmorphism */
  .cta-button.secondary {
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    color: var(--text-color);
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);
  }

  .cta-button.secondary:hover {
    background: var(--surface-hover);
    color: var(--primary-light);
    border: var(--glass-border-hover);
    transform: translateY(-3px) scale(1.02);
    box-shadow: var(--shadow-glass-hover);
    text-decoration: none;
    text-shadow: 0 2px 8px var(--shadow-colored);
  }

  .cta-button.secondary:active {
    transform: translateY(-1px) scale(1.01);
  }

  /* Glassmorphism overlay for enhanced depth */
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
    transition: opacity var(--transition-fast);
  }

  .cta-button:hover .glass-overlay {
    opacity: 1;
  }



  /* Focus styles for accessibility */
  .cta-button:focus-visible {
    outline: 3px solid var(--primary-color);
    outline-offset: 3px;
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .cta-button,
    .button-content,
    .button-icon,
    .glass-overlay {
      transition: none;
      animation: none;
    }

    .cta-button:hover {
      transform: none;
    }

    .cta-button:hover .button-icon {
      transform: none;
    }
  }

  /* Mobile responsive design */
  @media (max-width: 768px) {
    .cta-button {
      min-width: 100%;
      margin: var(--spacing-xs) 0;
      padding: var(--spacing-md) var(--spacing-lg);
      font-size: var(--font-size-sm);
    }

    .button-content {
      gap: var(--spacing-xs);
    }

    .button-icon {
      font-size: 1em;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .cta-button.primary {
      border: 2px solid white;
      background: var(--primary-color);
    }

    .cta-button.secondary {
      border: 2px solid var(--primary-color);
      background: white;
    }
  }
</style>
