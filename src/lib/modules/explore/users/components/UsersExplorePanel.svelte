<!--
UsersExplorePanel.svelte

Users browser for the Explore module.
Displays user profiles with their contributions and stats.
-->
<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { resolve, TYPES } from "$shared";
  import type {
    IUserExploreService,
    UserProfile,
  } from "../services/contracts/IUserExploreService";

  let users = $state<UserProfile[]>([]);
  let isLoading = $state(true);
  let searchQuery = $state("");
  let error = $state<string | null>(null);

  // Service instance and unsubscribe function
  let userService: IUserExploreService;
  let unsubscribe: (() => void) | null = null;

  // Filtered users based on search
  const filteredUsers = $derived(() => {
    if (!searchQuery) return users;
    const query = searchQuery.toLowerCase();
    return users.filter(
      (user) =>
        user.username.toLowerCase().includes(query) ||
        user.displayName.toLowerCase().includes(query)
    );
  });

  onMount(async () => {
    try {
      console.log("🔍 UsersExplorePanel: Initializing user service...");

      // Resolve the user service from DI container
      userService = resolve<IUserExploreService>(TYPES.IUserExploreService);

      // Subscribe to real-time user updates
      unsubscribe = userService.subscribeToUsers((updatedUsers) => {
        users = updatedUsers;
        isLoading = false;
        error = null;
        console.log(
          `✅ UsersExplorePanel: Updated with ${updatedUsers.length} users`
        );
      });

      console.log("✅ UsersExplorePanel: Real-time subscription active");
    } catch (err) {
      console.error(
        "❌ UsersExplorePanel: Error setting up subscription:",
        err
      );

      // Show generic error message
      error =
        err instanceof Error
          ? err.message
          : "Failed to load users. Please try again.";
      isLoading = false;
    }
  });

  onDestroy(() => {
    // Clean up the subscription when component is destroyed
    if (unsubscribe) {
      console.log("🔌 UsersExplorePanel: Unsubscribing from real-time updates");
      unsubscribe();
    }
  });

  function handleUserClick(user: UserProfile) {
    console.log("Navigate to user profile:", user.id);
    // TODO: Navigate to user profile page
  }

  function handleFollowToggle(user: UserProfile) {
    console.log("Toggle follow for user:", user.id);
    // TODO: Implement follow/unfollow functionality
  }
</script>

<div class="users-explore-panel">
  <!-- Search bar -->
  <div class="search-container">
    <i class="fas fa-search search-icon"></i>
    <input
      type="text"
      class="search-input"
      placeholder="Search users..."
      bind:value={searchQuery}
    />
  </div>

  <!-- Users grid -->
  {#if error}
    <div class="error-state">
      <i class="fas fa-exclamation-circle"></i>
      <p>{error}</p>
    </div>
  {:else if isLoading}
    <div class="loading-state">
      <i class="fas fa-spinner fa-spin"></i>
      <p>Loading users...</p>
    </div>
  {:else if filteredUsers().length === 0}
    <div class="empty-state">
      <i class="fas fa-users"></i>
      <p>No users found</p>
    </div>
  {:else}
    <div class="users-grid">
      {#each filteredUsers() as user (user.id)}
        <div class="user-card">
          <!-- Avatar -->
          <div class="user-avatar">
            {#if user.avatar}
              <img src={user.avatar} alt={user.displayName} />
            {:else}
              <div class="avatar-placeholder">
                <i class="fas fa-user"></i>
              </div>
            {/if}
          </div>

          <!-- User info -->
          <div class="user-info">
            <h3 class="display-name">{user.displayName}</h3>
            <p class="username">@{user.username}</p>

            <!-- Stats -->
            <div class="user-stats">
              <div class="stat">
                <i class="fas fa-list"></i>
                <span>{user.sequenceCount}</span>
              </div>
              <div class="stat">
                <i class="fas fa-folder"></i>
                <span>{user.collectionCount}</span>
              </div>
              <div class="stat">
                <i class="fas fa-users"></i>
                <span>{user.followerCount}</span>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="user-actions">
            <button
              class="view-profile-button"
              onclick={() => handleUserClick(user)}
            >
              View Profile
            </button>
            <button
              class="follow-button"
              class:following={user.isFollowing}
              onclick={() => handleFollowToggle(user)}
            >
              {user.isFollowing ? "Following" : "Follow"}
            </button>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .users-explore-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    padding: 16px;
    gap: 16px;
  }

  /* Search container with violet theme */
  .search-container {
    position: relative;
    width: 100%;
    max-width: 600px;
  }

  .search-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 255, 255, 0.5);
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    padding: 10px 12px 10px 40px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: white;
    font-size: 14px;
    transition: all 0.2s ease;
  }

  .search-input:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.05);
  }

  .search-input::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }

  /* Loading, empty, and error states */
  .loading-state,
  .empty-state,
  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    gap: 12px;
    color: rgba(255, 255, 255, 0.5);
  }

  .loading-state i,
  .empty-state i,
  .error-state i {
    font-size: 48px;
  }

  .error-state {
    color: rgba(239, 68, 68, 0.9);
  }

  /* Users grid */
  .users-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
    overflow-y: auto;
    padding: 4px;
  }

  /* User card */
  .user-card {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    transition: all 0.2s ease;
  }

  .user-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  /* Avatar */
  .user-avatar {
    width: 80px;
    height: 80px;
    margin: 0 auto;
  }

  .user-avatar img,
  .avatar-placeholder {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
  }

  .avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
  }

  .avatar-placeholder i {
    font-size: 32px;
    color: rgba(255, 255, 255, 0.4);
  }

  /* User info */
  .user-info {
    text-align: center;
  }

  .display-name {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: white;
  }

  .username {
    margin: 4px 0 0 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
  }

  /* User stats */
  .user-stats {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 12px;
  }

  .stat {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
  }

  .stat i {
    font-size: 12px;
  }

  /* Actions */
  .user-actions {
    display: flex;
    gap: 8px;
  }

  .view-profile-button,
  .follow-button {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .view-profile-button {
    background: rgba(255, 255, 255, 0.08);
    color: white;
  }

  .view-profile-button:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .follow-button {
    background: rgba(0, 123, 255, 0.15);
    border-color: rgba(0, 123, 255, 0.3);
    color: #4da3ff;
  }

  .follow-button:hover {
    background: rgba(0, 123, 255, 0.25);
    border-color: rgba(0, 123, 255, 0.5);
  }

  .follow-button.following {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.7);
  }

  /* Responsive design */
  @media (max-width: 480px) {
    .users-explore-panel {
      padding: 12px;
    }

    .users-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }

    .user-card {
      padding: 12px;
    }

    .user-avatar {
      width: 60px;
      height: 60px;
    }

    .display-name {
      font-size: 16px;
    }

    .user-actions {
      flex-direction: column;
    }
  }
</style>
