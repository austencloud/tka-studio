/**
 * 📳 HAPTIC FEEDBACK SERVICE
 * 
 * Simple haptic feedback service for mobile devices
 */

class HapticFeedbackService {
  /**
   * Check if haptic feedback is available
   */
  isAvailable() {
    return typeof window !== 'undefined' && 
           'navigator' in window && 
           'vibrate' in window.navigator;
  }

  /**
   * Trigger haptic feedback
   */
  trigger(type = 'selection') {
    if (!this.isAvailable()) return;

    try {
      switch (type) {
        case 'selection':
          navigator.vibrate(10); // Light tap
          break;
        case 'warning':
          navigator.vibrate([100, 50, 100]); // Double tap
          break;
        case 'error':
          navigator.vibrate([200, 100, 200, 100, 200]); // Multiple taps
          break;
        case 'success':
          navigator.vibrate(50); // Medium tap
          break;
        default:
          navigator.vibrate(10);
      }
    } catch (error) {
      // Silently fail if vibration is not supported
      console.debug('Haptic feedback not supported:', error);
    }
  }
}

// Export singleton instance
const hapticFeedbackService = new HapticFeedbackService();
export default hapticFeedbackService;