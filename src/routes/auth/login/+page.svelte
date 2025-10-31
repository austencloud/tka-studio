<script lang="ts">
  /**
   * Login Page
   *
   * Provides social authentication options for users
   */

  import SocialAuthButton from "$shared/auth/components/SocialAuthButton.svelte";
  import { isAuthenticated } from "$shared/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  // Redirect if already logged in
  onMount(() => {
    const unsubscribe = isAuthenticated.subscribe((authenticated) => {
      if (authenticated) {
        goto("/");
      }
    });

    return unsubscribe;
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

    <div class="login-footer">
      <p>
        By continuing, you agree to our
        <a href="/terms">Terms of Service</a> and
        <a href="/privacy">Privacy Policy</a>
      </p>
    </div>
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

  .social-buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
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

    .login-footer p {
      color: #9ca3af;
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
