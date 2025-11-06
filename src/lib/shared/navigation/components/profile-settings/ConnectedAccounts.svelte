<!--
  ConnectedAccounts Component

  Displays the list of OAuth providers connected to the user's account.
  Shows provider icons, names, and associated emails.
  Also manages Instagram Business account connection.
-->
<script lang="ts">
  import { onMount } from "svelte";
  import { authStore } from "$shared/auth";
  import { resolve, TYPES } from "$shared";
  import type { IInstagramAuthService } from "$create/share/services/contracts";
  import type { InstagramToken } from "$create/share/domain";
  import { INSTAGRAM_PERMISSIONS } from "$create/share/domain";

  // Instagram connection state
  let instagramService: IInstagramAuthService;
  let instagramToken = $state<InstagramToken | null>(null);
  let isLoadingInstagram = $state(true);
  let isConnecting = $state(false);
  let isDisconnecting = $state(false);

  onMount(async () => {
    try {
      instagramService = resolve<IInstagramAuthService>(
        TYPES.IInstagramAuthService
      );

      // Load Instagram connection status
      if (authStore.user) {
        await loadInstagramConnection();
      }
    } catch (error) {
      console.error("Failed to load Instagram service:", error);
    } finally {
      isLoadingInstagram = false;
    }
  });

  async function loadInstagramConnection() {
    if (!authStore.user) return;

    try {
      instagramToken = await instagramService.getToken(authStore.user.uid);
    } catch (error) {
      console.error("Failed to load Instagram connection:", error);
      instagramToken = null;
    }
  }

  async function handleConnectInstagram() {
    if (isConnecting || !instagramService) return;

    isConnecting = true;

    try {
      // Initiate OAuth flow - this will redirect user to Facebook
      await instagramService.initiateOAuthFlow([
        INSTAGRAM_PERMISSIONS.CONTENT_PUBLISH,
      ]);
    } catch (error: any) {
      console.error("Failed to initiate Instagram OAuth:", error);
      alert(`Failed to connect Instagram: ${error.message}`);
      isConnecting = false;
    }
  }

  async function handleDisconnectInstagram() {
    if (
      isDisconnecting ||
      !instagramService ||
      !authStore.user ||
      !instagramToken
    )
      return;

    // Confirm before disconnecting
    const confirmed = confirm(
      `Disconnect @${instagramToken.username}? You'll need to reconnect to post to Instagram.`
    );

    if (!confirmed) return;

    isDisconnecting = true;

    try {
      await instagramService.disconnectAccount(authStore.user.uid);
      instagramToken = null;
    } catch (error: any) {
      console.error("Failed to disconnect Instagram:", error);
      alert(`Failed to disconnect Instagram: ${error.message}`);
    } finally {
      isDisconnecting = false;
    }
  }

  // Derived state
  let isInstagramConnected = $derived(instagramToken !== null);
  let isTokenExpired = $derived(() => {
    if (!instagramToken) return false;
    return instagramToken.expiresAt.getTime() < Date.now();
  });
</script>

<div class="connected-accounts">
  <!-- Firebase Auth Providers (Google, Facebook) -->
  {#if authStore.user?.providerData && authStore.user.providerData.length > 0}
    <div class="section">
      <h4 class="section-title">Authentication Providers</h4>
      <div class="providers">
        {#each authStore.user.providerData as provider}
          <div class="provider">
            <i
              class="fab fa-{provider.providerId === 'google.com'
                ? 'google'
                : 'facebook'}"
            ></i>
            <span class="provider-name"
              >{provider.providerId === "google.com"
                ? "Google"
                : "Facebook"}</span
            >
            <span class="provider-email">{provider.email}</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Instagram Business Account -->
  <div class="section">
    <h4 class="section-title">Instagram Business Account</h4>

    {#if isLoadingInstagram}
      <div class="loading">
        <i class="fas fa-spinner fa-spin"></i>
        <span>Loading Instagram connection...</span>
      </div>
    {:else if isInstagramConnected && instagramToken}
      <!-- Connected Instagram Account -->
      <div class="provider instagram-account">
        <div class="instagram-icon">
          <i class="fab fa-instagram"></i>
        </div>
        <div class="account-info">
          <span class="provider-name">@{instagramToken.username}</span>
          <div class="account-meta">
            <span class="account-type">{instagramToken.accountType}</span>
            {#if isTokenExpired()}
              <span class="token-status expired">
                <i class="fas fa-exclamation-triangle"></i>
                Token expired
              </span>
            {:else}
              <span class="token-status valid">
                <i class="fas fa-check-circle"></i>
                Connected
              </span>
            {/if}
          </div>
        </div>
        <button
          class="disconnect-button"
          onclick={handleDisconnectInstagram}
          disabled={isDisconnecting}
        >
          {#if isDisconnecting}
            <i class="fas fa-spinner fa-spin"></i>
            Disconnecting...
          {:else}
            <i class="fas fa-unlink"></i>
            Disconnect
          {/if}
        </button>
      </div>

      {#if isTokenExpired()}
        <div class="warning-banner">
          <i class="fas fa-exclamation-triangle"></i>
          <div class="warning-content">
            <p class="warning-title">Token Expired</p>
            <p class="warning-message">
              Your Instagram connection has expired. Please disconnect and
              reconnect to continue posting.
            </p>
          </div>
        </div>
      {/if}
    {:else}
      <!-- Not Connected -->
      <div class="not-connected">
        <div class="instagram-placeholder">
          <i class="fab fa-instagram"></i>
        </div>
        <div class="connect-info">
          <p class="connect-title">Connect your Instagram Business Account</p>
          <p class="connect-description">
            Post carousels with your sequences directly to Instagram. Requires
            an Instagram Business or Creator account connected to a Facebook
            Page.
          </p>
          <button
            class="connect-button"
            onclick={handleConnectInstagram}
            disabled={isConnecting}
          >
            {#if isConnecting}
              <i class="fas fa-spinner fa-spin"></i>
              Connecting...
            {:else}
              <i class="fab fa-instagram"></i>
              Connect Instagram
            {/if}
          </button>
          <p class="connect-hint">
            <i class="fas fa-info-circle"></i>
            Personal accounts cannot post via API - you'll need a Business or
            Creator account
          </p>
        </div>
      </div>
    {/if}
  </div>

  {#if !authStore.user?.providerData?.length && !isInstagramConnected}
    <p class="hint">No connected accounts</p>
  {/if}
</div>

<style>
  .connected-accounts {
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .section-title {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .providers {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .provider {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    transition: all 0.2s ease;
    min-width: 0;
  }

  .provider:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.12);
  }

  .provider i {
    font-size: 20px;
    color: rgba(99, 102, 241, 0.8);
    flex-shrink: 0;
  }

  .provider-name {
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
    flex-shrink: 0;
  }

  .provider-email {
    margin-left: auto;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    min-width: 0;
    flex-shrink: 1;
  }

  /* Instagram Account Styles */
  .instagram-account {
    position: relative;
  }

  .instagram-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: linear-gradient(
      45deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
  }

  .instagram-icon i {
    font-size: 24px;
    color: white;
  }

  .account-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
    min-width: 0;
  }

  .account-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }

  .account-type {
    font-size: 0.75rem;
    padding: 2px 8px;
    background: rgba(99, 102, 241, 0.2);
    color: rgba(99, 102, 241, 1);
    border-radius: 4px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .token-status {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 0.8rem;
    font-weight: 500;
  }

  .token-status.valid {
    color: #10b981;
  }

  .token-status.expired {
    color: #ef4444;
  }

  .disconnect-button {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
  }

  .disconnect-button:hover:not(:disabled) {
    background: rgba(239, 68, 68, 0.2);
    border-color: rgba(239, 68, 68, 0.5);
  }

  .disconnect-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Not Connected Styles */
  .not-connected {
    display: flex;
    gap: 1.5rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
  }

  .instagram-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 16px;
    background: linear-gradient(
      45deg,
      rgba(240, 148, 51, 0.1) 0%,
      rgba(230, 104, 60, 0.1) 25%,
      rgba(220, 39, 67, 0.1) 50%,
      rgba(204, 35, 102, 0.1) 75%,
      rgba(188, 24, 136, 0.1) 100%
    );
    border: 2px solid rgba(240, 148, 51, 0.3);
    flex-shrink: 0;
  }

  .instagram-placeholder i {
    font-size: 32px;
    background: linear-gradient(
      45deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .connect-info {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    flex: 1;
  }

  .connect-title {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
  }

  .connect-description {
    margin: 0;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.5;
  }

  .connect-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 24px;
    background: linear-gradient(
      45deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    align-self: flex-start;
  }

  .connect-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(240, 148, 51, 0.4);
  }

  .connect-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .connect-hint {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.5);
    font-style: italic;
  }

  .connect-hint i {
    font-size: 0.9rem;
    color: rgba(99, 102, 241, 0.6);
  }

  /* Warning Banner */
  .warning-banner {
    display: flex;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    margin-top: 12px;
  }

  .warning-banner > i {
    font-size: 20px;
    color: #ef4444;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .warning-content {
    flex: 1;
  }

  .warning-title {
    margin: 0 0 4px 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: #ef4444;
  }

  .warning-message {
    margin: 0;
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.4;
  }

  /* Loading State */
  .loading {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    color: rgba(255, 255, 255, 0.6);
  }

  .loading i {
    font-size: 20px;
  }

  .hint {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.5);
    text-align: center;
    margin: 0;
    padding: 16px;
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .not-connected {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .instagram-placeholder {
      width: 56px;
      height: 56px;
    }

    .instagram-placeholder i {
      font-size: 28px;
    }

    .connect-button {
      align-self: stretch;
    }

    .instagram-account {
      flex-wrap: wrap;
    }

    .disconnect-button {
      width: 100%;
      justify-content: center;
      margin-top: 8px;
    }
  }

  /* Accessibility - Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .provider,
    .connect-button,
    .disconnect-button {
      transition: none;
    }
  }
</style>
