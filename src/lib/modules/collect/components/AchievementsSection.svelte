<!--
  AchievementsSection.svelte - Achievements summary in Collection module

  Displays:
  - Compact stats (Level, XP, Achievements count, Streak)
  - Recent 3 achievements
  - "View All" button that opens AchievementsBrowser panel
-->
<script lang="ts">
  import { onMount } from "svelte";
  import { resolve, TYPES } from "$shared/inversify";
  import { authStore } from "$shared/auth";
  import { getLevelProgress } from "$shared/gamification/domain/constants/xp-constants";
  import type {
    IAchievementService,
    IStreakService,
  } from "$shared/gamification/services/contracts";
  import AchievementsBrowser from "$shared/gamification/components/AchievementsBrowser.svelte";

  // Services
  let achievementService: IAchievementService | null = $state(null);
  let streakService: IStreakService | null = $state(null);

  // State
  let stats = $state<any>(null);
  let recentAchievements = $state<any[]>([]);
  let currentStreak = $state(0);
  let isLoading = $state(true);
  let isBrowserOpen = $state(false);

  // Container-aware sizing
  let sectionElement: HTMLElement | null = $state(null);
  let containerWidth = $state(0);
  let isCompact = $derived(containerWidth < 500);

  // Track dimensions
  $effect(() => {
    if (!sectionElement) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        containerWidth = entry.contentRect.width;
      }
    });

    resizeObserver.observe(sectionElement);
    return () => resizeObserver.disconnect();
  });

  // Initialize services
  onMount(async () => {
    try {
      achievementService = await resolve<IAchievementService>(
        TYPES.IAchievementService
      );
      streakService = await resolve<IStreakService>(TYPES.IStreakService);
      await loadData();
    } catch (err) {
      console.error("Failed to initialize AchievementsSection:", err);
      isLoading = false;
    }
  });

  async function loadData() {
    if (!achievementService || !streakService || !authStore.isAuthenticated) {
      isLoading = false;
      return;
    }

    try {
      isLoading = true;
      const [statsData, achievementsData, streakData] = await Promise.all([
        achievementService.getStats(),
        achievementService.getAllAchievements(),
        streakService.getCurrentStreak(),
      ]);

      stats = statsData;
      currentStreak = streakData.currentStreak;

      // Get recent 3 completed achievements
      recentAchievements = achievementsData
        .filter((a) => a.userProgress?.isCompleted)
        .sort(
          (a, b) =>
            (b.userProgress?.unlockedAt?.getTime() || 0) -
            (a.userProgress?.unlockedAt?.getTime() || 0)
        )
        .slice(0, 3);
    } catch (err) {
      console.error("Failed to load achievements data:", err);
    } finally {
      isLoading = false;
    }
  }

  function openBrowser() {
    isBrowserOpen = true;
  }

  function closeBrowser() {
    isBrowserOpen = false;
  }
</script>

<div class="achievements-section" bind:this={sectionElement}>
  {#if isLoading}
    <div class="loading-container">
      <div class="spinner"></div>
      <p>Loading your progress...</p>
    </div>
  {:else if !authStore.isAuthenticated}
    <div class="auth-required">
      <i class="fas fa-lock"></i>
      <h3>Sign In Required</h3>
      <p>Sign in to track your achievements and progress</p>
    </div>
  {:else}
    <!-- Stats Grid -->
    <div class="stats-grid" class:compact={isCompact}>
      <div class="stat-card glass-surface">
        <div class="stat-icon"><i class="fas fa-star"></i></div>
        <div class="stat-content">
          <div class="stat-value">{stats?.currentLevel || 0}</div>
          <div class="stat-label">Level</div>
        </div>
      </div>

      <div class="stat-card glass-surface">
        <div class="stat-icon"><i class="fas fa-sparkles"></i></div>
        <div class="stat-content">
          <div class="stat-value">{stats?.totalXP.toLocaleString() || 0}</div>
          <div class="stat-label">Total XP</div>
        </div>
      </div>

      <div class="stat-card glass-surface">
        <div class="stat-icon"><i class="fas fa-trophy"></i></div>
        <div class="stat-content">
          <div class="stat-value">
            {stats?.achievementsUnlocked || 0}/{stats?.totalAchievements || 0}
          </div>
          <div class="stat-label">Achievements</div>
        </div>
      </div>

      <div class="stat-card glass-surface">
        <div class="stat-icon"><i class="fas fa-fire"></i></div>
        <div class="stat-content">
          <div class="stat-value">{currentStreak}</div>
          <div class="stat-label">Day Streak</div>
        </div>
      </div>
    </div>

    <!-- Recent Achievements -->
    <div class="recent-section">
      <div class="section-header">
        <h3><i class="fas fa-trophy"></i> Recent Achievements</h3>
        <button class="view-all-button" onclick={openBrowser}>
          View All <i class="fas fa-arrow-right"></i>
        </button>
      </div>

      {#if recentAchievements.length === 0}
        <div class="empty-state">
          <i class="fas fa-trophy"></i>
          <p>No achievements unlocked yet</p>
          <p class="hint">
            Complete challenges to earn your first achievement!
          </p>
        </div>
      {:else}
        <div class="achievements-grid">
          {#each recentAchievements as achievement}
            <div class="achievement-item glass-surface">
              <div class="achievement-icon">
                <i class="fas {achievement.icon}"></i>
              </div>
              <div class="achievement-info">
                <h4>{achievement.title}</h4>
                <p>{achievement.description}</p>
                <span class="achievement-xp">+{achievement.xpReward} XP</span>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</div>

<!-- Full Achievements Browser Panel -->
<AchievementsBrowser isOpen={isBrowserOpen} onClose={closeBrowser} />

<style>
  .achievements-section {
    container-type: inline-size;
    container-name: achievements-section;
    display: flex;
    flex-direction: column;
    gap: clamp(16px, 4cqi, 24px);
    padding: clamp(16px, 4cqi, 24px);
    height: 100%;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
  }

  .achievements-section::-webkit-scrollbar {
    width: 8px;
  }

  .achievements-section::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
  }

  /* Loading & Empty States */
  .loading-container,
  .auth-required,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: clamp(24px, 6cqi, 48px);
    text-align: center;
    gap: clamp(12px, 3cqi, 16px);
  }

  .spinner {
    width: 48px;
    height: 48px;
    border: 4px solid rgba(255, 255, 255, 0.2);
    border-top-color: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .auth-required i,
  .empty-state i {
    font-size: clamp(32px, 8cqi, 48px);
    opacity: 0.5;
  }

  /* Stats Grid */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(
      auto-fit,
      minmax(clamp(140px, 30cqi, 200px), 1fr)
    );
    gap: clamp(12px, 3cqi, 16px);
  }

  @container achievements-section (max-width: 600px) {
    .stats-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @container achievements-section (max-width: 350px) {
    .stats-grid {
      grid-template-columns: 1fr;
    }
  }

  .stat-card {
    display: flex;
    align-items: center;
    gap: clamp(8px, 2cqi, 12px);
    padding: clamp(12px, 3cqi, 16px);
    border-radius: clamp(12px, 3cqi, 16px);
  }

  .stat-icon {
    font-size: clamp(24px, 6cqi, 32px);
    flex-shrink: 0;
  }

  .stat-content {
    flex: 1;
    min-width: 0;
  }

  .stat-value {
    font-size: clamp(18px, 4.5cqi, 24px);
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    line-height: 1.2;
  }

  .stat-label {
    font-size: clamp(10px, 2.5cqi, 12px);
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 2px;
  }

  /* Recent Achievements Section */
  .recent-section {
    display: flex;
    flex-direction: column;
    gap: clamp(12px, 3cqi, 16px);
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: clamp(8px, 2cqi, 12px);
    flex-wrap: wrap;
  }

  .section-header h3 {
    font-size: clamp(16px, 4cqi, 20px);
    font-weight: 600;
    margin: 0;
    display: flex;
    align-items: center;
    gap: clamp(6px, 1.5cqi, 8px);
  }

  .view-all-button {
    padding: clamp(8px, 2cqi, 10px) clamp(12px, 3cqi, 16px);
    border-radius: clamp(8px, 2cqi, 10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.9);
    font-size: clamp(12px, 3cqi, 14px);
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition-fast);
    display: flex;
    align-items: center;
    gap: clamp(6px, 1.5cqi, 8px);
  }

  .view-all-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }

  .view-all-button:focus-visible {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
  }

  /* Achievements Grid */
  .achievements-grid {
    display: flex;
    flex-direction: column;
    gap: clamp(10px, 2.5cqi, 12px);
  }

  .achievement-item {
    display: flex;
    gap: clamp(12px, 3cqi, 16px);
    padding: clamp(12px, 3cqi, 16px);
    border-radius: clamp(12px, 3cqi, 16px);
    border: 1px solid rgba(76, 175, 80, 0.3);
  }

  .achievement-icon {
    font-size: clamp(28px, 7cqi, 36px);
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(48px, 12cqi, 60px);
    height: clamp(48px, 12cqi, 60px);
  }

  .achievement-info {
    flex: 1;
    min-width: 0;
  }

  .achievement-info h4 {
    font-size: clamp(14px, 3.5cqi, 16px);
    font-weight: 600;
    margin: 0 0 clamp(4px, 1cqi, 6px);
    color: rgba(255, 255, 255, 0.95);
  }

  .achievement-info p {
    font-size: clamp(12px, 3cqi, 14px);
    color: rgba(255, 255, 255, 0.7);
    margin: 0 0 clamp(6px, 1.5cqi, 8px);
    line-height: 1.4;
  }

  .achievement-xp {
    font-size: clamp(11px, 2.8cqi, 13px);
    font-weight: 600;
    color: #ffd700;
  }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }

    .spinner {
      animation: none;
    }
  }
</style>
