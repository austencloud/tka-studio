/**
 * Instagram Authentication Service Contract
 *
 * Manages Instagram OAuth flow, token management, and account connection.
 */

import type { InstagramToken, InstagramScope } from '../../domain';

export interface IInstagramAuthService {
  /**
   * Initialize Instagram OAuth flow
   * Redirects user to Instagram/Facebook OAuth consent screen
   * @param scopes - Required permissions
   * @param redirectUri - Where to redirect after OAuth
   */
  initiateOAuthFlow(scopes: InstagramScope[], redirectUri?: string): Promise<void>;

  /**
   * Handle OAuth callback and exchange code for token
   * Call this after user returns from Instagram OAuth
   * @param code - Authorization code from OAuth callback
   * @param state - State parameter for CSRF protection
   */
  handleOAuthCallback(code: string, state: string): Promise<InstagramToken>;

  /**
   * Get current Instagram token for authenticated user
   * @param userId - Firebase user ID
   */
  getToken(userId: string): Promise<InstagramToken | null>;

  /**
   * Refresh Instagram access token
   * Exchanges short-lived token for long-lived token or refreshes existing
   * @param userId - Firebase user ID
   */
  refreshToken(userId: string): Promise<InstagramToken>;

  /**
   * Disconnect Instagram account
   * Revokes token and removes from Firestore
   * @param userId - Firebase user ID
   */
  disconnectAccount(userId: string): Promise<void>;

  /**
   * Check if user has connected Instagram account
   * @param userId - Firebase user ID
   */
  hasConnectedAccount(userId: string): Promise<boolean>;

  /**
   * Validate that token has required permissions
   * @param token - Instagram token
   * @param requiredScopes - Required permissions
   */
  validatePermissions(token: InstagramToken, requiredScopes: InstagramScope[]): Promise<boolean>;

  /**
   * Get Instagram account info
   * @param token - Instagram token
   */
  getAccountInfo(token: InstagramToken): Promise<{
    id: string;
    username: string;
    accountType: 'PERSONAL' | 'BUSINESS' | 'CREATOR';
    profilePictureUrl?: string;
    followersCount?: number;
  }>;
}
