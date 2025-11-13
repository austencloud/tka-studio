/**
 * Firebase Video Upload Service
 *
 * STUB INTERFACE - Not yet implemented
 *
 * Purpose: Upload user performance videos and animated sequences to Firebase Storage.
 * When ready to implement, this service will handle:
 * - Uploading performance videos from user's device to Firebase Storage
 * - Uploading animated WebP/GIF sequences generated from notation data
 * - Managing storage paths: sequences/{userId}/{sequenceId}/video|animation
 * - Progress callbacks for upload UI
 * - Cleanup of orphaned files
 *
 * Why Firebase Storage:
 * - Already using Firebase/Firestore
 * - Cost-effective for video hosting (~$0.026/GB/month)
 * - Integrates with Firestore security rules
 * - CDN built-in
 *
 * Integration points:
 * - Call from SequencePersistenceService when user saves sequence
 * - Call from Share flow before exporting to Instagram
 * - Referenced in SequenceData.performanceVideoUrl / animatedSequenceUrl
 */

export interface IFirebaseVideoUploadService {
  /**
   * Upload a user's performance video to Firebase Storage
   *
   * @param sequenceId - The sequence this video belongs to
   * @param videoFile - The video file from user's device (via input[type=file])
   * @param onProgress - Optional callback for upload progress (0-100)
   * @returns Promise resolving to Firebase Storage URL
   *
   * Storage path: sequences/{userId}/{sequenceId}/video/performance.mp4
   *
   * TODO: Implement with:
   * - Firebase Storage SDK: uploadBytesResumable()
   * - Video validation: format, size limits, duration
   * - Compression if needed (consider client-side with ffmpeg.wasm)
   * - Thumbnail extraction for preview
   */
  uploadPerformanceVideo(
    sequenceId: string,
    videoFile: File,
    onProgress?: (percent: number) => void
  ): Promise<string>;

  /**
   * Upload animated sequence (WebP or GIF) to Firebase Storage
   *
   * @param sequenceId - The sequence ID
   * @param animationBlob - The rendered animation blob (from canvas.toBlob)
   * @param format - 'webp' or 'gif'
   * @returns Promise resolving to Firebase Storage URL
   *
   * Storage path: sequences/{userId}/{sequenceId}/animation/sequence.{format}
   *
   * TODO: Integrate with existing render services:
   * - SequenceRenderService already renders sequences
   * - Canvas already exports to WebP
   * - Just need to upload the blob
   */
  uploadAnimatedSequence(
    sequenceId: string,
    animationBlob: Blob,
    format: "webp" | "gif"
  ): Promise<string>;

  /**
   * Delete all assets for a sequence (cleanup when sequence is deleted)
   *
   * @param sequenceId - The sequence ID to clean up
   *
   * TODO: Recursively delete folder: sequences/{userId}/{sequenceId}/
   */
  deleteSequenceAssets(sequenceId: string): Promise<void>;

  /**
   * Get a public download URL for a storage path
   * Needed for displaying videos in the app
   */
  getPublicUrl(storagePath: string): Promise<string>;
}
