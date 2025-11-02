<script lang="ts">
  /**
   * Admin Dashboard
   * 
   * Main admin interface for managing TKA system
   */
  
  import { onMount } from "svelte";
  import { resolve, TYPES } from "$shared";
  import type { IAdminChallengeService } from "../services/contracts";
  import DailyChallengeScheduler from "./DailyChallengeScheduler.svelte";
  
  // Services
  let adminChallengeService = $state<IAdminChallengeService | null>(null);

  // State
  let isLoading = $state(true);
  let activeSection = $state<"challenges" | "analytics" | "users" | "settings">("challenges");

  onMount(() => {
    try {
      adminChallengeService = resolve<IAdminChallengeService>(TYPES.IAdminChallengeService);
      isLoading = false;
    } catch (error) {
      console.error("❌ Failed to initialize AdminDashboard:", error);
      isLoading = false;
    }
  });
</script>

<div class="admin-dashboard">
  {#if isLoading}
    <div class="loading-state">
      <i class="fas fa-spinner fa-spin"></i>
      <p>Loading admin tools...</p>
    </div>
  {:else}
    <!-- Header (matches ProfileSettingsSheet pattern) -->
    <header class="header">
      <h2>
        <i class="fas fa-crown"></i>
        Admin Dashboard
      </h2>
    </header>

    <!-- Tabs (matches ProfileSettingsSheet pattern) -->
    <div class="tabs" role="tablist" aria-label="Admin sections">
      <button
        class="tab"
        class:active={activeSection === "challenges"}
        role="tab"
        aria-selected={activeSection === "challenges"}
        aria-controls="challenges-panel"
        onclick={() => activeSection = "challenges"}
      >
        <i class="fas fa-calendar-day"></i>
        <span>Challenges</span>
      </button>

      <button
        class="tab"
        class:active={activeSection === "analytics"}
        role="tab"
        aria-selected={activeSection === "analytics"}
        aria-controls="analytics-panel"
        onclick={() => activeSection = "analytics"}
      >
        <i class="fas fa-chart-line"></i>
        <span>Analytics</span>
      </button>

      <button
        class="tab"
        class:active={activeSection === "users"}
        role="tab"
        aria-selected={activeSection === "users"}
        aria-controls="users-panel"
        onclick={() => activeSection = "users"}
      >
        <i class="fas fa-users"></i>
        <span>Users</span>
      </button>

      <button
        class="tab"
        class:active={activeSection === "settings"}
        role="tab"
        aria-selected={activeSection === "settings"}
        aria-controls="settings-panel"
        onclick={() => activeSection = "settings"}
      >
        <i class="fas fa-cog"></i>
        <span>Settings</span>
      </button>
    </div>

    <!-- Content Area -->
    <main class="content">
      {#if activeSection === "challenges" && adminChallengeService}
        <div id="challenges-panel" role="tabpanel" aria-labelledby="challenges-tab">
          <DailyChallengeScheduler {adminChallengeService} />
        </div>
      {:else if activeSection === "analytics"}
        <div id="analytics-panel" role="tabpanel" aria-labelledby="analytics-tab" class="placeholder-section">
          <i class="fas fa-chart-line"></i>
          <h2>Analytics Dashboard</h2>
          <p>Coming soon: View app usage, popular sequences, and user engagement metrics.</p>
        </div>
      {:else if activeSection === "users"}
        <div id="users-panel" role="tabpanel" aria-labelledby="users-tab" class="placeholder-section">
          <i class="fas fa-users"></i>
          <h2>User Management</h2>
          <p>Coming soon: View users, grant achievements, and manage permissions.</p>
        </div>
      {:else if activeSection === "settings"}
        <div id="settings-panel" role="tabpanel" aria-labelledby="settings-tab" class="placeholder-section">
          <i class="fas fa-cog"></i>
          <h2>System Settings</h2>
          <p>Coming soon: Configure XP rewards, difficulty levels, and system parameters.</p>
        </div>
      {/if}
    </main>
  {/if}
</div>

<style>
  .admin-dashboard {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: var(--background-color, #1a1a2e);
    color: var(--text-color, #ffffff);
    overflow: hidden;
  }

  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 1rem;
    font-size: 1.2rem;
    opacity: 0.7;
  }

  .loading-state i {
    font-size: 3rem;
  }

  /* Header (matches ProfileSettingsSheet) */
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .header h2 {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 24px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .header h2 i {
    color: #ffd700;
    font-size: 24px;
  }

  /* Tabs (matches ProfileSettingsSheet) */
  .tabs {
    container-type: inline-size;
    display: flex;
    justify-content: space-evenly;
    flex-wrap: nowrap;
    gap: clamp(1px, 0.5cqi, 8px);
    padding: 0 clamp(4px, 1cqi, 24px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .tab {
    display: flex;
    align-items: center;
    gap: clamp(3px, 1cqi, 8px);
    padding: clamp(8px, 2cqi, 16px) clamp(4px, 2cqi, 24px);
    min-height: 48px;
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    color: rgba(255, 255, 255, 0.7);
    font-size: clamp(10px, 2.5cqi, 15px);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    white-space: nowrap;
    flex: 1 1 0;
    justify-content: center;
  }

  .tab i {
    font-size: clamp(12px, 2.5cqi, 16px);
    flex-shrink: 0;
  }

  .tab:hover:not(:disabled) {
    color: rgba(255, 255, 255, 0.9);
    background: rgba(255, 255, 255, 0.05);
  }

  .tab.active {
    color: #ffd700;
    border-bottom-color: #ffd700;
  }

  /* Container query: Switch to vertical layout on narrow containers */
  @container (max-width: 500px) {
    .tabs {
      gap: 1px;
      padding: 0 2px;
    }

    .tab {
      flex-direction: column;
      padding: 8px 2px;
      gap: 2px;
      font-size: 9px;
    }

    .tab i {
      font-size: 14px;
    }
  }

  /* Content Area */
  .content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0;
  }

  .placeholder-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    gap: 1rem;
    opacity: 0.6;
    text-align: center;
    padding: 2rem;
  }

  .placeholder-section i {
    font-size: 3rem;
    opacity: 0.5;
  }

  .placeholder-section h2 {
    font-size: 1.5rem;
    margin: 0;
  }

  .placeholder-section p {
    font-size: 1rem;
    max-width: 500px;
    line-height: 1.6;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .header {
      padding: 16px;
    }

    .header h2 {
      font-size: 20px;
    }

    .header h2 i {
      font-size: 20px;
    }

    .placeholder-section {
      padding: 1rem;
      min-height: 300px;
    }

    .placeholder-section i {
      font-size: 2rem;
    }

    .placeholder-section h2 {
      font-size: 1.25rem;
    }

    .placeholder-section p {
      font-size: 0.9rem;
    }
  }
</style>

