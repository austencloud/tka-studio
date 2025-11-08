/**
 * Authentication Service Implementation
 *
 * Handles all Firebase authentication operations including social auth
 * (Google, Facebook) and email/password authentication.
 */

import {
  GoogleAuthProvider,
  FacebookAuthProvider,
  signInWithRedirect,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut as firebaseSignOut,
  setPersistence,
  indexedDBLocalPersistence,
  browserLocalPersistence,
  sendEmailVerification,
  updateProfile,
} from "firebase/auth";
import { auth } from "../../firebase";
import { injectable } from "inversify";
import type { IAuthService } from "../contracts";

@injectable()
export class AuthService implements IAuthService {
  // ============================================================================
  // SOCIAL AUTHENTICATION
  // ============================================================================

  async signInWithGoogle(): Promise<void> {
    console.log("🔐 [google] Starting sign-in process...");

    try {
      // Create Google provider
      const provider = new GoogleAuthProvider();
      provider.addScope("email");
      provider.addScope("profile");

      console.log("🔐 [google] Redirecting to Google sign-in...");
      await signInWithRedirect(auth, provider);
    } catch (error: any) {
      console.error("❌ [google] Sign-in error:", error);
      throw new Error(`Google sign-in failed: ${error.message}`);
    }
  }

  async signInWithFacebook(): Promise<void> {
    console.log("🔐 [facebook] Starting sign-in process...");

    try {
      // Create Facebook provider
      const provider = new FacebookAuthProvider();
      provider.addScope("email");
      provider.addScope("public_profile");

      console.log("🔐 [facebook] Redirecting to Facebook sign-in...");
      await signInWithRedirect(auth, provider);
    } catch (error: any) {
      console.error("❌ [facebook] Sign-in error:", error);
      throw new Error(`Facebook sign-in failed: ${error.message}`);
    }
  }

  // ============================================================================
  // EMAIL/PASSWORD AUTHENTICATION
  // ============================================================================

  async signInWithEmail(email: string, password: string): Promise<void> {
    console.log("🔐 [email] Starting sign-in process...");

    try {
      // Set persistence first
      await this.setPersistence();

      // Sign in with email and password
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
      );

      console.log("✅ [email] Sign-in successful:", userCredential.user.email);
    } catch (error: any) {
      console.error("❌ [email] Sign-in error:", error);
      throw new Error(`Email sign-in failed: ${error.message}`);
    }
  }

  async signUpWithEmail(
    email: string,
    password: string,
    name?: string
  ): Promise<void> {
    console.log("🔐 [email] Starting sign-up process...");

    try {
      // Set persistence first
      await this.setPersistence();

      // Create user with email and password
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        email,
        password
      );

      console.log("✅ [email] User created:", userCredential.user.email);

      // Update profile with display name if provided
      if (name && userCredential.user) {
        await updateProfile(userCredential.user, { displayName: name });
        console.log("✅ [email] Profile updated with name:", name);
      }

      // Send email verification
      if (userCredential.user) {
        await sendEmailVerification(userCredential.user);
        console.log("✅ [email] Verification email sent");
      }
    } catch (error: any) {
      console.error("❌ [email] Sign-up error:", error);
      throw new Error(`Email sign-up failed: ${error.message}`);
    }
  }

  // ============================================================================
  // SIGN OUT
  // ============================================================================

  async signOut(): Promise<void> {
    console.log("🔐 [auth] Signing out...");

    try {
      await firebaseSignOut(auth);
      console.log("✅ [auth] Sign-out successful");
    } catch (error: any) {
      console.error("❌ [auth] Sign-out error:", error);
      throw new Error(`Sign-out failed: ${error.message}`);
    }
  }

  // ============================================================================
  // PERSISTENCE
  // ============================================================================

  async setPersistence(): Promise<void> {
    try {
      // Try IndexedDB first (preferred)
      await setPersistence(auth, indexedDBLocalPersistence);
      console.log("✅ [auth] IndexedDB persistence set");
    } catch (indexedDBError) {
      console.warn(
        "⚠️ [auth] IndexedDB persistence failed, falling back to localStorage"
      );

      try {
        // Fallback to localStorage
        await setPersistence(auth, browserLocalPersistence);
        console.log("✅ [auth] localStorage persistence set");
      } catch (localStorageError: any) {
        console.error(
          "❌ [auth] Failed to set persistence:",
          localStorageError
        );
        throw new Error(
          `Failed to set persistence: ${localStorageError.message}`
        );
      }
    }
  }
}
