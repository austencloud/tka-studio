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
  import { currentSection } from "$shared/navigation-coordinator/navigation-coordinator.svelte";

  // Services
  let adminChallengeService = $state<IAdminChallengeService | null>(null);

  // State
  let isLoading = $state(true);

  // Get current section from navigation coordinator
  const activeSection = $derived(currentSection());

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

