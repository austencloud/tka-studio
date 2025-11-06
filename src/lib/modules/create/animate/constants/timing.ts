/**
 * Animation timing constants
 * Centralized timing values for consistent animation behavior
 */

/**
 * Delay before loading animation to allow Drawer slide animation to complete
 */
export const ANIMATION_LOAD_DELAY_MS = 320;

/**
 * Delay before auto-starting animation after load
 */
export const ANIMATION_AUTO_START_DELAY_MS = 100;

/**
 * Delay before rendering frame during GIF export
 */
export const GIF_FRAME_RENDER_DELAY_MS = 50;

/**
 * Delay before initial frame capture during GIF export
 */
export const GIF_INITIAL_CAPTURE_DELAY_MS = 100;

/**
 * Delay before closing export dialog after successful export
 */
export const GIF_EXPORT_SUCCESS_DELAY_MS = 1500;

/**
 * Default frames per second for GIF export
 */
export const GIF_EXPORT_FPS = 30;

/**
 * Number of frames to capture per animation beat
 */
export const GIF_FRAMES_PER_BEAT = 30;

/**
 * GIF export quality (1-10, lower is better quality but larger file)
 */
export const GIF_EXPORT_QUALITY = 10;
