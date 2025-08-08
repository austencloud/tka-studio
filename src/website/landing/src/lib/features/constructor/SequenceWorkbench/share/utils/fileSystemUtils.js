/**
 * File System Utilities for TKA Constructor
 * Provides utilities for file system operations and device detection
 */

/**
 * Check if the current device is a mobile device
 * @returns {boolean} True if the device is mobile
 */
export function isMobileDevice() {
  // Check user agent for mobile indicators
  const userAgent = navigator.userAgent || navigator.vendor || window.opera;

  // Mobile device patterns
  const mobilePatterns = [
    /Android/i,
    /webOS/i,
    /iPhone/i,
    /iPad/i,
    /iPod/i,
    /BlackBerry/i,
    /Windows Phone/i,
    /Mobile/i,
    /Tablet/i
  ];

  // Check if any mobile pattern matches
  const isMobileUA = mobilePatterns.some(pattern => pattern.test(userAgent));

  // Also check for touch capability and screen size
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  const isSmallScreen = window.innerWidth <= 768;

  return isMobileUA || (isTouchDevice && isSmallScreen);
}

/**
 * Check if the current device is a tablet
 * @returns {boolean} True if the device is a tablet
 */
export function isTabletDevice() {
  const userAgent = navigator.userAgent || navigator.vendor || window.opera;

  // Tablet-specific patterns
  const tabletPatterns = [
    /iPad/i,
    /Android.*Tablet/i,
    /Windows.*Touch/i,
    /Kindle/i,
    /Silk/i,
    /PlayBook/i
  ];

  const isTabletUA = tabletPatterns.some(pattern => pattern.test(userAgent));
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  const isTabletScreen = window.innerWidth >= 768 && window.innerWidth <= 1024;

  return isTabletUA || (isTouchDevice && isTabletScreen);
}

/**
 * Check if the current device is a desktop
 * @returns {boolean} True if the device is desktop
 */
export function isDesktopDevice() {
  return !isMobileDevice() && !isTabletDevice();
}

/**
 * Get the device type as a string
 * @returns {'mobile'|'tablet'|'desktop'} Device type
 */
export function getDeviceType() {
  if (isMobileDevice()) return 'mobile';
  if (isTabletDevice()) return 'tablet';
  return 'desktop';
}

/**
 * Check if the File System Access API is supported
 * @returns {boolean} True if File System Access API is supported
 */
export function isFileSystemAccessSupported() {
  return 'showSaveFilePicker' in window && 'showOpenFilePicker' in window;
}

/**
 * Check if the device supports file downloads
 * @returns {boolean} True if file downloads are supported
 */
export function isDownloadSupported() {
  return typeof document !== 'undefined' &&
         'createElement' in document &&
         'createObjectURL' in URL;
}

/**
 * Get the preferred file save method for the current device
 * @returns {'filesystem'|'download'|'share'} Preferred save method
 */
export function getPreferredSaveMethod() {
  if (isMobileDevice()) {
    // Mobile devices prefer sharing
    return 'share';
  } else if (isFileSystemAccessSupported()) {
    // Modern browsers with File System Access API
    return 'filesystem';
  } else {
    // Fallback to download
    return 'download';
  }
}

/**
 * Check if the Web Share API is supported
 * @returns {boolean} True if Web Share API is supported
 */
export function isWebShareSupported() {
  return 'share' in navigator;
}

/**
 * Check if the device supports clipboard operations
 * @returns {boolean} True if clipboard operations are supported
 */
export function isClipboardSupported() {
  return 'clipboard' in navigator && 'writeText' in navigator.clipboard;
}

/**
 * Get device capabilities summary
 * @returns {Object} Object containing device capabilities
 */
export function getDeviceCapabilities() {
  return {
    deviceType: getDeviceType(),
    isMobile: isMobileDevice(),
    isTablet: isTabletDevice(),
    isDesktop: isDesktopDevice(),
    fileSystemAccess: isFileSystemAccessSupported(),
    download: isDownloadSupported(),
    webShare: isWebShareSupported(),
    clipboard: isClipboardSupported(),
    preferredSaveMethod: getPreferredSaveMethod()
  };
}
