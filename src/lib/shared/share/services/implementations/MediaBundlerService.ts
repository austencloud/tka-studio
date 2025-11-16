/**
 * Media Bundler Service Implementation
 *
 * Bundles sequence media (static image + animated GIF + user video) into Instagram carousel items.
 * Leverages the existing ShareService to generate sequence images and GIFs.
 */

import { injectable, inject } from "inversify";
import type { IShareService } from "../contracts";
import type { IMediaBundlerService } from "../contracts";
import type { SequenceData } from "$shared";
import type { InstagramMediaItem, ShareOptions } from "../../domain";
import { INSTAGRAM_MEDIA_CONSTRAINTS, validateMediaItem } from "../../domain";
import { TYPES } from "$shared/inversify";

@injectable()
export class MediaBundlerService implements IMediaBundlerService {
  constructor(
    @inject(TYPES.IShareService) private shareService: IShareService
  ) {}

  /**
   * Bundle sequence into Instagram media items
   * Creates both static image and animated GIF
   */
  async bundleSequenceMedia(
    sequence: SequenceData,
    options: ShareOptions
  ): Promise<InstagramMediaItem[]> {
    const items: InstagramMediaItem[] = [];

    try {
      // Generate static sequence image
      const imageBlob = await this.generateSequenceImage(sequence, options);
      const imageItem = await this.createMediaItemFromBlob(
        imageBlob,
        "IMAGE",
        items.length,
        `${sequence.word}_sequence.png`
      );
      items.push(imageItem);

      // Generate animated GIF
      const gifBlob = await this.generateSequenceGif(sequence, options);
      const gifItem = await this.createMediaItemFromBlob(
        gifBlob,
        "IMAGE", // GIFs are treated as images by Instagram
        items.length,
        `${sequence.word}_animated.gif`
      );
      items.push(gifItem);

      return items;
    } catch (error: any) {
      console.error("Failed to bundle sequence media:", error);
      throw new Error(`Media bundling failed: ${error.message}`);
    }
  }

  /**
   * Create media item from user-selected video
   */
  async createVideoMediaItem(
    videoFile: File,
    order: number
  ): Promise<InstagramMediaItem> {
    // Validate video file
    if (!videoFile.type.startsWith("video/")) {
      throw new Error("File must be a video");
    }

    // Create preview URL
    const url = URL.createObjectURL(videoFile);

    const mediaItem: InstagramMediaItem = {
      type: "VIDEO",
      blob: videoFile,
      url,
      filename: videoFile.name,
      order,
    };

    // Validate against Instagram constraints
    const validation = validateMediaItem(mediaItem);
    if (!validation.isValid) {
      // Revoke the URL since we're throwing an error
      URL.revokeObjectURL(url);
      throw new Error(validation.error);
    }

    return mediaItem;
  }

  /**
   * Create complete carousel bundle
   * video + sequence image + animated GIF
   */
  async createCarouselBundle(
    sequence: SequenceData,
    videoFile: File,
    options: ShareOptions,
    layout: "video-first" | "sequence-first" = "video-first"
  ): Promise<InstagramMediaItem[]> {
    try {
      // Generate sequence media (image + GIF)
      const sequenceMedia = await this.bundleSequenceMedia(sequence, options);

      // Create video media item
      const videoMedia = await this.createVideoMediaItem(videoFile, 0);

      // Arrange based on layout preference
      let items: InstagramMediaItem[];
      if (layout === "video-first") {
        items = [videoMedia, ...sequenceMedia];
      } else {
        items = [...sequenceMedia, videoMedia];
      }

      // Update order indices
      items = items.map((item, index) => ({
        ...item,
        order: index,
      }));

      // Validate the complete bundle
      const validation = this.validateBundle(items);
      if (!validation.isValid) {
        throw new Error(
          `Invalid carousel bundle: ${validation.errors.join(", ")}`
        );
      }

      return items;
    } catch (error: any) {
      console.error("Failed to create carousel bundle:", error);
      throw error;
    }
  }

  /**
   * Reorder media items (for drag-and-drop)
   */
  reorderMediaItems(
    items: InstagramMediaItem[],
    fromIndex: number,
    toIndex: number
  ): InstagramMediaItem[] {
    // Validate indices
    if (
      fromIndex < 0 ||
      fromIndex >= items.length ||
      toIndex < 0 ||
      toIndex >= items.length
    ) {
      return items;
    }

    // Create a copy
    const reordered = [...items];

    // Remove item from source
    const [movedItem] = reordered.splice(fromIndex, 1);

    // Insert at destination
    reordered.splice(toIndex, 0, movedItem!);

    // Update order indices
    return reordered.map((item, index) => ({
      ...item,
      order: index,
    }));
  }

  /**
   * Remove media item from bundle
   */
  removeMediaItem(
    items: InstagramMediaItem[],
    index: number
  ): InstagramMediaItem[] {
    if (index < 0 || index >= items.length) {
      return items;
    }

    // Revoke preview URL for cleanup
    const itemToRemove = items[index];
    if (itemToRemove && itemToRemove.url.startsWith("blob:")) {
      URL.revokeObjectURL(itemToRemove.url);
    }

    // Create copy without the item
    const filtered = items.filter((_, i) => i !== index);

    // Update order indices
    return filtered.map((item, idx) => ({
      ...item,
      order: idx,
    }));
  }

  /**
   * Validate media bundle
   */
  validateBundle(items: InstagramMediaItem[]): {
    isValid: boolean;
    errors: string[];
  } {
    const errors: string[] = [];

    // Check item count
    const count = items.length;
    if (count < INSTAGRAM_MEDIA_CONSTRAINTS.CAROUSEL_MIN_ITEMS) {
      errors.push(
        `Carousel must have at least ${INSTAGRAM_MEDIA_CONSTRAINTS.CAROUSEL_MIN_ITEMS} items`
      );
    }
    if (count > INSTAGRAM_MEDIA_CONSTRAINTS.CAROUSEL_MAX_ITEMS) {
      errors.push(
        `Carousel cannot exceed ${INSTAGRAM_MEDIA_CONSTRAINTS.CAROUSEL_MAX_ITEMS} items`
      );
    }

    // Validate each item
    items.forEach((item, index) => {
      const validation = validateMediaItem(item);
      if (!validation.isValid) {
        errors.push(`Item ${index + 1}: ${validation.error}`);
      }
    });

    return {
      isValid: errors.length === 0,
      errors,
    };
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================

  /**
   * Generate static sequence image using ShareService
   */
  private async generateSequenceImage(
    sequence: SequenceData,
    options: ShareOptions
  ): Promise<Blob> {
    // Use ShareService to generate image blob
    // This leverages your existing rendering infrastructure
    return await this.shareService.getImageBlob(sequence, options);
  }

  /**
   * Generate animated GIF using ShareService
   */
  private async generateSequenceGif(
    sequence: SequenceData,
    options: ShareOptions
  ): Promise<Blob> {
    // For now, use the same image blob until GIF support is added to IShareService
    // TODO: Add generateGif method to IShareService interface
    return await this.shareService.getImageBlob(sequence, options);
  }

  /**
   * Convert data URL to Blob
   */
  private async dataUrlToBlob(dataUrl: string): Promise<Blob> {
    const response = await fetch(dataUrl);
    return await response.blob();
  }

  /**
   * Create InstagramMediaItem from Blob
   */
  private async createMediaItemFromBlob(
    blob: Blob,
    type: "IMAGE" | "VIDEO",
    order: number,
    filename: string
  ): Promise<InstagramMediaItem> {
    // Create preview URL
    const url = URL.createObjectURL(blob);

    return {
      type,
      blob,
      url,
      filename,
      order,
    };
  }
}
