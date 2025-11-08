<script lang="ts">
  /**
   * Passwordless Email Link Authentication
   *
   * Sends a magic link to the user's email for passwordless sign-in
   */

  import {
    sendSignInLinkToEmail,
    isSignInWithEmailLink,
    signInWithEmailLink,
    browserLocalPersistence,
    indexedDBLocalPersistence,
    setPersistence,
  } from "firebase/auth";
  import { auth } from "../firebase";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  let email = $state("");
  let loading = $state(false);
  let error = $state<string | null>(null);
  let success = $state<string | null>(null);

  // Check if we're completing a sign-in from an email link
  onMount(async () => {
    if (isSignInWithEmailLink(auth, window.location.href)) {
      console.log("🔐 [email-link] Detected email link sign-in");
      await completeSignIn();
    }
  });

  async function sendEmailLink() {
    loading = true;
    error = null;
    success = null;

    try {
      console.log(`🔐 [email-link] Sending sign-in link to ${email}`);

      // Configure the email action handler
      const actionCodeSettings = {
        // URL where the user will be redirected after clicking the link
        url: window.location.origin + "/auth/login",
        handleCodeInApp: true,
      };

      // Send the email link
      await sendSignInLinkToEmail(auth, email, actionCodeSettings);

      // Save the email locally so we can complete sign-in on the same device
      window.localStorage.setItem("emailForSignIn", email);

      console.log(`✅ [email-link] Email sent successfully to ${email}`);
      success = `Magic link sent! Check your email at ${email}`;
    } catch (err: any) {
      console.error(`❌ [email-link] Error sending email:`, err);
      console.error(`❌ [email-link] Error code:`, err.code);

      if (err.code === "auth/invalid-email") {
        error = "Invalid email address.";
      } else if (err.code === "auth/missing-email") {
        error = "Please enter your email address.";
      } else {
        error = err.message || "Failed to send email. Please try again.";
      }
    } finally {
      loading = false;
    }
  }

  async function completeSignIn() {
    console.log("🔐 [email-link] Completing sign-in...");

    try {
      // Set persistence before sign-in
      console.log(`🔐 [email-link] Setting persistence...`);
      try {
        await setPersistence(auth, indexedDBLocalPersistence);
        console.log(`✅ [email-link] IndexedDB persistence set`);
      } catch (indexedDBErr) {
        await setPersistence(auth, browserLocalPersistence);
        console.log(`✅ [email-link] localStorage persistence set`);
      }

      // Get the email from localStorage
      let savedEmail = window.localStorage.getItem("emailForSignIn");

      if (!savedEmail) {
        // User opened the link on a different device
        // Ask for email to prevent session fixation attacks
        console.log("⚠️ [email-link] Email not found in storage, asking user");
        savedEmail = window.prompt(
          "Please enter your email address to confirm:"
        );
      }

      if (!savedEmail) {
        error = "Email address is required to complete sign-in.";
        return;
      }

      console.log(`🔐 [email-link] Signing in with email: ${savedEmail}`);

      // Sign in with the email link
      const result = await signInWithEmailLink(
        auth,
        savedEmail,
        window.location.href
      );

      console.log(`✅ [email-link] User signed in:`, result.user.uid);
      console.log(`✅ [email-link] Email verified:`, result.user.emailVerified);

      // Clear the email from storage
      window.localStorage.removeItem("emailForSignIn");

      // Navigate to home
      console.log(`🔐 [email-link] Navigating to home...`);
      goto("/");
    } catch (err: any) {
      console.error(`❌ [email-link] Sign-in error:`, err);
      console.error(`❌ [email-link] Error code:`, err.code);

      if (err.code === "auth/invalid-email") {
        error = "Invalid email address.";
      } else if (err.code === "auth/invalid-action-code") {
        error =
          "This link is invalid or has expired. Please request a new one.";
      } else if (err.code === "auth/expired-action-code") {
        error = "This link has expired. Please request a new one.";
      } else {
        error = err.message || "Failed to sign in. Please try again.";
      }
    }
  }

  function handleSubmit() {
    sendEmailLink();
  }
</script>

<form
  onsubmit={(e) => {
    e.preventDefault();
    handleSubmit();
  }}
  class="email-link-form"
>
  <div class="form-header">
    <h3>Sign in with Email Link</h3>
    <p>We'll send you a magic link - no password needed!</p>
  </div>

  <div class="form-group">
    <label for="email-link">Email</label>
    <input
      id="email-link"
      type="email"
      bind:value={email}
      placeholder="you@example.com"
      required
      disabled={loading}
    />
  </div>

  {#if error}
    <p class="error-message">{error}</p>
  {/if}

  {#if success}
    <div class="success-message">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
      <span>{success}</span>
    </div>
  {/if}

  <button type="submit" disabled={loading} class="submit-button">
    {#if loading}
      <span class="spinner"></span>
      Sending...
    {:else}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path
          d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
        ></path>
        <polyline points="22,6 12,13 2,6"></polyline>
      </svg>
      Send Magic Link
    {/if}
  </button>
</form>

<style>
  .email-link-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }

  .form-header {
    text-align: center;
    margin-bottom: 0.5rem;
  }

  .form-header h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1f2937;
    margin: 0 0 0.25rem 0;
  }

  .form-header p {
    font-size: 0.875rem;
    color: #6b7280;
    margin: 0;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #374151;
  }

  input {
    padding: 0.75rem;
    border: 2px solid #e5e7eb;
    border-radius: 0.5rem;
    font-size: 1rem;
    transition: all 0.2s ease;
  }

  input:focus {
    outline: none;
    border-color: #8b5cf6;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
  }

  input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .submit-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 44px;
    box-shadow: 0 4px 6px rgba(139, 92, 246, 0.2);
  }

  .submit-button:hover:not(:disabled) {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    box-shadow: 0 6px 8px rgba(139, 92, 246, 0.3);
    transform: translateY(-1px);
  }

  .submit-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .submit-button:active:not(:disabled) {
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
    text-align: center;
    padding: 0.75rem;
    background: rgba(239, 68, 68, 0.1);
    border-radius: 0.5rem;
    margin: 0;
  }

  .success-message {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    color: #10b981;
    font-size: 0.875rem;
    text-align: center;
    padding: 0.75rem;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 0.5rem;
    margin: 0;
  }

  .success-message svg {
    flex-shrink: 0;
  }

  /* Dark mode support */
  @media (prefers-color-scheme: dark) {
    .form-header h3 {
      color: #f9fafb;
    }

    .form-header p {
      color: #9ca3af;
    }

    label {
      color: #d1d5db;
    }

    input {
      background: #374151;
      border-color: #4b5563;
      color: white;
    }

    input:focus {
      border-color: #a78bfa;
      box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.1);
    }
  }
</style>
