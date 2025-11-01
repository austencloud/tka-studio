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

  // Props
  let { onclick = () => {} }: { onclick?: () => void } = $props();

  // State
  let achievementService: IAchievementService | null = $state(null);
  let userXP: UserXP | null = $state(null);
  let isLoading = $state(true);
  let error = $state<string | null>(null);

  // Derived state for level progress
  let levelProgress = $derived.by(() => {
    if (!userXP) return null;
    return getLevelProgress(userXP.totalXP);
  });

  // Initialize
  onMount(async () => {
    try {
      achievementService = await resolve<IAchievementService>(
        TYPES.IAchievementService
      );
      await loadUserXP();
      isLoading = false;

      // Refresh XP every 30 seconds
      const interval = setInterval(loadUserXP, 30000);
      return () => clearInterval(interval);
    } catch (err) {
      console.error("Failed to initialize GamificationButton:", err);
      error = "Failed to load";
      isLoading = false;
    }
  });

  async function loadUserXP() {
    if (!achievementService) return;
    try {
      userXP = await achievementService.getUserXP();
    } catch (err) {
      console.error("Failed to load user XP:", err);
    }
  }

  function handleClick() {
    onclick();
  }
</script>

<button class="gamification-button glass-surface" onclick={handleClick} title="View Achievements & Challenges">
  {#if isLoading}
    <div class="loading-state">
      <div class="spinner"></div>
    </div>
  {:else if error}
    <div class="error-state">
      <span class="icon">⚠️</span>
    </div>
  {:else if levelProgress}
    <div class="button-content">
      <!-- Level Badge -->
      <div class="level-badge">
        <span class="level-number">{levelProgress.currentLevel}</span>
      </div>

      <!-- XP Progress Ring -->
      <div class="progress-ring">
        <svg class="ring-svg" width="48" height="48" viewBox="0 0 48 48">
          <!-- Background ring -->
          <circle
            cx="24"
            cy="24"
            r="20"
            fill="none"
            stroke="rgba(255, 255, 255, 0.1)"
            stroke-width="3"
          />
          <!-- Progress ring -->
          <circle
            cx="24"
            cy="24"
            r="20"
            fill="none"
            stroke="url(#xp-gradient)"
            stroke-width="3"
            stroke-linecap="round"
            stroke-dasharray="{(levelProgress.progress / 100) * 125.6} 125.6"
            transform="rotate(-90 24 24)"
            class="progress-circle"
          />
          <!-- Gradient definition -->
          <defs>
            <linearGradient id="xp-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
            </linearGradient>
          </defs>
        </svg>

        <!-- Center icon -->
        <div class="center-icon">
          <span class="trophy-icon">🏆</span>
        </div>
      </div>

      <!-- XP Info (optional, for non-mobile) -->
      <div class="xp-info">
        <div class="xp-text">Level {levelProgress.currentLevel}</div>
        <div class="xp-subtext">{levelProgress.progress}%</div>
      </div>
    </div>
  {/if}
</button>

<style>
  .gamification-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-lg);
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    min-width: 56px;
    height: 56px;
  }

  .gamification-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  .gamification-button:active {
    transform: translateY(0);
  }

  /* Loading State */
  .loading-state,
  .error-state {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
  }

  .spinner {
    width: 24px;
    height: 24px;
    border: 3px solid rgba(255, 255, 255, 0.2);
    border-top-color: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Button Content */
  .button-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    position: relative;
  }

  /* Level Badge */
  .level-badge {
    position: absolute;
    top: -4px;
    left: -4px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    z-index: 2;
  }

  .level-number {
    font-size: 11px;
    font-weight: 700;
    color: white;
  }

  /* Progress Ring */
  .progress-ring {
    position: relative;
    width: 48px;
    height: 48px;
  }

  .ring-svg {
    transform: scale(1);
    filter: drop-shadow(0 2px 4px rgba(102, 126, 234, 0.3));
  }

  .progress-circle {
    transition: stroke-dasharray 0.5s ease;
  }

  .center-icon {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 20px;
    animation: float 3s ease-in-out infinite;
  }

  @keyframes float {
    0%,
    100% {
      transform: translate(-50%, -50%) translateY(0);
    }
    50% {
      transform: translate(-50%, -50%) translateY(-3px);
    }
  }

  .trophy-icon {
    filter: drop-shadow(0 0 4px rgba(255, 215, 0, 0.5));
  }

  /* XP Info */
  .xp-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding-left: var(--spacing-xs);
  }

  .xp-text {
    font-size: 14px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    line-height: 1;
  }

  .xp-subtext {
    font-size: 11px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .xp-info {
      display: none;
    }

    .gamification-button {
      min-width: 56px;
      padding: var(--spacing-xs);
    }
  }

  /* Accessibility */
  .gamification-button:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .gamification-button,
    .progress-circle,
    .spinner,
    .center-icon {
      animation: none;
      transition: none;
    }

    .gamification-button:hover {
      transform: none;
    }
  }
</style>
