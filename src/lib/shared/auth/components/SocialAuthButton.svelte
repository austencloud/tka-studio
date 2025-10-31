<script lang="ts">
  /**
   * Social Authentication Button
   *
   * Provides branded login buttons for social providers (Facebook, Google, etc.)
   */

  import {
    signInWithPopup,
    FacebookAuthProvider,
    GoogleAuthProvider,
    GithubAuthProvider,
    TwitterAuthProvider,
  } from "firebase/auth";
  import { auth } from "../firebase";

  let {
    provider,
    class: className = "",
    children,
  }: {
    provider: "facebook" | "google" | "github" | "twitter";
    class?: string;
    children: import("svelte").Snippet;
  } = $props();

  let loading = $state(false);
  let error = $state<string | null>(null);

  const getProvider = () => {
    switch (provider) {
      case "facebook":
        return new FacebookAuthProvider();
      case "google":
        return new GoogleAuthProvider();
      case "github":
        return new GithubAuthProvider();
      case "twitter":
        return new TwitterAuthProvider();
      default:
        throw new Error(`Unknown provider: ${provider}`);
    }
  };

  async function handleLogin() {
    loading = true;
    error = null;

    try {
      const authProvider = getProvider();

      // Add any additional scopes if needed
      if (provider === "facebook") {
        authProvider.addScope("email");
        authProvider.addScope("public_profile");
      }

      const result = await signInWithPopup(auth, authProvider);

      // User is now signed in
      console.log("User signed in:", result.user.uid);

      // The authStore will automatically update via onAuthStateChanged
    } catch (err: any) {
      console.error(`${provider} login error:`, err);

      // Handle specific error codes
      if (err.code === "auth/popup-closed-by-user") {
        error = "Sign-in cancelled";
      } else if (err.code === "auth/popup-blocked") {
        error = "Popup was blocked. Please allow popups for this site.";
      } else if (err.code === "auth/account-exists-with-different-credential") {
        error =
          "An account already exists with this email using a different sign-in method.";
      } else {
        error = err.message || "An error occurred during sign-in";
      }
    } finally {
      loading = false;
    }
  }

  const providerColors = {
    facebook: "bg-[#1877f2] hover:bg-[#166fe5]",
    google: "bg-white hover:bg-gray-50 text-gray-700 border border-gray-300",
    github: "bg-[#24292e] hover:bg-[#1b1f23]",
    twitter: "bg-[#1da1f2] hover:bg-[#1a91da]",
  };

  const colorClass =
    providerColors[provider] || "bg-gray-600 hover:bg-gray-700";
</script>

<button
  onclick={handleLogin}
  disabled={loading}
  class="social-auth-button {colorClass} {className}"
  aria-label="Sign in with {provider}"
>
  {#if loading}
    <span class="spinner"></span>
  {/if}
  {@render children()}
</button>

{#if error}
  <p class="error-message">{error}</p>
{/if}

<style>
  .social-auth-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 1rem;
    color: white;
    transition: all 0.2s ease;
    cursor: pointer;
    border: none;
    width: 100%;
    min-height: 44px; /* Accessibility: minimum touch target */
  }

  .social-auth-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .social-auth-button:not(:disabled):active {
    transform: scale(0.98);
  }

  .spinner {
    display: inline-block;
    width: 1rem;
    height: 1rem;
    border: 2px solid currentColor;
    border-right-color: transparent;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .error-message {
    color: #ef4444;
    font-size: 0.875rem;
    margin-top: 0.5rem;
    text-align: center;
  }
</style>
