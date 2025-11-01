<!--
  AuthSheet.svelte - Authentication Bottom Sheet

  Modern panel-based authentication (no routing!)
  Supports: Facebook, Google, Email/Password
-->
<script lang="ts">
  import { BottomSheet } from "$shared";
  import SocialAuthButton from "$shared/auth/components/SocialAuthButton.svelte";
  import EmailPasswordAuth from "$shared/auth/components/EmailPasswordAuth.svelte";
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { authStore } from "$shared/auth";
  import { onMount } from "svelte";
  import { slide, fade } from "svelte/transition";
  import {
    GoogleAuthProvider,
    FacebookAuthProvider,
    signInWithRedirect,
    setPersistence,
    indexedDBLocalPersistence,
    browserLocalPersistence,
  } from "firebase/auth";
  import { auth } from "$shared/auth/firebase";

  // Props
  let { isOpen = false, onClose } = $props<{
    isOpen?: boolean;
    onClose: () => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  // Track auth mode to update UI accordingly
  let authMode = $state<"signin" | "signup">("signin");

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Auto-close when user becomes authenticated
  $effect(() => {
    if (authStore.isAuthenticated && isOpen) {
      console.log("✅ User authenticated, auto-closing auth sheet");
      // Small delay for smooth transition
      setTimeout(() => {
        onClose();
      }, 300);
    }
  });

  function handleClose() {
    hapticService?.trigger("selection");
    onClose();
  }

  function openTerms(e: Event) {
    e.preventDefault();
    hapticService?.trigger("selection");
    import("../utils/sheet-router").then(({ openSheet }) => {
      openSheet("terms");
    });
  }

  function openPrivacy(e: Event) {
    e.preventDefault();
    hapticService?.trigger("selection");
    import("../utils/sheet-router").then(({ openSheet }) => {
      openSheet("privacy");
    });
  }

  async function handleSocialAuth(provider: "google" | "facebook") {
    hapticService?.trigger("selection");

    try {
      console.log(`🔐 [${provider}] Starting sign-up process...`);

      // Set persistence
      try {
        await setPersistence(auth, indexedDBLocalPersistence);
        console.log(`✅ [${provider}] IndexedDB persistence set`);
      } catch (indexedDBErr) {
        await setPersistence(auth, browserLocalPersistence);
        console.log(`✅ [${provider}] localStorage persistence set`);
      }

      const authProvider = provider === "google"
        ? new GoogleAuthProvider()
        : new FacebookAuthProvider();

      // Add scopes
      if (provider === "facebook") {
        authProvider.addScope("email");
        authProvider.addScope("public_profile");
      } else {
        authProvider.addScope("email");
        authProvider.addScope("profile");
      }

      console.log(`🔐 [${provider}] Redirecting to ${provider} sign-in...`);
      await signInWithRedirect(auth, authProvider);
    } catch (error: any) {
      console.error(`❌ [${provider}] Sign-up error:`, error);
      hapticService?.trigger("error");
    }
  }
</script>

<BottomSheet
  {isOpen}
  labelledBy="auth-sheet-title"
  on:close={onClose}
  class="auth-sheet"
  backdropClass="auth-sheet__backdrop"
>
  <div class="auth-sheet__container">
    <!-- Header -->
    <header class="auth-sheet__header">
      <div class="auth-sheet__header-content">
        <h2 id="auth-sheet-title" class="auth-sheet__title">
          {authMode === "signin" ? "Welcome to TKA" : "Create Your Account"}
        </h2>
        <p class="auth-sheet__subtitle">
          {authMode === "signin"
            ? "Sign in to access your library and track your progress"
            : "Join TKA to save your progress and access your library"}
        </p>
      </div>
      <button
        class="auth-sheet__close"
        onclick={handleClose}
        aria-label={authMode === "signin" ? "Close sign in" : "Close sign up"}
      >
        <i class="fas fa-times"></i>
      </button>
    </header>

    <!-- Content -->
    <div class="auth-sheet__content">
      <!-- Social Auth Buttons - Compact side-by-side layout -->
      <div class="auth-sheet__social-compact">
        <p class="social-compact-label">
          {authMode === "signin" ? "Sign in with" : "Or sign up with"}
        </p>
        <div class="social-compact-buttons">
          <button
            class="social-compact-button social-compact-button--google"
            onclick={() => handleSocialAuth("google")}
            aria-label={authMode === "signin" ? "Sign in with Google" : "Sign up with Google"}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                fill="#EA4335"
              />
            </svg>
            Google
          </button>
          <button
            class="social-compact-button social-compact-button--facebook"
            onclick={() => handleSocialAuth("facebook")}
            aria-label={authMode === "signin" ? "Sign in with Facebook" : "Sign up with Facebook"}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"
              />
            </svg>
            Facebook
          </button>
        </div>
      </div>

      <!-- Divider -->
      <div class="auth-sheet__divider">
        <span>{authMode === "signin" ? "or sign in with email" : "or sign up with email"}</span>
      </div>

      <!-- Email/Password Auth -->
      <div class="auth-sheet__email">
        <EmailPasswordAuth bind:mode={authMode} />
      </div>
    </div>

    <!-- Footer -->
    <footer class="auth-sheet__footer">
      <p class="auth-sheet__footer-text">
        By continuing, you agree to our
        <button class="auth-sheet__link" onclick={openTerms}>Terms of Service</button> and
        <button class="auth-sheet__link" onclick={openPrivacy}>Privacy Policy</button>
      </p>
    </footer>
  </div>
</BottomSheet>

<style>
  /* ============================================================================
     BACKDROP
     ============================================================================ */
  :global(.auth-sheet__backdrop) {
    z-index: 1100;
  }

  /* ============================================================================
     CONTAINER
     ============================================================================ */
  .auth-sheet__container {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-height: min(90dvh, 700px); /* Use dvh for better mobile keyboard support */
    height: auto;
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
  .auth-sheet__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .auth-sheet__header-content {
    flex: 1;
    min-width: 0;
  }

  .auth-sheet__title {
    font-size: 24px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 8px 0;
  }

  .auth-sheet__subtitle {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    line-height: 1.5;
  }

  .auth-sheet__close {
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
    margin-left: 16px;
  }

  .auth-sheet__close:hover {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(1.05);
  }

  .auth-sheet__close:active {
    transform: scale(0.95);
  }

  .auth-sheet__close:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* ============================================================================
     CONTENT
     ============================================================================ */
  .auth-sheet__content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 20px 24px;
    display: flex;
    flex-direction: column;
    min-height: 0; /* Important for flex scrolling */

    /* Smooth scrolling */
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;

    /* Hide scrollbar but keep functionality */
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
  }

  .auth-sheet__content::-webkit-scrollbar {
    width: 6px;
  }

  .auth-sheet__content::-webkit-scrollbar-track {
    background: transparent;
  }

  .auth-sheet__content::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
  }

  .auth-sheet__content::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  .auth-sheet__social {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  /* Compact social auth for sign-up mode */
  .auth-sheet__social-compact {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    margin-top: 4px;
  }

  .social-compact-label {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    font-weight: 500;
  }

  .social-compact-buttons {
    display: flex;
    gap: 10px;
    width: 100%;
    max-width: 400px;
  }

  .social-compact-button {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-height: 44px; /* WCAG minimum */
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }

  .social-compact-button svg {
    flex-shrink: 0;
  }

  /* Google button - white background with multicolor logo */
  .social-compact-button--google {
    background: white;
    color: #202124;
  }

  .social-compact-button--google:hover:not(:disabled) {
    background: #f8f9fa;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    transform: translateY(-1px);
  }

  /* Facebook button - brand blue */
  .social-compact-button--facebook {
    background: #1877F2;
    color: white;
  }

  .social-compact-button--facebook svg {
    fill: white;
  }

  .social-compact-button--facebook:hover:not(:disabled) {
    background: #0C63D4;
    box-shadow: 0 4px 10px rgba(24, 119, 242, 0.35);
    transform: translateY(-1px);
  }

  .social-compact-button:active:not(:disabled) {
    transform: scale(0.98);
  }

  .social-compact-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .social-compact-button:focus-visible {
    outline: 3px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* Override SocialAuthButton styles for better visibility on dark background */
  :global(.auth-sheet__social .social-auth-button) {
    font-weight: 600;
    font-size: 16px;
    padding: 14px 20px;
    min-height: 52px;
    border-radius: 12px;
    transition: all 0.2s ease;
  }

  /* Facebook button - vibrant blue with excellent contrast */
  :global(.auth-sheet__facebook-btn.social-auth-button) {
    background: #1877F2 !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(24, 119, 242, 0.35) !important;
  }

  :global(.auth-sheet__facebook-btn.social-auth-button:hover:not(:disabled)) {
    background: #0C63D4 !important;
    box-shadow: 0 6px 16px rgba(24, 119, 242, 0.45) !important;
    transform: translateY(-2px);
  }

  /* Google button - clean white with dark text for perfect readability */
  :global(.auth-sheet__google-btn.social-auth-button) {
    background: white !important;
    color: #202124 !important;
    border: 2px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  }

  :global(.auth-sheet__google-btn.social-auth-button:hover:not(:disabled)) {
    background: #f8f9fa !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2) !important;
    transform: translateY(-2px);
  }

  :global(.auth-sheet__social .social-auth-button:active:not(:disabled)) {
    transform: translateY(0) !important;
  }

  .auth-sheet__divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 8px 0;
  }

  .auth-sheet__divider::before,
  .auth-sheet__divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  }

  .auth-sheet__divider span {
    padding: 0 16px;
    color: rgba(255, 255, 255, 0.5);
    font-size: 14px;
    font-weight: 500;
  }

  .auth-sheet__email {
    width: 100%;
  }

  /* ============================================================================
     FOOTER
     ============================================================================ */
  .auth-sheet__footer {
    padding: 16px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
    flex-shrink: 0;
  }

  .auth-sheet__footer-text {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
    margin: 0;
    text-align: center;
    line-height: 1.6;
  }

  .auth-sheet__link {
    background: none;
    border: none;
    padding: 0;
    color: rgba(99, 102, 241, 0.9);
    font-size: inherit;
    font-family: inherit;
    text-decoration: none;
    cursor: pointer;
    transition: color 0.2s ease;
  }

  .auth-sheet__link:hover {
    color: rgba(99, 102, 241, 1);
    text-decoration: underline;
  }

  /* ============================================================================
     RESPONSIVE DESIGN
     ============================================================================ */
  @media (max-width: 480px) {
    .auth-sheet__container {
      max-height: 95dvh; /* More space on mobile */
    }

    .auth-sheet__header {
      padding: 16px;
    }

    .auth-sheet__title {
      font-size: 20px;
    }

    .auth-sheet__subtitle {
      font-size: 13px;
    }

    .auth-sheet__content {
      padding: 16px;
      gap: 16px;
    }

    .auth-sheet__social {
      gap: 10px;
    }

    .auth-sheet__footer {
      padding: 12px 16px;
    }

    .auth-sheet__footer-text {
      font-size: 11px;
    }
  }

  /* iPhone SE 2/3 and similar (667px height) */
  @media (max-height: 700px) {
    .auth-sheet__container {
      max-height: 96dvh;
    }

    .auth-sheet__header {
      padding: 14px 16px;
    }

    .auth-sheet__title {
      font-size: 19px;
      margin-bottom: 6px;
    }

    .auth-sheet__subtitle {
      font-size: 12.5px;
    }

    .auth-sheet__content {
      padding: 14px 16px;
      gap: 14px;
    }

    .auth-sheet__social {
      gap: 9px;
    }

    :global(.auth-sheet__social .social-auth-button) {
      min-height: 50px;
      padding: 13px 18px;
      font-size: 15px;
    }

    .auth-sheet__footer {
      padding: 11px 16px;
    }
  }

  /* Small screens - hide footer to save space */
  @media (max-height: 600px) {
    .auth-sheet__container {
      max-height: 98dvh;
    }

    .auth-sheet__header {
      padding: 10px 14px;
    }

    .auth-sheet__title {
      font-size: 18px;
      margin-bottom: 4px;
    }

    .auth-sheet__subtitle {
      font-size: 12px;
    }

    .auth-sheet__content {
      padding: 10px 14px;
      gap: 10px;
    }

    .auth-sheet__social {
      gap: 8px;
    }

    :global(.auth-sheet__social .social-auth-button) {
      min-height: 48px;
      padding: 11px 16px;
      font-size: 14px;
    }

    .auth-sheet__divider {
      margin: 4px 0;
    }

    /* Hide footer on small screens to save space */
    .auth-sheet__footer {
      display: none;
    }
  }

  /* iPhone SE 1st gen and very small devices (568px height) */
  @media (max-height: 568px) {
    .auth-sheet__container {
      max-height: 100dvh;
    }

    .auth-sheet__header {
      padding: 8px 12px;
    }

    .auth-sheet__title {
      font-size: 17px;
      margin-bottom: 0;
    }

    /* Hide subtitle on very small screens */
    .auth-sheet__subtitle {
      display: none;
    }

    .auth-sheet__content {
      padding: 8px 12px;
      gap: 8px;
    }

    .auth-sheet__social {
      gap: 6px;
    }

    :global(.auth-sheet__social .social-auth-button) {
      min-height: 44px;
      padding: 10px 14px;
      font-size: 13px;
    }

    .auth-sheet__divider {
      margin: 2px 0;
    }

    .auth-sheet__divider span {
      font-size: 12px;
      padding: 0 12px;
    }

    .auth-sheet__social-compact {
      gap: 10px;
      margin-top: 0;
    }

    .social-compact-label {
      font-size: 12px;
    }

    .social-compact-buttons {
      gap: 8px;
    }

    .social-compact-button {
      min-height: 44px;
      padding: 9px 12px;
      font-size: 13px;
      gap: 6px;
    }

    .social-compact-button svg {
      width: 16px;
      height: 16px;
    }
  }

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .auth-sheet__close {
      transition: none;
    }

    .auth-sheet__close:hover,
    .auth-sheet__close:active {
      transform: none;
    }

    .social-compact-button {
      transition: none;
    }

    .social-compact-button:hover,
    .social-compact-button:active {
      transform: none;
    }
  }

  @media (prefers-contrast: high) {
    .auth-sheet__container {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    .auth-sheet__header,
    .auth-sheet__footer {
      border-color: white;
    }

    .auth-sheet__divider::before,
    .auth-sheet__divider::after {
      border-color: white;
    }
  }
</style>
