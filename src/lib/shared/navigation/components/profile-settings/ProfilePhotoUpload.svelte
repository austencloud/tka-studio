<!--
  ProfilePhotoUpload Component

  Displays user profile photo with upload functionality.
  Features horizontal layout with photo preview and upload button.
-->
<script lang="ts">
  import { authStore } from "$shared/auth";
  import type { IHapticFeedbackService } from "$shared";
  import { isCompactMode, isVeryCompactMode, uiState } from "../../state/profile-settings-state.svelte";

  let {
    onPhotoUpload,
    hapticService
  } = $props<{
    onPhotoUpload: (file: File) => Promise<void>;
    hapticService: IHapticFeedbackService | null;
  }>();

  let displayName = $derived(authStore.user?.displayName || "");
  let email = $derived(authStore.user?.email || "");

  function triggerFileInput() {
    hapticService?.trigger("selection");
    document.getElementById("photo-upload")?.click();
  }

  async function handlePhotoUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    await onPhotoUpload(file);
  }
</script>

<div
  class="photo-container"
  class:compact={isCompactMode}
  class:very-compact={isVeryCompactMode}
>
  <div class="photo-wrapper">
    {#if authStore.user?.photoURL}
      <img
        src={authStore.user.photoURL}
        alt={authStore.user.displayName || "User"}
        class="photo"
      />
    {:else}
      <div class="photo-placeholder">
        {(displayName || email || "?").charAt(0).toUpperCase()}
      </div>
    {/if}
  </div>

  <div class="photo-info">
    <h4 class="photo-title">Profile Photo</h4>
    <p class="photo-hint">JPG, PNG or GIF. Max size 2MB.</p>
    <button
      class="photo-button"
      onclick={triggerFileInput}
      disabled={uiState.uploadingPhoto}
    >
      <i class="fas fa-camera"></i>
      {uiState.uploadingPhoto ? "Uploading..." : "Change Photo"}
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

<style>
  @import "./profile-settings-shared.css";
</style>
