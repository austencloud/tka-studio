<script lang="ts">
  /**
   * Email/Password Authentication Component
   *
   * Provides email/password sign-in and sign-up functionality
   */

  import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    sendEmailVerification,
    browserLocalPersistence,
    indexedDBLocalPersistence,
    setPersistence,
    updateProfile,
  } from "firebase/auth";
  import { auth } from "../firebase";
  import { goto } from "$app/navigation";
  import { slide, fade } from "svelte/transition";

  // Props - accept mode as a binding
  let { mode = $bindable("signin" as "signin" | "signup") } = $props();

  let email = $state("");
  let password = $state("");
  let name = $state("");
  let showPassword = $state(false);
  let loading = $state(false);
  let error = $state<string | null>(null);
  let success = $state<string | null>(null);

  function togglePasswordVisibility() {
    showPassword = !showPassword;
  }

  async function handleSubmit() {
    loading = true;
    error = null;
    success = null;

    try {
      console.log(
        `🔐 [email] ${mode === "signin" ? "Signing in" : "Signing up"}...`
      );

      // Set persistence
      console.log(`🔐 [email] Setting persistence to IndexedDB...`);
      try {
        await setPersistence(auth, indexedDBLocalPersistence);
        console.log(`✅ [email] IndexedDB persistence set`);
      } catch (indexedDBErr) {
        await setPersistence(auth, browserLocalPersistence);
        console.log(`✅ [email] localStorage persistence set`);
      }

      if (mode === "signup") {
        // Sign up new user
        const result = await createUserWithEmailAndPassword(
          auth,
          email,
          password
        );
        console.log(`✅ [email] User created:`, result.user.uid);

        // Update profile with display name if provided
        if (name.trim()) {
          await updateProfile(result.user, {
            displayName: name.trim(),
          });
          console.log(`✅ [email] Display name set to:`, name.trim());
        }

        // Send verification email
        await sendEmailVerification(result.user);
        success =
          "Account created! Please check your email to verify your account.";

        // Wait a bit before redirecting
        await new Promise((resolve) => setTimeout(resolve, 2000));
      } else {
        // Sign in existing user
        const result = await signInWithEmailAndPassword(auth, email, password);
        console.log(`✅ [email] User signed in:`, result.user.uid);
      }

      // Navigate to home
      console.log(`🔐 [email] Navigating to home page...`);
      goto("/");
    } catch (err: any) {
      console.error(`❌ [email] Auth error:`, err);
      console.error(`❌ [email] Error code:`, err.code);

      // Handle specific error codes
      if (err.code === "auth/email-already-in-use") {
        error = "This email is already registered. Try signing in instead.";
        mode = "signin";
      } else if (err.code === "auth/weak-password") {
        error = "Password is too weak. Use at least 6 characters.";
      } else if (err.code === "auth/invalid-email") {
        error = "Invalid email address.";
      } else if (err.code === "auth/user-not-found") {
        error = "No account found with this email. Sign up instead?";
      } else if (err.code === "auth/wrong-password") {
        error = "Incorrect password.";
      } else if (err.code === "auth/invalid-credential") {
        error = "Invalid email or password.";
      } else {
        error = err.message || "An error occurred during authentication";
      }
    } finally {
      loading = false;
    }
  }

  function toggleMode() {
    mode = mode === "signin" ? "signup" : "signin";
    error = null;
    success = null;
    // Clear name field when switching modes
    if (mode === "signin") {
      name = "";
    }
  }
</script>

<form
  onsubmit={(e) => {
    e.preventDefault();
    handleSubmit();
  }}
  class="email-auth-form"
>
  <!-- Name field - only shown in signup mode -->
  {#if mode === "signup"}
    <div class="form-group" transition:slide={{ duration: 300 }}>
      <label for="name">Name (optional)</label>
      <input
        id="name"
        type="text"
        bind:value={name}
        placeholder="Your name"
        disabled={loading}
        autocomplete="name"
      />
    </div>
  {/if}

  <div class="form-group">
    <label for="email">Email</label>
    <input
      id="email"
      type="email"
      bind:value={email}
      placeholder="you@example.com"
      required
      disabled={loading}
      autocomplete="email"
    />
  </div>

  <div class="form-group">
    <label for="password">Password</label>
    <div class="password-input-wrapper">
      <input
        id="password"
        type={showPassword ? "text" : "password"}
        bind:value={password}
        placeholder="••••••••"
        required
        disabled={loading}
        minlength="6"
        autocomplete={mode === "signin" ? "current-password" : "new-password"}
      />
      <button
        type="button"
        class="password-toggle"
        onclick={togglePasswordVisibility}
        disabled={loading}
        aria-label={showPassword ? "Hide password" : "Show password"}
      >
        <i class="fas {showPassword ? 'fa-eye-slash' : 'fa-eye'}"></i>
      </button>
    </div>
    {#if mode === "signup"}
      <small class="password-hint" transition:slide={{ duration: 200 }}>
        Must be at least 6 characters
      </small>
    {/if}
  </div>

  {#if error}
    <p class="error-message" transition:slide={{ duration: 200 }}>{error}</p>
  {/if}

  {#if success}
    <p class="success-message" transition:slide={{ duration: 200 }}>
      {success}
    </p>
  {/if}

  <button type="submit" disabled={loading} class="submit-button">
    {#if loading}
      <span class="spinner"></span>
    {/if}
    {mode === "signin" ? "Sign In" : "Create Account"}
  </button>

  <button
    type="button"
    onclick={toggleMode}
    class="toggle-button"
    disabled={loading}
  >
    {mode === "signin"
      ? "Need an account? Sign up"
      : "Already have an account? Sign in"}
  </button>
</form>

<style>
  .email-auth-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  label {
    font-size: 0.875rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
  }

  input {
    padding: 0.75rem;
    padding-right: 0.75rem;
    border: 2px solid rgba(255, 255, 255, 0.15);
    border-radius: 0.75rem;
    font-size: 1rem;
    transition: all 0.2s ease;
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.95);
  }

  input::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }

  input:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.8);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    background: rgba(255, 255, 255, 0.08);
  }

  input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Password input wrapper for toggle button */
  .password-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }

  .password-input-wrapper input {
    width: 100%;
    padding-right: 3rem;
  }

  .password-toggle {
    position: absolute;
    right: 0.5rem;
    top: 50%;
    transform: translateY(-50%);
    width: 2.5rem;
    height: 2.5rem;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    font-size: 1rem;
  }

  .password-toggle:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
  }

  .password-toggle:active:not(:disabled) {
    transform: translateY(-50%) scale(0.95);
  }

  .password-toggle:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .password-toggle:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  .password-hint {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.5);
    margin-top: -0.25rem;
  }

  .submit-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 0.875rem 1.5rem;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: white;
    border: none;
    border-radius: 0.75rem;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 52px;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  }

  .submit-button:hover:not(:disabled) {
    background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
    transform: translateY(-1px);
  }

  .submit-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .submit-button:active:not(:disabled) {
    transform: translateY(0);
  }

  .toggle-button {
    padding: 0.75rem;
    background: transparent;
    color: rgba(99, 102, 241, 0.9);
    border: none;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border-radius: 0.5rem;
  }

  .toggle-button:hover:not(:disabled) {
    color: rgba(99, 102, 241, 1);
    background: rgba(99, 102, 241, 0.1);
  }

  .toggle-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
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
    color: #fca5a5;
    font-size: 0.875rem;
    text-align: center;
    padding: 0.75rem 1rem;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 0.75rem;
    margin: 0;
    line-height: 1.5;
  }

  .success-message {
    color: #86efac;
    font-size: 0.875rem;
    text-align: center;
    padding: 0.75rem 1rem;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 0.75rem;
    margin: 0;
    line-height: 1.5;
  }

  /* Responsive Design - iPhone SE and small screens */
  @media (max-height: 700px) {
    .email-auth-form {
      gap: 0.65rem; /* Reduced from 0.85rem to save space */
    }

    .form-group {
      gap: 0.35rem; /* Reduced from 0.4rem */
    }

    label {
      font-size: 0.8125rem;
    }

    input {
      padding: 0.65rem;
      font-size: 0.9375rem;
    }

    .submit-button {
      min-height: 50px;
      padding: 0.8125rem 1.375rem;
      font-size: 0.9375rem;
    }

    .toggle-button {
      padding: 0.65rem;
      font-size: 0.8125rem;
    }

    .password-hint {
      font-size: 0.6875rem;
    }
  }

  @media (max-height: 600px) {
    .email-auth-form {
      gap: 0.75rem;
    }

    .form-group {
      gap: 0.35rem;
    }

    label {
      font-size: 0.75rem;
    }

    input {
      padding: 0.5625rem;
      font-size: 0.875rem;
      border-radius: 0.625rem;
    }

    .password-input-wrapper input {
      padding-right: 2.75rem;
    }

    .password-toggle {
      width: 2.25rem;
      height: 2.25rem;
      font-size: 0.9375rem;
    }

    .submit-button {
      min-height: 48px;
      padding: 0.75rem 1.25rem;
      font-size: 0.875rem;
      gap: 0.625rem;
    }

    .toggle-button {
      padding: 0.5625rem;
      font-size: 0.75rem;
    }

    .password-hint,
    .error-message,
    .success-message {
      font-size: 0.625rem;
      padding: 0.625rem 0.875rem;
    }
  }

  @media (max-height: 568px) {
    .email-auth-form {
      gap: 0.625rem;
    }

    .form-group {
      gap: 0.25rem;
    }

    label {
      font-size: 0.6875rem;
    }

    input {
      padding: 0.5rem;
      font-size: 0.8125rem;
      border-radius: 0.5rem;
    }

    .password-input-wrapper input {
      padding-right: 2.5rem;
    }

    .password-toggle {
      width: 2rem;
      height: 2rem;
      font-size: 0.875rem;
      right: 0.375rem;
    }

    .submit-button {
      min-height: 44px;
      padding: 0.625rem 1.125rem;
      font-size: 0.8125rem;
      gap: 0.5rem;
      border-radius: 0.625rem;
    }

    .toggle-button {
      padding: 0.5rem;
      font-size: 0.6875rem;
      border-radius: 0.375rem;
    }

    .password-hint,
    .error-message,
    .success-message {
      font-size: 0.5625rem;
      padding: 0.5rem 0.75rem;
      line-height: 1.4;
    }

    .spinner {
      width: 0.875rem;
      height: 0.875rem;
    }
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .submit-button:hover,
    .password-toggle:active {
      transform: none;
    }
  }
</style>
