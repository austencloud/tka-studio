<!--
  AccountTab.svelte - User Account Management in Settings

  Displays user profile information and authentication controls
  within the settings sheet for a modern, integrated experience.
-->
<script lang="ts">
  import { authStore } from "$shared/auth";
  import { goto } from "$app/navigation";

  let signingOut = $state(false);

  async function handleSignOut() {
    signingOut = true;
    try {
      await authStore.signOut();
      // Optional: show a toast notification
      console.log("✅ Successfully signed out");
    } catch (error) {
      console.error("Failed to sign out:", error);
    } finally {
      signingOut = false;
    }
  }

  function handleSignIn() {
    goto("/auth/login");
  }
</script>

<div class="account-tab">
  <h3 class="account-tab__title">Account</h3>

  {#if authStore.isLoading}
    <div class="account-tab__loading">
      <div class="spinner"></div>
      <p>Loading account info...</p>
    </div>
  {:else if authStore.isAuthenticated && authStore.user}
    <!-- Logged in state -->
    <div class="account-tab__profile">
      <!-- Avatar and Name -->
      <div class="account-tab__header">
        {#if authStore.user.photoURL}
          <img
            src={authStore.user.photoURL}
            alt={authStore.user.displayName || "User"}
            class="account-tab__avatar"
          />
        {:else}
          <div class="account-tab__avatar-fallback">
            {(authStore.user.displayName || authStore.user.email || "?")
              .charAt(0)
              .toUpperCase()}
          </div>
        {/if}

        <div class="account-tab__header-info">
          <h4 class="account-tab__name">
            {authStore.user.displayName || authStore.user.email || "User"}
          </h4>
          <p class="account-tab__email">{authStore.user.email || "No email"}</p>
        </div>
      </div>

      <!-- Actions -->
      <button
        class="account-tab__button account-tab__button--danger"
        onclick={handleSignOut}
        disabled={signingOut}
      >
        <i class="fas fa-sign-out-alt"></i>
        {signingOut ? "Signing out..." : "Sign Out"}
      </button>
    </div>
  {:else}
    <!-- Logged out state -->
    <div class="account-tab__logged-out">
      <div class="account-tab__logged-out-icon">
        <i class="fas fa-user-circle"></i>
      </div>
      <h4 class="account-tab__logged-out-title">Not signed in</h4>
      <p class="account-tab__logged-out-text">
        Sign in to save your sequences, sync across devices, and access your
        profile.
      </p>
      <button
        class="account-tab__button account-tab__button--primary"
        onclick={handleSignIn}
      >
        <i class="fas fa-sign-in-alt"></i>
        Sign In
      </button>
    </div>
  {/if}
</div>

<style>
  /* Container */
  .account-tab {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }

  .account-tab__title {
    font-size: 20px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 24px 0;
  }

  /* Loading state */
  .account-tab__loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    gap: 16px;
    color: rgba(255, 255, 255, 0.6);
  }

  .spinner {
    width: 32px;
    height: 32px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Profile section */
  .account-tab__profile {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 500px;
  }

  /* Header with avatar */
  .account-tab__header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .account-tab__avatar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.2);
  }

  .account-tab__avatar-fallback {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: 600;
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.2);
  }

  .account-tab__header-info {
    flex: 1;
    min-width: 0;
  }

  .account-tab__name {
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 4px 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .account-tab__email {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* Action button */
  .account-tab__button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px 24px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    min-height: 48px;
  }

  .account-tab__button i {
    font-size: 14px;
  }

  .account-tab__button--primary {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  .account-tab__button--primary:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    transform: translateY(-1px);
  }

  .account-tab__button--danger {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: 1.5px solid rgba(239, 68, 68, 0.3);
  }

  .account-tab__button--danger:hover {
    background: rgba(239, 68, 68, 0.15);
    border-color: rgba(239, 68, 68, 0.5);
    transform: translateY(-1px);
  }

  .account-tab__button:active {
    transform: translateY(0);
  }

  .account-tab__button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  /* Logged out state */
  .account-tab__logged-out {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 60px 20px;
    gap: 20px;
  }

  .account-tab__logged-out-icon {
    font-size: 64px;
    color: rgba(255, 255, 255, 0.3);
    margin-bottom: 8px;
  }

  .account-tab__logged-out-title {
    font-size: 20px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
  }

  .account-tab__logged-out-text {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    max-width: 400px;
    line-height: 1.6;
    margin: 0 0 12px 0;
  }

  /* Responsive */
  @media (max-width: 480px) {
    .account-tab__header {
      flex-direction: column;
      text-align: center;
    }

    .account-tab__header-info {
      width: 100%;
    }

    .account-tab__name,
    .account-tab__email {
      white-space: normal;
      word-break: break-word;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .account-tab__button {
      transition: none;
    }

    .account-tab__button:hover {
      transform: none;
    }

    .spinner {
      animation: none;
    }
  }
</style>
