/**
 * Google Identity Services Integration
 *
 * Uses Google's Identity Services (GIS) to handle OAuth sign-in,
 * then exchanges the credential with Firebase Auth.
 *
 * This bypasses Firebase's signInWithRedirect/signInWithPopup issues
 * caused by third-party storage blocking in modern browsers.
 *
 * Reference: https://developers.google.com/identity/gsi/web
 */

import {
  GoogleAuthProvider,
  signInWithCredential,
  signInWithPopup,
} from "firebase/auth";
import { auth } from "../../firebase";

interface GoogleIdentityConfig {
  clientId: string;
  callback: (response: GoogleCredentialResponse) => void;
}

interface GoogleCredentialResponse {
  credential: string;
  select_by?: string;
}

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (config: GoogleIdentityConfig) => void;
          prompt: (momentListener?: (notification: any) => void) => void;
          renderButton: (
            parent: HTMLElement,
            options: {
              type?: "standard" | "icon";
              theme?: "outline" | "filled_blue" | "filled_black";
              size?: "large" | "medium" | "small";
              text?: "signin_with" | "signup_with" | "continue_with" | "signin";
              shape?: "rectangular" | "pill" | "circle" | "square";
              logo_alignment?: "left" | "center";
              width?: number;
              locale?: string;
            }
          ) => void;
          cancel: () => void;
        };
      };
    };
  }
}

export class GoogleIdentityService {
  private clientId: string;
  private initialized = false;

  constructor(clientId: string) {
    this.clientId = clientId;
  }

  /**
   * Initialize Google Identity Services
   * Call this once when your app loads
   */
  initialize(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.initialized) {
        console.log("🔐 [GoogleIdentity] Already initialized");
        resolve();
        return;
      }

      if (typeof window === "undefined") {
        reject(
          new Error("Google Identity Services requires browser environment")
        );
        return;
      }

      // Check if script is already loaded
      if (window.google?.accounts?.id) {
        console.log("🔐 [GoogleIdentity] SDK already loaded");
        this.initializeGoogleIdentity();
        this.initialized = true;
        resolve();
        return;
      }

      // Wait for script to load (added in app.html)
      const checkInterval = setInterval(() => {
        if (window.google?.accounts?.id) {
          clearInterval(checkInterval);
          console.log("🔐 [GoogleIdentity] SDK loaded, initializing...");
          this.initializeGoogleIdentity();
          this.initialized = true;
          resolve();
        }
      }, 100);

      // Timeout after 5 seconds
      setTimeout(() => {
        clearInterval(checkInterval);
        if (!this.initialized) {
          reject(
            new Error(
              "Google Identity Services script failed to load after 5 seconds"
            )
          );
        }
      }, 5000);
    });
  }

  /**
   * Initialize Google Identity Services SDK
   */
  private initializeGoogleIdentity(): void {
    if (!window.google?.accounts?.id) {
      console.error("❌ [GoogleIdentity] SDK not available");
      return;
    }

    window.google.accounts.id.initialize({
      clientId: this.clientId,
      callback: this.handleCredentialResponse.bind(this),
    });

    console.log(
      "✅ [GoogleIdentity] Initialized with client ID:",
      this.clientId
    );
  }

  /**
   * Handle the credential response from Google
   */
  private async handleCredentialResponse(
    response: GoogleCredentialResponse
  ): Promise<void> {
    console.log("🔐 [GoogleIdentity] Received credential response");

    try {
      // Create a Google credential for Firebase
      const credential = GoogleAuthProvider.credential(response.credential);

      console.log("🔐 [GoogleIdentity] Exchanging credential with Firebase...");

      // Sign in to Firebase with the credential
      const userCredential = await signInWithCredential(auth, credential);

      console.log("✅ [GoogleIdentity] Sign-in successful:", {
        uid: userCredential.user.uid,
        email: userCredential.user.email,
        displayName: userCredential.user.displayName,
      });
    } catch (error: any) {
      console.error("❌ [GoogleIdentity] Sign-in error:", error);
      throw new Error(`Google sign-in failed: ${error.message}`);
    }
  }

  /**
   * Trigger Google sign-in using popup
   * Falls back from One Tap since it doesn't work reliably on localhost
   */
  async signInWithPopup(): Promise<void> {
    console.log("🔐 [GoogleIdentity] Using Firebase popup flow as fallback...");

    try {
      const provider = new GoogleAuthProvider();
      provider.addScope("email");
      provider.addScope("profile");

      console.log("🔐 [GoogleIdentity] Opening popup...");
      const userCredential = await signInWithPopup(auth, provider);

      console.log("✅ [GoogleIdentity] Sign-in successful:", {
        uid: userCredential.user.uid,
        email: userCredential.user.email,
        displayName: userCredential.user.displayName,
      });
    } catch (error: any) {
      console.error("❌ [GoogleIdentity] Popup sign-in error:", error);

      // If popup is blocked by COOP, provide helpful error
      if (
        error.code === "auth/popup-blocked" ||
        error.code === "auth/popup-closed-by-user"
      ) {
        throw new Error(
          "Popup was blocked. Please allow popups for this site and try again."
        );
      } else if (error.code === "auth/cancelled-popup-request") {
        throw new Error("Sign-in cancelled. Please try again.");
      } else {
        throw new Error(`Google sign-in failed: ${error.message}`);
      }
    }
  }

  /**
   * Render a Google Sign-In button
   * @param element - The HTML element to render the button into
   * @param options - Button customization options
   */
  renderButton(
    element: HTMLElement,
    options?: {
      type?: "standard" | "icon";
      theme?: "outline" | "filled_blue" | "filled_black";
      size?: "large" | "medium" | "small";
      text?: "signin_with" | "signup_with" | "continue_with" | "signin";
      width?: number;
    }
  ): void {
    if (!this.initialized) {
      console.error(
        "❌ [GoogleIdentity] Not initialized. Call initialize() first."
      );
      return;
    }

    if (!window.google?.accounts?.id) {
      console.error("❌ [GoogleIdentity] SDK not available");
      return;
    }

    console.log("🔐 [GoogleIdentity] Rendering button...");
    window.google.accounts.id.renderButton(element, {
      type: options?.type || "standard",
      theme: options?.theme || "outline",
      size: options?.size || "large",
      text: options?.text || "signin_with",
      ...(options?.width !== undefined && { width: options.width }),
      shape: "rectangular",
      logo_alignment: "left",
    });
  }

  /**
   * Cancel any ongoing One Tap flows
   */
  cancel(): void {
    if (window.google?.accounts?.id) {
      window.google.accounts.id.cancel();
    }
  }
}
