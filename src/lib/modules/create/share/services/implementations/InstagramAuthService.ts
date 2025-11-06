/**
 * Instagram Authentication Service Implementation
 *
 * Manages Instagram OAuth flow using Facebook Login for Instagram Business accounts.
 * Uses Firestore to store and manage Instagram tokens.
 */

import { injectable } from 'inversify';
import { doc, getDoc, setDoc, deleteDoc } from 'firebase/firestore';
import { firestore } from '$shared/auth/firebase';
import type { IInstagramAuthService } from '../contracts';
import type { InstagramToken, InstagramScope } from '../../domain';
import {
  createInstagramToken,
  isTokenExpired,
  needsRefresh,
  INSTAGRAM_PERMISSIONS,
} from '../../domain';

/**
 * Instagram OAuth configuration
 * Uses Facebook OAuth as Instagram Graph API requires it
 */
const INSTAGRAM_OAUTH_CONFIG = {
  // You'll need to create a Facebook App and get these credentials
  CLIENT_ID: import.meta.env.VITE_FACEBOOK_APP_ID || '',
  CLIENT_SECRET: import.meta.env.VITE_FACEBOOK_APP_SECRET || '',

  // Facebook OAuth URLs
  AUTHORIZE_URL: 'https://www.facebook.com/v18.0/dialog/oauth',
  TOKEN_URL: 'https://graph.facebook.com/v18.0/oauth/access_token',

  // Instagram Graph API base URL
  GRAPH_API_URL: 'https://graph.facebook.com/v18.0',

  // OAuth redirect URI (must match Facebook App settings)
  REDIRECT_URI: typeof window !== 'undefined'
    ? `${window.location.origin}/auth/instagram/callback`
    : '',
} as const;

@injectable()
export class InstagramAuthService implements IInstagramAuthService {
  /**
   * Initialize Instagram OAuth flow
   * Opens Facebook OAuth dialog for Instagram permissions
   */
  async initiateOAuthFlow(scopes: InstagramScope[], redirectUri?: string): Promise<void> {
    // Generate CSRF token for state parameter
    const state = this.generateState();
    this.saveState(state);

    // Build scope string (Facebook permissions)
    const scopeString = this.buildScopeString(scopes);

    // Build OAuth URL
    const authUrl = new URL(INSTAGRAM_OAUTH_CONFIG.AUTHORIZE_URL);
    authUrl.searchParams.set('client_id', INSTAGRAM_OAUTH_CONFIG.CLIENT_ID);
    authUrl.searchParams.set('redirect_uri', redirectUri || INSTAGRAM_OAUTH_CONFIG.REDIRECT_URI);
    authUrl.searchParams.set('scope', scopeString);
    authUrl.searchParams.set('response_type', 'code');
    authUrl.searchParams.set('state', state);

    // Redirect to Facebook OAuth
    window.location.href = authUrl.toString();
  }

  /**
   * Handle OAuth callback
   * Exchanges authorization code for access token
   */
  async handleOAuthCallback(code: string, state: string): Promise<InstagramToken> {
    // Verify state parameter (CSRF protection)
    const savedState = this.getState();
    if (state !== savedState) {
      throw new Error('Invalid state parameter - possible CSRF attack');
    }
    this.clearState();

    try {
      // Step 1: Exchange code for short-lived Facebook token
      const shortLivedToken = await this.exchangeCodeForToken(code);

      // Step 2: Exchange short-lived token for long-lived token (60 days)
      const longLivedToken = await this.exchangeForLongLivedToken(shortLivedToken);

      // Step 3: Get Instagram Business Account ID
      const { instagramAccountId, facebookPageId } = await this.getInstagramAccountId(longLivedToken);

      // Step 4: Get Instagram account info
      const accountInfo = await this.fetchInstagramAccountInfo(instagramAccountId, longLivedToken);

      // Step 5: Create Instagram token object
      const token = createInstagramToken(
        accountInfo.id,
        accountInfo.username,
        longLivedToken,
        60 * 24 * 60 * 60, // 60 days in seconds
        accountInfo.accountType,
        {
          businessAccountId: instagramAccountId,
          facebookPageId,
        }
      );

      return token;
    } catch (error: any) {
      console.error('Instagram OAuth callback error:', error);
      throw new Error(`Failed to complete Instagram authentication: ${error.message}`);
    }
  }

  /**
   * Get current Instagram token from Firestore
   */
  async getToken(userId: string): Promise<InstagramToken | null> {
    try {
      const tokenRef = doc(firestore, `users/${userId}/instagram_tokens/current`);
      const tokenDoc = await getDoc(tokenRef);

      if (!tokenDoc.exists()) {
        return null;
      }

      const data = tokenDoc.data();
      return {
        userId: data.userId,
        username: data.username,
        accessToken: data.accessToken,
        expiresAt: data.expiresAt.toDate(),
        isLongLived: data.isLongLived,
        accountType: data.accountType,
        lastRefreshed: data.lastRefreshed.toDate(),
        businessAccountId: data.businessAccountId,
        facebookPageId: data.facebookPageId,
      };
    } catch (error: any) {
      console.error('Failed to get Instagram token:', error);
      return null;
    }
  }

  /**
   * Save Instagram token to Firestore
   */
  private async saveToken(userId: string, token: InstagramToken): Promise<void> {
    const tokenRef = doc(firestore, `users/${userId}/instagram_tokens/current`);
    await setDoc(tokenRef, {
      userId: token.userId,
      username: token.username,
      accessToken: token.accessToken,
      expiresAt: token.expiresAt,
      isLongLived: token.isLongLived,
      accountType: token.accountType,
      lastRefreshed: token.lastRefreshed,
      businessAccountId: token.businessAccountId,
      facebookPageId: token.facebookPageId,
    });
  }

  /**
   * Refresh Instagram token
   */
  async refreshToken(userId: string): Promise<InstagramToken> {
    const currentToken = await this.getToken(userId);

    if (!currentToken) {
      throw new Error('No Instagram token found for user');
    }

    // If token doesn't need refresh, return current
    if (!needsRefresh(currentToken)) {
      return currentToken;
    }

    try {
      // Refresh long-lived token
      const newAccessToken = await this.refreshLongLivedToken(currentToken.accessToken);

      // Create updated token
      const refreshedToken = createInstagramToken(
        currentToken.userId,
        currentToken.username,
        newAccessToken,
        60 * 24 * 60 * 60, // 60 days
        currentToken.accountType,
        {
          businessAccountId: currentToken.businessAccountId,
          facebookPageId: currentToken.facebookPageId,
        }
      );

      // Save to Firestore
      await this.saveToken(userId, refreshedToken);

      return refreshedToken;
    } catch (error: any) {
      console.error('Failed to refresh Instagram token:', error);
      throw new Error(`Token refresh failed: ${error.message}`);
    }
  }

  /**
   * Disconnect Instagram account
   */
  async disconnectAccount(userId: string): Promise<void> {
    try {
      const tokenRef = doc(firestore, `users/${userId}/instagram_tokens/current`);
      await deleteDoc(tokenRef);
    } catch (error: any) {
      console.error('Failed to disconnect Instagram account:', error);
      throw new Error(`Failed to disconnect: ${error.message}`);
    }
  }

  /**
   * Check if user has connected account
   */
  async hasConnectedAccount(userId: string): Promise<boolean> {
    const token = await this.getToken(userId);
    return token !== null && !isTokenExpired(token);
  }

  /**
   * Validate permissions
   */
  async validatePermissions(token: InstagramToken, requiredScopes: InstagramScope[]): Promise<boolean> {
    // In a real implementation, you'd call Facebook Graph API to check granted permissions
    // For now, we'll assume all permissions are granted if token exists
    return true;
  }

  /**
   * Get Instagram account info
   */
  async getAccountInfo(token: InstagramToken): Promise<{
    id: string;
    username: string;
    accountType: 'PERSONAL' | 'BUSINESS' | 'CREATOR';
    profilePictureUrl?: string;
    followersCount?: number;
  }> {
    if (!token.businessAccountId) {
      throw new Error('No Instagram Business Account ID found');
    }

    return await this.fetchInstagramAccountInfo(token.businessAccountId, token.accessToken);
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================

  /**
   * Exchange authorization code for short-lived token
   */
  private async exchangeCodeForToken(code: string): Promise<string> {
    const url = new URL(INSTAGRAM_OAUTH_CONFIG.TOKEN_URL);
    url.searchParams.set('client_id', INSTAGRAM_OAUTH_CONFIG.CLIENT_ID);
    url.searchParams.set('client_secret', INSTAGRAM_OAUTH_CONFIG.CLIENT_SECRET);
    url.searchParams.set('redirect_uri', INSTAGRAM_OAUTH_CONFIG.REDIRECT_URI);
    url.searchParams.set('code', code);

    const response = await fetch(url.toString());
    const data = await response.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    return data.access_token;
  }

  /**
   * Exchange short-lived token for long-lived token (60 days)
   */
  private async exchangeForLongLivedToken(shortLivedToken: string): Promise<string> {
    const url = new URL(`${INSTAGRAM_OAUTH_CONFIG.GRAPH_API_URL}/oauth/access_token`);
    url.searchParams.set('grant_type', 'fb_exchange_token');
    url.searchParams.set('client_id', INSTAGRAM_OAUTH_CONFIG.CLIENT_ID);
    url.searchParams.set('client_secret', INSTAGRAM_OAUTH_CONFIG.CLIENT_SECRET);
    url.searchParams.set('fb_exchange_token', shortLivedToken);

    const response = await fetch(url.toString());
    const data = await response.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    return data.access_token;
  }

  /**
   * Refresh long-lived token
   */
  private async refreshLongLivedToken(currentToken: string): Promise<string> {
    const url = new URL(`${INSTAGRAM_OAUTH_CONFIG.GRAPH_API_URL}/oauth/access_token`);
    url.searchParams.set('grant_type', 'ig_refresh_token');
    url.searchParams.set('access_token', currentToken);

    const response = await fetch(url.toString());
    const data = await response.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    return data.access_token;
  }

  /**
   * Get Instagram Business Account ID from Facebook Page
   */
  private async getInstagramAccountId(accessToken: string): Promise<{
    instagramAccountId: string;
    facebookPageId: string;
  }> {
    // Get Facebook Pages managed by the user
    const url = new URL(`${INSTAGRAM_OAUTH_CONFIG.GRAPH_API_URL}/me/accounts`);
    url.searchParams.set('access_token', accessToken);

    const response = await fetch(url.toString());
    const data = await response.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    // Get the first page (or let user choose in future)
    const page = data.data[0];
    if (!page) {
      throw new Error('No Facebook Pages found. You need a Facebook Page connected to an Instagram Business account.');
    }

    // Get Instagram Business Account from the page
    const igUrl = new URL(`${INSTAGRAM_OAUTH_CONFIG.GRAPH_API_URL}/${page.id}`);
    igUrl.searchParams.set('fields', 'instagram_business_account');
    igUrl.searchParams.set('access_token', accessToken);

    const igResponse = await fetch(igUrl.toString());
    const igData = await igResponse.json();

    if (igData.error) {
      throw new Error(igData.error.message);
    }

    if (!igData.instagram_business_account) {
      throw new Error('No Instagram Business account connected to this Facebook Page.');
    }

    return {
      instagramAccountId: igData.instagram_business_account.id,
      facebookPageId: page.id,
    };
  }

  /**
   * Fetch Instagram account info from Graph API
   */
  private async fetchInstagramAccountInfo(
    accountId: string,
    accessToken: string
  ): Promise<{
    id: string;
    username: string;
    accountType: 'PERSONAL' | 'BUSINESS' | 'CREATOR';
    profilePictureUrl?: string;
    followersCount?: number;
  }> {
    const url = new URL(`${INSTAGRAM_OAUTH_CONFIG.GRAPH_API_URL}/${accountId}`);
    url.searchParams.set('fields', 'id,username,profile_picture_url,followers_count');
    url.searchParams.set('access_token', accessToken);

    const response = await fetch(url.toString());
    const data = await response.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    return {
      id: data.id,
      username: data.username,
      accountType: 'BUSINESS', // Instagram Graph API only works with Business/Creator accounts
      profilePictureUrl: data.profile_picture_url,
      followersCount: data.followers_count,
    };
  }

  /**
   * Build Facebook scope string from Instagram permissions
   */
  private buildScopeString(scopes: InstagramScope[]): string {
    const facebookScopes = new Set<string>([
      'pages_show_list',  // Required to list Facebook Pages
      'pages_read_engagement', // Required to read page info
    ]);

    // Map Instagram scopes to Facebook scopes
    scopes.forEach((scope) => {
      if (scope === INSTAGRAM_PERMISSIONS.CONTENT_PUBLISH) {
        facebookScopes.add('instagram_basic');
        facebookScopes.add('instagram_content_publish');
      } else if (scope === INSTAGRAM_PERMISSIONS.INSIGHTS) {
        facebookScopes.add('instagram_manage_insights');
      } else if (scope === INSTAGRAM_PERMISSIONS.MESSAGES) {
        facebookScopes.add('instagram_manage_messages');
      }
    });

    return Array.from(facebookScopes).join(',');
  }

  /**
   * Generate random state for CSRF protection
   */
  private generateState(): string {
    return Math.random().toString(36).substring(2, 15) +
           Math.random().toString(36).substring(2, 15);
  }

  /**
   * Save state to sessionStorage
   */
  private saveState(state: string): void {
    if (typeof window !== 'undefined') {
      sessionStorage.setItem('instagram_oauth_state', state);
    }
  }

  /**
   * Get state from sessionStorage
   */
  private getState(): string | null {
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem('instagram_oauth_state');
    }
    return null;
  }

  /**
   * Clear state from sessionStorage
   */
  private clearState(): void {
    if (typeof window !== 'undefined') {
      sessionStorage.removeItem('instagram_oauth_state');
    }
  }
}
