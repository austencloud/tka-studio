<script lang="ts">
  /**
   * Gamification Button Component
   *
   * Main entry point for the gamification system.
   * Shows current level, XP progress, and opens achievements panel.
   */

  import { onMount } from "svelte";
  import { resolve, TYPES } from "../../inversify";
  import type { IAchievementService } from "../services/contracts";
  import type { UserXP } from "../domain/models";
  import { getLevelProgress } from "../domain/constants/xp-constants";
  import { auth } from "../../auth/firebase";

  // Props
  let { onclick = () => {} }: { onclick?: () => void } = $props();

  // State
  let achievementService: IAchievementService | null = $state(null);
  let userXP: UserXP | null = $state(null);
  let isLoading = $state(true);
  let error = $state<string | null>(null);
  let isLoggedIn = $state(false);

  // Derived state for level progress
  let levelProgress = $derived.by(() => {
    if (!userXP) return null;
    return getLevelProgress(userXP.totalXP);
  });

  // Initialize
  onMount(() => {
    let interval: ReturnType<typeof setInterval> | null = null;
    let unsubscribe: (() => void) | null = null;

    (async () => {
      try {
        achievementService = await resolve<IAchievementService>(
          TYPES.IAchievementService
        );

        // Listen for auth state changes
        unsubscribe = auth.onAuthStateChanged((user) => {
          isLoggedIn = !!user;
          if (user) {
            loadUserXP();
          } else {
            userXP = null;
          }
        });

        isLoading = false;

        // Refresh XP every 30 seconds (only if logged in)
        interval = setInterval(() => {
          if (isLoggedIn) {
            loadUserXP();
          }
        }, 30000);
      } catch (err) {
        console.error("Failed to initialize GamificationButton:", err);
        error = "Failed to load";
        isLoading = false;
      }
    })();

    return () => {
      if (interval) clearInterval(interval);
      if (unsubscribe) unsubscribe();
    };
  });

  async function loadUserXP() {
    if (!achievementService || !isLoggedIn) return;
    try {
      userXP = await achievementService.getUserXP();
    } catch (err) {
      // Silently fail - user might not be logged in
      userXP = null;
    }
  }

  function handleClick() {
    onclick();
  }
</script>

{#if isLoggedIn || isLoading}
  <button
    class="gamification-button glass-surface"
    onclick={handleClick}
    title="View Achievements & Challenges"
  >
    {#if isLoading}
      <div class="loading-state">
        <div class="spinner"></div>
      </div>
    {:else if error}
      <div class="error-state">
        <span class="icon">⚠️</span>
      </div>
    {:else}
      <!-- Simple trophy icon - minimal design -->
      <i class="fas fa-trophy icon-minimal"></i>
      <!-- Optional: Small level badge for levels > 1 -->
      {#if levelProgress && levelProgress.currentLevel > 1}
        <span class="level-badge-minimal">{levelProgress.currentLevel}</span>
      {/if}
    {/if}
  </button>
{/if}

<style>
  .gamification-button {
    /* Match ProfileButton sizing - WCAG AAA minimum touch target */
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.1);
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
  }

  .gamification-button:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: scale(1.05);
  }

  .gamification-button:active {
    transform: scale(0.95);
  }

  /* Loading State */
  .loading-state,
  .error-state {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

  .spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-top-color: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Minimal icon styling */
  .icon-minimal {
    font-size: 20px;
    color: rgba(255, 255, 255, 0.9);
  }

  /* Small level badge - subtle notification style */
  .level-badge-minimal {
    position: absolute;
    top: -2px;
    right: -2px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 9px;
    font-weight: 700;
    color: white;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
    z-index: 2;
  }

  /* Accessibility */
  .gamification-button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .gamification-button,
    .spinner {
      animation: none;
      transition: none;
    }

    .gamification-button:hover,
    .gamification-button:active {
      transform: none;
    }
  }

  /* High Contrast */
  @media (prefers-contrast: high) {
    .gamification-button {
      background: rgba(255, 255, 255, 0.2);
      border: 2px solid white;
    }
  }
</style>
