/**
 * Instagram OAuth & API Domain Models
 *
 * Models for Instagram Graph API authentication, token management,
 * and media posting capabilities.
 */

/**
 * Instagram OAuth token data
 * Stored securely in Firestore per user
 */
export interface InstagramToken {
  /** Instagram User ID */
  readonly userId: string;

  /** Instagram username */
  readonly username: string;

  /** OAuth access token (short-lived or long-lived) */
  readonly accessToken: string;

  /** Token expiration timestamp */
  readonly expiresAt: Date;

  /** Whether this is a long-lived token (60 days) vs short-lived (1 hour) */
  readonly isLongLived: boolean;

  /** Instagram account type: PERSONAL, BUSINESS, or CREATOR */
  readonly accountType: 'PERSONAL' | 'BUSINESS' | 'CREATOR';

  /** When the token was created/refreshed */
  readonly lastRefreshed: Date;

  /** Instagram Business Account ID (if connected to a Business account) */
  readonly businessAccountId?: string;

  /** Connected Facebook Page ID (required for posting) */
  readonly facebookPageId?: string;
}

/**
 * Instagram media item for carousel posts
 */
export interface InstagramMediaItem {
  /** Media type: IMAGE or VIDEO */
  readonly type: 'IMAGE' | 'VIDEO';

  /** Media file (as Blob or File) */
  readonly file: Blob | File;

  /** Local preview URL (for UI) */
  readonly previewUrl: string;

  /** File size in bytes */
  readonly sizeBytes: number;

  /** MIME type */
  readonly mimeType: string;

  /** Optional caption for this specific item */
  readonly caption?: string;

  /** Order in carousel (0-indexed) */
  readonly order: number;
}

/**
 * Instagram carousel post data
 */
export interface InstagramCarouselPost {
  /** Array of media items (2-10 items) */
  readonly items: readonly InstagramMediaItem[];

  /** Post caption (max 2200 characters) */
  readonly caption: string;

  /** Location tag (optional) */
  readonly location?: {
    readonly id: string;
    readonly name: string;
  };

  /** Whether to share to Facebook (if connected) */
  readonly shareToFacebook: boolean;

  /** Associated TKA sequence ID */
  readonly sequenceId: string;

  /** Hashtags (extracted from caption or added separately) */
  readonly hashtags: readonly string[];
}

/**
 * Instagram posting progress/status
 */
export interface InstagramPostStatus {
  /** Current status */
  readonly status: 'uploading' | 'processing' | 'publishing' | 'completed' | 'failed';

  /** Progress percentage (0-100) */
  readonly progress: number;

  /** Status message */
  readonly message: string;

  /** Instagram post ID (once published) */
  readonly postId?: string;

  /** Instagram post URL (once published) */
  readonly postUrl?: string;

  /** Error details (if failed) */
  readonly error?: {
    readonly code: string;
    readonly message: string;
  };
}

/**
 * Instagram API permissions required
 */
export const INSTAGRAM_PERMISSIONS = {
  /** View Instagram account info */
  USER_PROFILE: 'instagram_basic',

  /** Manage Instagram content */
  CONTENT_PUBLISH: 'instagram_content_publish',

  /** View Instagram insights */
  INSIGHTS: 'instagram_manage_insights',

  /** Manage Instagram messages */
  MESSAGES: 'instagram_manage_messages',
} as const;

/**
 * Instagram API scopes for different features
 */
export type InstagramScope = typeof INSTAGRAM_PERMISSIONS[keyof typeof INSTAGRAM_PERMISSIONS];

/**
 * Instagram media constraints (from Instagram Graph API)
 */
export const INSTAGRAM_MEDIA_CONSTRAINTS = {
  /** Carousel must have 2-10 items */
  CAROUSEL_MIN_ITEMS: 2,
  CAROUSEL_MAX_ITEMS: 10,

  /** Image constraints */
  IMAGE_MAX_SIZE_MB: 8,
  IMAGE_MIN_WIDTH: 320,
  IMAGE_MIN_HEIGHT: 320,
  IMAGE_MAX_WIDTH: 1440,
  IMAGE_MAX_HEIGHT: 1440,
  IMAGE_ASPECT_RATIO_MIN: 0.8,  // 4:5
  IMAGE_ASPECT_RATIO_MAX: 1.91, // 1.91:1

  /** Video constraints */
  VIDEO_MAX_SIZE_MB: 100,
  VIDEO_MIN_WIDTH: 320,
  VIDEO_MIN_HEIGHT: 320,
  VIDEO_MAX_WIDTH: 1920,
  VIDEO_MAX_HEIGHT: 1920,
  VIDEO_MIN_DURATION_SEC: 3,
  VIDEO_MAX_DURATION_SEC: 60,
  VIDEO_ASPECT_RATIO_MIN: 0.8,
  VIDEO_ASPECT_RATIO_MAX: 1.91,

  /** Caption constraints */
  CAPTION_MAX_LENGTH: 2200,
  HASHTAG_MAX_COUNT: 30,
} as const;

/**
 * Helper to create an Instagram token
 */
export function createInstagramToken(
  userId: string,
  username: string,
  accessToken: string,
  expiresIn: number,
  accountType: 'PERSONAL' | 'BUSINESS' | 'CREATOR',
  options?: {
    businessAccountId?: string;
    facebookPageId?: string;
  }
): InstagramToken {
  const now = new Date();
  const expiresAt = new Date(now.getTime() + expiresIn * 1000);

  // Tokens with expiration > 24 hours are considered long-lived
  const isLongLived = expiresIn > 24 * 60 * 60;

  return {
    userId,
    username,
    accessToken,
    expiresAt,
    isLongLived,
    accountType,
    lastRefreshed: now,
    businessAccountId: options?.businessAccountId,
    facebookPageId: options?.facebookPageId,
  };
}

/**
 * Check if Instagram token is expired or about to expire
 */
export function isTokenExpired(token: InstagramToken, bufferMinutes: number = 30): boolean {
  const now = new Date();
  const bufferMs = bufferMinutes * 60 * 1000;
  return token.expiresAt.getTime() - bufferMs <= now.getTime();
}

/**
 * Check if token needs refresh (within 7 days of expiration for long-lived tokens)
 */
export function needsRefresh(token: InstagramToken): boolean {
  if (!token.isLongLived) {
    return isTokenExpired(token, 30); // Refresh short-lived tokens 30 min before expiry
  }

  // For long-lived tokens, refresh if within 7 days of expiration
  const now = new Date();
  const sevenDaysMs = 7 * 24 * 60 * 60 * 1000;
  return token.expiresAt.getTime() - sevenDaysMs <= now.getTime();
}

/**
 * Validate media item against Instagram constraints
 */
export function validateMediaItem(item: InstagramMediaItem): { isValid: boolean; error?: string } {
  const { type, sizeBytes, file } = item;

  if (type === 'IMAGE') {
    const maxSize = INSTAGRAM_MEDIA_CONSTRAINTS.IMAGE_MAX_SIZE_MB * 1024 * 1024;
    if (sizeBytes > maxSize) {
      return {
        isValid: false,
        error: `Image exceeds ${INSTAGRAM_MEDIA_CONSTRAINTS.IMAGE_MAX_SIZE_MB}MB limit`,
      };
    }
  } else if (type === 'VIDEO') {
    const maxSize = INSTAGRAM_MEDIA_CONSTRAINTS.VIDEO_MAX_SIZE_MB * 1024 * 1024;
    if (sizeBytes > maxSize) {
      return {
        isValid: false,
        error: `Video exceeds ${INSTAGRAM_MEDIA_CONSTRAINTS.VIDEO_MAX_SIZE_MB}MB limit`,
      };
    }
  }

  return { isValid: true };
}

/**
 * Validate carousel post
 */
export function validateCarouselPost(post: InstagramCarouselPost): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  // Validate item count
  const itemCount = post.items.length;
  if (itemCount < INSTAGRAM_MEDIA_CONSTRAINTS.CAROUSEL_MIN_ITEMS) {
    errors.push(`Carousel must have at least ${INSTAGRAM_MEDIA_CONSTRAINTS.CAROUSEL_MIN_ITEMS} items`);
  }
  if (itemCount > INSTAGRAM_MEDIA_CONSTRAINTS.CAROUSEL_MAX_ITEMS) {
    errors.push(`Carousel cannot have more than ${INSTAGRAM_MEDIA_CONSTRAINTS.CAROUSEL_MAX_ITEMS} items`);
  }

  // Validate each item
  post.items.forEach((item, index) => {
    const validation = validateMediaItem(item);
    if (!validation.isValid) {
      errors.push(`Item ${index + 1}: ${validation.error}`);
    }
  });

  // Validate caption length
  if (post.caption.length > INSTAGRAM_MEDIA_CONSTRAINTS.CAPTION_MAX_LENGTH) {
    errors.push(`Caption exceeds ${INSTAGRAM_MEDIA_CONSTRAINTS.CAPTION_MAX_LENGTH} character limit`);
  }

  // Validate hashtag count
  if (post.hashtags.length > INSTAGRAM_MEDIA_CONSTRAINTS.HASHTAG_MAX_COUNT) {
    errors.push(`Too many hashtags (max ${INSTAGRAM_MEDIA_CONSTRAINTS.HASHTAG_MAX_COUNT})`);
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}
