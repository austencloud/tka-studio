<!--
  PersonalTab Component

  Handles personal information editing: profile photo, display name, email.
  Features sticky footer with save button and adaptive layout.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { authStore } from "$shared/auth";
  import {
    personalInfoState,
    originalPersonalInfoState,
    uiState,
    isCompactMode,
    isVeryCompactMode,
    canChangeEmail,
    hasPersonalInfoChanges,
  } from "../../state/profile-settings-state.svelte";
  import ProfilePhotoUpload from "./ProfilePhotoUpload.svelte";
  import EmailChangeSection from "./EmailChangeSection.svelte";
  import { slide } from "svelte/transition";

  let {
    onSave,
    onPhotoUpload,
    onChangeEmail,
    onSignOut,
    signingOut,
    hapticService,
  } = $props<{
    onSave: () => Promise<void>;
    onPhotoUpload: (file: File) => Promise<void>;
    onChangeEmail: () => Promise<void>;
    onSignOut: () => Promise<void>;
    signingOut: boolean;
    hapticService: IHapticFeedbackService | null;
  }>();

  // Sync with auth store
  $effect(() => {
    if (authStore.user) {
      const displayName = authStore.user.displayName || "";
      const email = authStore.user.email || "";

      personalInfoState.displayName = displayName;
      personalInfoState.email = email;

      // Update original values to track changes
      originalPersonalInfoState.displayName = displayName;
      originalPersonalInfoState.email = email;
    }
  });
</script>

<section
  class="section section--with-footer"
  class:compact={isCompactMode()}
  class:very-compact={isVeryCompactMode()}
>
  <!-- Scrollable form content -->
  <div class="form-content">
    <h3 class="section-title">
      <i class="fas fa-user"></i>
      Personal Information
    </h3>

    <!-- Profile Photo -->
    <ProfilePhotoUpload {onPhotoUpload} {hapticService} />

    <!-- Display Name -->
    <div class="field">
      <label class="label" for="display-name">Display Name</label>
      <input
        id="display-name"
        type="text"
        class="input"
        bind:value={personalInfoState.displayName}
        placeholder="Enter your display name"
      />
    </div>

    <!-- Email Section -->
    <div class="field">
      <label class="label" for="email">Email</label>
      {#if !uiState.showEmailChangeSection}
        <div class="email-field-wrapper">
          <input
            id="email"
            type="email"
            class="input input--readonly"
            value={personalInfoState.email}
            readonly
            aria-readonly="true"
          />
          {#if canChangeEmail()}
            <button
              class="button button--link"
              onclick={() => {
                hapticService?.trigger("selection");
                uiState.showEmailChangeSection = true;
              }}
              type="button"
            >
              <i class="fas fa-edit" aria-hidden="true"></i>
              Change Email
            </button>
          {:else}
            <p class="hint">Email is managed by your authentication provider</p>
          {/if}
        </div>
      {:else}
        <EmailChangeSection
          {onChangeEmail}
          onCancel={() => {
            uiState.showEmailChangeSection = false;
          }}
          {hapticService}
        />
      {/if}
    </div>

    <!-- Sign Out Section -->
    <div class="sign-out-section">
      <button
        class="sign-out-button"
        onclick={onSignOut}
        disabled={signingOut}
        aria-busy={signingOut}
      >
        <i class="fas fa-sign-out-alt" aria-hidden="true"></i>
        {signingOut ? "Signing out..." : "Sign Out"}
      </button>
    </div>
  </div>

  <!-- Sticky footer with save button - only shown when there are changes -->
  {#if hasPersonalInfoChanges()}
    <div class="footer" transition:slide={{ duration: 200 }}>
      <button
        class="button button--primary"
        onclick={onSave}
        disabled={uiState.saving}
        aria-busy={uiState.saving}
      >
        <i class="fas fa-save" aria-hidden="true"></i>
        {uiState.saving ? "Saving..." : "Save Changes"}
      </button>
    </div>
  {/if}
</section>

<style>
  /* Section Layout */
  .section {
    min-height: 100%;
    display: flex;
    flex-direction: column;
  }

  .section--with-footer {
    height: 100%;
    min-height: 100%;
  }

  .section-title {
    display: none; /* Hide since tabs show the title */
  }

  .form-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: clamp(16px, 3vh, 32px) clamp(20px, 4vw, 48px); /* Fluid padding */
    min-height: 0;
    transition: padding 0.2s ease;
    display: flex;
    flex-direction: column;
    align-items: center; /* Center form fields horizontally */
    justify-content: center; /* Center vertically when there's space */
  }

  .section.compact .form-content {
    padding: 18px;
  }

  .section.very-compact .form-content {
    padding: 12px;
  }

  .footer {
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

  .section.compact .footer {
    padding: 14px 18px;
  }

  .section.very-compact .footer {
    padding: 10px 12px;
  }

  .footer :global(.button) {
    margin-top: 0;
  }

  /* Form Fields */
  :global(.field) {
    margin-bottom: clamp(16px, 3vh, 24px); /* Fluid vertical spacing */
    width: 100%;
    max-width: min(800px, 80vw); /* Responsive width - adapts to viewport */
    text-align: center; /* Center labels and hints */
  }

  .section.compact :global(.field) {
    margin-bottom: 14px;
  }

  .section.very-compact :global(.field) {
    margin-bottom: 10px;
  }

  :global(.label) {
    display: block;
    font-size: clamp(13px, 1.8vh, 16px); /* Fluid font sizing */
    font-weight: 500;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: clamp(6px, 1vh, 10px);
    transition: all 0.2s ease;
  }

  .section.compact :global(.label) {
    font-size: 13px;
    margin-bottom: 6px;
  }

  .section.very-compact :global(.label) {
    font-size: 12px;
    margin-bottom: 4px;
  }

  :global(.input) {
    width: 100%;
    padding: clamp(10px, 1.5vh, 14px) clamp(14px, 2vh, 18px);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.95);
    font-size: clamp(14px, 1.9vh, 17px); /* Fluid font size */
    transition: all 0.2s ease;
  }

  .section.compact :global(.input) {
    padding: 10px 14px;
    font-size: 14px;
    border-radius: 6px;
  }

  .section.very-compact :global(.input) {
    padding: 8px 12px;
    font-size: 13px;
    border-radius: 6px;
  }

  :global(.input:focus) {
    outline: none;
    border-color: rgba(99, 102, 241, 0.6);
    background: rgba(255, 255, 255, 0.08);
  }

  :global(.input:disabled),
  :global(.input--readonly) {
    opacity: 0.5;
    cursor: not-allowed;
  }

  :global(.input--readonly) {
    background: rgba(255, 255, 255, 0.02);
  }

  .email-field-wrapper {
    display: flex;
    flex-direction: column;
    gap: clamp(8px, 1.2vh, 12px);
  }

  .section.compact .email-field-wrapper {
    gap: 8px;
  }

  .section.very-compact .email-field-wrapper {
    gap: 6px;
  }

  /* Sign Out Section */
  .sign-out-section {
    width: 100%;
    max-width: min(800px, 80vw);
    margin-top: clamp(20px, 3vh, 32px);
    padding-top: clamp(20px, 3vh, 32px);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .section.compact .sign-out-section {
    margin-top: 20px;
    padding-top: 20px;
  }

  .section.very-compact .sign-out-section {
    margin-top: 16px;
    padding-top: 16px;
  }

  .sign-out-button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(8px, 1.2vh, 12px);
    padding: clamp(12px, 1.8vh, 16px) clamp(20px, 3vw, 28px);
    min-height: 48px;
    border-radius: 10px;
    font-size: clamp(14px, 1.9vh, 17px);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid rgba(239, 68, 68, 0.4);
    background: rgba(239, 68, 68, 0.1);
    color: rgba(239, 68, 68, 0.95);
  }

  .section.compact .sign-out-button {
    padding: 11px 20px;
    min-height: 44px;
    font-size: 14px;
    gap: 8px;
    border-radius: 8px;
  }

  .section.very-compact .sign-out-button {
    padding: 11px 18px;
    min-height: 44px;
    font-size: 13px;
    gap: 6px;
    border-radius: 8px;
  }

  .sign-out-button i {
    font-size: 16px;
  }

  .section.compact .sign-out-button i {
    font-size: 14px;
  }

  .section.very-compact .sign-out-button i {
    font-size: 13px;
  }

  .sign-out-button:hover:not(:disabled) {
    background: rgba(239, 68, 68, 0.2);
    border-color: rgba(239, 68, 68, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  }

  .sign-out-button:active:not(:disabled) {
    transform: scale(0.98);
  }

  .sign-out-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  .sign-out-button:focus-visible {
    outline: 3px solid rgba(239, 68, 68, 0.7);
    outline-offset: 2px;
  }

  :global(.hint) {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.65); /* Improved contrast for WCAG AA */
    margin: 6px 0 0 0;
    transition: all 0.2s ease;
  }

  .section.compact :global(.hint) {
    font-size: 12px;
    margin: 4px 0 0 0;
  }

  .section.very-compact :global(.hint) {
    font-size: 11px;
    margin: 3px 0 0 0;
  }

  /* Button */
  :global(.button) {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(8px, 1.2vh, 12px);
    padding: clamp(12px, 1.8vh, 16px) clamp(20px, 3vw, 28px);
    min-height: 48px; /* WCAG minimum maintained */
    border-radius: 10px;
    font-size: clamp(14px, 1.9vh, 17px);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    margin-top: clamp(6px, 1vh, 10px);
  }

  .section.compact :global(.button) {
    padding: 11px 20px;
    min-height: 44px; /* WCAG 2.1 AA minimum touch target size */
    font-size: 14px;
    gap: 8px;
    border-radius: 8px;
    margin-top: 6px;
  }

  .section.very-compact :global(.button) {
    padding: 11px 18px;
    min-height: 44px; /* WCAG 2.1 AA minimum touch target size */
    font-size: 13px;
    gap: 6px;
    border-radius: 8px;
    margin-top: 4px;
  }

  :global(.button i) {
    font-size: 16px;
    transition: font-size 0.2s ease;
  }

  .section.compact :global(.button i) {
    font-size: 14px;
  }

  .section.very-compact :global(.button i) {
    font-size: 13px;
  }

  :global(.button--primary) {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  :global(.button--primary:hover:not(:disabled)) {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  :global(.button:active:not(:disabled)) {
    transform: scale(0.98);
  }

  :global(.button:disabled) {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  :global(.button--link) {
    background: transparent;
    color: rgba(99, 102, 241, 0.9);
    box-shadow: none;
    padding: clamp(8px, 1.2vh, 10px) 0;
    min-height: auto;
    justify-content: flex-start;
    font-size: clamp(13px, 1.8vh, 15px);
  }

  .section.compact :global(.button--link) {
    padding: 8px 0;
    font-size: 13px;
  }

  .section.very-compact :global(.button--link) {
    padding: 6px 0;
    font-size: 12px;
  }

  :global(.button--link:hover:not(:disabled)) {
    background: transparent;
    color: rgba(99, 102, 241, 1);
    transform: none;
    box-shadow: none;
    text-decoration: underline;
  }

  :global(.button--link:active:not(:disabled)) {
    transform: scale(0.98);
  }

  /* Mobile Responsive */
  @media (max-width: 480px) {
    .form-content {
      padding: 16px;
    }

    .footer {
      padding: 12px 16px;
    }
  }

  /* Accessibility - Focus Indicators */
  :global(.input:focus-visible) {
    outline: 3px solid rgba(99, 102, 241, 0.9);
    outline-offset: 2px;
  }

  :global(.button:focus-visible) {
    outline: 3px solid rgba(99, 102, 241, 0.9);
    outline-offset: 2px;
  }

  /* Accessibility - Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    :global(.button) {
      transition: none;
    }

    :global(.button:hover),
    :global(.button:active) {
      transform: none;
    }
  }

  /* Accessibility - High Contrast */
  @media (prefers-contrast: high) {
    :global(.input:focus-visible) {
      outline: 3px solid white;
    }

    :global(.button:focus-visible) {
      outline: 3px solid white;
    }

    .sign-out-button:focus-visible {
      outline: 3px solid white;
    }
  }
</style>
