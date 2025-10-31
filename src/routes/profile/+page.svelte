<script lang="ts">
  /**
   * User Profile Page
   *
   * Displays user profile information and provides account management options
   */

  import { user, isAuthenticated, isLoading } from "$shared/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  let copying = $state(false);

  onMount(() => {
    const unsubscribe = isAuthenticated.subscribe((authenticated) => {
      if (!authenticated && !$isLoading) {
        goto("/auth/login");
      }
    });

    return unsubscribe;
  });

  async function copyUserId() {
    if (!$user?.uid) return;

    try {
      await navigator.clipboard.writeText($user.uid);
      copying = true;
      setTimeout(() => (copying = false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  }

  const providerName = $derived(() => {
    const providerId = $user?.providerData?.[0]?.providerId;
    if (providerId === "facebook.com") return "Facebook";
    if (providerId === "google.com") return "Google";
    if (providerId === "github.com") return "GitHub";
    if (providerId === "twitter.com") return "Twitter";
    return providerId || "Email";
  });

  const avatarUrl = $derived($user?.photoURL);

  const displayName = $derived($user?.displayName || $user?.email || "User");

  const joinedDate = $derived(() => {
    if (!$user?.metadata?.creationTime) return "Unknown";
    return new Date($user.metadata.creationTime).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  });
</script>

<svelte:head>
  <title>Profile - TKA</title>
</svelte:head>

{#if $isLoading}
  <div class="loading-container">
    <div class="spinner"></div>
    <p>Loading profile...</p>
  </div>
{:else if $user}
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-header">
        {#if avatarUrl}
          <img src={avatarUrl} alt={displayName} class="profile-avatar" />
        {:else}
          <div class="profile-avatar-fallback">
            {displayName.charAt(0).toUpperCase()}
          </div>
        {/if}

        <h1 class="profile-name">{displayName}</h1>
        <p class="profile-email">{$user.email}</p>

        <div class="profile-badge">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          Connected via {providerName()}
        </div>
      </div>

      <div class="profile-details">
        <h2>Account Information</h2>

        <div class="detail-row">
          <span class="detail-label">User ID</span>
          <div class="detail-value">
            <code class="user-id">{$user.uid.slice(0, 20)}...</code>
            <button
              onclick={copyUserId}
              class="copy-button"
              aria-label="Copy user ID"
            >
              {#if copying}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              {:else}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"
                  ></path>
                </svg>
              {/if}
            </button>
          </div>
        </div>

        <div class="detail-row">
          <span class="detail-label">Member since</span>
          <span class="detail-value">{joinedDate()}</span>
        </div>

        <div class="detail-row">
          <span class="detail-label">Last sign in</span>
          <span class="detail-value">
            {$user.metadata?.lastSignInTime
              ? new Date($user.metadata.lastSignInTime).toLocaleString()
              : "Unknown"}
          </span>
        </div>

        <div class="detail-row">
          <span class="detail-label">Email verified</span>
          <span class="detail-value">
            {#if $user.emailVerified}
              <span class="verified">✓ Verified</span>
            {:else}
              <span class="unverified">Not verified</span>
            {/if}
          </span>
        </div>
      </div>

      <div class="profile-actions">
        <a href="/" class="button button-secondary">Back to Home</a>
      </div>
    </div>
  </div>
{/if}

<style>
  .loading-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    color: #6b7280;
  }

  .spinner {
    width: 2rem;
    height: 2rem;
    border: 3px solid #e5e7eb;
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .profile-container {
    min-height: 100vh;
    padding: 2rem 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  .profile-card {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    border-radius: 1rem;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    overflow: hidden;
  }

  .profile-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem 2rem;
    text-align: center;
    color: white;
  }

  .profile-avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 4px solid white;
    object-fit: cover;
    margin-bottom: 1rem;
  }

  .profile-avatar-fallback {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 4px solid white;
    background: rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0 auto 1rem;
  }

  .profile-name {
    font-size: 1.875rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
  }

  .profile-email {
    opacity: 0.9;
    margin: 0 0 1rem 0;
    font-size: 1rem;
  }

  .profile-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.2);
    padding: 0.5rem 1rem;
    border-radius: 2rem;
    font-size: 0.875rem;
    backdrop-filter: blur(10px);
  }

  .profile-details {
    padding: 2rem;
  }

  .profile-details h2 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
    margin: 0 0 1.5rem 0;
  }

  .detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid #e5e7eb;
    gap: 1rem;
  }

  .detail-row:last-child {
    border-bottom: none;
  }

  .detail-label {
    font-weight: 500;
    color: #6b7280;
    font-size: 0.875rem;
  }

  .detail-value {
    color: #1f2937;
    font-size: 0.875rem;
    text-align: right;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .user-id {
    font-family: monospace;
    background: #f3f4f6;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
  }

  .copy-button {
    padding: 0.25rem;
    background: transparent;
    border: none;
    color: #6b7280;
    cursor: pointer;
    border-radius: 0.25rem;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
  }

  .copy-button:hover {
    background: #f3f4f6;
    color: #3b82f6;
  }

  .verified {
    color: #10b981;
    font-weight: 600;
  }

  .unverified {
    color: #f59e0b;
  }

  .profile-actions {
    padding: 1.5rem 2rem;
    background: #f9fafb;
    display: flex;
    gap: 1rem;
  }

  .button {
    flex: 1;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    transition: all 0.2s ease;
    border: none;
    cursor: pointer;
    font-size: 1rem;
  }

  .button-secondary {
    background: white;
    color: #374151;
    border: 1px solid #d1d5db;
  }

  .button-secondary:hover {
    background: #f9fafb;
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .profile-container {
      padding: 1rem 0.5rem;
    }

    .profile-header {
      padding: 2rem 1rem 1.5rem;
    }

    .profile-details {
      padding: 1.5rem;
    }

    .detail-row {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .detail-value {
      text-align: left;
    }
  }

  /* Dark mode */
  @media (prefers-color-scheme: dark) {
    .profile-card {
      background: #1f2937;
    }

    .profile-details h2 {
      color: #f9fafb;
    }

    .detail-label {
      color: #9ca3af;
    }

    .detail-value {
      color: #f9fafb;
    }

    .user-id {
      background: #374151;
    }

    .detail-row {
      border-bottom-color: #374151;
    }

    .profile-actions {
      background: #111827;
    }

    .button-secondary {
      background: #374151;
      color: #f9fafb;
      border-color: #4b5563;
    }

    .button-secondary:hover {
      background: #4b5563;
    }
  }
</style>
