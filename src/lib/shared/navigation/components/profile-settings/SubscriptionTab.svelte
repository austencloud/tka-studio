<!--
  SubscriptionTab Component

  Handles subscription management: current plan, upgrade/downgrade, billing.
  Features centered layout matching other tabs with card-style sections.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import {
    isCompactMode,
    isVeryCompactMode,
  } from "../../state/profile-settings-state.svelte";

  let { hapticService } = $props<{
    hapticService: IHapticFeedbackService | null;
  }>();

  // TODO: Replace with actual subscription data from backend
  const currentPlan = "Free Tier";
  const isPremium = false;

  function handleUpgrade() {
    hapticService?.trigger("selection");
    // TODO: Implement upgrade flow
    console.log("Upgrade to Premium");
  }

  function handleManageBilling() {
    hapticService?.trigger("selection");
    // TODO: Implement billing management (redirect to Stripe portal, etc.)
    console.log("Manage billing");
  }

  function handleCancelSubscription() {
    hapticService?.trigger("warning");
    // TODO: Implement subscription cancellation
    console.log("Cancel subscription");
  }
</script>

<section
  class="section section--subscription"
  class:compact={isCompactMode()}
  class:very-compact={isVeryCompactMode()}
>
  <!-- Centered content container -->
  <div class="form-content">
    <!-- Current Plan Card -->
    <div class="subscription-card">
      <div class="card-header">
        <i class="fas fa-star" aria-hidden="true"></i>
        <h3 class="card-title">Current Plan</h3>
      </div>

      <div class="plan-badge" class:premium={isPremium}>
        <i class="fas {isPremium ? 'fa-crown' : 'fa-heart'}" aria-hidden="true"></i>
        <span>{currentPlan}</span>
      </div>

      <p class="plan-description">
        {#if isPremium}
          Build and share your own sequence library as part of the ecosystem.
        {:else}
          Join the ecosystem to unlock premium features when they become available.
        {/if}
      </p>

      {#if !isPremium}
        <button class="button button--primary" onclick={handleUpgrade} disabled>
          <i class="fas fa-rocket" aria-hidden="true"></i>
          Premium Coming Soon
        </button>
      {:else}
        <button class="button button--secondary" onclick={handleManageBilling}>
          <i class="fas fa-cog" aria-hidden="true"></i>
          Manage Billing
        </button>
      {/if}
    </div>

    {#if !isPremium}
      <!-- Premium Features Preview -->
      <div class="subscription-card features-card">
        <div class="card-header">
          <i class="fas fa-sparkles" aria-hidden="true"></i>
          <h3 class="card-title">Premium Features</h3>
        </div>
        <p class="card-description">
          What's coming with premium membership
        </p>

        <ul class="features-list">
          <li>
            <i class="fas fa-book" aria-hidden="true"></i>
            <span>Create your own sequence library</span>
          </li>
          <li>
            <i class="fas fa-users" aria-hidden="true"></i>
            <span>Share sequences with the community</span>
          </li>
          <li>
            <i class="fas fa-plus" aria-hidden="true"></i>
            <span>More features to be announced...</span>
          </li>
        </ul>
      </div>
    {/if}
  </div>
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
    padding: clamp(16px, 3vh, 32px) clamp(20px, 4vw, 48px);
    padding-bottom: clamp(10px, 1.5vh, 16px);
    min-height: 0;
    transition: padding 0.2s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center; /* Center vertically when there's space */
    gap: clamp(18px, 3vh, 32px); /* Fluid gap instead of margin */
  }

  .section.compact .form-content {
    padding: 16px;
    padding-bottom: 8px;
  }

  .section.very-compact .form-content {
    padding: 12px;
    padding-bottom: 6px;
  }

  /* Subscription Cards */
  .subscription-card {
    width: 100%;
    max-width: min(900px, 85vw); /* Fluid responsive width */
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(10px, 1.5vh, 14px);
    padding: clamp(16px, 2.5vh, 24px);
    transition: all 0.2s ease;
  }

  .section.compact .subscription-card {
    padding: 16px;
    border-radius: 10px;
  }

  .section.very-compact .subscription-card {
    padding: 12px;
    border-radius: 8px;
  }

  .subscription-card:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.15);
  }

  /* Card Header */
  .card-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(8px, 1.2vh, 12px);
    margin-bottom: clamp(12px, 2vh, 18px);
  }

  .section.compact .card-header {
    margin-bottom: 12px;
  }

  .section.very-compact .card-header {
    margin-bottom: 10px;
  }

  .card-header i {
    font-size: clamp(16px, 2.2vh, 20px);
    color: rgba(99, 102, 241, 0.8);
  }

  .section.compact .card-header i {
    font-size: 16px;
  }

  .section.very-compact .card-header i {
    font-size: 14px;
  }

  .card-title {
    font-size: clamp(16px, 2.1vh, 19px);
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
    font-size: clamp(13px, 1.7vh, 15px);
    color: rgba(255, 255, 255, 0.65);
    text-align: center;
    margin: 0 0 clamp(12px, 2vh, 18px) 0;
    line-height: 1.4;
  }

  .section.compact .card-description {
    font-size: 13px;
    margin-bottom: 12px;
  }

  .section.very-compact .card-description {
    font-size: 12px;
    margin-bottom: 10px;
  }

  /* Plan Badge */
  .plan-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(6px, 1vh, 10px);
    padding: clamp(10px, 1.5vh, 14px) clamp(16px, 2.5vw, 24px);
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    margin-bottom: clamp(10px, 1.5vh, 14px);
  }

  .section.compact .plan-badge {
    padding: 10px 16px;
    margin-bottom: 10px;
  }

  .section.very-compact .plan-badge {
    padding: 8px 14px;
    margin-bottom: 8px;
  }

  .plan-badge.premium {
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 165, 0, 0.15));
    border-color: rgba(255, 215, 0, 0.4);
  }

  .plan-badge i {
    font-size: clamp(18px, 2.5vh, 22px);
    color: rgba(255, 255, 255, 0.8);
  }

  .section.compact .plan-badge i {
    font-size: 18px;
  }

  .section.very-compact .plan-badge i {
    font-size: 16px;
  }

  .plan-badge.premium i {
    color: rgba(255, 215, 0, 0.9);
  }

  .plan-badge span {
    font-size: clamp(16px, 2.2vh, 20px);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .section.compact .plan-badge span {
    font-size: 17px;
  }

  .section.very-compact .plan-badge span {
    font-size: 16px;
  }

  .plan-description {
    font-size: clamp(13px, 1.7vh, 15px);
    color: rgba(255, 255, 255, 0.7);
    text-align: center;
    line-height: 1.5;
    margin: 0 0 clamp(12px, 2vh, 18px) 0;
  }

  .section.compact .plan-description {
    font-size: 13px;
    margin-bottom: 12px;
  }

  .section.very-compact .plan-description {
    font-size: 12px;
    margin-bottom: 10px;
  }

  /* Features Card */
  .features-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.04), rgba(79, 70, 229, 0.04));
  }

  .features-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: clamp(8px, 1.2vh, 12px);
  }

  .section.compact .features-list {
    gap: 8px;
  }

  .section.very-compact .features-list {
    gap: 6px;
  }

  .features-list li {
    display: flex;
    align-items: center;
    gap: clamp(10px, 1.5vh, 14px);
    padding: clamp(8px, 1.2vh, 12px) clamp(10px, 1.5vw, 14px);
    background: rgba(255, 255, 255, 0.02);
    border-radius: 8px;
  }

  .section.compact .features-list li {
    padding: 8px 10px;
    gap: 10px;
  }

  .section.very-compact .features-list li {
    padding: 6px 8px;
    gap: 8px;
  }

  .features-list i {
    font-size: clamp(13px, 1.7vh, 15px);
    color: rgba(99, 102, 241, 0.8);
    flex-shrink: 0;
  }

  .section.compact .features-list i {
    font-size: 13px;
  }

  .section.very-compact .features-list i {
    font-size: 12px;
  }

  .features-list span {
    font-size: clamp(12px, 1.6vh, 14px);
    color: rgba(255, 255, 255, 0.8);
  }

  .section.compact .features-list span {
    font-size: 12px;
  }

  .section.very-compact .features-list span {
    font-size: 11px;
  }

  /* Buttons */
  .button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(8px, 1.2vh, 12px);
    padding: clamp(10px, 1.5vh, 14px) clamp(18px, 2.5vw, 24px);
    min-height: 48px; /* WCAG minimum */
    border-radius: 8px;
    font-size: clamp(13px, 1.7vh, 16px);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
  }

  .section.compact .button {
    padding: 10px 18px;
    min-height: 44px;
    font-size: 13px;
    gap: 8px;
  }

  .section.very-compact .button {
    padding: 8px 16px;
    min-height: 44px;
    font-size: 13px;
    gap: 6px;
  }

  .button i {
    font-size: clamp(13px, 1.7vh, 15px);
  }

  .section.compact .button i {
    font-size: 13px;
  }

  .section.very-compact .button i {
    font-size: 12px;
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

  .button--danger {
    background: rgba(239, 68, 68, 0.1);
    color: rgba(239, 68, 68, 0.9);
    border: 1px solid rgba(239, 68, 68, 0.25);
  }

  .button--danger:hover:not(:disabled) {
    background: rgba(239, 68, 68, 0.15);
    border-color: rgba(239, 68, 68, 0.4);
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
      padding: 12px;
      padding-bottom: 6px;
    }

    .subscription-card {
      padding: 14px;
    }
  }

  /* Accessibility - Focus Indicators */
  .button:focus-visible {
    outline: 3px solid rgba(99, 102, 241, 0.9);
    outline-offset: 2px;
  }

  .button--danger:focus-visible {
    outline: 3px solid rgba(239, 68, 68, 0.9);
    outline-offset: 2px;
  }

  /* Accessibility - Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .button,
    .subscription-card {
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

    .subscription-card {
      border: 2px solid white;
    }
  }
</style>
