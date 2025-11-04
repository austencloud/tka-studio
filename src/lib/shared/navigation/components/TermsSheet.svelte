<!--
  TermsSheet.svelte - Terms of Service Bottom Sheet
-->
<script lang="ts">
  import {
    Drawer,
    resolve,
    TYPES,
    type IHapticFeedbackService,
  } from "$shared";
  import { onMount } from "svelte";

  // Props
  let { isOpen = false, onClose } = $props<{
    isOpen?: boolean;
    onClose: () => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleClose() {
    hapticService?.trigger("selection");
    onClose();
  }
</script>

<Drawer
  {isOpen}
  labelledBy="terms-sheet-title"
  on:close={onClose}
  class="terms-sheet"
  backdropClass="terms-sheet__backdrop"
>
  <div class="terms-sheet__container">
    <!-- Header -->
    <header class="terms-sheet__header">
      <h2 id="terms-sheet-title" class="terms-sheet__title">
        Terms of Service
      </h2>
      <button
        class="terms-sheet__close"
        onclick={handleClose}
        aria-label="Close terms"
      >
        <i class="fas fa-times"></i>
      </button>
    </header>

    <!-- Content -->
    <div class="terms-sheet__content">
      <p class="last-updated">
        Last Updated: {new Date().toLocaleDateString()}
      </p>

      <section>
        <h3>1. Acceptance of Terms</h3>
        <p>
          By accessing and using The Kinetic Alphabet (TKA) application, you
          agree to be bound by these Terms of Service. If you do not agree to
          these terms, please do not use the application.
        </p>
      </section>

      <section>
        <h3>2. Description of Service</h3>
        <p>
          TKA Studio is an educational platform that provides tools for
          learning, creating, and sharing kinetic alphabet sequences. The
          service includes sequence building tools, learning modules, and
          community features.
        </p>
      </section>

      <section>
        <h3>3. User Accounts</h3>
        <p>
          You are responsible for maintaining the confidentiality of your
          account credentials. You agree to accept responsibility for all
          activities that occur under your account.
        </p>
      </section>

      <section>
        <h3>4. User Content</h3>
        <p>
          You retain ownership of any sequences, content, or materials you
          create using TKA. By sharing content publicly, you grant TKA a license
          to display and distribute that content within the application.
        </p>
      </section>

      <section>
        <h3>5. Acceptable Use</h3>
        <p>You agree not to:</p>
        <ul>
          <li>Use the service for any illegal purposes</li>
          <li>Attempt to gain unauthorized access to the service</li>
          <li>Interfere with or disrupt the service</li>
          <li>Upload malicious code or harmful content</li>
          <li>Harass or harm other users</li>
        </ul>
      </section>

      <section>
        <h3>6. Intellectual Property</h3>
        <p>
          The TKA Studio application, including its design, features, and
          underlying technology, is owned by TKA Studio and protected by
          intellectual property laws. The Kinetic Alphabet system and
          methodology remain the intellectual property of their respective
          creators.
        </p>
      </section>

      <section>
        <h3>7. Disclaimers</h3>
        <p>
          TKA Studio is provided "as is" without warranties of any kind. We do
          not guarantee that the service will be uninterrupted, secure, or
          error-free.
        </p>
      </section>

      <section>
        <h3>8. Limitation of Liability</h3>
        <p>
          TKA shall not be liable for any indirect, incidental, special, or
          consequential damages arising from your use of the service.
        </p>
      </section>

      <section>
        <h3>9. Changes to Terms</h3>
        <p>
          We reserve the right to modify these terms at any time. Continued use
          of the service after changes constitutes acceptance of the modified
          terms.
        </p>
      </section>

      <section>
        <h3>10. Contact</h3>
        <p>
          If you have questions about these Terms of Service, please contact us
          through the application's support channels.
        </p>
      </section>
    </div>
  </div>
</Drawer>

<style>
  /* ============================================================================
     BACKDROP
     ============================================================================ */
  :global(.terms-sheet__backdrop) {
    z-index: 1200;
  }

  /* ============================================================================
     CONTAINER
     ============================================================================ */
  .terms-sheet__container {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-height: 90vh;
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(15, 20, 30, 0.95) 100%
    );
    overflow: hidden;
  }

  /* ============================================================================
     HEADER
     ============================================================================ */
  .terms-sheet__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .terms-sheet__title {
    font-size: 24px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .terms-sheet__close {
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

  .terms-sheet__close:hover {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(1.05);
  }

  .terms-sheet__close:active {
    transform: scale(0.95);
  }

  .terms-sheet__close:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* ============================================================================
     CONTENT
     ============================================================================ */
  .terms-sheet__content {
    flex: 1;
    min-height: 0; /* Critical for flexbox scrolling */
    overflow-y: auto;
    overflow-x: hidden;
    padding: 24px;
    -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
    touch-action: pan-y; /* Allow vertical scrolling on touch devices */
    overscroll-behavior-y: contain; /* Prevent scroll chaining */
  }

  .last-updated {
    color: rgba(255, 255, 255, 0.5);
    font-size: 14px;
    margin: 0 0 24px 0;
  }

  section {
    margin-bottom: 24px;
  }

  h3 {
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 12px 0;
  }

  p {
    color: rgba(255, 255, 255, 0.75);
    line-height: 1.6;
    margin: 0 0 12px 0;
  }

  ul {
    color: rgba(255, 255, 255, 0.75);
    line-height: 1.6;
    margin: 0 0 12px 0;
    padding-left: 24px;
  }

  li {
    margin-bottom: 8px;
  }

  /* ============================================================================
     RESPONSIVE DESIGN
     ============================================================================ */
  @media (max-width: 480px) {
    .terms-sheet__header {
      padding: 20px;
    }

    .terms-sheet__title {
      font-size: 20px;
    }

    .terms-sheet__content {
      padding: 20px;
    }

    h3 {
      font-size: 16px;
    }

    p,
    ul {
      font-size: 14px;
    }
  }

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .terms-sheet__close {
      transition: none;
    }

    .terms-sheet__close:hover,
    .terms-sheet__close:active {
      transform: none;
    }
  }
</style>
