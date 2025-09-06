/**
 * Thumbnail management service
 */
export interface IGalleryThumbnailService {
  getThumbnailUrl(sequenceId: string, thumbnailPath: string): string;
  preloadThumbnail(sequenceId: string, thumbnailPath: string): Promise<void>;
  getThumbnailMetadata(
    sequenceId: string
  ): Promise<{ width: number; height: number } | null>;
  clearThumbnailCache(): void;
}
