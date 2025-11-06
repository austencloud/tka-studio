<!--
  Instagram OAuth Callback Page

  Handles the OAuth redirect from Facebook/Instagram after user authorizes the app.
  Exchanges the authorization code for an access token and saves it to Firestore.
-->
<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { resolve, TYPES } from '$shared';
  import type { IInstagramAuthService } from '$create/share/services/contracts';
  import { authStore } from '$shared/auth';

  let status = $state<'processing' | 'success' | 'error'>('processing');
  let message = $state('Processing Instagram authorization...');
  let errorDetails = $state<string | null>(null);

  onMount(async () => {
    try {
      // Get the authorization code and state from URL params
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const state = urlParams.get('state');
      const error = urlParams.get('error');
      const errorDescription = urlParams.get('error_description');

      // Check for errors from Instagram/Facebook
      if (error) {
        throw new Error(errorDescription || error);
      }

      // Validate we have the required parameters
      if (!code || !state) {
        throw new Error('Missing authorization code or state parameter');
      }

      // Check if user is authenticated
      if (!authStore.user) {
        throw new Error('You must be logged in to connect Instagram');
      }

      // Get Instagram Auth Service
      const instagramAuthService = resolve<IInstagramAuthService>(
        TYPES.IInstagramAuthService
      );

      message = 'Exchanging authorization code for access token...';

      // Handle the OAuth callback
      const token = await instagramAuthService.handleOAuthCallback(code, state);

      message = 'Saving Instagram connection...';

      // Save the token to Firestore (this is done in handleOAuthCallback via saveToken)
      // The service handles this internally

      // Success!
      status = 'success';
      message = `Successfully connected Instagram account @${token.username}!`;

      // Redirect to profile settings after 2 seconds
      setTimeout(() => {
        goto('/profile?tab=connected-accounts');
      }, 2000);
    } catch (error: any) {
      console.error('Instagram OAuth callback error:', error);
      status = 'error';
      message = 'Failed to connect Instagram account';
      errorDetails = error.message || 'An unknown error occurred';
    }
  });
</script>

<div class="callback-container">
  <div class="callback-card">
    {#if status === 'processing'}
      <!-- Processing -->
      <div class="status-icon processing">
        <i class="fa-brands fa-instagram fa-spin"></i>
      </div>
      <h1>Connecting Instagram</h1>
      <p class="message">{message}</p>
      <div class="loader"></div>
    {:else if status === 'success'}
      <!-- Success -->
      <div class="status-icon success">
        <i class="fas fa-check-circle"></i>
      </div>
      <h1>Connection Successful!</h1>
      <p class="message">{message}</p>
      <p class="redirect-message">Redirecting to your profile...</p>
    {:else}
      <!-- Error -->
      <div class="status-icon error">
        <i class="fas fa-exclamation-circle"></i>
      </div>
      <h1>Connection Failed</h1>
      <p class="message">{message}</p>
      {#if errorDetails}
        <div class="error-details">
          <p class="error-label">Error Details:</p>
          <p class="error-text">{errorDetails}</p>
        </div>
      {/if}
      <div class="actions">
        <button class="btn-primary" onclick={() => goto('/profile?tab=connected-accounts')}>
          <i class="fas fa-arrow-left"></i>
          Back to Profile
        </button>
        <button class="btn-secondary" onclick={() => window.location.reload()}>
          <i class="fas fa-redo"></i>
          Try Again
        </button>
      </div>
    {/if}
  </div>
</div>

<style>
  .callback-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(20, 20, 30, 0.98) 0%, rgba(30, 30, 45, 0.98) 100%);
  }

  .callback-card {
    max-width: 500px;
    width: 100%;
    padding: 3rem 2rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 24px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  }

  .status-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
  }

  .status-icon.processing {
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .status-icon.success {
    color: #10b981;
  }

  .status-icon.error {
    color: #ef4444;
  }

  h1 {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 1rem 0;
  }

  .message {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin: 0 0 1.5rem 0;
  }

  .redirect-message {
    font-size: 0.9rem;
    color: var(--text-tertiary);
    font-style: italic;
    margin: 0;
  }

  .loader {
    width: 48px;
    height: 48px;
    margin: 2rem auto 0;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-top: 4px solid rgba(59, 130, 246, 0.8);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .error-details {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 12px;
    padding: 1rem;
    margin: 1.5rem 0;
    text-align: left;
  }

  .error-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #ef4444;
    margin: 0 0 0.5rem 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .error-text {
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin: 0;
    font-family: monospace;
  }

  .actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 2rem;
  }

  .btn-primary,
  .btn-secondary {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-primary {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
  }

  .btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }

  .btn-secondary {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-primary);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
  }

  /* Mobile responsive */
  @media (max-width: 640px) {
    .callback-container {
      padding: 1rem;
    }

    .callback-card {
      padding: 2rem 1.5rem;
    }

    h1 {
      font-size: 1.5rem;
    }

    .message {
      font-size: 1rem;
    }

    .actions {
      flex-direction: column;
    }

    .btn-primary,
    .btn-secondary {
      width: 100%;
      justify-content: center;
    }
  }
</style>
