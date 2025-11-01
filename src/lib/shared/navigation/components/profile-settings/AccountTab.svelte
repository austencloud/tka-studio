<!--
  AccountTab Component (Security Tab)

  Handles security & account management: connected accounts, password, data export, account deletion.
  Features centered layout matching PersonalTab with descriptive hints.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import {
    hasPasswordProvider,
    isCompactMode,
    isVeryCompactMode,
  } from "../../state/profile-settings-state.svelte";
  import ConnectedAccounts from "./ConnectedAccounts.svelte";
  import PasswordSection from "./PasswordSection.svelte";
  import DangerZone from "./DangerZone.svelte";

  let { onChangePassword, onDeleteAccount, hapticService } =
    $props<{
      onChangePassword: () => Promise<void>;
      onDeleteAccount: () => Promise<void>;
      hapticService: IHapticFeedbackService | null;
    }>();
</script>

<section
  class="section section--account"
  class:compact={isCompactMode()}
  class:very-compact={isVeryCompactMode()}
>
  <!-- Centered content container -->
  <div class="form-content">
    <!-- Connected Accounts Card -->
    <div class="security-card">
      <div class="card-header">
        <i class="fas fa-link" aria-hidden="true"></i>
        <h3 class="card-title">Connected Accounts</h3>
      </div>
      <p class="card-description">
        Manage the authentication providers linked to your account
      </p>
      <ConnectedAccounts />
    </div>

    <!-- Password Section (only for password-authenticated users) -->
    {#if hasPasswordProvider()}
      <div class="security-card">
        <div class="card-header">
          <i class="fas fa-key" aria-hidden="true"></i>
          <h3 class="card-title">Password</h3>
        </div>
        <p class="card-description">
          Update your password to keep your account secure
        </p>
        <PasswordSection {onChangePassword} {hapticService} />
      </div>
    {/if}
  </div>

  <!-- Account Deletion (outside of centered cards) -->
  <DangerZone {onDeleteAccount} {hapticService} />
</section>

<style>
  /* Section Layout */
  .section {
    min-height: 100%;
    display: flex;
    flex-direction: column;
    height: 100%;
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
    align-items: center; /* Center cards horizontally */
    justify-content: center; /* Center vertically when there's space */
    gap: clamp(18px, 3vh, 32px); /* Fluid spacing between cards */
  }

  .section.compact .form-content {
    padding: 18px;
    gap: 18px;
  }

  .section.very-compact .form-content {
    padding: 12px;
    gap: 12px;
  }

  /* Security Cards */
  .security-card {
    width: 100%;
    max-width: min(900px, 85vw); /* Fluid responsive width */
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(12px, 2vh, 18px);
    padding: clamp(18px, 3vh, 28px);
    transition: all 0.2s ease;
  }

  .section.compact .security-card {
    padding: 18px;
    border-radius: 12px;
  }

  .section.very-compact .security-card {
    padding: 14px;
    border-radius: 10px;
  }

  .security-card:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.15);
  }

  /* Card Header */
  .card-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(10px, 1.5vh, 14px);
    margin-bottom: clamp(10px, 1.5vh, 16px);
  }

  .card-header i {
    font-size: clamp(18px, 2.5vh, 22px);
    color: rgba(99, 102, 241, 0.8);
  }

  .section.compact .card-header i {
    font-size: 18px;
  }

  .section.very-compact .card-header i {
    font-size: 16px;
  }

  .card-title {
    font-size: clamp(16px, 2.2vh, 20px);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
    text-align: center;
  }

  .section.compact .card-title {
    font-size: 16px;
  }

  .section.very-compact .card-title {
    font-size: 15px;
  }

  .card-description {
    font-size: clamp(13px, 1.8vh, 15px);
    color: rgba(255, 255, 255, 0.65);
    text-align: center;
    margin: 0 0 clamp(16px, 2.5vh, 24px) 0;
    line-height: 1.5;
  }

  .section.compact .card-description {
    font-size: 13px;
    margin-bottom: 16px;
  }

  .section.very-compact .card-description {
    font-size: 12px;
    margin-bottom: 12px;
  }

  /* Buttons */
  .button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(8px, 1.2vh, 12px);
    padding: clamp(12px, 1.8vh, 16px) clamp(20px, 3vw, 28px);
    min-height: 48px; /* WCAG minimum */
    border-radius: 10px;
    font-size: clamp(14px, 1.9vh, 17px);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    margin-top: clamp(6px, 1vh, 10px);
  }

  .section.compact .button {
    padding: 11px 20px;
    min-height: 44px;
    font-size: 14px;
    gap: 8px;
    border-radius: 8px;
    margin-top: 6px;
  }

  .section.very-compact .button {
    padding: 11px 18px;
    min-height: 44px;
    font-size: 13px;
    gap: 6px;
    border-radius: 8px;
    margin-top: 4px;
  }

  .button i {
    font-size: 16px;
  }

  .section.compact .button i {
    font-size: 14px;
  }

  .section.very-compact .button i {
    font-size: 13px;
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
    .form-content {
      padding: 16px;
      gap: 16px;
    }

    .security-card {
      padding: 16px;
    }
  }

  /* Accessibility - Focus Indicators */
  .button:focus-visible {
    outline: 3px solid rgba(99, 102, 241, 0.9);
    outline-offset: 2px;
  }

  /* Accessibility - Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .button,
    .security-card {
      transition: none;
    }

    .button:hover,
    .button:active {
      transform: none;
    }
  }

  /* Accessibility - High Contrast */
  @media (prefers-contrast: high) {
    .button:focus-visible {
      outline: 3px solid white;
    }

    .security-card {
      border: 2px solid white;
    }
  }
</style>
