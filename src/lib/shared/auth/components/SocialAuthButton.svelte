<script lang="ts">
  /**
   * Social Authentication Button
   *
   * Provides branded login buttons for social providers (Facebook, Google, etc.)
   */

  import { goto } from "$app/navigation";
  import { resolve, TYPES, type IDeviceDetector } from "$shared";
  import type { ResponsiveSettings } from "$shared/device/domain/models/device-models";
  import {
    browserLocalPersistence,
    FacebookAuthProvider,
    fetchSignInMethodsForEmail,
    GithubAuthProvider,
    GoogleAuthProvider,
    indexedDBLocalPersistence,
    setPersistence,
    signInWithPopup,
    signInWithRedirect,
    TwitterAuthProvider,
    updateProfile,
    type User,
  } from "firebase/auth";
  import { onMount } from "svelte";
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

  // Services
  let deviceDetector: IDeviceDetector | null = null;

  // Reactive responsive settings from DeviceDetector
  let responsiveSettings = $state<ResponsiveSettings | null>(null);

  /**
   * Update Facebook profile picture to high resolution
   * Facebook Graph API provides higher resolution pictures than the default Firebase photoURL
   */
  async function updateFacebookProfilePicture(user: User) {
    try {
      console.log(`🖼️ [facebook] Fetching high-res profile picture...`);

      // Get the Facebook user ID from providerData
      const facebookData = user.providerData.find(
        (data) => data.providerId === "facebook.com"
      );

      if (!facebookData?.uid) {
        console.warn(`⚠️ [facebook] No Facebook UID found`);
        return;
      }

      // Facebook Graph API URL for high-resolution profile picture
      // Using type=large gives us a 200x200 picture (better than default)
      const highResPhotoURL = `https://graph.facebook.com/${facebookData.uid}/picture?type=large&access_token=OPTIONAL`;

      // Simpler approach: just use the direct Graph API URL without access token
      // Facebook allows fetching public profile pictures without authentication
      const photoURL = `https://graph.facebook.com/${facebookData.uid}/picture?type=large`;

      console.log(`🖼️ [facebook] Updating profile picture to:`, photoURL);

      // Update the user's profile with the high-res photo URL
      await updateProfile(user, {
        photoURL: photoURL,
      });

      console.log(`✅ [facebook] Profile picture updated successfully`);
    } catch (err) {
      console.error(`❌ [facebook] Failed to update profile picture:`, err);
      // Don't throw - this is a non-critical enhancement
    }
  }

  /**
   * Detect if user is on a mobile device
   * Mobile devices should use redirect flow for better UX with native apps
   * Uses DeviceDetector service for consistent device detection
   */
  const isMobileDevice = (): boolean => {
    // Use DeviceDetector if available, with touch support check
    if (responsiveSettings) {
      return responsiveSettings.touchSupported && responsiveSettings.isMobile;
    }

    // Fallback for early initialization
    const hasTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    return hasTouch && window.innerWidth < 768;
  };

  // Initialize DeviceDetector service
  onMount(() => {
    try {
      deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
      responsiveSettings = deviceDetector.getResponsiveSettings();

      // Return cleanup function from onCapabilitiesChanged
      const cleanup = deviceDetector.onCapabilitiesChanged(() => {
        responsiveSettings = deviceDetector!.getResponsiveSettings();
      });
      return cleanup || undefined;
    } catch (error) {
      console.warn("SocialAuthButton: Failed to resolve DeviceDetector", error);
      return undefined;
    }
  });

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

    // Get provider instance (defined before try block so it's accessible in catch)
    const authProvider = getProvider();

    try {
      console.log(`🔐 [${provider}] Starting login process...`);

      // CRITICAL: Track auth attempt in BOTH localStorage AND sessionStorage
      // This ensures we can detect the redirect even with strict browser privacy
      const authAttempt = {
        provider,
        timestamp: Date.now(),
        redirectUrl: window.location.href,
      };

      console.log(`🔐 [${provider}] Storing auth attempt markers...`);
      try {
        localStorage.setItem("tka_auth_attempt", JSON.stringify(authAttempt));
        sessionStorage.setItem("tka_auth_attempt", JSON.stringify(authAttempt));
        console.log(`✅ [${provider}] Auth attempt stored in both storages`);
      } catch (storageErr) {
        console.error(
          `⚠️ [${provider}] Could not store auth attempt:`,
          storageErr
        );
      }

      // CRITICAL: Set persistence - try IndexedDB first (more reliable), fallback to localStorage
      console.log(`🔐 [${provider}] Setting persistence to IndexedDB...`);
      try {
        await setPersistence(auth, indexedDBLocalPersistence);
        console.log(`✅ [${provider}] IndexedDB persistence set successfully`);
      } catch (indexedDBErr) {
        console.warn(
          `⚠️ [${provider}] IndexedDB persistence failed, falling back to localStorage:`,
          indexedDBErr
        );
        await setPersistence(auth, browserLocalPersistence);
        console.log(
          `✅ [${provider}] localStorage persistence set successfully`
        );
      }

      // Add any additional scopes if needed
      if (provider === "facebook") {
        authProvider.addScope("email");
        authProvider.addScope("public_profile");
      } else if (provider === "google") {
        authProvider.addScope("email");
        authProvider.addScope("profile");
      }

      // Use popup flow - more reliable for localhost development
      // Popup doesn't clear browser storage like redirect does
      console.log(`🔐 [${provider}] Using popup flow`);
      console.log(`🔐 [${provider}] Current URL:`, window.location.href);

      const result = await signInWithPopup(auth, authProvider);

      // User is now signed in
      console.log(
        `✅ [${provider}] User signed in via popup:`,
        result.user.uid
      );
      console.log(`✅ [${provider}] User email:`, result.user.email);

      // Update Facebook profile picture to high resolution if available
      if (provider === "facebook" && result.user) {
        await updateFacebookProfilePicture(result.user);
      }

      // Clear auth attempt markers on success
      try {
        localStorage.removeItem("tka_auth_attempt");
        sessionStorage.removeItem("tka_auth_attempt");
      } catch (e) {
        // Ignore
      }

      // Wait for auth state to propagate
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Navigate to home page
      console.log(`🔐 [${provider}] Navigating to home page...`);
      goto("/");
    } catch (err: any) {
      console.error(`❌ [${provider}] Login error:`, err);
      console.error(`❌ [${provider}] Error code:`, err.code);
      console.error(`❌ [${provider}] Error message:`, err.message);
      console.error(`❌ [${provider}] Full error:`, err);

      // Clear auth attempt markers on error
      try {
        localStorage.removeItem("tka_auth_attempt");
        sessionStorage.removeItem("tka_auth_attempt");
      } catch (e) {
        // Ignore storage errors
      }

      // Handle specific error codes
      if (err.code === "auth/popup-closed-by-user") {
        error = "Sign-in cancelled";
      } else if (err.code === "auth/popup-blocked") {
        error = "Popup was blocked. Trying redirect method...";
        try {
          await signInWithRedirect(auth, authProvider);
        } catch (redirectErr) {
          console.error(`❌ [${provider}] Redirect also failed:`, redirectErr);
          error = "Unable to sign in. Please check your browser settings.";
        }
      } else if (err.code === "auth/account-exists-with-different-credential") {
        // AUTOMATIC ACCOUNT LINKING
        console.log(
          "🔗 Account exists with different credential, attempting to link..."
        );

        try {
          const email = err.customData?.email;
          const pendingCred = (err as any).credential;

          if (email && pendingCred) {
            console.log(`🔗 Fetching existing sign-in methods for: ${email}`);
            const methods = await fetchSignInMethodsForEmail(auth, email);
            console.log(`🔗 Existing methods:`, methods);

            // Prompt user to sign in with their existing method
            error = `This email is already registered with ${methods[0]}. Please sign in with ${methods[0]} to link your accounts.`;

            // TODO: In the future, we can automatically trigger the other provider's sign-in
            // and then link the accounts programmatically
          } else {
            error =
              "An account already exists with this email using a different sign-in method. Please use your original sign-in method.";
          }
        } catch (linkError) {
          console.error("❌ Error during account linking:", linkError);
          error =
            "An account already exists with this email using a different sign-in method.";
        }
      } else if (err.code === "auth/unauthorized-domain") {
        error =
          "This domain is not authorized for OAuth. Please contact support.";
        console.error(
          `❌ [${provider}] UNAUTHORIZED DOMAIN - Check Firebase Console -> Authentication -> Settings -> Authorized domains`
        );
      } else {
        error = err.message || "An error occurred during sign-in";
      }
    } finally {
      loading = false;
      console.log(`🔐 [${provider}] Login process completed, loading = false`);
    }
  }

  // Modern 2025 provider styles with proper contrast
  const providerStyles = {
    facebook: {
      bg: "bg-[#0866FF]", // Facebook's 2025 brand blue
      hover: "hover:bg-[#0952CC]",
      text: "text-white",
      shadow: "shadow-lg shadow-blue-500/30",
      hoverShadow: "hover:shadow-xl hover:shadow-blue-500/40",
    },
    google: {
      bg: "bg-white",
      hover: "hover:bg-gray-50",
      text: "text-gray-800",
      border: "border-2 border-gray-200",
      shadow: "shadow-md",
      hoverShadow: "hover:shadow-lg",
    },
    github: {
      bg: "bg-[#24292e]",
      hover: "hover:bg-[#1a1e21]",
      text: "text-white",
      shadow: "shadow-lg shadow-gray-700/30",
      hoverShadow: "hover:shadow-xl hover:shadow-gray-700/40",
    },
    twitter: {
      bg: "bg-[#1DA1F2]",
      hover: "hover:bg-[#1a8cd8]",
      text: "text-white",
      shadow: "shadow-lg shadow-blue-400/30",
      hoverShadow: "hover:shadow-xl hover:shadow-blue-400/40",
    },
  };

  const styles =
    providerStyles[provider as keyof typeof providerStyles] ||
    providerStyles.facebook;

  const styleClasses =
    `${styles.bg} ${styles.hover} ${styles.text} ${"border" in styles ? styles.border : ""} ${styles.shadow} ${styles.hoverShadow}`.trim();
</script>

<button
  onclick={handleLogin}
  disabled={loading}
  class="social-auth-button {styleClasses} {className}"
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
