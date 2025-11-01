/**
 * Authentication Store (Svelte 5 Runes)
 *
 * Manages authentication state across the application using Firebase Auth.
 * Provides reactive user data and auth status using Svelte 5 runes.
 */

import {
  onAuthStateChanged,
  signOut as firebaseSignOut,
  updateProfile,
  updateEmail,
  sendEmailVerification,
  EmailAuthProvider,
  reauthenticateWithCredential,
  getRedirectResult,
  type User,
} from "firebase/auth";
import { auth } from "../firebase";

/**
 * Update Facebook profile picture to high resolution
 * Facebook Graph API provides higher resolution pictures than the default Firebase photoURL
 */
async function updateFacebookProfilePictureIfNeeded(user: User) {
  try {
    // Check if user has Facebook provider
    const facebookData = user.providerData.find(
      (data) => data.providerId === "facebook.com"
    );

    if (!facebookData?.uid) {
      return; // Not a Facebook user
    }

    // Check if we need to update the profile picture
    // If photoURL doesn't contain graph.facebook.com, it's the low-res default
    if (user.photoURL && user.photoURL.includes("graph.facebook.com")) {
      console.log(`ℹ️ [authStore] Facebook profile picture already high-res`);
      return; // Already using high-res picture
    }

    console.log(`🖼️ [authStore] Updating Facebook profile picture to high-res...`);

    // Facebook Graph API URL for high-resolution profile picture
    const photoURL = `https://graph.facebook.com/${facebookData.uid}/picture?type=large`;

    // Update the user's profile with the high-res photo URL
    await updateProfile(user, {
      photoURL: photoURL,
    });

    console.log(`✅ [authStore] Facebook profile picture updated successfully`);
  } catch (err) {
    console.error(`❌ [authStore] Failed to update Facebook profile picture:`, err);
    // Don't throw - this is a non-critical enhancement
  }
}

interface AuthState {
  user: User | null;
  loading: boolean;
  initialized: boolean;
}

// ============================================================================
// REACTIVE STATE (Svelte 5 Runes - Module Pattern)
// ============================================================================

// Internal reactive state
let _state = $state<AuthState>({
  user: null,
  loading: true,
  initialized: false,
});

// Cleanup function reference
let cleanupAuthListener: (() => void) | null = null;

// ============================================================================
// PUBLIC API - Reactive Getters
// ============================================================================

/**
 * Authentication store object with reactive getters
 */
export const authStore = {
  /**
   * Current authenticated user (or null)
   */
  get user() {
    return _state.user;
  },

  /**
   * Whether a user is currently authenticated
   */
  get isAuthenticated() {
    return !!_state.user;
  },

  /**
   * Whether auth state is currently loading
   */
  get isLoading() {
    return _state.loading;
  },

  /**
   * Whether auth has been initialized
   */
  get isInitialized() {
    return _state.initialized;
  },

  // ============================================================================
  // Methods
  // ============================================================================

  /**
   * Initialize the auth listener
   * Call this once when your app starts
   */
  async initialize() {
    if (cleanupAuthListener) {
      console.log("🔐 [authStore] Already initialized, skipping");
      return; // Already initialized
    }

    console.log("🔐 [authStore] Initializing auth state listener...");
    console.log("🔐 [authStore] Current URL:", typeof window !== "undefined" ? window.location.href : "SSR");

    // Handle redirect result from Google/Facebook sign-in
    try {
      console.log("🔐 [authStore] Checking for redirect result...");
      console.log("🔐 [authStore] Auth state before getRedirectResult:", {
        currentUser: auth.currentUser?.email || "none",
        appName: auth.app.name,
      });

      const result = await getRedirectResult(auth);

      if (result) {
        console.log("✅ [authStore] Sign-in redirect successful:", {
          uid: result.user.uid,
          email: result.user.email,
          displayName: result.user.displayName,
          provider: result.providerId,
          photoURL: result.user.photoURL,
        });
        console.log("🔐 [authStore] Full user object:", result.user);
        console.log("🔐 [authStore] Credential:", result.providerId);
      } else {
        console.log("ℹ️ [authStore] No redirect result (normal page load)");
        console.log("🔐 [authStore] URL at redirect check:", window.location.href);
        console.log("🔐 [authStore] URL search params:", window.location.search);
        console.log("🔐 [authStore] URL hash:", window.location.hash);
      }
    } catch (error: any) {
      console.error("❌ [authStore] Redirect result error:", {
        code: error.code,
        message: error.message,
        stack: error.stack,
      });
      // Don't block initialization on redirect errors
    }

    cleanupAuthListener = onAuthStateChanged(
      auth,
      async (user) => {
        if (user) {
          console.log("✅ [authStore] User authenticated:", {
            uid: user.uid,
            email: user.email,
            displayName: user.displayName,
            photoURL: user.photoURL,
            providerId: user.providerData?.[0]?.providerId,
          });

          // Update Facebook profile picture if needed (async, non-blocking)
          updateFacebookProfilePictureIfNeeded(user);
        } else {
          console.log("ℹ️ [authStore] User signed out");
        }

        _state = {
          user,
          loading: false,
          initialized: true,
        };
      },
      (error) => {
        console.error("❌ [authStore] Auth state change error:", error);
        _state = {
          user: null,
          loading: false,
          initialized: true,
        };
      }
    );

    console.log("🔐 [authStore] Auth state listener initialized");
  },

  /**
   * Sign out the current user
   */
  async signOut() {
    try {
      await firebaseSignOut(auth);
      // State will be updated automatically by onAuthStateChanged
    } catch (error) {
      console.error("Sign out error:", error);
      throw error;
    }
  },

  /**
   * Change user email (requires re-authentication)
   * @param newEmail - The new email address
   * @param currentPassword - Current password for re-authentication
   */
  async changeEmail(newEmail: string, currentPassword: string) {
    const user = _state.user;
    if (!user || !user.email) {
      throw new Error("No authenticated user");
    }

    try {
      console.log("🔐 [authStore] Re-authenticating user for email change...");

      // Re-authenticate user with current password
      const credential = EmailAuthProvider.credential(
        user.email,
        currentPassword
      );
      await reauthenticateWithCredential(user, credential);

      console.log("✅ [authStore] Re-authentication successful");
      console.log("📧 [authStore] Updating email to:", newEmail);

      // Update email
      await updateEmail(user, newEmail);

      console.log("✅ [authStore] Email updated successfully");
      console.log("📨 [authStore] Sending verification email...");

      // Send verification email to new address
      await sendEmailVerification(user);

      console.log("✅ [authStore] Verification email sent to:", newEmail);

      return {
        success: true,
        message: "Email updated successfully. Please check your inbox to verify your new email address.",
      };
    } catch (error: any) {
      console.error("❌ [authStore] Email change error:", error);

      // Handle specific Firebase errors
      if (error.code === "auth/wrong-password") {
        throw new Error("Incorrect password. Please try again.");
      } else if (error.code === "auth/email-already-in-use") {
        throw new Error("This email is already in use by another account.");
      } else if (error.code === "auth/invalid-email") {
        throw new Error("Invalid email address format.");
      } else if (error.code === "auth/requires-recent-login") {
        throw new Error("Please sign out and sign in again before changing your email.");
      } else {
        throw new Error(error.message || "Failed to change email. Please try again.");
      }
    }
  },

  /**
   * Update user's display name
   * @param displayName - The new display name
   */
  async updateDisplayName(displayName: string) {
    const user = _state.user;
    if (!user) {
      throw new Error("No authenticated user");
    }

    try {
      console.log("👤 [authStore] Updating display name to:", displayName);

      // Update display name
      await updateProfile(user, {
        displayName: displayName.trim() || null,
      });

      console.log("✅ [authStore] Display name updated successfully");

      return {
        success: true,
        message: "Display name updated successfully.",
      };
    } catch (error: any) {
      console.error("❌ [authStore] Display name update error:", error);
      throw new Error(error.message || "Failed to update display name. Please try again.");
    }
  },

  /**
   * Clean up the auth listener
   * Call this when your app unmounts (if ever)
   */
  cleanup() {
    if (cleanupAuthListener) {
      cleanupAuthListener();
      cleanupAuthListener = null;
    }
  },
};
