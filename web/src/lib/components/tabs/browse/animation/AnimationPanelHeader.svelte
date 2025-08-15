<!--
Animation Panel Header Component

Handles the panel header with collapse/expand and close functionality.
Shows minimal collapsed state or full header with controls.
-->
<script lang="ts">
  // Props
  const {
    isCollapsed = false,
    onToggle = () => {},
    onClose = () => {},
  } = $props<{
    isCollapsed?: boolean;
    onToggle?: () => void;
    onClose?: () => void;
  }>();
</script>

<div class="panel-header">
  {#if isCollapsed}
    <!-- Collapsed header - minimal with expand button -->
    <div class="collapsed-header">
      <button
        class="expand-button"
        onclick={onToggle}
        title="Expand animation panel"
        aria-label="Expand animation panel"
      >
        🎬
      </button>
    </div>
  {:else}
    <!-- Full header -->
    <div class="full-header">
      <h3>🎬 Animation</h3>
      <div class="panel-controls">
        <button
          class="toggle-button"
          onclick={onToggle}
          title="Collapse animation panel"
          aria-label="Collapse animation panel"
        >
          ▶
        </button>
        <button
          class="close-button"
          onclick={onClose}
          title="Close animation panel"
          aria-label="Close animation panel"
        >
          ✕
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  /* Panel Header */
  .panel-header {
    flex-shrink: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08) 0%,
      rgba(255, 255, 255, 0.04) 100%
    );
    backdrop-filter: blur(10px);
  }

  /* Collapsed Header */
  .collapsed-header {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem;
    height: 60px;
  }

  .expand-button {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 1.5rem;
    cursor: pointer;
    color: rgba(255, 255, 255, 0.8);
    padding: 0.75rem;
    border-radius: 12px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .expand-button:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(99, 102, 241, 0.3);
    color: #818cf8;
    transform: scale(1.05);
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);
  }

  /* Full Header */
  .full-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.25rem;
  }

  .full-header h3 {
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .panel-controls {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .toggle-button,
  .close-button {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 1.125rem;
    cursor: pointer;
    color: rgba(255, 255, 255, 0.7);
    padding: 0.5rem;
    border-radius: 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 36px;
    height: 36px;
  }

  .toggle-button:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(99, 102, 241, 0.3);
    color: #818cf8;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(239, 68, 68, 0.3);
    color: #f87171;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
  }

  /* Focus improvements for accessibility */
  .expand-button:focus-visible,
  .toggle-button:focus-visible,
  .close-button:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .expand-button,
    .toggle-button,
    .close-button {
      border: 2px solid currentColor;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .expand-button,
    .toggle-button,
    .close-button {
      transition: none;
    }
  }
</style>
