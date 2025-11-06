/**
 * Instagram Media Upload API Endpoint
 *
 * Accepts media files (images/videos) and uploads them to Firebase Storage.
 * Returns a publicly accessible URL that Instagram Graph API can use.
 *
 * This endpoint is CRITICAL for production Instagram posting since Instagram
 * requires media to be hosted on a publicly accessible URL with appropriate CORS headers.
 */

import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { app } from '$shared/auth/firebase';

// Initialize Firebase Storage
const storage = getStorage(app);

// Maximum file sizes (Instagram limits)
const MAX_IMAGE_SIZE = 8 * 1024 * 1024; // 8MB
const MAX_VIDEO_SIZE = 100 * 1024 * 1024; // 100MB

// Allowed MIME types
const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif'];
const ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/quicktime', 'video/x-m4v'];

/**
 * POST /api/instagram/upload-media
 *
 * Uploads a media file to Firebase Storage and returns the public URL.
 *
 * Request Body (multipart/form-data):
 * - file: The media file to upload
 *
 * Response:
 * - url: Public URL to the uploaded file
 * - path: Storage path (for cleanup)
 * - expiresAt: When the file will be automatically deleted (24 hours)
 */
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    // Parse multipart form data
    const formData = await request.formData();
    const file = formData.get('file');

    // Validate file exists
    if (!file || !(file instanceof File)) {
      throw error(400, 'No file provided');
    }

    // Validate file type
    const isImage = ALLOWED_IMAGE_TYPES.includes(file.type);
    const isVideo = ALLOWED_VIDEO_TYPES.includes(file.type);

    if (!isImage && !isVideo) {
      throw error(400, `Unsupported file type: ${file.type}`);
    }

    // Validate file size
    const maxSize = isImage ? MAX_IMAGE_SIZE : MAX_VIDEO_SIZE;
    if (file.size > maxSize) {
      const maxSizeMB = maxSize / (1024 * 1024);
      throw error(400, `File too large. Max size: ${maxSizeMB}MB`);
    }

    // Generate unique filename with timestamp
    const timestamp = Date.now();
    const randomString = Math.random().toString(36).substring(7);
    const fileExtension = file.name.split('.').pop() || 'jpg';
    const filename = `${timestamp}-${randomString}.${fileExtension}`;

    // Create storage path (files will be in instagram-uploads folder)
    const storagePath = `instagram-uploads/${filename}`;
    const storageRef = ref(storage, storagePath);

    // Convert File to ArrayBuffer for upload
    const arrayBuffer = await file.arrayBuffer();
    const buffer = new Uint8Array(arrayBuffer);

    // Upload to Firebase Storage with metadata
    const metadata = {
      contentType: file.type,
      customMetadata: {
        originalName: file.name,
        uploadedAt: new Date().toISOString(),
        // Auto-delete after 24 hours (handled by Firebase Storage lifecycle rules)
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
      },
    };

    await uploadBytes(storageRef, buffer, metadata);

    // Get public download URL
    const downloadURL = await getDownloadURL(storageRef);

    // Calculate expiration (24 hours from now)
    const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000);

    return json({
      url: downloadURL,
      path: storagePath,
      expiresAt: expiresAt.toISOString(),
      size: file.size,
      type: file.type,
    });
  } catch (err: any) {
    console.error('Instagram media upload error:', err);

    // Handle known errors
    if (err.status) {
      throw err; // Re-throw SvelteKit errors
    }

    // Generic error
    throw error(500, `Upload failed: ${err.message}`);
  }
};

/**
 * DELETE /api/instagram/upload-media
 *
 * Deletes a previously uploaded media file from Firebase Storage.
 *
 * Request Body (JSON):
 * - path: Storage path of the file to delete
 *
 * Response:
 * - success: true if deleted successfully
 */
export const DELETE: RequestHandler = async ({ request }) => {
  try {
    const { path } = await request.json();

    if (!path || typeof path !== 'string') {
      throw error(400, 'Storage path is required');
    }

    // Only allow deletion of files in instagram-uploads folder
    if (!path.startsWith('instagram-uploads/')) {
      throw error(403, 'Can only delete files from instagram-uploads folder');
    }

    const storageRef = ref(storage, path);

    // Delete the file
    const { deleteObject } = await import('firebase/storage');
    await deleteObject(storageRef);

    return json({
      success: true,
      path,
    });
  } catch (err: any) {
    console.error('Instagram media deletion error:', err);

    if (err.status) {
      throw err;
    }

    throw error(500, `Deletion failed: ${err.message}`);
  }
};
