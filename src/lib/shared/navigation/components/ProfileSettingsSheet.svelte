<!--
  ProfileSettingsSheet.svelte - Profile & Account Settings

  Features:
  - Personal Info (display name, email, profile photo)
  - Account Security (password, connected accounts)
  - Account Management (download data, delete account)
  - 95vh tall bottom sheet for complex forms
  - Route-aware (opens via /settings/account)
-->
<script lang="ts">
  import { authStore } from "$shared/auth";
  import { resolve, TYPES, type IHapticFeedbackService, BottomSheet } from "$shared";
  import { onMount } from "svelte";

  // Props
  let { isOpen = false, onClose } = $props<{
    isOpen?: boolean;
    onClose: () => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  // State
  let saving = $state(false);
  let uploadingPhoto = $state(false);
  let showDeleteConfirmation = $state(false);
  let showPasswordSection = $state(false);
  let activeTab = $state<'personal' | 'account'>('personal');

  // Reactive viewport tracking for adaptive layout
  let contentContainer: HTMLDivElement | null = $state(null);
  let availableHeight = $state(0);

  // Derive compact mode based on available height
  const isCompactMode = $derived(availableHeight > 0 && availableHeight < 600);
  const isVeryCompactMode = $derived(availableHeight > 0 && availableHeight < 500);

  // Form state (local copy for editing)
  let displayName = $state(authStore.user?.displayName || "");
  let email = $state(authStore.user?.email || "");
  let currentPassword = $state("");
  let newPassword = $state("");
  let confirmPassword = $state("");

  // Sync with authStore when it changes
  $effect(() => {
    if (authStore.user) {
      displayName = authStore.user.displayName || "";
      email = authStore.user.email || "";
    }
  });

  // Check if user has password authentication (email/password provider)
  const hasPasswordProvider = $derived.by(() => {
    if (!authStore.user?.providerData) return false;
    return authStore.user.providerData.some(
      (provider) => provider.providerId === 'password'
    );
  });

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Track content container size for adaptive layout
  $effect(() => {
    if (!contentContainer) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        availableHeight = entry.contentRect.height;
      }
    });

    resizeObserver.observe(contentContainer);

    return () => {
      resizeObserver.disconnect();
    };
  });

  async function handleSavePersonalInfo() {
    if (saving) return;

    hapticService?.trigger("selection");
    saving = true;

    try {
      // TODO: Implement profile update via Firebase
      // await authStore.updateProfile({ displayName });
      console.log("Saving personal info:", { displayName });

      hapticService?.trigger("success");
      alert("Profile updated successfully!");
    } catch (error) {
      console.error("Failed to update profile:", error);
      hapticService?.trigger("error");
      alert("Failed to update profile. Please try again.");
    } finally {
      saving = false;
    }
  }

  async function handlePhotoUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    hapticService?.trigger("selection");
    uploadingPhoto = true;

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
      uploadingPhoto = false;
    }
  }

  async function handleChangePassword() {
    if (saving) return;
    if (newPassword !== confirmPassword) {
      alert("Passwords don't match!");
      return;
    }

    hapticService?.trigger("selection");
    saving = true;

    try {
      // TODO: Implement password change via Firebase
      console.log("Changing password");

      hapticService?.trigger("success");
      alert("Password changed successfully!");
      currentPassword = "";
      newPassword = "";
      confirmPassword = "";
      showPasswordSection = false;
    } catch (error) {
      console.error("Failed to change password:", error);
      hapticService?.trigger("error");
      alert("Failed to change password. Please try again.");
    } finally {
      saving = false;
    }
  }

  async function handleDownloadData() {
    hapticService?.trigger("selection");

    try {
      // TODO: Implement data export
      console.log("Downloading user data");
      alert("Data export will be sent to your email.");
    } catch (error) {
      console.error("Failed to export data:", error);
      alert("Failed to export data. Please try again.");
    }
  }

  async function handleDeleteAccount() {
    if (!showDeleteConfirmation) {
      showDeleteConfirmation = true;
      return;
    }

    hapticService?.trigger("warning");

    const confirmed = confirm(
      "Are you absolutely sure? This action cannot be undone. All your data will be permanently deleted."
    );

    if (!confirmed) {
      showDeleteConfirmation = false;
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

  function triggerFileInput() {
    hapticService?.trigger("selection");
    document.getElementById("photo-upload")?.click();
  }
</script>

<BottomSheet
  {isOpen}
  labelledBy="profile-settings-title"
  on:close={onClose}
  class="profile-settings-sheet"
  backdropClass="profile-settings-sheet__backdrop"
>
  <div class="profile-settings__container">
    <!-- Header -->
    <header class="profile-settings__header">
      <h2 id="profile-settings-title">Account Settings</h2>
      <button
        class="profile-settings__close"
        onclick={onClose}
        aria-label="Close settings"
      >
        <i class="fas fa-times"></i>
      </button>
    </header>

    <!-- Tabs -->
    <div class="profile-settings__tabs">
      <button
        class="profile-settings__tab"
        class:active={activeTab === 'personal'}
        onclick={() => {
          hapticService?.trigger("selection");
          activeTab = 'personal';
        }}
      >
        <i class="fas fa-user"></i>
        Personal
      </button>
      <button
        class="profile-settings__tab"
        class:active={activeTab === 'account'}
        onclick={() => {
          hapticService?.trigger("selection");
          activeTab = 'account';
        }}
      >
        <i class="fas fa-cog"></i>
        Account
      </button>
    </div>

    <!-- Content -->
    <div class="profile-settings__content" bind:this={contentContainer}>
      <!-- Personal Info Tab -->
      {#if activeTab === 'personal'}
      <section
        class="profile-settings__section profile-settings__section--with-footer"
        class:compact={isCompactMode}
        class:very-compact={isVeryCompactMode}
      >
        <!-- Scrollable form content -->
        <div class="profile-settings__form-content">
          <h3 class="profile-settings__section-title">
            <i class="fas fa-user"></i>
            Personal Information
          </h3>

          <!-- Profile Photo -->
          <div
            class="profile-settings__photo-container"
            class:compact={isCompactMode}
            class:very-compact={isVeryCompactMode}
          >
            <div class="profile-settings__photo-wrapper">
              {#if authStore.user?.photoURL}
                <img
                  src={authStore.user.photoURL}
                  alt={authStore.user.displayName || "User"}
                  class="profile-settings__photo"
                />
              {:else}
                <div class="profile-settings__photo-placeholder">
                  {(displayName || email || "?").charAt(0).toUpperCase()}
                </div>
              {/if}
            </div>

            <div class="profile-settings__photo-info">
              <h4 class="profile-settings__photo-title">Profile Photo</h4>
              <p class="profile-settings__photo-hint">JPG, PNG or GIF. Max size 2MB.</p>
              <button
                class="profile-settings__photo-button"
                onclick={triggerFileInput}
                disabled={uploadingPhoto}
              >
                <i class="fas fa-camera"></i>
                {uploadingPhoto ? "Uploading..." : "Change Photo"}
              </button>
            </div>

            <input
              id="photo-upload"
              type="file"
              accept="image/*"
              onchange={handlePhotoUpload}
              style="display: none;"
            />
          </div>

          <!-- Display Name -->
          <div class="profile-settings__field">
            <label class="profile-settings__label" for="display-name">Display Name</label>
            <input
              id="display-name"
              type="text"
              class="profile-settings__input"
              bind:value={displayName}
              placeholder="Enter your display name"
            />
          </div>

          <!-- Email (read-only for now) -->
          <div class="profile-settings__field">
            <label class="profile-settings__label" for="email">Email</label>
            <input
              id="email"
              type="email"
              class="profile-settings__input"
              value={email}
              readonly
              disabled
            />
            <p class="profile-settings__hint">
              Email cannot be changed at this time
            </p>
          </div>
        </div>

        <!-- Sticky footer with save button -->
        <div class="profile-settings__footer">
          <button
            class="profile-settings__button profile-settings__button--primary"
            onclick={handleSavePersonalInfo}
            disabled={saving}
          >
            <i class="fas fa-save"></i>
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </div>
      </section>
      {/if}

      <!-- Account Tab -->
      {#if activeTab === 'account'}
      <section class="profile-settings__section profile-settings__section--account">
        <h3 class="profile-settings__section-title">
          <i class="fas fa-cog"></i>
          Account Management
        </h3>

        <!-- Connected Accounts -->
        <div class="profile-settings__connected-accounts">
          <h4 class="profile-settings__subsection-title">Connected Accounts</h4>
          {#if authStore.user?.providerData && authStore.user.providerData.length > 0}
            <div class="profile-settings__providers">
              {#each authStore.user.providerData as provider}
                <div class="profile-settings__provider">
                  <i class="fab fa-{provider.providerId === 'google.com' ? 'google' : provider.providerId}"></i>
                  <span>{provider.providerId === 'google.com' ? 'Google' : provider.providerId}</span>
                  <span class="profile-settings__provider-email">{provider.email}</span>
                </div>
              {/each}
            </div>
          {:else}
            <p class="profile-settings__hint">No connected accounts</p>
          {/if}
        </div>

        <!-- Change Password (only show for password-authenticated users) -->
        {#if hasPasswordProvider}
          <div class="profile-settings__password-section">
            <h4 class="profile-settings__subsection-title">Password</h4>
            {#if !showPasswordSection}
              <button
                class="profile-settings__button profile-settings__button--secondary"
                onclick={() => {
                  hapticService?.trigger("selection");
                  showPasswordSection = true;
                }}
              >
                <i class="fas fa-key"></i>
                Change Password
              </button>
            {:else}
              <div class="profile-settings__password-form">
                <div class="profile-settings__field">
                  <label class="profile-settings__label" for="current-password">
                    Current Password
                  </label>
                  <input
                    id="current-password"
                    type="password"
                    class="profile-settings__input"
                    bind:value={currentPassword}
                    placeholder="Enter current password"
                  />
                </div>

                <div class="profile-settings__field">
                  <label class="profile-settings__label" for="new-password">
                    New Password
                  </label>
                  <input
                    id="new-password"
                    type="password"
                    class="profile-settings__input"
                    bind:value={newPassword}
                    placeholder="Enter new password"
                  />
                </div>

                <div class="profile-settings__field">
                  <label class="profile-settings__label" for="confirm-password">
                    Confirm Password
                  </label>
                  <input
                    id="confirm-password"
                    type="password"
                    class="profile-settings__input"
                    bind:value={confirmPassword}
                    placeholder="Confirm new password"
                  />
                </div>

                <div class="profile-settings__button-row">
                  <button
                    class="profile-settings__button profile-settings__button--secondary"
                    onclick={() => {
                      hapticService?.trigger("selection");
                      showPasswordSection = false;
                      currentPassword = "";
                      newPassword = "";
                      confirmPassword = "";
                    }}
                  >
                    Cancel
                  </button>
                  <button
                    class="profile-settings__button profile-settings__button--primary"
                    onclick={handleChangePassword}
                    disabled={saving || !currentPassword || !newPassword || !confirmPassword}
                  >
                    <i class="fas fa-check"></i>
                    Update Password
                  </button>
                </div>
              </div>
            {/if}
          </div>
        {/if}

        <!-- Data Export -->
        <div class="profile-settings__data-section">
          <h4 class="profile-settings__subsection-title">Your Data</h4>
          <button
            class="profile-settings__button profile-settings__button--secondary"
            onclick={handleDownloadData}
          >
            <i class="fas fa-download"></i>
            Download My Data
          </button>
        </div>

        <!-- Danger Zone -->
        <div class="profile-settings__danger-zone">
          <h4 class="profile-settings__danger-title">Danger Zone</h4>
          <p class="profile-settings__danger-text">
            Once you delete your account, there is no going back. Please be certain.
          </p>

          {#if !showDeleteConfirmation}
            <button
              class="profile-settings__button profile-settings__button--danger"
              onclick={handleDeleteAccount}
            >
              <i class="fas fa-trash-alt"></i>
              Delete Account
            </button>
          {:else}
            <div class="profile-settings__delete-confirmation">
              <p class="profile-settings__delete-warning">
                <i class="fas fa-exclamation-circle"></i>
                Are you sure? This action cannot be undone!
              </p>
              <div class="profile-settings__button-row">
                <button
                  class="profile-settings__button profile-settings__button--secondary"
                  onclick={() => {
                    hapticService?.trigger("selection");
                    showDeleteConfirmation = false;
                  }}
                >
                  Cancel
                </button>
                <button
                  class="profile-settings__button profile-settings__button--danger"
                  onclick={handleDeleteAccount}
                >
                  <i class="fas fa-trash-alt"></i>
                  Yes, Delete My Account
                </button>
              </div>
            </div>
          {/if}
        </div>
      </section>
      {/if}
    </div>
  </div>
</BottomSheet>

<style>
  /* Backdrop */
  :global(.profile-settings-sheet__backdrop) {
    z-index: 1200; /* Higher than ProfileSheet (1100) */
  }

  /* Container - 95vh for complex forms */
  .profile-settings__container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 95vh;
    max-height: 95vh;
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(15, 20, 30, 0.95) 100%
    );
    overflow: hidden;
  }

  /* Header */
  .profile-settings__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .profile-settings__header h2 {
    font-size: 24px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .profile-settings__close {
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

  .profile-settings__close:hover {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(1.05);
  }

  .profile-settings__close:active {
    transform: scale(0.95);
  }

  /* Tabs */
  .profile-settings__tabs {
    display: flex;
    justify-content: center;
    gap: 8px;
    padding: 0 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .profile-settings__tab {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 14px 20px;
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    color: rgba(255, 255, 255, 0.6);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
  }

  .profile-settings__tab i {
    font-size: 16px;
  }

  .profile-settings__tab:hover {
    color: rgba(255, 255, 255, 0.9);
    background: rgba(255, 255, 255, 0.05);
  }

  .profile-settings__tab.active {
    color: rgba(99, 102, 241, 0.95);
    border-bottom-color: rgba(99, 102, 241, 0.9);
  }

  /* Content */
  .profile-settings__content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0; /* Critical: allows flex child to shrink below content size */
  }

  /* Sections */
  .profile-settings__section {
    min-height: 100%;
    display: flex;
    flex-direction: column;
  }

  /* Section with sticky footer (Personal tab) */
  .profile-settings__section--with-footer {
    height: 100%;
    min-height: 100%;
  }

  /* Account section with padding */
  .profile-settings__section--account {
    padding: 24px;
    min-height: auto;
  }

  .profile-settings__section:last-child {
    border-bottom: none;
  }

  .profile-settings__section-title {
    display: none; /* Hide section titles since tabs show them */
  }

  /* Scrollable form content area */
  .profile-settings__form-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 24px;
    min-height: 0;
    transition: padding 0.2s ease;
  }

  /* Adaptive form content padding */
  .profile-settings__section.compact .profile-settings__form-content {
    padding: 18px;
  }

  .profile-settings__section.very-compact .profile-settings__form-content {
    padding: 12px;
  }

  /* Sticky footer */
  .profile-settings__footer {
    flex-shrink: 0;
    padding: 16px 24px;
    background: linear-gradient(
      to top,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(20, 25, 35, 0.95) 50%,
      rgba(20, 25, 35, 0) 100%
    );
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    transition: padding 0.2s ease;
  }

  /* Adaptive footer padding */
  .profile-settings__section.compact .profile-settings__footer {
    padding: 14px 18px;
  }

  .profile-settings__section.very-compact .profile-settings__footer {
    padding: 10px 12px;
  }

  /* Footer button should not have top margin since it's in a footer */
  .profile-settings__footer .profile-settings__button {
    margin-top: 0;
  }

  /* Fields */
  .profile-settings__field {
    margin-bottom: 20px;
  }

  .profile-settings__section.compact .profile-settings__field {
    margin-bottom: 14px;
  }

  .profile-settings__section.very-compact .profile-settings__field {
    margin-bottom: 10px;
  }

  .profile-settings__label {
    display: block;
    font-size: 14px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 8px;
    transition: all 0.2s ease;
  }

  .profile-settings__section.compact .profile-settings__label {
    font-size: 13px;
    margin-bottom: 6px;
  }

  .profile-settings__section.very-compact .profile-settings__label {
    font-size: 12px;
    margin-bottom: 4px;
  }

  .profile-settings__input {
    width: 100%;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.95);
    font-size: 15px;
    transition: all 0.2s ease;
  }

  .profile-settings__section.compact .profile-settings__input {
    padding: 10px 14px;
    font-size: 14px;
    border-radius: 6px;
  }

  .profile-settings__section.very-compact .profile-settings__input {
    padding: 8px 12px;
    font-size: 13px;
    border-radius: 6px;
  }

  .profile-settings__input:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.6);
    background: rgba(255, 255, 255, 0.08);
  }

  .profile-settings__input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .profile-settings__hint {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
    margin: 6px 0 0 0;
    transition: all 0.2s ease;
  }

  .profile-settings__section.compact .profile-settings__hint {
    font-size: 12px;
    margin: 4px 0 0 0;
  }

  .profile-settings__section.very-compact .profile-settings__hint {
    font-size: 11px;
    margin: 3px 0 0 0;
  }

  /* Photo Container - Horizontal Layout */
  .profile-settings__photo-container {
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    margin-bottom: 24px;
    transition: all 0.2s ease;
  }

  /* Adaptive compact mode - reduces size and spacing */
  .profile-settings__photo-container.compact {
    gap: 16px;
    padding: 14px;
    margin-bottom: 16px;
  }

  .profile-settings__photo-container.very-compact {
    gap: 12px;
    padding: 10px;
    margin-bottom: 12px;
  }

  .profile-settings__photo-wrapper {
    flex-shrink: 0;
  }

  .profile-settings__photo {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid rgba(255, 255, 255, 0.15);
    display: block;
    transition: all 0.2s ease;
  }

  .profile-settings__photo-container.compact .profile-settings__photo {
    width: 72px;
    height: 72px;
    border-width: 2px;
  }

  .profile-settings__photo-container.very-compact .profile-settings__photo {
    width: 60px;
    height: 60px;
    border-width: 2px;
  }

  .profile-settings__photo-placeholder {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    font-weight: 600;
    color: white;
    border: 3px solid rgba(255, 255, 255, 0.15);
    transition: all 0.2s ease;
  }

  .profile-settings__photo-container.compact .profile-settings__photo-placeholder {
    width: 72px;
    height: 72px;
    font-size: 28px;
    border-width: 2px;
  }

  .profile-settings__photo-container.very-compact .profile-settings__photo-placeholder {
    width: 60px;
    height: 60px;
    font-size: 24px;
    border-width: 2px;
  }

  .profile-settings__photo-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
    transition: gap 0.2s ease;
  }

  .profile-settings__photo-container.compact .profile-settings__photo-info {
    gap: 6px;
  }

  .profile-settings__photo-container.very-compact .profile-settings__photo-info {
    gap: 4px;
  }

  .profile-settings__photo-title {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
    transition: font-size 0.2s ease;
  }

  .profile-settings__photo-container.compact .profile-settings__photo-title {
    font-size: 15px;
  }

  .profile-settings__photo-container.very-compact .profile-settings__photo-title {
    font-size: 14px;
  }

  .profile-settings__photo-hint {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
    margin: 0;
    transition: font-size 0.2s ease;
  }

  .profile-settings__photo-container.compact .profile-settings__photo-hint {
    font-size: 12px;
  }

  .profile-settings__photo-container.very-compact .profile-settings__photo-hint {
    font-size: 11px;
  }

  .profile-settings__photo-button {
    align-self: flex-start;
    padding: 10px 20px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 4px;
  }

  .profile-settings__photo-container.compact .profile-settings__photo-button {
    padding: 8px 16px;
    font-size: 13px;
    gap: 6px;
    border-radius: 6px;
    margin-top: 2px;
  }

  .profile-settings__photo-container.very-compact .profile-settings__photo-button {
    padding: 6px 14px;
    font-size: 12px;
    gap: 5px;
    border-radius: 6px;
    margin-top: 0;
  }

  .profile-settings__photo-button:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-1px);
  }

  .profile-settings__photo-button:active:not(:disabled) {
    transform: translateY(0);
  }

  .profile-settings__photo-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Buttons */
  .profile-settings__button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 14px 24px;
    min-height: 48px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    margin-top: 8px;
  }

  .profile-settings__section.compact .profile-settings__button {
    padding: 12px 20px;
    min-height: 42px;
    font-size: 14px;
    gap: 8px;
    border-radius: 8px;
    margin-top: 6px;
  }

  .profile-settings__section.very-compact .profile-settings__button {
    padding: 10px 18px;
    min-height: 38px;
    font-size: 13px;
    gap: 6px;
    border-radius: 8px;
    margin-top: 4px;
  }

  .profile-settings__button i {
    font-size: 16px;
    transition: font-size 0.2s ease;
  }

  .profile-settings__section.compact .profile-settings__button i {
    font-size: 14px;
  }

  .profile-settings__section.very-compact .profile-settings__button i {
    font-size: 13px;
  }

  .profile-settings__button--primary {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  .profile-settings__button--primary:hover:not(:disabled) {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  .profile-settings__button--secondary {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.15);
  }

  .profile-settings__button--secondary:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.25);
  }

  .profile-settings__button--danger {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 2px solid rgba(239, 68, 68, 0.3);
  }

  .profile-settings__button--danger:hover:not(:disabled) {
    background: rgba(239, 68, 68, 0.25);
    border-color: rgba(239, 68, 68, 0.5);
  }

  .profile-settings__button:active:not(:disabled) {
    transform: scale(0.98);
  }

  .profile-settings__button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  .profile-settings__button-row {
    display: flex;
    gap: 12px;
    margin-top: 16px;
  }

  .profile-settings__button-row .profile-settings__button {
    width: auto;
    flex: 1;
    margin-top: 0;
  }

  /* Password Form */
  .profile-settings__password-form {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
  }

  /* Account Tab Sections */
  .profile-settings__connected-accounts,
  .profile-settings__password-section,
  .profile-settings__data-section {
    margin-top: 24px;
    padding-top: 24px;
  }

  .profile-settings__connected-accounts {
    padding-top: 0;
    margin-top: 0;
  }

  .profile-settings__password-section,
  .profile-settings__data-section {
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .profile-settings__subsection-title {
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin: 0 0 12px 0;
  }

  .profile-settings__providers {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .profile-settings__provider {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
  }

  .profile-settings__provider i {
    font-size: 20px;
    color: rgba(255, 255, 255, 0.7);
  }

  .profile-settings__provider-email {
    margin-left: auto;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
  }

  /* Danger Zone */
  .profile-settings__danger-zone {
    background: rgba(239, 68, 68, 0.05);
    border: 2px solid rgba(239, 68, 68, 0.2);
    border-radius: 12px;
    padding: 20px;
    margin-top: 20px;
  }

  .profile-settings__danger-title {
    font-size: 16px;
    font-weight: 600;
    color: #ef4444;
    margin: 0 0 8px 0;
  }

  .profile-settings__danger-text {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    margin: 0 0 16px 0;
  }

  .profile-settings__delete-confirmation {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 8px;
    padding: 16px;
  }

  .profile-settings__delete-warning {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    color: #ef4444;
    margin: 0 0 16px 0;
    font-weight: 500;
  }

  .profile-settings__delete-warning i {
    font-size: 18px;
  }

  /* Responsive */
  @media (max-width: 480px) {
    .profile-settings__container {
      height: 98vh;
      max-height: 98vh;
    }

    .profile-settings__header {
      padding: 16px;
    }

    .profile-settings__header h2 {
      font-size: 18px;
    }

    .profile-settings__tabs {
      padding: 0 16px;
      gap: 4px;
    }

    .profile-settings__tab {
      padding: 12px 12px;
      font-size: 12px;
      gap: 6px;
    }

    .profile-settings__tab i {
      font-size: 14px;
    }

    .profile-settings__form-content {
      padding: 16px;
    }

    .profile-settings__footer {
      padding: 12px 16px;
    }

    .profile-settings__button-row {
      flex-direction: column;
    }

    .profile-settings__button-row .profile-settings__button {
      width: 100%;
    }

    .profile-settings__photo-container {
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 16px;
      gap: 16px;
    }

    .profile-settings__photo-info {
      align-items: center;
    }

    .profile-settings__photo-button {
      align-self: stretch;
    }
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .profile-settings__close,
    .profile-settings__button,
    .profile-settings__tab {
      transition: none;
    }

    .profile-settings__close:hover,
    .profile-settings__close:active,
    .profile-settings__button:hover,
    .profile-settings__button:active {
      transform: none;
    }
  }

  @media (prefers-contrast: high) {
    .profile-settings__container {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    .profile-settings__input {
      border-color: rgba(255, 255, 255, 0.5);
    }
  }
</style>
