/**
 * Vite HMR 404 Error Recovery
 *
 * CRITICAL: This module must be imported at the TOP of the app entry point
 * to catch module loading failures before Svelte components initialize.
 *
 * When DevTools is open and page is refreshed, Vite sometimes returns 404 for
 * dynamically imported modules. This is a known Vite bug - we detect it and
 * automatically reload to recover.
 */

// Execute immediately when this module is loaded
if (typeof window !== 'undefined') {
  let hasAttemptedRecovery = false;

  // Listen for unhandled promise rejections (module loading failures)
  window.addEventListener('unhandledrejection', (event) => {
    const error = event.reason;

    // Check if this is a Vite module loading error
    if (error instanceof TypeError &&
        error.message?.includes('Failed to fetch dynamically imported module') &&
        !hasAttemptedRecovery) {

      console.warn('🔄 [AUTO-RECOVERY] Detected Vite HMR module loading failure (common with DevTools open during refresh)');
      console.warn('🔄 [AUTO-RECOVERY] Error:', error.message);
      console.warn('🔄 [AUTO-RECOVERY] Automatically reloading page to recover...');

      hasAttemptedRecovery = true;

      // Slight delay to ensure console messages are visible
      setTimeout(() => {
        window.location.reload();
      }, 500);

      // Prevent the error from appearing in console as unhandled
      event.preventDefault();
    }
  });

  // Also listen for regular errors
  window.addEventListener('error', (event) => {
    const error = event.error;

    // Check if this is a module loading error
    if (error instanceof TypeError &&
        error.message?.includes('Failed to fetch dynamically imported module') &&
        !hasAttemptedRecovery) {

      console.warn('🔄 [AUTO-RECOVERY] Detected Vite module loading error via error event');
      console.warn('🔄 [AUTO-RECOVERY] Error:', error.message);
      console.warn('🔄 [AUTO-RECOVERY] Reloading page...');

      hasAttemptedRecovery = true;

      setTimeout(() => {
        window.location.reload();
      }, 500);

      event.preventDefault();
    }
  });

  console.log('✅ [VITE-HMR-RECOVERY] Error recovery system active');
}

export {}; // Make this a module
