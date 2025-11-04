<!--
  AchievementsTab.svelte - Achievements & Progress

  Displays gamification achievements inline within profile settings.
-->
<script lang="ts">
  import { onMount } from "svelte";
  import { resolve, TYPES } from "$shared/inversify";
  import type { IAchievementService } from "$shared/gamification/services/contracts";
  import type {
    Achievement,
    UserXP,
    UserAchievement,
  } from "$shared/gamification/domain/models";
  import { auth } from "$shared/auth";
  import { getLevelProgress } from "$shared/gamification/domain/constants/xp-constants";

  type AchievementWithProgress = Achievement & {
    userProgress: UserAchievement | null;
  };

  // Services
  let achievementService: IAchievementService | null = $state(null);

  // State
  let userXP: UserXP | null = $state(null);
  let achievements: AchievementWithProgress[] = $state([]);
  let unlockedAchievements: AchievementWithProgress[] = $state([]);
  let lockedAchievements: AchievementWithProgress[] = $state([]);
  let loading = $state(true);
  let error = $state<string | null>(null);
  let isLoggedIn = $state(false);

  // Derived state
  let levelProgress = $derived.by(() => {
    if (!userXP) return null;
    return getLevelProgress(userXP.totalXP);
  });

  onMount(() => {
    const initAsync = async (): Promise<(() => void) | undefined> => {
      try {
        achievementService = await resolve<IAchievementService>(
          TYPES.IAchievementService
        );

        // Listen for auth state
        const unsubscribe = auth.onAuthStateChanged(async (user) => {
          isLoggedIn = !!user;
          if (user) {
            await loadData();
          } else {
            userXP = null;
            achievements = [];
            unlockedAchievements = [];
            lockedAchievements = [];
          }
        });

        return () => {
          unsubscribe();
        };
      } catch (err) {
        console.error("Failed to initialize AchievementsTab:", err);
        error = "Failed to load achievements";
        loading = false;
        return undefined;
      }
    };

    const cleanup = initAsync();
    return () => {
      cleanup.then((fn) => fn?.());
    };
  });

  async function loadData() {
    if (!achievementService || !isLoggedIn) return;

    loading = true;
    error = null;

    try {
      // Load user XP and achievements
      const [xpData, achievementsData] = await Promise.all([
        achievementService.getUserXP(),
        achievementService.getAllAchievements(),
      ]);

      userXP = xpData;
      achievements = achievementsData;

      // Separate unlocked and locked achievements
      unlockedAchievements = achievements.filter(
        (a) => a.userProgress?.isCompleted && a.userProgress?.unlockedAt
      );
      lockedAchievements = achievements.filter(
        (a) => !a.userProgress?.isCompleted
      );

      // Sort unlocked by date (newest first)
      unlockedAchievements.sort((a, b) => {
        const dateA = a.userProgress?.unlockedAt
          ? new Date(a.userProgress.unlockedAt).getTime()
          : 0;
        const dateB = b.userProgress?.unlockedAt
          ? new Date(b.userProgress.unlockedAt).getTime()
          : 0;
        return dateB - dateA;
      });

      // Sort locked by XP reward (highest first)
      lockedAchievements.sort((a, b) => b.xpReward - a.xpReward);
    } catch (err) {
      console.error("Failed to load achievements data:", err);
      error = "Failed to load achievements";
    } finally {
      loading = false;
    }
  }

  function formatDate(dateInput: Date | string): string {
    const date =
      typeof dateInput === "string" ? new Date(dateInput) : dateInput;
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return date.toLocaleDateString();
  }
</script>

{#if !isLoggedIn}
  <div class="achievements-tab">
    <div class="empty-state">
      <i class="fas fa-sign-in-alt"></i>
      <p>Sign in to view your achievements and progress</p>
    </div>
  </div>
{:else if loading}
  <div class="achievements-tab">
    <div class="loading-state">
      <div class="spinner"></div>
      <p>Loading achievements...</p>
    </div>
  </div>
{:else if error}
  <div class="achievements-tab">
    <div class="error-state">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{error}</p>
      <button class="retry-button" onclick={loadData}>Retry</button>
    </div>
  </div>
{:else}
  <div class="achievements-tab">
    <!-- Level Progress -->
    {#if levelProgress}
      <div class="level-section">
        <div class="level-header">
          <div class="level-badge">
            <i class="fas fa-star"></i>
            <span class="level-number">{levelProgress.currentLevel}</span>
          </div>
          <div class="level-info">
            <h3>Level {levelProgress.currentLevel}</h3>
            <p>{userXP?.totalXP.toLocaleString()} XP Total</p>
          </div>
        </div>
        <div class="level-progress">
          <div class="progress-bar">
            <div
              class="progress-fill"
              style="width: {levelProgress.progress}%"
            ></div>
          </div>
          <p class="progress-text">
            {levelProgress.xpIntoCurrentLevel.toLocaleString()} / {levelProgress.xpRequiredForLevel.toLocaleString()}
            XP
          </p>
        </div>
      </div>
    {/if}

    <!-- Unlocked Achievements -->
    {#if unlockedAchievements.length > 0}
      <div class="section">
        <h3>
          <i class="fas fa-trophy"></i>
          Unlocked ({unlockedAchievements.length})
        </h3>
        <div class="achievements-grid">
          {#each unlockedAchievements as achievement}
            <div class="achievement unlocked">
              <div class="achievement-icon">{achievement.icon}</div>
              <div class="achievement-content">
                <h4>{achievement.title}</h4>
                <p>{achievement.description}</p>
                {#if achievement.userProgress?.unlockedAt}
                  <span class="date">
                    Unlocked {formatDate(achievement.userProgress.unlockedAt)}
                  </span>
                {/if}
              </div>
              <div class="achievement-xp">+{achievement.xpReward} XP</div>
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Locked Achievements -->
    {#if lockedAchievements.length > 0}
      <div class="section">
        <h3>
          <i class="fas fa-lock"></i>
          Locked ({lockedAchievements.length})
        </h3>
        <div class="achievements-grid">
          {#each lockedAchievements as achievement}
            <div class="achievement locked">
              <div class="achievement-icon">{achievement.icon}</div>
              <div class="achievement-content">
                <h4>{achievement.title}</h4>
                <p>{achievement.description}</p>
              </div>
              <div class="achievement-xp">+{achievement.xpReward} XP</div>
            </div>
          {/each}
        </div>
      </div>
    {/if}

    {#if achievements.length === 0}
      <div class="empty-state">
        <i class="fas fa-trophy"></i>
        <p>No achievements yet. Keep using the app to unlock achievements!</p>
      </div>
    {/if}
  </div>
{/if}

<style>
  .achievements-tab {
    padding: 20px;
    max-width: 800px;
  }

  /* Loading, Error, Empty States */
  .loading-state,
  .error-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    text-align: center;
  }

  .error-state i,
  .empty-state i {
    font-size: 48px;
    color: rgba(255, 255, 255, 0.3);
    margin-bottom: 16px;
  }

  .loading-state p,
  .error-state p,
  .empty-state p {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.6);
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-top-color: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 16px;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .retry-button {
    margin-top: 16px;
    padding: 10px 20px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .retry-button:hover {
    background: rgba(255, 255, 255, 0.15);
  }

  /* Level Section */
  .level-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 32px;
  }

  .level-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
  }

  .level-badge {
    width: 64px;
    height: 64px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .level-badge i {
    font-size: 20px;
    color: white;
    margin-bottom: 4px;
  }

  .level-number {
    font-size: 18px;
    font-weight: 700;
    color: white;
  }

  .level-info h3 {
    margin: 0 0 4px 0;
    font-size: 24px;
    font-weight: 700;
    color: white;
  }

  .level-info p {
    margin: 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
  }

  .level-progress {
    margin-top: 16px;
  }

  .progress-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: white;
    transition: width 0.3s ease;
  }

  .progress-text {
    margin: 8px 0 0 0;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.9);
    text-align: center;
  }

  /* Sections */
  .section {
    margin-bottom: 32px;
  }

  .section h3 {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin-bottom: 16px;
  }

  .section h3 i {
    font-size: 16px;
  }

  /* Achievements Grid */
  .achievements-grid {
    display: grid;
    gap: 12px;
  }

  .achievement {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    transition: all 0.2s ease;
  }

  .achievement.unlocked {
    background: rgba(16, 185, 129, 0.1);
    border-color: rgba(16, 185, 129, 0.3);
  }

  .achievement.locked {
    opacity: 0.6;
  }

  .achievement-icon {
    font-size: 32px;
    flex-shrink: 0;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .achievement-content {
    flex: 1;
    min-width: 0;
  }

  .achievement-content h4 {
    margin: 0 0 4px 0;
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .achievement-content p {
    margin: 0 0 8px 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
  }

  .achievement-content .date {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
  }

  .achievement-xp {
    flex-shrink: 0;
    font-size: 14px;
    font-weight: 600;
    color: #fbbf24;
  }

  @media (max-width: 600px) {
    .achievements-tab {
      padding: 16px;
    }

    .level-section {
      padding: 20px;
    }

    .level-badge {
      width: 56px;
      height: 56px;
    }

    .level-info h3 {
      font-size: 20px;
    }
  }
</style>
