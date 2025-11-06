/**
 * Instagram Graph API Service Implementation
 *
 * Handles Instagram Graph API operations for media upload and carousel publishing.
 * Implements the complete workflow: upload → create container → publish.
 */

import { injectable } from 'inversify';
import type { IInstagramGraphApiService, MediaContainerId, PublishedMedia } from '../contracts';
import type {
  InstagramToken,
  InstagramCarouselPost,
  InstagramPostStatus,
  InstagramMediaItem,
} from '../../domain';
import { validateCarouselPost, INSTAGRAM_MEDIA_CONSTRAINTS } from '../../domain';

/**
 * Instagram Graph API configuration
 */
const GRAPH_API_CONFIG = {
  BASE_URL: 'https://graph.facebook.com/v18.0',
  UPLOAD_TIMEOUT: 120000, // 2 minutes per upload
  POLL_INTERVAL: 2000, // Poll every 2 seconds for container status
  MAX_POLLS: 30, // Max 60 seconds of polling
} as const;

@injectable()
export class InstagramGraphApiService implements IInstagramGraphApiService {
  /**
   * Upload single media item to Instagram
   * Creates a media container (staging) before publishing
   */
  async uploadMediaItem(
    token: InstagramToken,
    mediaItem: InstagramMediaItem
  ): Promise<MediaContainerId> {
    const accountId = token.businessAccountId;
    if (!accountId) {
      throw new Error('No Instagram Business Account ID found');
    }

    try {
      // Upload media to Instagram's servers
      const uploadUrl = await this.uploadToInstagram(mediaItem, token.accessToken);

      // Create media container
      const endpoint = mediaItem.type === 'IMAGE'
        ? 'media'
        : 'media';

      const url = new URL(`${GRAPH_API_CONFIG.BASE_URL}/${accountId}/${endpoint}`);
      url.searchParams.set('access_token', token.accessToken);

      // Different parameters for image vs video
      const formData = new FormData();
      if (mediaItem.type === 'IMAGE') {
        formData.append('image_url', uploadUrl);
        formData.append('is_carousel_item', 'true');
      } else {
        formData.append('video_url', uploadUrl);
        formData.append('is_carousel_item', 'true');
        formData.append('media_type', 'VIDEO');
      }

      const response = await fetch(url.toString(), {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error.message);
      }

      return {
        id: data.id,
        status: 'IN_PROGRESS',
      };
    } catch (error: any) {
      console.error('Failed to upload media item:', error);
      throw new Error(`Media upload failed: ${error.message}`);
    }
  }

  /**
   * Create carousel container with multiple media items
   */
  async createCarouselContainer(
    token: InstagramToken,
    items: MediaContainerId[],
    caption: string
  ): Promise<MediaContainerId> {
    const accountId = token.businessAccountId;
    if (!accountId) {
      throw new Error('No Instagram Business Account ID found');
    }

    try {
      // Wait for all media items to finish processing
      await this.waitForMediaProcessing(items, token);

      // Create carousel container
      const url = new URL(`${GRAPH_API_CONFIG.BASE_URL}/${accountId}/media`);
      url.searchParams.set('access_token', token.accessToken);

      const formData = new FormData();
      formData.append('media_type', 'CAROUSEL');
      formData.append('caption', caption);

      // Add children (uploaded media containers)
      const childrenIds = items.map(item => item.id).join(',');
      formData.append('children', childrenIds);

      const response = await fetch(url.toString(), {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error.message);
      }

      return {
        id: data.id,
        status: 'IN_PROGRESS',
      };
    } catch (error: any) {
      console.error('Failed to create carousel container:', error);
      throw new Error(`Carousel creation failed: ${error.message}`);
    }
  }

  /**
   * Publish carousel post
   */
  async publishCarousel(
    token: InstagramToken,
    containerId: MediaContainerId
  ): Promise<PublishedMedia> {
    const accountId = token.businessAccountId;
    if (!accountId) {
      throw new Error('No Instagram Business Account ID found');
    }

    try {
      // Wait for carousel container to be ready
      await this.waitForContainerReady(containerId, token);

      // Publish the carousel
      const url = new URL(`${GRAPH_API_CONFIG.BASE_URL}/${accountId}/media_publish`);
      url.searchParams.set('access_token', token.accessToken);

      const formData = new FormData();
      formData.append('creation_id', containerId.id);

      const response = await fetch(url.toString(), {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error.message);
      }

      // Get the permalink for the published post
      const permalink = await this.getPostPermalink(data.id, token.accessToken);

      return {
        id: data.id,
        permalink,
      };
    } catch (error: any) {
      console.error('Failed to publish carousel:', error);
      throw new Error(`Publishing failed: ${error.message}`);
    }
  }

  /**
   * Complete carousel post workflow
   * Main method for posting carousels with progress tracking
   */
  async postCarousel(
    token: InstagramToken,
    post: InstagramCarouselPost,
    onProgress?: (status: InstagramPostStatus) => void
  ): Promise<PublishedMedia> {
    // Validate the post
    const validation = validateCarouselPost(post);
    if (!validation.isValid) {
      throw new Error(`Invalid carousel post: ${validation.errors.join(', ')}`);
    }

    try {
      // Step 1: Upload all media items
      onProgress?.({
        status: 'uploading',
        progress: 0,
        message: `Uploading ${post.items.length} media items...`,
      });

      const uploadedItems: MediaContainerId[] = [];
      for (let i = 0; i < post.items.length; i++) {
        const item = post.items[i]!;
        const progress = Math.round((i / post.items.length) * 30); // 0-30%

        onProgress?.({
          status: 'uploading',
          progress,
          message: `Uploading ${item.type.toLowerCase()} ${i + 1}/${post.items.length}...`,
        });

        const containerId = await this.uploadMediaItem(token, item);
        uploadedItems.push(containerId);
      }

      // Step 2: Create carousel container
      onProgress?.({
        status: 'processing',
        progress: 40,
        message: 'Creating carousel...',
      });

      const carouselContainer = await this.createCarouselContainer(
        token,
        uploadedItems,
        post.caption
      );

      // Step 3: Publish carousel
      onProgress?.({
        status: 'publishing',
        progress: 70,
        message: 'Publishing to Instagram...',
      });

      const publishedMedia = await this.publishCarousel(token, carouselContainer);

      // Step 4: Complete
      onProgress?.({
        status: 'completed',
        progress: 100,
        message: 'Successfully posted to Instagram!',
        postId: publishedMedia.id,
        postUrl: publishedMedia.permalink,
      });

      return publishedMedia;
    } catch (error: any) {
      onProgress?.({
        status: 'failed',
        progress: 0,
        message: 'Failed to post to Instagram',
        error: {
          code: error.code || 'UNKNOWN_ERROR',
          message: error.message,
        },
      });

      throw error;
    }
  }

  /**
   * Get media container status
   */
  async getContainerStatus(
    token: InstagramToken,
    containerId: string
  ): Promise<MediaContainerId> {
    try {
      const url = new URL(`${GRAPH_API_CONFIG.BASE_URL}/${containerId}`);
      url.searchParams.set('fields', 'status_code');
      url.searchParams.set('access_token', token.accessToken);

      const response = await fetch(url.toString());
      const data = await response.json();

      if (data.error) {
        throw new Error(data.error.message);
      }

      // Map Instagram status codes to our status enum
      const status = this.mapStatusCode(data.status_code);

      return {
        id: containerId,
        status,
      };
    } catch (error: any) {
      console.error('Failed to get container status:', error);
      return {
        id: containerId,
        status: 'ERROR',
      };
    }
  }

  /**
   * Delete media container
   */
  async deleteContainer(token: InstagramToken, containerId: string): Promise<void> {
    try {
      const url = new URL(`${GRAPH_API_CONFIG.BASE_URL}/${containerId}`);
      url.searchParams.set('access_token', token.accessToken);

      await fetch(url.toString(), {
        method: 'DELETE',
      });
    } catch (error: any) {
      console.error('Failed to delete container:', error);
      // Don't throw - deletion is best-effort cleanup
    }
  }

  /**
   * Get Instagram Business Account ID
   */
  async getBusinessAccountId(token: InstagramToken): Promise<string> {
    if (token.businessAccountId) {
      return token.businessAccountId;
    }

    throw new Error('No Instagram Business Account ID found in token');
  }

  /**
   * Check if account can publish
   */
  async canPublish(token: InstagramToken): Promise<{
    canPublish: boolean;
    reason?: string;
  }> {
    // Check if we have a Business Account ID
    if (!token.businessAccountId) {
      return {
        canPublish: false,
        reason: 'Instagram Business Account required for posting',
      };
    }

    // Check if token is expired
    if (token.expiresAt.getTime() < Date.now()) {
      return {
        canPublish: false,
        reason: 'Access token expired - please reconnect your Instagram account',
      };
    }

    // Check account type
    if (token.accountType === 'PERSONAL') {
      return {
        canPublish: false,
        reason: 'Personal accounts cannot post via API - convert to Business or Creator account',
      };
    }

    return {
      canPublish: true,
    };
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================

  /**
   * Upload media file to Instagram's servers
   * Returns a URL that Instagram can use to download the media
   */
  private async uploadToInstagram(
    mediaItem: InstagramMediaItem,
    accessToken: string
  ): Promise<string> {
    // Upload file to Firebase Storage via our API endpoint
    const formData = new FormData();
    formData.append('file', mediaItem.file);

    const uploadEndpoint = '/api/instagram/upload-media';

    const response = await fetch(uploadEndpoint, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to upload media to storage');
    }

    const data = await response.json();
    return data.url; // Public URL to the uploaded file
  }

  /**
   * Wait for all media items to finish processing
   */
  private async waitForMediaProcessing(
    items: MediaContainerId[],
    token: InstagramToken
  ): Promise<void> {
    const pollPromises = items.map(item => this.waitForContainerReady(item, token));
    await Promise.all(pollPromises);
  }

  /**
   * Wait for a container to be ready (status = FINISHED)
   */
  private async waitForContainerReady(
    container: MediaContainerId,
    token: InstagramToken
  ): Promise<void> {
    let attempts = 0;

    while (attempts < GRAPH_API_CONFIG.MAX_POLLS) {
      const status = await this.getContainerStatus(token, container.id);

      if (status.status === 'FINISHED') {
        return; // Ready!
      }

      if (status.status === 'ERROR') {
        throw new Error(`Media processing failed for container ${container.id}`);
      }

      // Wait before polling again
      await new Promise(resolve => setTimeout(resolve, GRAPH_API_CONFIG.POLL_INTERVAL));
      attempts++;
    }

    throw new Error(`Media processing timed out for container ${container.id}`);
  }

  /**
   * Get permalink for a published post
   */
  private async getPostPermalink(postId: string, accessToken: string): Promise<string> {
    try {
      const url = new URL(`${GRAPH_API_CONFIG.BASE_URL}/${postId}`);
      url.searchParams.set('fields', 'permalink');
      url.searchParams.set('access_token', accessToken);

      const response = await fetch(url.toString());
      const data = await response.json();

      if (data.error) {
        throw new Error(data.error.message);
      }

      return data.permalink || `https://www.instagram.com/p/${postId}/`;
    } catch (error: any) {
      console.error('Failed to get permalink:', error);
      // Fallback to constructing URL
      return `https://www.instagram.com/p/${postId}/`;
    }
  }

  /**
   * Map Instagram API status codes to our status enum
   */
  private mapStatusCode(statusCode: string): MediaContainerId['status'] {
    switch (statusCode) {
      case 'FINISHED':
        return 'FINISHED';
      case 'IN_PROGRESS':
      case 'PUBLISHED':
        return 'IN_PROGRESS';
      case 'ERROR':
      case 'EXPIRED':
        return 'ERROR';
      default:
        return 'IN_PROGRESS';
    }
  }
}
