/**
 * Smart Contact Utilities
 *
 * Handles intelligent contact functionality that can detect Google sign-in status
 * and automatically open Gmail with pre-filled compose window when appropriate.
 *
 * Features:
 * - Detects if user is signed into Google using multiple methods:
 *   1. Google authentication cookies (most reliable)
 *   2. Domain access detection
 *   3. Local/session storage auth state
 *   4. Google API library presence
 *
 * - If Google sign-in detected: Opens Gmail compose with pre-filled content
 * - If not detected: Falls back to standard mailto: link
 *
 * - Provides user feedback during detection process
 * - Graceful fallback if any method fails
 *
 * Usage:
 * ```typescript
 * import { smartContact, DEV_CONTACT_OPTIONS } from './smart-contact';
 *
 * // Use predefined dev contact options
 * await smartContact(DEV_CONTACT_OPTIONS);
 *
 * // Or create custom options
 * await smartContact({
 *   to: 'user@example.com',
 *   subject: 'Custom Subject',
 *   body: 'Custom message body'
 * });
 * ```
 */

export interface ContactOptions {
  to: string;
  subject?: string;
  body?: string;
  cc?: string;
  bcc?: string;
}

/**
 * Checks if user is likely signed into Google using multiple detection methods
 */
async function isGoogleSignedIn(): Promise<boolean> {
  try {
    // Method 1: Check for Google accounts cookies (most reliable)
    if (
      document.cookie.includes("__Secure-3PSID") ||
      document.cookie.includes("SAPISID")
    ) {
      return true;
    }

    // Method 2: Try to detect if user has Gmail open in another tab
    // by checking if we can access gmail.com domain
    try {
      const response = await fetch(
        "https://accounts.google.com/signin/v2/identifier",
        {
          method: "HEAD",
          mode: "no-cors",
          credentials: "include",
        }
      );
      // If this doesn't throw, user might be signed in
      return true;
    } catch {
      // CORS or network error - continue to next method
    }

    // Method 3: Check for Google Auth state in localStorage (if app uses Google Auth)
    const googleAuthState =
      localStorage.getItem("google_auth_state") ||
      localStorage.getItem("google_user") ||
      sessionStorage.getItem("google_auth_state");

    if (googleAuthState) {
      try {
        const authData = JSON.parse(googleAuthState);
        return (
          authData &&
          (authData.signedIn || authData.isSignedIn || authData.access_token)
        );
      } catch {
        // Invalid JSON - ignore
      }
    }

    // Method 4: Check if gapi is loaded and user is signed in
    if (typeof window !== "undefined" && (window as any).gapi?.auth2) {
      const authInstance = (window as any).gapi.auth2.getAuthInstance();
      if (
        authInstance &&
        authInstance.isSignedIn &&
        authInstance.isSignedIn.get()
      ) {
        return true;
      }
    }

    // Default to false if no indicators found
    return false;
  } catch (error) {
    console.debug("Google sign-in detection failed:", error);
    return false;
  }
}

/**
 * Opens Gmail compose window with pre-filled fields
 */
function openGmailCompose(options: ContactOptions): void {
  const params = new URLSearchParams();

  params.set("to", options.to);
  if (options.subject) params.set("su", options.subject);
  if (options.body) params.set("body", options.body);
  if (options.cc) params.set("cc", options.cc);
  if (options.bcc) params.set("bcc", options.bcc);

  const gmailUrl = `https://mail.google.com/mail/?view=cm&fs=1&${params.toString()}`;
  window.open(gmailUrl, "_blank", "noopener,noreferrer");
}

/**
 * Opens default email client with mailto: link
 */
function openMailtoLink(options: ContactOptions): void {
  const params = new URLSearchParams();

  if (options.subject) params.set("subject", options.subject);
  if (options.body) params.set("body", options.body);
  if (options.cc) params.set("cc", options.cc);
  if (options.bcc) params.set("bcc", options.bcc);

  const mailtoUrl = `mailto:${options.to}?${params.toString()}`;
  window.location.href = mailtoUrl;
}

/**
 * Smart contact function that detects Google sign-in and chooses the best method
 */
export async function smartContact(options: ContactOptions): Promise<void> {
  try {
    // Show user we're detecting their preferred email method
    console.log("🔍 Detecting your preferred email method...");

    const isSignedIn = await isGoogleSignedIn();

    if (isSignedIn) {
      console.log("✅ Gmail detected - opening Gmail compose window");
      // User is signed into Google - open Gmail compose
      openGmailCompose(options);
    } else {
      console.log("📧 Opening default email client");
      // User is not signed in or detection failed - use mailto
      openMailtoLink(options);
    }
  } catch (error) {
    console.warn(
      "Smart contact detection failed, falling back to mailto:",
      error
    );
    // Fallback to mailto if anything goes wrong
    openMailtoLink(options);
  }
}

/**
 * Predefined contact options for development collaboration
 */
export const DEV_CONTACT_OPTIONS: ContactOptions = {
  to: "austencloud@gmail.com",
  subject: "Development Collaboration - TKA Studio",
  body: `Hi there!

I'm interested in collaborating on TKA Studio. Here are some details about my background and what I'd like to contribute:

[Please describe your experience and how you'd like to help]

Technical Background:
- Programming languages:
- Areas of expertise:
- Availability:

Specific Interests:
- [ ] Frontend development (Svelte/TypeScript)
- [ ] Backend/API development
- [ ] UI/UX design
- [ ] Testing and quality assurance
- [ ] Documentation
- [ ] Other:

Looking forward to hearing from you!

Best regards,
[Your name]`,
};

/**
 * Copies text to clipboard using modern Clipboard API
 */
async function copyToClipboard(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    } else {
      // Fallback for older browsers
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-999999px";
      textArea.style.top = "-999999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      const successful = document.execCommand("copy");
      document.body.removeChild(textArea);
      return successful;
    }
  } catch (error) {
    console.error("Failed to copy to clipboard:", error);
    return false;
  }
}

/**
 * Shows a temporary toast notification
 */
function showToast(message: string, duration: number = 3000): void {
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    font-size: 0.9375rem;
    font-weight: 600;
    z-index: 100000;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    animation: slideUp 0.3s ease;
  `;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = "slideDown 0.3s ease";
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, duration);
}

/**
 * Smart email contact using 2025 best practices:
 * 1. Web Share API (native OS sharing dialog) - PRIMARY
 * 2. Copy to clipboard - UNIVERSAL FALLBACK
 * 3. Mailto link - LAST RESORT
 *
 * This approach avoids the PayPal redirect bug and other mailto issues on mobile.
 */
export async function smartEmailContact(email: string): Promise<void> {
  try {
    // Try Web Share API first (works on all mobile browsers except Firefox)
    if (navigator.share) {
      try {
        await navigator.share({
          title: "Email Contact",
          text: `Contact us at: ${email}`,
          url: `mailto:${email}`,
        });
        console.log("✅ Email shared via Web Share API");
        return;
      } catch (error: any) {
        // User cancelled or share failed
        if (error.name !== "AbortError") {
          console.debug("Web Share API failed:", error);
        }
      }
    }

    // Fallback to copy-to-clipboard
    const copied = await copyToClipboard(email);
    if (copied) {
      showToast(`✓ Email copied: ${email}`);
      console.log("✅ Email copied to clipboard");
      return;
    }

    // Last resort: mailto link
    console.log("📧 Opening mailto link");
    window.location.href = `mailto:${email}`;
  } catch (error) {
    console.error("Smart email contact failed:", error);
    // Final fallback
    window.location.href = `mailto:${email}`;
  }
}
