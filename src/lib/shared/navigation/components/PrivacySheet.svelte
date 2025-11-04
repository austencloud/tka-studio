<!--
  PrivacySheet.svelte - Privacy Policy Bottom Sheet
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
  labelledBy="privacy-sheet-title"
  on:close={onClose}
  class="privacy-sheet"
  backdropClass="privacy-sheet__backdrop"
>
  <div class="privacy-sheet__container">
    <!-- Header -->
    <header class="privacy-sheet__header">
      <h2 id="privacy-sheet-title" class="privacy-sheet__title">
        Privacy Policy
      </h2>
      <button
        class="privacy-sheet__close"
        onclick={handleClose}
        aria-label="Close privacy policy"
      >
        <i class="fas fa-times"></i>
      </button>
    </header>

    <!-- Content -->
    <div class="privacy-sheet__content">
      <p class="last-updated">
        Last Updated: {new Date().toLocaleDateString()}
      </p>

      <section>
        <h3>1. Information We Collect</h3>
        <p>
          When you use TKA, we collect information that you provide directly to
          us, including:
        </p>
        <ul>
          <li>
            <strong>Account Information:</strong> Name, email address, and profile
            information
          </li>
          <li>
            <strong>User Content:</strong> Sequences, animations, and other content
            you create
          </li>
          <li>
            <strong>Usage Data:</strong> Information about how you interact with
            the application
          </li>
          <li>
            <strong>Authentication Data:</strong> When you sign in via Facebook or
            Google, we receive basic profile information
          </li>
        </ul>
      </section>

      <section>
        <h3>2. How We Use Your Information</h3>
        <p>We use the information we collect to:</p>
        <ul>
          <li>Provide, maintain, and improve the TKA service</li>
          <li>Authenticate your account and provide access to your content</li>
          <li>Send you technical notices and support messages</li>
          <li>Respond to your comments and questions</li>
          <li>Analyze usage patterns to improve the application</li>
        </ul>
      </section>

      <section>
        <h3>3. Information Sharing</h3>
        <p>
          We do not sell your personal information. We may share your
          information only in the following circumstances:
        </p>
        <ul>
          <li>
            <strong>With Your Consent:</strong> When you choose to share content
            publicly
          </li>
          <li>
            <strong>Service Providers:</strong> With vendors who perform services
            on our behalf (e.g., Firebase for authentication and database)
          </li>
          <li>
            <strong>Legal Requirements:</strong> When required by law or to protect
            rights and safety
          </li>
        </ul>
      </section>

      <section>
        <h3>4. Data Storage and Security</h3>
        <p>
          Your data is stored securely using Firebase services, which employ
          industry-standard security measures. We use HTTPS encryption for all
          data transmission and implement authentication measures to protect
          your account.
        </p>
      </section>

      <section>
        <h3>5. Third-Party Services</h3>
        <p>TKA uses the following third-party services:</p>
        <ul>
          <li>
            <strong>Firebase Authentication:</strong> For secure user authentication
          </li>
          <li><strong>Firebase Firestore:</strong> For data storage</li>
          <li>
            <strong>Facebook Login:</strong> Optional authentication method
          </li>
          <li>
            <strong>Google Sign-In:</strong> Optional authentication method
          </li>
        </ul>
        <p>
          These services have their own privacy policies governing their use of
          your information.
        </p>
      </section>

      <section>
        <h3>6. Your Rights and Choices</h3>
        <p>You have the right to:</p>
        <ul>
          <li>Access your personal information</li>
          <li>
            Update or correct your information through your account settings
          </li>
          <li>Delete your account and associated data</li>
          <li>Export your data (sequences and content you've created)</li>
          <li>Opt out of certain data collection practices</li>
        </ul>
      </section>

      <section>
        <h3>7. Cookies and Local Storage</h3>
        <p>We use browser local storage and cookies to:</p>
        <ul>
          <li>Keep you logged in</li>
          <li>Remember your preferences and settings</li>
          <li>Improve application performance</li>
        </ul>
        <p>
          You can manage these through your browser settings, but some features
          may not work properly if disabled.
        </p>
      </section>

      <section>
        <h3>8. Children's Privacy</h3>
        <p>
          TKA Studio is designed for general audiences. We do not knowingly
          collect personal information from children under 13. If you believe we
          have collected information from a child under 13, please contact us
          immediately.
        </p>
      </section>

      <section>
        <h3>9. Data Retention</h3>
        <p>
          We retain your information for as long as your account is active or as
          needed to provide you services. You may request deletion of your
          account at any time through your account settings.
        </p>
      </section>

      <section>
        <h3>10. Changes to This Policy</h3>
        <p>
          We may update this Privacy Policy from time to time. We will notify
          you of any changes by posting the new policy within the application
          and updating the "Last Updated" date.
        </p>
      </section>

      <section>
        <h3>11. Contact Us</h3>
        <p>
          If you have questions about this Privacy Policy or our data practices,
          please contact us through the application's support channels.
        </p>
      </section>
    </div>
  </div>
</Drawer>

<style>
  /* ============================================================================
     BACKDROP
     ============================================================================ */
  :global(.privacy-sheet__backdrop) {
    z-index: 1200;
  }

  /* ============================================================================
     CONTAINER
     ============================================================================ */
  .privacy-sheet__container {
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
  .privacy-sheet__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .privacy-sheet__title {
    font-size: 24px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .privacy-sheet__close {
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

  .privacy-sheet__close:hover {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(1.05);
  }

  .privacy-sheet__close:active {
    transform: scale(0.95);
  }

  .privacy-sheet__close:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* ============================================================================
     CONTENT
     ============================================================================ */
  .privacy-sheet__content {
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

  strong {
    color: rgba(255, 255, 255, 0.9);
    font-weight: 600;
  }

  /* ============================================================================
     RESPONSIVE DESIGN
     ============================================================================ */
  @media (max-width: 480px) {
    .privacy-sheet__header {
      padding: 20px;
    }

    .privacy-sheet__title {
      font-size: 20px;
    }

    .privacy-sheet__content {
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
    .privacy-sheet__close {
      transition: none;
    }

    .privacy-sheet__close:hover,
    .privacy-sheet__close:active {
      transform: none;
    }
  }
</style>
