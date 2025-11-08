<!--
  Settings Button Component

  Simple settings button with icon that triggers the settings dialog.
  Displays user profile picture if authenticated.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { authStore } from "$shared/auth";

  let { navigationLayout = "top" } = $props<{
    navigationLayout?: "top" | "left";
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Initialize services (without onMount to avoid timing issues)
  if (typeof window !== "undefined") {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  }

  // Handle settings button click
  function handleSettingsClick() {
    hapticService?.trigger("selection");
    // Use route-based navigation
    import("../utils/sheet-router").then(({ openSheet }) => {
      openSheet("settings");
    });
  }
</script>

<button
  class="nav-action"
  class:layout-left={navigationLayout === "left"}
  class:has-avatar={authStore.isAuthenticated && authStore.user?.photoURL}
  onclick={handleSettingsClick}
  title="Settings (Ctrl+,) - Auth: {authStore.isAuthenticated}, Photo: {authStore
    .user?.photoURL
    ? 'yes'
    : 'no'}"
  aria-label="Open Settings"
>
  <!-- DEBUG: Auth={authStore.isAuthenticated ? 'Y' : 'N'} Photo={authStore.user?.photoURL ? 'Y' : 'N'} -->
  {#if authStore.isAuthenticated && authStore.user?.photoURL}
    <img
      src={authStore.user.photoURL}
      alt={authStore.user.displayName || "User"}
      class="user-avatar"
    />
  {:else if authStore.isAuthenticated && authStore.user}
    <div class="user-initial">
      {(authStore.user.displayName || authStore.user.email || "?")
        .charAt(0)
        .toUpperCase()}
    </div>
  {:else}
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
      <path
        d="M12 15a3 3 0 100-6 3 3 0 000 6z"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <path
        d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
  {/if}
</button>

<style>
  .nav-action {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 48px;
    height: 100%;
    padding: 0 var(--spacing-sm);
    background: rgba(100, 116, 139, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.3);
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    color: #ffffff;
    cursor: pointer;
    transition: all var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1));
  }

  .nav-action.layout-left {
    width: 48px;
    height: 48px;
    flex-shrink: 0;
    padding: 0;
  }

  .nav-action:hover {
    transform: scale(1.05);
    background: rgba(100, 116, 139, 0.9);
    border-color: rgba(148, 163, 184, 0.4);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    color: #ffffff;
  }

  .nav-action:focus-visible {
    outline: 2px solid var(--primary-light, #818cf8);
    outline-offset: 2px;
  }

  /* User avatar styling */
  .nav-action.has-avatar {
    padding: 0;
    overflow: hidden;
  }

  .user-avatar {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .user-initial {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    font-size: 14px;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
  }

  /* ACCESSIBILITY & MOTION */
  @media (prefers-reduced-motion: reduce) {
    .nav-action {
      transition: none;
    }
  }
</style>
