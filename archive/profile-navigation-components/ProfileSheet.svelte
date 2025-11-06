<!--
  ProfileSheet.svelte - Profile & Account Bottom Sheet

  Features:
  - User avatar, name, email
  - Navigation to My Library
  - My Progress (coming soon)
  - Profile Settings (coming soon)
  - Sign out
  - 44px minimum touch targets (WCAG AAA)
-->
<script lang="ts">
  import { authStore } from "$shared/auth";
  import { resolve, TYPES, type IHapticFeedbackService, BottomSheet } from "$shared";
  import { navigationState } from "$shared/navigation";
  import { onMount } from "svelte";

  // Props
  let { isOpen = false, onClose } = $props<{
    isOpen?: boolean;
    onClose: () => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  // State
  let signingOut = $state(false);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  async function handleSignOut() {
    if (signingOut) return;

    hapticService?.trigger("selection");
    signingOut = true;

    try {
      await authStore.signOut();
      console.log("✅ Successfully signed out");
      onClose();
    } catch (error) {
      console.error("Failed to sign out:", error);
    } finally {
      signingOut = false;
    }
  }

  function handleSignIn() {
    hapticService?.trigger("selection");
    // Close this sheet and navigate to auth
    onClose();

    // Small delay to allow sheet to close smoothly before opening new one
    setTimeout(() => {
      // Import dynamically to avoid circular deps
      import("../utils/sheet-router").then(({ openSheet }) => {
        openSheet("auth");
      });
    }, 200);
  }

  function handleNavigateToLibrary() {
    hapticService?.trigger("selection");
    navigationState.setCurrentModule("library");
    onClose();
  }

  function handleMyProgress() {
    hapticService?.trigger("selection");
    // TODO: Implement My Progress view
    console.log("My Progress - Coming Soon");
    onClose();
  }

  function handleProfileSettings() {
    hapticService?.trigger("selection");
    // Close this sheet and navigate to profile settings
    onClose();

    // Small delay to allow sheet to close smoothly before opening new one
    setTimeout(() => {
      // Import dynamically to avoid circular deps
      import("../utils/sheet-router").then(({ openSheet }) => {
        openSheet("profile-settings");
      });
    }, 200);
  }
</script>

<Drawer
  {isOpen}
  labelledBy="profile-sheet-title"
  on:close={onClose}
  class="profile-sheet"
  backdropClass="profile-sheet__backdrop"
>
  <div class="profile-sheet__container">
    {#if authStore.isAuthenticated && authStore.user}
      <!-- Logged in state -->

      <!-- Header with profile info -->
      <header class="profile-sheet__header">
        <div class="profile-sheet__profile-info">
          {#if authStore.user.photoURL}
            <img
              src={authStore.user.photoURL}
              alt={authStore.user.displayName || "User"}
              class="profile-sheet__avatar"
            />
          {:else}
            <div class="profile-sheet__avatar-fallback">
              {(authStore.user.displayName || authStore.user.email || "?").charAt(0).toUpperCase()}
            </div>
          {/if}

          <div class="profile-sheet__user-details">
            <h2 id="profile-sheet-title" class="profile-sheet__name">
              {authStore.user.displayName || authStore.user.email || "User"}
            </h2>
            {#if authStore.user.email}
              <p class="profile-sheet__email">{authStore.user.email}</p>
            {/if}
          </div>
        </div>

        <button
          class="profile-sheet__close"
          onclick={() => {
            hapticService?.trigger("selection");
            onClose();
          }}
          aria-label="Close profile"
        >
          <i class="fas fa-times"></i>
        </button>
      </header>

      <!-- Menu items -->
      <nav class="profile-sheet__menu" aria-label="Profile menu">
        <button
          class="profile-sheet__menu-item"
          onclick={handleNavigateToLibrary}
        >
          <i class="fas fa-book"></i>
          <span>My Library</span>
          <i class="fas fa-chevron-right profile-sheet__menu-arrow"></i>
        </button>

        <button
          class="profile-sheet__menu-item profile-sheet__menu-item--disabled"
          onclick={handleMyProgress}
          disabled
          title="Coming Soon"
        >
          <i class="fas fa-chart-line"></i>
          <span>My Progress</span>
          <span class="profile-sheet__badge">Soon</span>
        </button>

        <button
          class="profile-sheet__menu-item"
          onclick={handleProfileSettings}
        >
          <i class="fas fa-cog"></i>
          <span>Settings</span>
          <i class="fas fa-chevron-right profile-sheet__menu-arrow"></i>
        </button>
      </nav>

      <!-- Footer with sign out -->
      <footer class="profile-sheet__footer">
        <button
          class="profile-sheet__button profile-sheet__button--danger"
          onclick={handleSignOut}
          disabled={signingOut}
        >
          <i class="fas fa-sign-out-alt"></i>
          {signingOut ? "Signing out..." : "Sign Out"}
        </button>
      </footer>

    {:else}
      <!-- Logged out state -->
      <div class="profile-sheet__logged-out">
        <button
          class="profile-sheet__close profile-sheet__close--corner"
          onclick={() => {
            hapticService?.trigger("selection");
            onClose();
          }}
          aria-label="Close"
        >
          <i class="fas fa-times"></i>
        </button>

        <div class="profile-sheet__logged-out-icon">
          <i class="fas fa-user-circle"></i>
        </div>
        <h2 id="profile-sheet-title" class="profile-sheet__logged-out-title">Not Signed In</h2>
        <p class="profile-sheet__logged-out-text">Sign in to access your library and track your progress</p>
        <button
          class="profile-sheet__button profile-sheet__button--primary"
          onclick={handleSignIn}
        >
          <i class="fas fa-sign-in-alt"></i>
          Sign In
        </button>
      </div>
    {/if}
  </div>
</Drawer>

<style>
  /* ============================================================================
     BACKDROP
     ============================================================================ */
  :global(.profile-sheet__backdrop) {
    z-index: 1100;
  }

  /* ============================================================================
     CONTAINER
     ============================================================================ */
  .profile-sheet__container {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-height: 80vh;
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(15, 20, 30, 0.95) 100%
    );
    overflow: hidden;
  }

  /* ============================================================================
     HEADER (Logged In)
     ============================================================================ */
  .profile-sheet__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .profile-sheet__profile-info {
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
    min-width: 0;
  }

  .profile-sheet__avatar {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.2);
    flex-shrink: 0;
  }

  .profile-sheet__avatar-fallback {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: 600;
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.2);
    flex-shrink: 0;
  }

  .profile-sheet__user-details {
    flex: 1;
    min-width: 0;
  }

  .profile-sheet__name {
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 4px 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .profile-sheet__email {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .profile-sheet__close {
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
    font-size: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .profile-sheet__close:hover {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(1.05);
  }

  .profile-sheet__close:active {
    transform: scale(0.95);
  }

  .profile-sheet__close:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* ============================================================================
     MENU (Navigation & Settings)
     ============================================================================ */
  .profile-sheet__menu {
    flex: 1;
    overflow-y: auto;
    padding: 8px 16px;
  }

  .profile-sheet__menu-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    min-height: 56px; /* 44px + padding = good touch target */
    border-radius: 12px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.9);
    text-align: left;
    margin-bottom: 4px;
  }

  .profile-sheet__menu-item i:first-child {
    font-size: 20px;
    width: 24px;
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    flex-shrink: 0;
  }

  .profile-sheet__menu-item span:nth-child(2) {
    flex: 1;
  }

  .profile-sheet__menu-arrow {
    font-size: 14px !important;
    color: rgba(255, 255, 255, 0.4) !important;
    transition: transform 0.2s ease;
  }

  .profile-sheet__menu-item:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.08);
  }

  .profile-sheet__menu-item:hover:not(:disabled) .profile-sheet__menu-arrow {
    color: rgba(255, 255, 255, 0.7) !important;
    transform: translateX(4px);
  }

  .profile-sheet__menu-item:active:not(:disabled) {
    background: rgba(255, 255, 255, 0.12);
    transform: scale(0.98);
  }

  .profile-sheet__menu-item--disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .profile-sheet__badge {
    padding: 4px 10px;
    background: rgba(16, 185, 129, 0.2);
    border: 1px solid rgba(16, 185, 129, 0.4);
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    color: rgba(16, 185, 129, 1);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    flex-shrink: 0;
  }

  /* ============================================================================
     FOOTER
     ============================================================================ */
  .profile-sheet__footer {
    padding: 16px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
    flex-shrink: 0;
  }

  .profile-sheet__button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 14px 24px;
    min-height: 48px; /* 44px + a bit extra for comfort */
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
  }

  .profile-sheet__button i {
    font-size: 16px;
  }

  /* Primary button (Sign In) */
  .profile-sheet__button--primary {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  .profile-sheet__button--primary:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  .profile-sheet__button--primary:active {
    transform: translateY(0);
  }

  /* Danger button (Sign Out) */
  .profile-sheet__button--danger {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: 2px solid rgba(239, 68, 68, 0.3);
  }

  .profile-sheet__button--danger:hover:not(:disabled) {
    background: rgba(239, 68, 68, 0.15);
    border-color: rgba(239, 68, 68, 0.5);
  }

  .profile-sheet__button--danger:active:not(:disabled) {
    transform: scale(0.98);
  }

  .profile-sheet__button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  .profile-sheet__button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* ============================================================================
     LOGGED OUT STATE
     ============================================================================ */
  .profile-sheet__logged-out {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 48px 32px;
    gap: 20px;
    position: relative;
    min-height: 400px;
  }

  .profile-sheet__close--corner {
    position: absolute;
    top: 16px;
    right: 16px;
  }

  .profile-sheet__logged-out-icon {
    font-size: 80px;
    color: rgba(255, 255, 255, 0.3);
  }

  .profile-sheet__logged-out-title {
    font-size: 24px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .profile-sheet__logged-out-text {
    font-size: 15px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    max-width: 300px;
    line-height: 1.5;
  }

  /* ============================================================================
     RESPONSIVE DESIGN
     ============================================================================ */
  @media (max-width: 480px) {
    .profile-sheet__header {
      padding: 20px;
    }

    .profile-sheet__name {
      font-size: 16px;
    }

    .profile-sheet__email {
      font-size: 13px;
    }

    .profile-sheet__menu {
      padding: 8px 12px;
    }

    .profile-sheet__menu-item {
      padding: 14px;
      font-size: 15px;
    }

    .profile-sheet__button {
      padding: 12px 20px;
      font-size: 15px;
    }

    .profile-sheet__logged-out {
      padding: 40px 24px;
    }

    .profile-sheet__logged-out-icon {
      font-size: 64px;
    }

    .profile-sheet__logged-out-title {
      font-size: 20px;
    }
  }

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .profile-sheet__close,
    .profile-sheet__menu-item,
    .profile-sheet__button {
      transition: none;
    }

    .profile-sheet__close:hover,
    .profile-sheet__close:active,
    .profile-sheet__menu-item:hover,
    .profile-sheet__menu-item:active,
    .profile-sheet__button:hover,
    .profile-sheet__button:active {
      transform: none;
    }

    .profile-sheet__menu-arrow {
      transition: none;
    }
  }

  @media (prefers-contrast: high) {
    .profile-sheet__container {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    .profile-sheet__header,
    .profile-sheet__footer {
      border-color: white;
    }

    .profile-sheet__menu-item {
      border: 1px solid rgba(255, 255, 255, 0.3);
    }
  }
</style>
