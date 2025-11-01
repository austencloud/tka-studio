<script lang="ts">
  /**
   * Achievements Panel Component
   *
   * Full-screen modal displaying:
   * - User stats (level, XP, achievements)
   * - Daily challenge
   * - Achievement list by category
   * - Recent unlocks
   */

  import { onMount } from "svelte";
  import { resolve, TYPES } from "../../inversify";
  import type {
    IAchievementService,
    IDailyChallengeService,
    IStreakService,
  } from "../services/contracts";
  import type {
    Achievement,
    DailyChallenge,
    UserAchievement,
    UserChallengeProgress,
  } from "../domain/models";
  import { getLevelProgress } from "../domain/constants/xp-constants";

  // Props
  let { isOpen = false, onClose = () => {} }: { isOpen: boolean; onClose: () => void } = $props();

  // Services
  let achievementService: IAchievementService | null = $state(null);
  let challengeService: IDailyChallengeService | null = $state(null);
  let streakService: IStreakService | null = $state(null);

  // State
  let stats = $state<any>(null);
  let achievements = $state<Array<Achievement & { userProgress: UserAchievement | null }>>([]);
  let dailyChallenge = $state<DailyChallenge | null>(null);
  let challengeProgress = $state<UserChallengeProgress | null>(null);
  let currentStreak = $state(0);
  let selectedCategory = $state<Achievement["category"]>("creator");
  let isLoading = $state(true);

  // Derived
  let levelProgress = $derived.by(() => {
    if (!stats) return null;
    return getLevelProgress(stats.totalXP);
  });

  let filteredAchievements = $derived.by(() => {
    return achievements.filter((a) => a.category === selectedCategory);
  });

  let challengeProgressPercent = $derived.by(() => {
    if (!dailyChallenge || !challengeProgress) return 0;
    return Math.round(
      (challengeProgress.progress / dailyChallenge.requirement.target) * 100
    );
  });

  // Initialize
  onMount(async () => {
    try {
      achievementService = await resolve<IAchievementService>(TYPES.IAchievementService);
      challengeService = await resolve<IDailyChallengeService>(TYPES.IDailyChallengeService);
      streakService = await resolve<IStreakService>(TYPES.IStreakService);

      await loadData();
      isLoading = false;
    } catch (err) {
      console.error("Failed to initialize AchievementsPanel:", err);
      isLoading = false;
    }
  });

  async function loadData() {
    if (!achievementService || !challengeService || !streakService) return;

    try {
      [stats, achievements, dailyChallenge, challengeProgress] = await Promise.all([
        achievementService.getStats(),
        achievementService.getAllAchievements(),
        challengeService.getTodayChallenge(),
        challengeService.getChallengeProgress(),
      ]);

      const streakData = await streakService.getCurrentStreak();
      currentStreak = streakData.currentStreak;
    } catch (err) {
      console.error("Failed to load gamification data:", err);
    }
  }

  function handleClose() {
    onClose();
  }

  function selectCategory(category: Achievement["category"]) {
    selectedCategory = category;
  }

  // Category icons
  const categoryIcons: Record<Achievement["category"], string> = {
    creator: "🎨",
    scholar: "📚",
    practitioner: "💪",
    explorer: "🔍",
    performer: "🎥",
  };

  // Category names
  const categoryNames: Record<Achievement["category"], string> = {
    creator: "Creator",
    scholar: "Scholar",
    practitioner: "Practitioner",
    explorer: "Explorer",
    performer: "Performer",
  };
</script>

{#if isOpen}
  <div class="achievements-overlay" onclick={handleClose}>
    <div class="achievements-panel glass-surface" onclick={(e) => e.stopPropagation()}>
      <!-- Header -->
      <div class="panel-header">
        <h2 class="panel-title">🏆 Achievements & Challenges</h2>
        <button class="close-button" onclick={handleClose} aria-label="Close">×</button>
      </div>

      {#if isLoading}
        <div class="loading-container">
          <div class="spinner-large"></div>
          <p>Loading your progress...</p>
        </div>
      {:else}
        <!-- Stats Section -->
        <div class="stats-section">
          <div class="stat-card glass-surface">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <div class="stat-value">{stats?.currentLevel || 0}</div>
              <div class="stat-label">Level</div>
            </div>
          </div>

          <div class="stat-card glass-surface">
            <div class="stat-icon">✨</div>
            <div class="stat-content">
              <div class="stat-value">{stats?.totalXP.toLocaleString() || 0}</div>
              <div class="stat-label">Total XP</div>
            </div>
          </div>

          <div class="stat-card glass-surface">
            <div class="stat-icon">🎯</div>
            <div class="stat-content">
              <div class="stat-value">{stats?.achievementsUnlocked || 0}/{stats?.totalAchievements || 0}</div>
              <div class="stat-label">Achievements</div>
            </div>
          </div>

          <div class="stat-card glass-surface">
            <div class="stat-icon">🔥</div>
            <div class="stat-content">
              <div class="stat-value">{currentStreak}</div>
              <div class="stat-label">Day Streak</div>
            </div>
          </div>
        </div>

        <!-- Daily Challenge -->
        {#if dailyChallenge}
          <div class="daily-challenge glass-surface">
            <div class="challenge-header">
              <h3>🎯 Daily Challenge</h3>
              <span class="difficulty-badge {dailyChallenge.difficulty}">{dailyChallenge.difficulty}</span>
            </div>
            <p class="challenge-title">{dailyChallenge.title}</p>
            <p class="challenge-description">{dailyChallenge.description}</p>
            <div class="challenge-progress">
              <div class="progress-bar">
                <div class="progress-fill" style="width: {challengeProgressPercent}%"></div>
              </div>
              <span class="progress-text">{challengeProgressPercent}% ({challengeProgress?.progress || 0}/{dailyChallenge.requirement.target})</span>
            </div>
            <div class="challenge-reward">+{dailyChallenge.xpReward} XP</div>
          </div>
        {/if}

        <!-- Category Tabs -->
        <div class="category-tabs">
          {#each Object.entries(categoryNames) as [category, name]}
            <button
              class="category-tab"
              class:active={selectedCategory === category}
              onclick={() => selectCategory(category as Achievement["category"])}
            >
              <span class="tab-icon">{categoryIcons[category as Achievement["category"]]}</span>
              <span class="tab-name">{name}</span>
            </button>
          {/each}
        </div>

        <!-- Achievements List -->
        <div class="achievements-list">
          {#each filteredAchievements as achievement}
            {@const userProgress = achievement.userProgress}
            {@const isCompleted = userProgress?.isCompleted || false}
            {@const progress = userProgress?.progress || 0}
            {@const progressPercent = Math.round((progress / achievement.requirement.target) * 100)}

            <div class="achievement-card glass-surface" class:completed={isCompleted}>
              <div class="achievement-icon">{achievement.icon}</div>
              <div class="achievement-content">
                <div class="achievement-header">
                  <h4 class="achievement-title">{achievement.title}</h4>
                  <span class="tier-badge {achievement.tier}">{achievement.tier}</span>
                </div>
                <p class="achievement-description">{achievement.description}</p>
                <div class="achievement-progress">
                  {#if isCompleted}
                    <span class="completed-badge">✓ Completed</span>
                  {:else}
                    <div class="progress-bar-small">
                      <div class="progress-fill-small" style="width: {progressPercent}%"></div>
                    </div>
                    <span class="progress-text-small">{progress}/{achievement.requirement.target}</span>
                  {/if}
                </div>
              </div>
              <div class="achievement-xp">+{achievement.xpReward} XP</div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  /* Overlay */
  .achievements-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(8px);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  /* Panel */
  .achievements-panel {
    width: 100%;
    max-width: 900px;
    max-height: 90vh;
    border-radius: var(--radius-xl);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    animation: slideUp 0.3s ease;
  }

  @keyframes slideUp {
    from {
      transform: translateY(20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  /* Header */
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-lg);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .panel-title {
    font-size: 24px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .close-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.8);
    font-size: 28px;
    line-height: 1;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: rotate(90deg);
  }

  /* Loading */
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xl);
    gap: var(--spacing-md);
  }

  .spinner-large {
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

  /* Stats Section */
  .stats-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
  }

  .stat-card {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    border-radius: var(--radius-lg);
  }

  .stat-icon {
    font-size: 32px;
  }

  .stat-value {
    font-size: 24px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    line-height: 1;
  }

  .stat-label {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* Daily Challenge */
  .daily-challenge {
    margin: 0 var(--spacing-lg) var(--spacing-lg);
    padding: var(--spacing-lg);
    border-radius: var(--radius-lg);
    border: 2px solid rgba(102, 126, 234, 0.3);
  }

  .challenge-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-sm);
  }

  .challenge-header h3 {
    font-size: 18px;
    margin: 0;
  }

  .difficulty-badge {
    padding: 4px 12px;
    border-radius: var(--radius-md);
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
  }

  .difficulty-badge.beginner {
    background: rgba(76, 175, 80, 0.2);
    color: #4caf50;
  }

  .difficulty-badge.intermediate {
    background: rgba(255, 152, 0, 0.2);
    color: #ff9800;
  }

  .difficulty-badge.advanced {
    background: rgba(244, 67, 54, 0.2);
    color: #f44336;
  }

  .challenge-title {
    font-size: 16px;
    font-weight: 600;
    margin: var(--spacing-sm) 0;
  }

  .challenge-description {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: var(--spacing-md);
  }

  .challenge-progress {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .progress-bar {
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    transition: width 0.3s ease;
  }

  .progress-text {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
  }

  .challenge-reward {
    margin-top: var(--spacing-sm);
    font-weight: 600;
    color: #ffd700;
  }

  /* Category Tabs */
  .category-tabs {
    display: flex;
    gap: var(--spacing-xs);
    padding: 0 var(--spacing-lg) var(--spacing-md);
    overflow-x: auto;
  }

  .category-tab {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-lg);
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
  }

  .category-tab:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .category-tab.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: transparent;
    color: white;
  }

  /* Achievements List */
  .achievements-list {
    flex: 1;
    overflow-y: auto;
    padding: 0 var(--spacing-lg) var(--spacing-lg);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .achievement-card {
    display: flex;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
    border-radius: var(--radius-lg);
    transition: all 0.2s ease;
  }

  .achievement-card.completed {
    border: 1px solid rgba(76, 175, 80, 0.3);
  }

  .achievement-icon {
    font-size: 40px;
    flex-shrink: 0;
  }

  .achievement-content {
    flex: 1;
  }

  .achievement-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-xs);
  }

  .achievement-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
  }

  .tier-badge {
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
  }

  .tier-badge.bronze {
    background: rgba(205, 127, 50, 0.2);
    color: #cd7f32;
  }

  .tier-badge.silver {
    background: rgba(192, 192, 192, 0.2);
    color: #c0c0c0;
  }

  .tier-badge.gold {
    background: rgba(255, 215, 0, 0.2);
    color: #ffd700;
  }

  .tier-badge.platinum {
    background: rgba(229, 228, 226, 0.2);
    color: #e5e4e2;
  }

  .achievement-description {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: var(--spacing-sm);
  }

  .achievement-progress {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .completed-badge {
    color: #4caf50;
    font-weight: 600;
    font-size: 14px;
  }

  .progress-bar-small {
    flex: 1;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
    overflow: hidden;
  }

  .progress-fill-small {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    transition: width 0.3s ease;
  }

  .progress-text-small {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
  }

  .achievement-xp {
    flex-shrink: 0;
    font-weight: 600;
    color: #ffd700;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .achievements-overlay {
      padding: 0;
    }

    .achievements-panel {
      max-width: 100%;
      max-height: 100vh;
      border-radius: 0;
    }

    .stats-section {
      grid-template-columns: repeat(2, 1fr);
    }

    .category-tab .tab-name {
      display: none;
    }
  }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .achievements-overlay,
    .achievements-panel,
    .spinner-large {
      animation: none;
    }

    .close-button:hover {
      transform: none;
    }
  }
</style>
