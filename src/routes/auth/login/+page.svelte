<script lang="ts">
  /**
   * Login Page
   *
   * Provides social authentication options for users
   */

  import SocialAuthButton from "$shared/auth/components/SocialAuthButton.svelte";
  import EmailPasswordAuth from "$shared/auth/components/EmailPasswordAuth.svelte";
  import EmailLinkAuth from "$shared/auth/components/EmailLinkAuth.svelte";
  import { authStore } from "$shared/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { getRedirectResult } from "firebase/auth";
  import { auth } from "$shared/auth/firebase";

  let loadingRedirect = $state(true);
  let redirectError = $state<string | null>(null);
  let emailAuthMode: "password" | "link" = $state("link"); // Default to passwordless

  // Handle redirect result (for OAuth flow)
  onMount(() => {
    console.log("🔐 Login page mounted, checking for redirect result...");
    console.log("🔐 Current URL:", window.location.href);
    console.log("🔐 URL search params:", window.location.search);
    console.log("🔐 URL hash:", window.location.hash);

    // Check for auth attempt markers
    let authAttempt: any = null;
    try {
      const localStorageItem = localStorage.getItem("tka_auth_attempt");
      const sessionStorageItem = sessionStorage.getItem("tka_auth_attempt");
      console.log("🔐 localStorage auth_attempt:", localStorageItem);
      console.log("🔐 sessionStorage auth_attempt:", sessionStorageItem);

      authAttempt = JSON.parse(
        localStorageItem || sessionStorageItem || "null"
      );
      if (authAttempt) {
        console.log("✅ Found auth attempt marker:", authAttempt);
        const timeSinceAttempt = Date.now() - authAttempt.timestamp;
        console.log(`🔐 Time since auth attempt: ${timeSinceAttempt}ms`);
      } else {
        console.log(
          "ℹ️ No auth attempt marker found (first page load or not returning from OAuth)"
        );
      }
    } catch (e) {
      console.error("⚠️ Error reading auth attempt markers:", e);
    }

    let hasRedirected = false;

    // Async initialization
    (async () => {
      // Check for redirect result first
      try {
        console.log("🔐 Calling getRedirectResult...");
        console.log("🔐 Auth instance:", auth);
        console.log(
          "🔐 Auth currentUser before getRedirectResult:",
          auth.currentUser
        );

        const result = await getRedirectResult(auth);

        console.log("🔐 getRedirectResult returned:", result);
        console.log("🔐 Result details:", {
          hasResult: !!result,
          hasUser: !!result?.user,
          user: result?.user
            ? {
                uid: result.user.uid,
                email: result.user.email,
                displayName: result.user.displayName,
              }
            : null,
          credential: result?.providerId,
        });
        console.log(
          "🔐 Auth currentUser after getRedirectResult:",
          auth.currentUser
        );

        // Clear auth attempt markers after processing
        if (authAttempt) {
          try {
            localStorage.removeItem("tka_auth_attempt");
            sessionStorage.removeItem("tka_auth_attempt");
            console.log("🔐 Cleared auth attempt markers");
          } catch (e) {
            console.error("⚠️ Could not clear auth attempt markers:", e);
          }
        }

        if (result && result.user) {
          // User successfully signed in via redirect
          console.log("✅ User signed in via redirect:", result.user.uid);
          hasRedirected = true;
          // Give auth state time to propagate
          await new Promise((resolve) => setTimeout(resolve, 300));
          goto("/");
          return;
        } else {
          console.log("ℹ️ No redirect result found");

          if (authAttempt) {
            console.error(
              "⚠️ Auth attempt marker exists but no redirect result!"
            );
            console.error(
              "⚠️ This suggests Firebase Auth state was lost during redirect"
            );

            // RECOVERY ATTEMPT: Check if there's any auth data in storage
            console.log(
              "🔧 Attempting recovery: checking localStorage for Firebase auth data..."
            );
            try {
              const firebaseKeys = Object.keys(localStorage).filter(
                (key) => key.startsWith("firebase:") || key.includes("auth")
              );
              console.log(
                "🔧 Firebase-related localStorage keys:",
                firebaseKeys
              );

              // Check IndexedDB for Firebase data
              if ("indexedDB" in window) {
                const dbs = await indexedDB.databases?.();
                console.log("🔧 IndexedDB databases:", dbs);
              }
            } catch (storageCheck) {
              console.error("⚠️ Could not check storage:", storageCheck);
            }

            redirectError =
              "Authentication failed. Firebase lost your login session during redirect. This is likely caused by strict browser privacy settings. Try: (1) Allowing cookies for this site, (2) Disabling strict tracking prevention, or (3) Using a different browser.";
          } else {
            console.log(
              "ℹ️ This is likely a first page load (no OAuth redirect happened)"
            );
          }
        }
      } catch (error: any) {
        console.error("❌ Redirect sign-in error:", error);
        console.error("❌ Error details:", {
          code: error.code,
          message: error.message,
          name: error.name,
          stack: error.stack,
        });

        // Clear auth attempt markers on error
        if (authAttempt) {
          try {
            localStorage.removeItem("tka_auth_attempt");
            sessionStorage.removeItem("tka_auth_attempt");
          } catch (e) {
            // Ignore
          }
        }

        if (error.code === "auth/account-exists-with-different-credential") {
          redirectError =
            "An account already exists with this email using a different sign-in method.";
        } else if (error.code === "auth/network-request-failed") {
          redirectError =
            "Network error. Please check your internet connection and firewall settings.";
        } else {
          redirectError = error.message || "An error occurred during sign-in";
        }
      } finally {
        loadingRedirect = false;
        console.log(
          "🔐 Finished checking redirect result, loadingRedirect = false"
        );
      }
    })();

    // Redirect if already logged in
    // This handles cases where the user is already authenticated from a previous session
    $effect(() => {
      if (authStore.isAuthenticated && !hasRedirected && !loadingRedirect) {
        console.log("✅ User is authenticated, redirecting to home...");
        hasRedirected = true;
        goto("/");
      }
    });
  });
</script>

<svelte:head>
  <title>Login - TKA</title>
</svelte:head>

<div class="login-container">
  <div class="login-card">
    <div class="login-header">
      <h1>Welcome to TKA</h1>
      <p>Sign in to continue</p>
    </div>

    {#if loadingRedirect}
      <div class="loading-state">
        <div class="spinner"></div>
        <p>Completing sign-in...</p>
      </div>
    {:else}
      {#if redirectError}
        <div class="error-banner">
          <i class="fas fa-exclamation-circle"></i>
          {redirectError}
        </div>
      {/if}

      <div class="social-buttons">
        <SocialAuthButton provider="facebook">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path
              d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"
            />
          </svg>
          Continue with Facebook
        </SocialAuthButton>

        <!-- Optional: Add Google login -->
        <SocialAuthButton provider="google">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
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
          Continue with Google
        </SocialAuthButton>
      </div>

      <div class="divider">
        <span>or</span>
      </div>

      <!-- Toggle between passwordless and password-based auth -->
      <div class="auth-mode-toggle">
        <button
          type="button"
          class:active={emailAuthMode === "link"}
          onclick={() => (emailAuthMode = "link")}
        >
          Magic Link
        </button>
        <button
          type="button"
          class:active={emailAuthMode === "password"}
          onclick={() => (emailAuthMode = "password")}
        >
          Password
        </button>
      </div>

      {#if emailAuthMode === "link"}
        <EmailLinkAuth />
      {:else}
        <EmailPasswordAuth />
      {/if}

      <div class="login-footer">
        <p>
          By continuing, you agree to our
          <a href="/terms">Terms of Service</a> and
          <a href="/privacy">Privacy Policy</a>
        </p>
      </div>
    {/if}
  </div>
</div>

<style>
  .login-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  .login-card {
    background: white;
    border-radius: 1rem;
    padding: 2rem;
    width: 100%;
    max-width: 400px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  }

  .login-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .login-header h1 {
    font-size: 1.875rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0 0 0.5rem 0;
  }

  .login-header p {
    color: #6b7280;
    margin: 0;
    font-size: 1rem;
  }

  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 2rem;
    gap: 1rem;
  }

  .loading-state .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(99, 102, 241, 0.2);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .loading-state p {
    color: #6b7280;
    font-size: 0.95rem;
    margin: 0;
  }

  .error-banner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 0.5rem;
    color: #dc2626;
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
  }

  .error-banner i {
    font-size: 1.25rem;
    flex-shrink: 0;
  }

  .social-buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 1.5rem 0;
  }

  .divider::before,
  .divider::after {
    content: "";
    flex: 1;
    border-bottom: 1px solid #e5e7eb;
  }

  .divider span {
    padding: 0 1rem;
    color: #6b7280;
    font-size: 0.875rem;
  }

  .auth-mode-toggle {
    display: flex;
    gap: 0.5rem;
    background: #f3f4f6;
    padding: 0.25rem;
    border-radius: 0.5rem;
  }

  .auth-mode-toggle button {
    flex: 1;
    padding: 0.5rem 1rem;
    background: transparent;
    border: none;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: #6b7280;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .auth-mode-toggle button:hover {
    color: #374151;
  }

  .auth-mode-toggle button.active {
    background: white;
    color: #1f2937;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .login-footer {
    margin-top: 2rem;
    text-align: center;
  }

  .login-footer p {
    color: #6b7280;
    font-size: 0.75rem;
    margin: 0;
    line-height: 1.5;
  }

  .login-footer a {
    color: #3b82f6;
    text-decoration: none;
  }

  .login-footer a:hover {
    text-decoration: underline;
  }

  /* Dark mode support */
  @media (prefers-color-scheme: dark) {
    .login-card {
      background: #1f2937;
    }

    .login-header h1 {
      color: #f9fafb;
    }

    .login-header p {
      color: #9ca3af;
    }

    .divider::before,
    .divider::after {
      border-color: #4b5563;
    }

    .divider span {
      color: #9ca3af;
    }

    .login-footer p {
      color: #9ca3af;
    }

    .loading-state p {
      color: #d1d5db;
    }

    .error-banner {
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.4);
      color: #fca5a5;
    }
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .login-card {
      padding: 1.5rem;
    }

    .login-header h1 {
      font-size: 1.5rem;
    }
  }
</style>
