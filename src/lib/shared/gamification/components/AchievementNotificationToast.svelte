<script lang="ts">
  /**
   * Achievement Notification Toast
   *
   * Displays toast notifications for achievement unlocks, level-ups, etc.
   * Automatically appears and disappears with smooth animations.
   */

  import { onMount } from "svelte";
  import { notificationQueue, removeNotification } from "../state/notification-state.svelte";
  import type { AchievementNotification } from "../domain/models";

  // State
  let activeNotification = $state<AchievementNotification | null>(null);
  let isVisible = $state(false);
  let timeout: ReturnType<typeof setTimeout> | null = null;

  // Watch notification queue
  $effect(() => {
    if (notificationQueue.length > 0 && !activeNotification) {
      showNextNotification();
    }
  });

  function showNextNotification() {
    if (notificationQueue.length === 0) return;

    // Get next notification
    const notification = removeNotification();
    if (!notification) return;

    activeNotification = notification;
    isVisible = true;

    // Auto-hide after 5 seconds
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => {
      hideNotification();
    }, 5000);
  }

  function hideNotification() {
    isVisible = false;

    // Wait for animation to complete before clearing
    setTimeout(() => {
      activeNotification = null;
      // Show next notification if any
      if (notificationQueue.length > 0) {
        setTimeout(showNextNotification, 300);
      }
    }, 300);
  }

  function handleClick() {
    hideNotification();
  }

  onMount(() => {
    return () => {
      if (timeout) clearTimeout(timeout);
    };
  });
</script>

{#if activeNotification}
  <div class="toast-container" class:visible={isVisible}>
    <div
      class="toast glass-surface {activeNotification.type}"
      onclick={handleClick}
      role="alert"
      aria-live="polite"
    >
      <div class="toast-icon">
        {activeNotification.icon || "🎉"}
      </div>
      <div class="toast-content">
        <div class="toast-title">{activeNotification.title}</div>
        <div class="toast-message">{activeNotification.message}</div>
      </div>
      <button class="toast-close" onclick={hideNotification} aria-label="Dismiss">×</button>
    </div>
  </div>
{/if}

<style>
  .toast-container {
    position: fixed;
    top: 80px;
    left: 50%;
    transform: translateX(-50%) translateY(-120%);
    z-index: 2000;
    transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    pointer-events: none;
  }

  .toast-container.visible {
    transform: translateX(-50%) translateY(0);
    pointer-events: auto;
  }

  .toast {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-md) var(--spacing-lg);
    border-radius: var(--radius-xl);
    min-width: 320px;
    max-width: 480px;
    cursor: pointer;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.2);
    animation: glow 2s ease-in-out infinite alternate;
  }

  @keyframes glow {
    from {
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 20px rgba(102, 126, 234, 0.3);
    }
    to {
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 40px rgba(102, 126, 234, 0.5);
    }
  }

  .toast.achievement {
    border-color: rgba(255, 215, 0, 0.5);
  }

  .toast.level_up {
    border-color: rgba(102, 126, 234, 0.5);
  }

  .toast.challenge_complete {
    border-color: rgba(76, 175, 80, 0.5);
  }

  .toast.streak_milestone {
    border-color: rgba(255, 87, 34, 0.5);
  }

  .toast-icon {
    font-size: 40px;
    flex-shrink: 0;
    animation: bounce 1s ease-in-out;
  }

  @keyframes bounce {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.2);
    }
  }

  .toast-content {
    flex: 1;
    min-width: 0;
  }

  .toast-title {
    font-size: 16px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    margin-bottom: 4px;
  }

  .toast-message {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.4;
  }

  .toast-close {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.7);
    font-size: 20px;
    line-height: 1;
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.2s ease;
  }

  .toast-close:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: rotate(90deg);
  }

  /* Mobile */
  @media (max-width: 768px) {
    .toast-container {
      top: 70px;
      left: var(--spacing-md);
      right: var(--spacing-md);
      transform: translateX(0) translateY(-120%);
    }

    .toast-container.visible {
      transform: translateX(0) translateY(0);
    }

    .toast {
      min-width: auto;
      width: 100%;
    }
  }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .toast-container,
    .toast-icon,
    .toast-close {
      animation: none;
      transition: opacity 0.2s ease;
    }

    .toast-container:not(.visible) {
      opacity: 0;
    }

    .toast-container.visible {
      opacity: 1;
    }
  }
</style>
