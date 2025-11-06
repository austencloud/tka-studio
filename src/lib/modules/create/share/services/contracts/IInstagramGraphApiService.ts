/**
 * Instagram Graph API Service Contract
 *
 * Handles Instagram Graph API operations for media upload and publishing.
 */

import type {
  InstagramToken,
  InstagramCarouselPost,
  InstagramPostStatus,
  InstagramMediaItem,
} from '../../domain';

/**
 * Container ID from Instagram API (for staging media before publishing)
 */
export interface MediaContainerId {
  readonly id: string;
  readonly status: 'IN_PROGRESS' | 'FINISHED' | 'ERROR';
}

/**
 * Published media response
 */
export interface PublishedMedia {
  readonly id: string;
  readonly permalink: string;
}

export interface IInstagramGraphApiService {
  /**
   * Upload single media item to Instagram
   * Creates a media container (staging area) before publishing
   * @param token - Instagram auth token
   * @param mediaItem - Media file to upload
   * @returns Container ID for the uploaded media
   */
  uploadMediaItem(
    token: InstagramToken,
    mediaItem: InstagramMediaItem
  ): Promise<MediaContainerId>;

  /**
   * Create carousel container with multiple media items
   * @param token - Instagram auth token
   * @param items - Array of uploaded media container IDs
   * @param caption - Post caption
   * @returns Carousel container ID
   */
  createCarouselContainer(
    token: InstagramToken,
    items: MediaContainerId[],
    caption: string
  ): Promise<MediaContainerId>;

  /**
   * Publish carousel post
   * @param token - Instagram auth token
   * @param containerId - Carousel container ID
   * @returns Published media info
   */
  publishCarousel(
    token: InstagramToken,
    containerId: MediaContainerId
  ): Promise<PublishedMedia>;

  /**
   * Complete carousel post workflow (upload, create container, publish)
   * This is the main method for posting carousels
   * @param token - Instagram auth token
   * @param post - Carousel post data
   * @param onProgress - Progress callback
   * @returns Published media info
   */
  postCarousel(
    token: InstagramToken,
    post: InstagramCarouselPost,
    onProgress?: (status: InstagramPostStatus) => void
  ): Promise<PublishedMedia>;

  /**
   * Get media container status
   * Used to check if media upload/processing is complete
   * @param token - Instagram auth token
   * @param containerId - Container ID to check
   */
  getContainerStatus(
    token: InstagramToken,
    containerId: string
  ): Promise<MediaContainerId>;

  /**
   * Delete media container (if not published)
   * @param token - Instagram auth token
   * @param containerId - Container ID to delete
   */
  deleteContainer(
    token: InstagramToken,
    containerId: string
  ): Promise<void>;

  /**
   * Get Instagram Business Account ID from token
   * Required for posting - converts Personal account to Business account if needed
   * @param token - Instagram auth token
   */
  getBusinessAccountId(token: InstagramToken): Promise<string>;

  /**
   * Check if account can publish content
   * Validates account type and permissions
   * @param token - Instagram auth token
   */
  canPublish(token: InstagramToken): Promise<{
    canPublish: boolean;
    reason?: string;
  }>;
}
