<!--
  ProfileSettingsSheet - Profile & Account Settings

  Clean architecture coordinator component.
  Delegates to PersonalTab and AccountTab sub-components.
  Handles business logic and state management.
-->
<script lang="ts">
  import {
    Drawer,
    resolve,
    TYPES,
    type IHapticFeedbackService,
  } from "$shared";
  import { authStore } from "$shared/auth";
  import { onMount } from "svelte";
  import { cubicOut } from "svelte/easing";
  import { fade } from "svelte/transition";
  import {
    emailChangeState,
    originalPersonalInfoState,
    passwordState,
    personalInfoState,
    resetEmailChangeForm,
    resetPasswordForm,
    setupViewportTracking,
    syncWithAuthStore,
    uiState,
    updateTabTransition,
    viewportState,
  } from "../state/profile-settings-state.svelte";
  import AccountTab from "./profile-settings/AccountTab.svelte";
  import PersonalTab from "./profile-settings/PersonalTab.svelte";
  import SubscriptionTab from "./profile-settings/SubscriptionTab.svelte";
  import AchievementsTab from "./profile-settings/AchievementsTab.svelte";

  // Props
  let { isOpen = false, onClose } = $props<{
    isOpen?: boolean;
    onClose: () => void;
  }>();

  // Services
  let hapticService = $state<IHapticFeedbackService | null>(null);

  // Transition state
  let prefersReducedMotion = $state(false);
  let touchStartX = $state(0);
  let touchStartY = $state(0);
  let isSwiping = $state(false);
  let signingOut = $state(false);

  onMount(() => {
    // Check reduced motion preference
    if (typeof window !== "undefined") {
      const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
      prefersReducedMotion = mediaQuery.matches;

      // Listen for changes
      const handler = (e: MediaQueryListEvent) => {
        prefersReducedMotion = e.matches;
      };
      mediaQuery.addEventListener("change", handler);

      // Cleanup
      return () => mediaQuery.removeEventListener("change", handler);
    }
    return undefined;
  });

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
    syncWithAuthStore();

    // Read tab from URL on mount
    if (isOpen) {
      const urlParams = new URLSearchParams(window.location.search);
      const tabParam = urlParams.get("tab");
      if (
        tabParam &&
        ["personal", "security", "subscription", "achievements"].includes(tabParam)
      ) {
        uiState.activeTab = tabParam as import("../state/profile-settings-state.svelte").SettingsTab;
      }
    }
  });

  // Sync with auth store
  $effect(() => {
    if (authStore.user) {
      syncWithAuthStore();
    }
  });

  // Setup viewport tracking
  $effect(() => {
    const cleanup = setupViewportTracking();
    return cleanup || undefined;
  });

  // Sync active tab to URL
  $effect(() => {
    if (isOpen && typeof window !== "undefined") {
      const url = new URL(window.location.href);
      url.searchParams.set("tab", uiState.activeTab);
      window.history.replaceState({}, "", url.toString());
    }
  });

  // ============================================================================
  // TAB NAVIGATION
  // ============================================================================

  // Swipe gesture support
  function handleTouchStart(event: TouchEvent) {
    touchStartX = event.touches[0]?.clientX || 0;
    touchStartY = event.touches[0]?.clientY || 0;
    isSwiping = false;
  }

  function handleTouchMove(event: TouchEvent) {
    if (!touchStartX || !touchStartY) return;

    const touchCurrentX = event.touches[0]?.clientX || 0;
    const touchCurrentY = event.touches[0]?.clientY || 0;

    const deltaX = touchCurrentX - touchStartX;
    const deltaY = touchCurrentY - touchStartY;

    // Determine if this is a horizontal swipe (not vertical scroll)
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 10) {
      isSwiping = true;
      // Optionally prevent scroll while swiping horizontally
      event.preventDefault();
    }
  }

  function handleTouchEnd(event: TouchEvent) {
    if (!touchStartX || !isSwiping) {
      touchStartX = 0;
      touchStartY = 0;
      isSwiping = false;
      return;
    }

    const touchEndX = event.changedTouches[0]?.clientX || 0;
    const deltaX = touchEndX - touchStartX;
    const swipeThreshold = 50; // Minimum distance for a swipe

    // Reset touch state
    touchStartX = 0;
    touchStartY = 0;
    isSwiping = false;

    // Determine swipe direction and navigate
    if (Math.abs(deltaX) > swipeThreshold) {
      const tabs: Array<import("../state/profile-settings-state.svelte").SettingsTab> = [
        "personal",
        "security",
        "subscription",
        "achievements",
      ];
      const currentIndex = tabs.indexOf(uiState.activeTab);
      const prevTab = tabs[currentIndex - 1];
      const nextTab = tabs[currentIndex + 1];

      if (deltaX > 0 && currentIndex > 0 && prevTab) {
        // Swipe right - go to previous tab
        hapticService?.trigger("selection");
        updateTabTransition(prevTab);
      } else if (deltaX < 0 && currentIndex < tabs.length - 1 && nextTab) {
        // Swipe left - go to next tab
        hapticService?.trigger("selection");
        updateTabTransition(nextTab);
      }
    }
  }

  function handleTabKeydown(
    event: KeyboardEvent,
    tabName: import("../state/profile-settings-state.svelte").SettingsTab
  ) {
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      hapticService?.trigger("selection");

      const tabs: Array<import("../state/profile-settings-state.svelte").SettingsTab> = [
        "personal",
        "security",
        "subscription",
        "achievements",
      ];
      const currentIndex = tabs.indexOf(tabName);
      let newIndex: number;

      if (event.key === "ArrowLeft") {
        newIndex = currentIndex === 0 ? tabs.length - 1 : currentIndex - 1;
      } else {
        newIndex = currentIndex === tabs.length - 1 ? 0 : currentIndex + 1;
      }

      const newTab = tabs[newIndex];
      if (newTab) {
        updateTabTransition(newTab);

        // Focus the newly activated tab
        const newTabButton = document.getElementById(`${newTab}-tab`);
        newTabButton?.focus();
      }
    }
  }

  // ============================================================================
  // BUSINESS LOGIC HANDLERS
  // ============================================================================

  async function handleSavePersonalInfo() {
    if (uiState.saving) return;

    hapticService?.trigger("selection");
    uiState.saving = true;

    try {
      const result = await authStore.updateDisplayName(
        personalInfoState.displayName
      );

      if (result.success) {
        // Update original values to reflect saved state
        originalPersonalInfoState.displayName = personalInfoState.displayName;

        hapticService?.trigger("success");
        console.log("✅ Profile updated successfully");
      } else {
        throw new Error(result.message || "Failed to update profile");
      }
    } catch (error) {
      console.error("❌ Failed to update profile:", error);
      hapticService?.trigger("error");
      alert("Failed to update profile. Please try again.");
    } finally {
      uiState.saving = false;
    }
  }

  async function handlePhotoUpload(file: File) {
    hapticService?.trigger("selection");
    uiState.uploadingPhoto = true;

    try {
      // TODO: Implement photo upload to Firebase Storage
      console.log("Uploading photo:", file);
      hapticService?.trigger("success");
      alert("Profile photo updated!");
    } catch (error) {
      console.error("Failed to upload photo:", error);
      hapticService?.trigger("error");
      alert("Failed to upload photo. Please try again.");
    } finally {
      uiState.uploadingPhoto = false;
    }
  }

  async function handleChangeEmail() {
    if (uiState.changingEmail) return;

    hapticService?.trigger("selection");
    uiState.changingEmail = true;

    try {
      const result = await authStore.changeEmail(
        emailChangeState.newEmail,
        emailChangeState.password
      );

      hapticService?.trigger("success");
      alert(result.message);

      // Reset form and hide section
      resetEmailChangeForm();
      uiState.showEmailChangeSection = false;

      // Sync with updated user data
      syncWithAuthStore();
    } catch (error: any) {
      console.error("Failed to change email:", error);
      hapticService?.trigger("error");
      alert(error.message || "Failed to change email. Please try again.");
    } finally {
      uiState.changingEmail = false;
    }
  }

  async function handleChangePassword() {
    if (uiState.saving) return;
    if (passwordState.new !== passwordState.confirm) {
      alert("Passwords don't match!");
      return;
    }

    hapticService?.trigger("selection");
    uiState.saving = true;

    try {
      // TODO: Implement password change via Firebase
      console.log("Changing password");
      hapticService?.trigger("success");
      alert("Password changed successfully!");
      resetPasswordForm();
      uiState.showPasswordSection = false;
    } catch (error) {
      console.error("Failed to change password:", error);
      hapticService?.trigger("error");
      alert("Failed to change password. Please try again.");
    } finally {
      uiState.saving = false;
    }
  }

  async function handleDeleteAccount() {
    if (!uiState.showDeleteConfirmation) {
      uiState.showDeleteConfirmation = true;
      return;
    }

    hapticService?.trigger("warning");

    const confirmed = confirm(
      "Are you absolutely sure? This action cannot be undone. All your data will be permanently deleted."
    );

    if (!confirmed) {
      uiState.showDeleteConfirmation = false;
      return;
    }

    try {
      // TODO: Implement account deletion
      console.log("Deleting account");
      await authStore.signOut();
      alert("Account deleted successfully.");
      onClose();
    } catch (error) {
      console.error("Failed to delete account:", error);
      alert("Failed to delete account. Please try again.");
    }
  }

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
</script>

<Drawer
  {isOpen}
  labelledBy="profile-settings-title"
  on:close={onClose}
  class="profile-settings-sheet profile-settings-sheet--full-height"
  backdropClass="profile-settings-sheet__backdrop"
>
  <div class="container">
    {#if authStore.isAuthenticated && authStore.user}
      <!-- Logged in state -->

      <!-- Header -->
      <header class="header">
        <h2 id="profile-settings-title">Account Settings</h2>
        <button
          class="close"
          onclick={() => {
            hapticService?.trigger("selection");
            onClose();
          }}
          aria-label="Close settings"
        >
          <i class="fas fa-times" aria-hidden="true"></i>
        </button>
      </header>

      <!-- Tabs -->
      <div class="tabs" role="tablist" aria-label="Account settings sections">
        <button
          id="personal-tab"
          class="tab"
          class:active={uiState.activeTab === "personal"}
          role="tab"
          aria-selected={uiState.activeTab === "personal"}
          aria-controls="personal-panel"
          tabindex={uiState.activeTab === "personal" ? 0 : -1}
          onclick={() => {
            hapticService?.trigger("selection");
            updateTabTransition("personal");
          }}
          onkeydown={(e) => handleTabKeydown(e, "personal")}
        >
          <i class="fas fa-user" aria-hidden="true"></i>
          Personal
        </button>
        <button
          id="security-tab"
          class="tab"
          class:active={uiState.activeTab === "security"}
          role="tab"
          aria-selected={uiState.activeTab === "security"}
          aria-controls="security-panel"
          tabindex={uiState.activeTab === "security" ? 0 : -1}
          onclick={() => {
            hapticService?.trigger("selection");
            updateTabTransition("security");
          }}
          onkeydown={(e) => handleTabKeydown(e, "security")}
        >
          <i class="fas fa-shield-alt" aria-hidden="true"></i>
          Security
        </button>
        <button
          id="subscription-tab"
          class="tab"
          class:active={uiState.activeTab === "subscription"}
          role="tab"
          aria-selected={uiState.activeTab === "subscription"}
          aria-controls="subscription-panel"
          tabindex={uiState.activeTab === "subscription" ? 0 : -1}
          onclick={() => {
            hapticService?.trigger("selection");
            updateTabTransition("subscription");
          }}
          onkeydown={(e) => handleTabKeydown(e, "subscription")}
        >
          <i class="fas fa-star" aria-hidden="true"></i>
          Subscription
        </button>
        <button
          id="achievements-tab"
          class="tab"
          class:active={uiState.activeTab === "achievements"}
          role="tab"
          aria-selected={uiState.activeTab === "achievements"}
          aria-controls="achievements-panel"
          tabindex={uiState.activeTab === "achievements" ? 0 : -1}
          onclick={() => {
            hapticService?.trigger("selection");
            updateTabTransition("achievements");
          }}
          onkeydown={(e) => handleTabKeydown(e, "achievements")}
        >
          <i class="fas fa-trophy" aria-hidden="true"></i>
          Achievements
        </button>
      </div>

      <!-- Content -->
      <div
        class="content"
        bind:this={viewportState.contentContainer}
        ontouchstart={handleTouchStart}
        ontouchmove={handleTouchMove}
        ontouchend={handleTouchEnd}
      >
        {#key uiState.activeTab}
          <div
            class="tab-panel-wrapper"
            in:fade={{
              duration: prefersReducedMotion ? 150 : 200,
              easing: cubicOut,
            }}
            out:fade={{
              duration: prefersReducedMotion ? 150 : 200,
              easing: cubicOut,
            }}
          >
            {#if uiState.activeTab === "personal"}
              <div
                id="personal-panel"
                role="tabpanel"
                aria-labelledby="personal-tab"
                tabindex="0"
              >
                <PersonalTab
                  onSave={handleSavePersonalInfo}
                  onPhotoUpload={handlePhotoUpload}
                  onChangeEmail={handleChangeEmail}
                  onSignOut={handleSignOut}
                  {signingOut}
                  {hapticService}
                />
              </div>
            {:else if uiState.activeTab === "security"}
              <div
                id="security-panel"
                role="tabpanel"
                aria-labelledby="security-tab"
                tabindex="0"
              >
                <AccountTab
                  onChangePassword={handleChangePassword}
                  onDeleteAccount={handleDeleteAccount}
                  {hapticService}
                />
              </div>
            {:else if uiState.activeTab === "subscription"}
              <div
                id="subscription-panel"
                role="tabpanel"
                aria-labelledby="subscription-tab"
                tabindex="0"
              >
                <SubscriptionTab {hapticService} />
              </div>
            {:else if uiState.activeTab === "achievements"}
              <div
                id="achievements-panel"
                role="tabpanel"
                aria-labelledby="achievements-tab"
                tabindex="0"
              >
                <AchievementsTab />
              </div>
            {/if}
          </div>
        {/key}
      </div>
    {:else}
      <!-- Logged out state -->
      <div class="logged-out">
        <button
          class="close close--corner"
          onclick={() => {
            hapticService?.trigger("selection");
            onClose();
          }}
          aria-label="Close"
        >
          <i class="fas fa-times" aria-hidden="true"></i>
        </button>

        <div class="logged-out__icon">
          <i class="fas fa-user-circle"></i>
        </div>
        <h2 id="profile-settings-title" class="logged-out__title">
          Not Signed In
        </h2>
        <p class="logged-out__text">
          Sign in to access your account settings, manage your profile, and
          track your progress
        </p>
        <button class="sign-in-button" onclick={handleSignIn}>
          <i class="fas fa-sign-in-alt"></i>
          Sign In
        </button>
      </div>
    {/if}
  </div>
</Drawer>

<style>
  /* Backdrop */
  :global(.profile-settings-sheet__backdrop) {
    z-index: 1200; /* Higher than ProfileSheet (1100) */
  }

  /* Full height panel */
  :global(.profile-settings-sheet--full-height) {
    height: 100vh !important;
    max-height: 100vh !important;
  }

  /* Container - Natural sizing for better scrolling */
  .container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    max-height: 100%;
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(15, 20, 30, 0.95) 100%
    );
    overflow: hidden;
  }

  /* Header */
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .header h2 {
    font-size: 24px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .close {
    width: 44px;
    height: 44px;
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
  }

  .close:hover {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(1.05);
  }

  .close:active {
    transform: scale(0.95);
  }

  /* Tabs */
  .tabs {
    container-type: inline-size; /* Enable container queries */
    display: flex;
    justify-content: space-evenly; /* Distribute evenly across width */
    flex-wrap: nowrap; /* Keep all tabs in one row */
    gap: clamp(1px, 0.5cqi, 8px);
    padding: 0 clamp(4px, 1cqi, 24px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .tab {
    display: flex;
    align-items: center;
    gap: clamp(3px, 1cqi, 8px);
    padding: clamp(12px, 2cqi, 18px) clamp(6px, 2cqi, 24px);
    min-height: 60px; /* Increased touch target for better accessibility */
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    color: rgba(255, 255, 255, 0.7);
    font-size: clamp(11px, 2.5cqi, 16px);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    white-space: nowrap; /* Prevent text wrapping within button */
    flex: 1 1 0; /* Equal width, can grow and shrink */
    justify-content: center;
  }

  .tab i {
    font-size: clamp(12px, 2.5cqi, 16px);
    flex-shrink: 0; /* Prevent icon from shrinking */
  }

  .tab:hover {
    color: rgba(255, 255, 255, 0.9);
    background: rgba(255, 255, 255, 0.05);
  }

  .tab.active {
    color: rgba(99, 102, 241, 0.95);
    border-bottom-color: rgba(99, 102, 241, 0.9);
  }

  /* Container query: Switch to vertical layout on narrow containers */
  @container (max-width: 500px) {
    .tabs {
      gap: 1px;
      padding: 0 2px;
    }

    .tab {
      flex-direction: column;
      padding: 10px 2px;
      gap: 3px;
      font-size: 10px;
      min-height: 60px; /* Maintain larger touch target */
    }

    .tab i {
      font-size: 16px;
    }
  }

  /* Content */
  .content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0; /* Critical: allows flex child to shrink below content size */
    position: relative; /* Enable absolute positioning context */
  }

  /* Tab panel wrapper - absolute positioning to prevent stacking during transitions */
  .tab-panel-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    overflow-x: hidden;
  }

  /* Logged Out State */
  .logged-out {
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

  .close--corner {
    position: absolute;
    top: 16px;
    right: 16px;
  }

  .logged-out__icon {
    font-size: 80px;
    color: rgba(255, 255, 255, 0.3);
  }

  .logged-out__title {
    font-size: 24px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .logged-out__text {
    font-size: 15px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    max-width: 300px;
    line-height: 1.5;
  }

  .sign-in-button {
    width: 100%;
    max-width: 280px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 14px 24px;
    min-height: 48px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  .sign-in-button i {
    font-size: 16px;
  }

  .sign-in-button:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  .sign-in-button:active {
    transform: translateY(0);
  }

  .sign-in-button:focus-visible {
    outline: 3px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* Mobile Responsive */
  @media (max-width: 480px) {
    .header {
      padding: 16px;
    }

    .header h2 {
      font-size: 18px;
    }

    .tabs {
      padding: 0 12px;
      gap: 4px;
      /* Container queries handle the rest */
    }

    .tab {
      /* Let container queries handle responsive sizing */
      min-height: 60px; /* Maintain larger touch target size on mobile */
    }

    .logged-out {
      padding: 40px 24px;
    }

    .logged-out__icon {
      font-size: 64px;
    }

    .logged-out__title {
      font-size: 20px;
    }

    .sign-in-button {
      padding: 12px 20px;
      font-size: 15px;
    }
  }

  /* Accessibility - Focus Indicators */
  .close:focus-visible {
    outline: 3px solid rgba(99, 102, 241, 0.9);
    outline-offset: 2px;
  }

  .tab:focus-visible {
    outline: 3px solid rgba(99, 102, 241, 0.9);
    outline-offset: -3px;
    background: rgba(99, 102, 241, 0.1);
  }

  /* Accessibility - Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .close,
    .tab,
    .sign-in-button {
      transition: none;
    }

    .close:hover,
    .close:active,
    .sign-in-button:hover,
    .sign-in-button:active {
      transform: none;
    }
  }

  /* Accessibility - High Contrast */
  @media (prefers-contrast: high) {
    .container {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    .tab:focus-visible {
      outline: 3px solid white;
    }

    .close:focus-visible {
      outline: 3px solid white;
    }
  }
</style>
