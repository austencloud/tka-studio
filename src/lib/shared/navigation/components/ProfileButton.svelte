<!--
  ProfileButton.svelte - Global Profile/Account Button

  Features:
  - Profile picture display or initial fallback
  - Opens profile settings sheet directly via route-based navigation
  - Haptic feedback on interaction
  - 44px minimum touch target (WCAG AAA)
-->
<script lang="ts">
  import { authStore } from "$shared/auth";
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleProfileClick() {
    hapticService?.trigger("selection");
    // Open profile settings sheet directly
    import("../utils/sheet-router").then(({ openSheet }) => {
      openSheet("profile-settings");
    });
  }
</script>

<div class="profile-button-container">
  <button
    class="profile-button"
    class:has-avatar={authStore.isAuthenticated && authStore.user?.photoURL}
    onclick={handleProfileClick}
    aria-label={authStore.isAuthenticated ? "Account menu" : "Sign in"}
  >
    {#if authStore.isAuthenticated && authStore.user?.photoURL}
      <img
        src={authStore.user.photoURL}
        alt={authStore.user.displayName || "User"}
        class="profile-avatar"
      />
    {:else if authStore.isAuthenticated && authStore.user}
      <div class="profile-initial">
        {(authStore.user.displayName || authStore.user.email || "?").charAt(0).toUpperCase()}
      </div>
    {:else}
      <i class="fas fa-user-circle"></i>
    {/if}
  </button>
</div>

<style>
  /* ============================================================================
     PROFILE BUTTON CONTAINER
     ============================================================================ */
  .profile-button-container {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* ============================================================================
     PROFILE BUTTON - 44px minimum (WCAG AAA)
     ============================================================================ */
  .profile-button {
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    position: relative;
  }

  .profile-button:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: scale(1.05);
  }

  .profile-button:active {
    transform: scale(0.95);
  }

  .profile-button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* Profile avatar image */
  .profile-button.has-avatar {
    padding: 0;
    overflow: hidden;
    border: 2px solid rgba(255, 255, 255, 0.2);
  }

  .profile-button.has-avatar:hover {
    border-color: rgba(255, 255, 255, 0.4);
  }

  .profile-avatar {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  /* Profile initial fallback */
  .profile-initial {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
  }

  /* ============================================================================
     RESPONSIVE DESIGN
     ============================================================================ */
  /* Note: Button size stays 44px on all devices for accessibility (WCAG AAA) */

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .profile-button {
      transition: none;
    }

    .profile-button:hover,
    .profile-button:active {
      transform: none;
    }
  }

  @media (prefers-contrast: high) {
    .profile-button {
      background: rgba(255, 255, 255, 0.2);
      border: 2px solid white;
    }
  }
</style>
