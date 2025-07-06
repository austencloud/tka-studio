// Haptic feedback service
class HapticFeedbackService {
  constructor() {
    this.enabled = true;
  }

  vibrate(pattern = 50) {
    if (!this.enabled) return;

    if (typeof navigator !== "undefined" && navigator.vibrate) {
      try {
        navigator.vibrate(pattern);
      } catch (error) {
        console.warn("Haptic feedback not supported:", error);
      }
    }
  }

  enable() {
    this.enabled = true;
  }

  disable() {
    this.enabled = false;
  }

  // Common haptic patterns
  light() {
    this.vibrate(10);
  }

  medium() {
    this.vibrate(50);
  }

  heavy() {
    this.vibrate(100);
  }

  success() {
    this.vibrate([50, 50, 50]);
  }

  error() {
    this.vibrate([100, 50, 100]);
  }
}

export default new HapticFeedbackService();
