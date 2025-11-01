<!--
  EmailChangeSection Component

  Handles email change for password-authenticated users.
  Requires password re-authentication for security.
  Sends verification email to new address.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import {
    emailChangeState,
    uiState,
    isCompactMode,
    isVeryCompactMode,
  } from "../../state/profile-settings-state.svelte";

  let { onChangeEmail, onCancel, hapticService } = $props<{
    onChangeEmail: () => Promise<void>;
    onCancel: () => void;
    hapticService: IHapticFeedbackService | null;
  }>();

  // Validation state
  let emailError = $state("");
  let passwordError = $state("");

  function validateEmail() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailChangeState.newEmail) {
      emailError = "Email is required";
      return false;
    }
    if (!emailRegex.test(emailChangeState.newEmail)) {
      emailError = "Please enter a valid email address";
      return false;
    }
    emailError = "";
    return true;
  }

  function validatePassword() {
    if (!emailChangeState.password) {
      passwordError = "Password is required for verification";
      return false;
    }
    passwordError = "";
    return true;
  }

  async function handleSubmit() {
    const emailValid = validateEmail();
    const passwordValid = validatePassword();

    if (!emailValid || !passwordValid) {
      return;
    }

    await onChangeEmail();
  }

  function handleCancel() {
    hapticService?.trigger("selection");
    onCancel();
  }
</script>

<div
  class="email-change-section"
  class:compact={isCompactMode()}
  class:very-compact={isVeryCompactMode()}
>
  <div class="section-header">
    <i class="fas fa-envelope" aria-hidden="true"></i>
    <h4>Change Email Address</h4>
  </div>

  <p class="description">
    Enter your new email address and current password to verify this change.
    We'll send a verification email to your new address.
  </p>

  <!-- New Email -->
  <div class="field">
    <label class="label" for="new-email">New Email Address</label>
    <input
      id="new-email"
      type="email"
      class="input"
      class:error={emailError}
      bind:value={emailChangeState.newEmail}
      onblur={validateEmail}
      placeholder="Enter new email address"
      disabled={uiState.changingEmail}
      aria-invalid={!!emailError}
      aria-describedby={emailError ? "new-email-error" : undefined}
    />
    {#if emailError}
      <p id="new-email-error" class="error-message" role="alert">
        <i class="fas fa-exclamation-circle"></i>
        {emailError}
      </p>
    {/if}
  </div>

  <!-- Current Password -->
  <div class="field">
    <label class="label" for="verify-password">Current Password</label>
    <input
      id="verify-password"
      type="password"
      class="input"
      class:error={passwordError}
      bind:value={emailChangeState.password}
      onblur={validatePassword}
      placeholder="Enter your current password"
      disabled={uiState.changingEmail}
      aria-invalid={!!passwordError}
      aria-describedby={passwordError ? "verify-password-error" : undefined}
    />
    {#if passwordError}
      <p id="verify-password-error" class="error-message" role="alert">
        <i class="fas fa-exclamation-circle"></i>
        {passwordError}
      </p>
    {/if}
  </div>

  <!-- Action Buttons -->
  <div class="actions">
    <button
      class="button button--secondary"
      onclick={handleCancel}
      disabled={uiState.changingEmail}
    >
      <i class="fas fa-times"></i>
      Cancel
    </button>
    <button
      class="button button--primary"
      onclick={handleSubmit}
      disabled={uiState.changingEmail}
      aria-busy={uiState.changingEmail}
    >
      <i class="fas fa-paper-plane"></i>
      {uiState.changingEmail ? "Sending..." : "Send Verification Email"}
    </button>
  </div>
</div>

<style>
  .email-change-section {
    padding: clamp(18px, 3vh, 28px);
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(12px, 2vh, 18px);
    transition: all 0.2s ease;
  }

  .email-change-section.compact {
    padding: 18px;
    border-radius: 12px;
  }

  .email-change-section.very-compact {
    padding: 14px;
    border-radius: 10px;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: clamp(10px, 1.5vh, 14px);
    margin-bottom: clamp(12px, 2vh, 16px);
  }

  .section-header i {
    font-size: clamp(18px, 2.5vh, 22px);
    color: rgba(99, 102, 241, 0.8);
  }

  .email-change-section.compact .section-header i {
    font-size: 18px;
  }

  .email-change-section.very-compact .section-header i {
    font-size: 16px;
  }

  .section-header h4 {
    font-size: clamp(16px, 2.2vh, 20px);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .email-change-section.compact .section-header h4 {
    font-size: 16px;
  }

  .email-change-section.very-compact .section-header h4 {
    font-size: 15px;
  }

  .description {
    font-size: clamp(13px, 1.8vh, 15px);
    color: rgba(255, 255, 255, 0.65);
    margin: 0 0 clamp(16px, 2.5vh, 24px) 0;
    line-height: 1.5;
  }

  .email-change-section.compact .description {
    font-size: 13px;
    margin-bottom: 16px;
  }

  .email-change-section.very-compact .description {
    font-size: 12px;
    margin-bottom: 12px;
  }

  /* Form Fields */
  .field {
    margin-bottom: clamp(16px, 3vh, 24px);
  }

  .email-change-section.compact .field {
    margin-bottom: 14px;
  }

  .email-change-section.very-compact .field {
    margin-bottom: 10px;
  }

  .label {
    display: block;
    font-size: clamp(13px, 1.8vh, 16px);
    font-weight: 500;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: clamp(6px, 1vh, 10px);
  }

  .email-change-section.compact .label {
    font-size: 13px;
    margin-bottom: 6px;
  }

  .email-change-section.very-compact .label {
    font-size: 12px;
    margin-bottom: 4px;
  }

  .input {
    width: 100%;
    padding: clamp(10px, 1.5vh, 14px) clamp(14px, 2vh, 18px);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.95);
    font-size: clamp(14px, 1.9vh, 17px);
    transition: all 0.2s ease;
  }

  .email-change-section.compact .input {
    padding: 10px 14px;
    font-size: 14px;
    border-radius: 6px;
  }

  .email-change-section.very-compact .input {
    padding: 8px 12px;
    font-size: 13px;
    border-radius: 6px;
  }

  .input:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.6);
    background: rgba(255, 255, 255, 0.08);
  }

  .input.error {
    border-color: rgba(239, 68, 68, 0.6);
  }

  .input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .error-message {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: rgba(239, 68, 68, 0.9);
    margin: 6px 0 0 0;
  }

  .email-change-section.compact .error-message {
    font-size: 12px;
    margin: 4px 0 0 0;
  }

  .email-change-section.very-compact .error-message {
    font-size: 11px;
    margin: 3px 0 0 0;
  }

  .error-message i {
    font-size: 12px;
  }

  /* Actions */
  .actions {
    display: flex;
    gap: 12px;
    margin-top: clamp(20px, 3vh, 28px);
  }

  .email-change-section.compact .actions {
    gap: 10px;
    margin-top: 18px;
  }

  .email-change-section.very-compact .actions {
    gap: 8px;
    margin-top: 14px;
  }

  .button {
    flex: 1;
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
    border: none;
  }

  .email-change-section.compact .button {
    padding: 11px 20px;
    min-height: 44px;
    font-size: 14px;
    gap: 8px;
    border-radius: 8px;
  }

  .email-change-section.very-compact .button {
    padding: 11px 18px;
    min-height: 44px;
    font-size: 13px;
    gap: 6px;
    border-radius: 8px;
  }

  .button i {
    font-size: 16px;
  }

  .email-change-section.compact .button i {
    font-size: 14px;
  }

  .email-change-section.very-compact .button i {
    font-size: 13px;
  }

  .button--primary {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  .button--primary:hover:not(:disabled) {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  .button--secondary {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.15);
  }

  .button--secondary:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
  }

  .button:active:not(:disabled) {
    transform: scale(0.98);
  }

  .button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  /* Mobile Responsive */
  @media (max-width: 480px) {
    .actions {
      flex-direction: column;
    }

    .button {
      width: 100%;
    }
  }

  /* Accessibility - Focus Indicators */
  .input:focus-visible {
    outline: 3px solid rgba(99, 102, 241, 0.9);
    outline-offset: 2px;
  }

  .button:focus-visible {
    outline: 3px solid rgba(99, 102, 241, 0.9);
    outline-offset: 2px;
  }

  /* Accessibility - Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .button,
    .email-change-section {
      transition: none;
    }

    .button:hover,
    .button:active {
      transform: none;
    }
  }

  /* Accessibility - High Contrast */
  @media (prefers-contrast: high) {
    .input:focus-visible {
      outline: 3px solid white;
    }

    .button:focus-visible {
      outline: 3px solid white;
    }

    .email-change-section {
      border: 2px solid white;
    }
  }
</style>
