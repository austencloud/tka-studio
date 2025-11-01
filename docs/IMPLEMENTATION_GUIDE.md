# Complete Implementation Guide

This guide shows you how to use the authentication system throughout your TKA Studio application.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Using Auth in Components](#using-auth-in-components)
3. [Protected Routes](#protected-routes)
4. [Adding Login to Navigation](#adding-login-to-navigation)
5. [Customizing UI](#customizing-ui)
6. [Advanced Usage](#advanced-usage)

## Quick Start

### 1. Set Up Firebase

Follow these guides in order:

1. [Firebase Setup](./FIREBASE_SETUP.md) - Create Firebase project and get credentials
2. [Facebook OAuth Setup](./FACEBOOK_OAUTH_SETUP.md) - Enable Facebook login

### 2. Configure Environment

Your `.env` file should look like this:

```env
PUBLIC_FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
PUBLIC_FIREBASE_PROJECT_ID=your-project-id
PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789012
PUBLIC_FIREBASE_APP_ID=1:123456789012:web:abcdef1234567890
```

### 3. Test Authentication

Start your server and test:

```bash
npm run dev
```

Visit:

- `/auth/login` - Login page
- `/profile` - User profile (requires login)

## Using Auth in Components

The authentication system provides reactive stores you can use anywhere in your app.

### Basic Usage

```svelte
<script lang="ts">
  import { user, isAuthenticated, isLoading } from "$shared/auth";
</script>

{#if $isLoading}
  <p>Loading...</p>
{:else if $isAuthenticated}
  <p>Welcome, {$user?.displayName || $user?.email}!</p>
{:else}
  <a href="/auth/login">Sign in</a>
{/if}
```

### Available Stores

```typescript
import {
  user, // Firebase User object (or null)
  isAuthenticated, // boolean - true if logged in
  isLoading, // boolean - true while checking auth state
  isInitialized, // boolean - true after first auth check
  authStore, // Full store with helper methods
} from "$shared/auth";
```

### User Object Properties

When a user is logged in, `$user` contains:

```typescript
{
  uid: string; // Unique user ID
  email: string | null; // User's email
  displayName: string | null; // User's name
  photoURL: string | null; // Profile picture URL
  emailVerified: boolean; // Email verification status
  providerData: Array<{
    // Info about login providers
    providerId: string; // "facebook.com", "google.com", etc.
    uid: string;
    displayName: string | null;
    email: string | null;
    photoURL: string | null;
  }>;
  metadata: {
    creationTime: string; // Account creation date
    lastSignInTime: string; // Last login date
  }
}
```

## Protected Routes

There are two ways to protect routes that require authentication:

### Method 1: Component-Level (Recommended)

Redirect unauthenticated users in the component:

```svelte
<script lang="ts">
  import { isAuthenticated, isLoading } from "$shared/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  onMount(() => {
    const unsubscribe = isAuthenticated.subscribe((authenticated) => {
      if (!authenticated && !$isLoading) {
        goto("/auth/login");
      }
    });

    return unsubscribe;
  });
</script>

{#if $isLoading}
  <p>Loading...</p>
{:else if $isAuthenticated}
  <!-- Your protected content -->
  <h1>Protected Page</h1>
{/if}
```

### Method 2: Layout-Level

Create a protected layout for multiple pages:

```svelte
<!-- src/routes/(protected)/+layout.svelte -->
<script lang="ts">
  import { isAuthenticated, isLoading } from "$shared/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import type { Snippet } from "svelte";

  let { children } = $props<{ children: Snippet }>();

  onMount(() => {
    const unsubscribe = isAuthenticated.subscribe((authenticated) => {
      if (!authenticated && !$isLoading) {
        goto(
          "/auth/login?redirect=" + encodeURIComponent(window.location.pathname)
        );
      }
    });

    return unsubscribe;
  });
</script>

{#if $isLoading}
  <div class="loading">Checking authentication...</div>
{:else if $isAuthenticated}
  {@render children()}
{/if}
```

Then any route under `(protected)` will require login:

```
src/routes/
  (protected)/
    dashboard/
      +page.svelte  ← Requires login
    settings/
      +page.svelte  ← Requires login
  auth/
    login/
      +page.svelte  ← Public
```

## Adding Login to Navigation

### Simple Navigation Button

```svelte
<script lang="ts">
  import { user, isAuthenticated } from "$shared/auth";
  import { UserMenu } from "$shared/auth/components";
</script>

<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>

  {#if $isAuthenticated}
    <UserMenu />
  {:else}
    <a href="/auth/login">Sign In</a>
  {/if}
</nav>
```

### Advanced Navigation with User Menu

```svelte
<script lang="ts">
  import { user, isAuthenticated } from "$shared/auth";
  import { UserMenu } from "$shared/auth/components";
</script>

<nav class="navbar">
  <div class="nav-brand">
    <a href="/">TKA</a>
  </div>

  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/explore">Explore</a>

    {#if $isAuthenticated}
      <a href="/build">Build</a>
      <a href="/profile">Profile</a>
    {/if}
  </div>

  <div class="nav-actions">
    {#if $isAuthenticated}
      <UserMenu />
    {:else}
      <a href="/auth/login" class="btn-primary">Sign In</a>
    {/if}
  </div>
</nav>

<style>
  .navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .nav-links {
    display: flex;
    gap: 2rem;
  }

  .btn-primary {
    padding: 0.5rem 1rem;
    background: #3b82f6;
    color: white;
    border-radius: 0.5rem;
    text-decoration: none;
  }
</style>
```

## Customizing UI

### Custom Login Button

Create your own styled login button:

```svelte
<script lang="ts">
  import { signInWithPopup, FacebookAuthProvider } from "firebase/auth";
  import { auth } from "$shared/auth";

  let loading = $state(false);
  let error = $state<string | null>(null);

  async function handleLogin() {
    loading = true;
    error = null;

    try {
      const provider = new FacebookAuthProvider();
      await signInWithPopup(auth, provider);
      // User is now logged in!
    } catch (err: any) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<button onclick={handleLogin} disabled={loading} class="my-custom-button">
  {#if loading}
    <span class="spinner"></span>
  {:else}
    <img src="/facebook-icon.svg" alt="" />
  {/if}
  Login with Facebook
</button>

{#if error}
  <p class="error">{error}</p>
{/if}
```

### Custom User Avatar

```svelte
<script lang="ts">
  import { user } from "$shared/auth";

  const avatarUrl = $derived($user?.photoURL);
  const displayName = $derived($user?.displayName || $user?.email || "User");
  const initials = $derived(
    displayName
      .split(" ")
      .map((n: string) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2)
  );
</script>

<div class="avatar">
  {#if avatarUrl}
    <img src={avatarUrl} alt={displayName} />
  {:else}
    <div class="avatar-fallback">{initials}</div>
  {/if}
</div>

<style>
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
  }

  .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .avatar-fallback {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: 600;
  }
</style>
```

## Advanced Usage

### Sign Out Programmatically

```svelte
<script lang="ts">
  import { authStore } from "$shared/auth";

  async function handleSignOut() {
    try {
      await authStore.signOut();
      // User is now signed out
    } catch (error) {
      console.error("Sign out error:", error);
    }
  }
</script>

<button onclick={handleSignOut}>Sign Out</button>
```

### Check Specific Provider

```svelte
<script lang="ts">
  import { user } from "$shared/auth";

  const isLoggedInWithFacebook = $derived(
    $user?.providerData?.some((p) => p.providerId === "facebook.com") ?? false
  );

  const isLoggedInWithGoogle = $derived(
    $user?.providerData?.some((p) => p.providerId === "google.com") ?? false
  );
</script>

{#if isLoggedInWithFacebook}
  <p>You're logged in with Facebook</p>
{:else if isLoggedInWithGoogle}
  <p>You're logged in with Google</p>
{/if}
```

### Request Additional Permissions

```typescript
import { signInWithPopup, FacebookAuthProvider } from "firebase/auth";
import { auth } from "$shared/auth";

async function loginWithExtraPermissions() {
  const provider = new FacebookAuthProvider();

  // Request additional Facebook permissions
  provider.addScope("user_birthday");
  provider.addScope("user_location");

  try {
    const result = await signInWithPopup(auth, provider);

    // Get Facebook access token
    const credential = FacebookAuthProvider.credentialFromResult(result);
    const accessToken = credential?.accessToken;

    // Use access token to call Facebook Graph API
    if (accessToken) {
      const response = await fetch(
        `https://graph.facebook.com/me?fields=birthday,location&access_token=${accessToken}`
      );
      const data = await response.json();
      console.log("Additional data:", data);
    }
  } catch (error) {
    console.error("Login error:", error);
  }
}
```

### Handle Authentication Errors

```typescript
import { signInWithPopup, FacebookAuthProvider } from "firebase/auth";
import { auth } from "$shared/auth";

async function handleLogin() {
  try {
    const provider = new FacebookAuthProvider();
    await signInWithPopup(auth, provider);
  } catch (error: any) {
    switch (error.code) {
      case "auth/popup-closed-by-user":
        console.log("User closed the popup");
        break;

      case "auth/popup-blocked":
        alert("Please allow popups for this site");
        break;

      case "auth/account-exists-with-different-credential":
        alert(
          "An account already exists with the same email using a different sign-in method"
        );
        break;

      case "auth/cancelled-popup-request":
        // Another popup is already open, ignore
        break;

      default:
        console.error("Authentication error:", error);
        alert("An error occurred. Please try again.");
    }
  }
}
```

### Persist Auth State Across Tabs

Firebase Auth automatically syncs across browser tabs! No extra configuration needed.

### Listen to Auth Changes

```typescript
import { onMount } from "svelte";
import { authStore } from "$shared/auth";

onMount(() => {
  // The authStore automatically listens to auth changes
  const unsubscribe = authStore.subscribe((state) => {
    if (state.user) {
      console.log("User logged in:", state.user.uid);
    } else {
      console.log("User logged out");
    }
  });

  return unsubscribe;
});
```

### Update User Profile

```typescript
import { updateProfile } from "firebase/auth";
import { auth } from "$shared/auth";

async function updateUserProfile(displayName: string, photoURL: string) {
  const user = auth.currentUser;

  if (!user) return;

  try {
    await updateProfile(user, {
      displayName,
      photoURL,
    });

    console.log("Profile updated!");
    // The authStore will automatically update
  } catch (error) {
    console.error("Profile update error:", error);
  }
}
```

## Example: Complete Feature

Here's a complete example showing how to build a user settings page:

```svelte
<!-- src/routes/settings/+page.svelte -->
<script lang="ts">
  import { user, isAuthenticated, authStore } from "$shared/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { updateProfile } from "firebase/auth";
  import { auth } from "$shared/auth";

  // Protect the route
  onMount(() => {
    const unsubscribe = isAuthenticated.subscribe((authenticated) => {
      if (!authenticated) {
        goto("/auth/login");
      }
    });

    return unsubscribe;
  });

  // Form state
  let displayName = $state($user?.displayName || "");
  let saving = $state(false);
  let message = $state<string | null>(null);

  // Update when user changes
  $effect(() => {
    if ($user?.displayName) {
      displayName = $user.displayName;
    }
  });

  async function handleSave() {
    if (!auth.currentUser) return;

    saving = true;
    message = null;

    try {
      await updateProfile(auth.currentUser, { displayName });
      message = "Profile updated successfully!";
    } catch (error) {
      message = "Failed to update profile";
      console.error(error);
    } finally {
      saving = false;
    }
  }

  async function handleSignOut() {
    try {
      await authStore.signOut();
      goto("/");
    } catch (error) {
      console.error("Sign out error:", error);
    }
  }
</script>

<svelte:head>
  <title>Settings - TKA</title>
</svelte:head>

{#if $isAuthenticated}
  <div class="settings-page">
    <h1>Settings</h1>

    <div class="settings-section">
      <h2>Profile</h2>

      <form
        onsubmit={(e) => {
          e.preventDefault();
          handleSave();
        }}
      >
        <div class="form-group">
          <label for="displayName">Display Name</label>
          <input
            id="displayName"
            type="text"
            bind:value={displayName}
            placeholder="Enter your name"
          />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input type="email" value={$user?.email || ""} disabled />
          <small>Email cannot be changed</small>
        </div>

        {#if message}
          <div class="message">{message}</div>
        {/if}

        <button type="submit" disabled={saving}>
          {saving ? "Saving..." : "Save Changes"}
        </button>
      </form>
    </div>

    <div class="settings-section danger-zone">
      <h2>Account</h2>
      <button onclick={handleSignOut} class="btn-danger"> Sign Out </button>
    </div>
  </div>
{/if}

<style>
  .settings-page {
    max-width: 600px;
    margin: 2rem auto;
    padding: 0 1rem;
  }

  .settings-section {
    background: white;
    padding: 2rem;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    font-size: 1rem;
  }

  input:disabled {
    background: #f3f4f6;
    color: #6b7280;
  }

  small {
    color: #6b7280;
    font-size: 0.875rem;
  }

  button {
    padding: 0.75rem 1.5rem;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-danger {
    background: #ef4444;
  }

  .message {
    padding: 1rem;
    margin-bottom: 1rem;
    background: #d1fae5;
    color: #065f46;
    border-radius: 0.5rem;
  }
</style>
```

## Next Steps

Now that authentication is set up:

1. **Add user data to Firestore** - Store user preferences, saved items, etc.
2. **Implement authorization** - Control what users can access
3. **Add email verification** - Ensure users have valid emails
4. **Set up password reset** - For email/password auth (if you add it)
5. **Monitor usage** - Check Firebase Console for authentication analytics

## Need Help?

- Check the [Firebase Documentation](https://firebase.google.com/docs/auth)
- Review [Facebook Login Docs](https://developers.facebook.com/docs/facebook-login)
- Look at the example pages in `src/routes/auth/` and `src/routes/profile/`

Happy coding! 🎉
