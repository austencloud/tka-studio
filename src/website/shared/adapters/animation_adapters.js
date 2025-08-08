/**
 * Web-specific implementations of animation protocols.
 *
 * This module provides web browser implementations of the animation protocols
 * using CSS transitions, Web Animations API, and DOM manipulation to achieve
 * cross-platform animation compatibility.
 */

/**
 * Web adapter for stack-like containers using CSS display toggling.
 * Implements the StackContainer protocol for web browsers.
 */
class WebStackAdapter {
  /**
   * Initialize with a container element.
   * @param {HTMLElement} containerElement - The container holding stack children
   */
  constructor(containerElement) {
    this.container = containerElement;
    this.currentIndex = 0;

    // Initialize by hiding all children except the first
    this._initializeStack();
  }

  /**
   * Initialize the stack by hiding all children except the first visible one.
   * @private
   */
  _initializeStack() {
    const children = this.container.children;
    let firstVisibleFound = false;

    for (let i = 0; i < children.length; i++) {
      const child = children[i];
      const isVisible = child.style.display !== "none";

      if (isVisible && !firstVisibleFound) {
        this.currentIndex = i;
        firstVisibleFound = true;
      } else {
        child.style.display = "none";
      }
    }
  }

  /**
   * Get the index of the currently visible element.
   * @returns {number} Current index
   */
  getCurrentIndex() {
    return this.currentIndex;
  }

  /**
   * Set which element should be visible by index.
   * @param {number} index - Index of element to show
   */
  setCurrentIndex(index) {
    const children = this.container.children;

    // Hide all children
    for (let i = 0; i < children.length; i++) {
      children[i].style.display = "none";
    }

    // Show selected child
    if (children[index]) {
      children[index].style.display = "block";
      this.currentIndex = index;
    }
  }

  /**
   * Get the element at the specified index.
   * @param {number} index - Index of element to get
   * @returns {HTMLElement|null} Element at index
   */
  getWidgetAt(index) {
    return this.container.children[index] || null;
  }

  /**
   * Get the total number of elements in the stack.
   * @returns {number} Number of child elements
   */
  getWidgetCount() {
    return this.container.children.length;
  }
}

/**
 * Web adapter for opacity effects using CSS opacity property.
 * Implements the OpacityEffect protocol for web browsers.
 */
class WebOpacityEffectAdapter {
  /**
   * Initialize with a DOM element.
   * @param {HTMLElement} element - The element to control opacity for
   */
  constructor(element) {
    this.element = element;
  }

  /**
   * Get the current opacity value.
   * @returns {number} Opacity value (0.0 to 1.0)
   */
  getOpacity() {
    const opacity = this.element.style.opacity;
    return opacity === "" ? 1.0 : parseFloat(opacity);
  }

  /**
   * Set the opacity value.
   * @param {number} opacity - Opacity value (0.0 to 1.0)
   */
  setOpacity(opacity) {
    this.element.style.opacity = opacity.toString();
  }
}

/**
 * Web adapter for property animations using CSS transitions and Web Animations API.
 * Implements the PropertyAnimation protocol for web browsers.
 */
class WebPropertyAnimationAdapter {
  /**
   * Initialize with element and property to animate.
   * @param {HTMLElement} element - Element to animate
   * @param {string} property - CSS property to animate
   */
  constructor(element, property) {
    this.element = element;
    this.property = property;
    this.duration = 250; // Default duration in ms
    this.startValue = null;
    this.endValue = null;
    this.animation = null;

    // Check for reduced motion preference
    this.respectsReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
  }

  /**
   * Start the animation.
   */
  start() {
    if (this.respectsReducedMotion) {
      // Skip animation for accessibility
      this.element.style[this.property] = this.endValue;
      return;
    }

    // Use Web Animations API if available, fallback to CSS transitions
    if (
      this.element.animate &&
      this.startValue !== null &&
      this.endValue !== null
    ) {
      this._startWebAnimation();
    } else {
      this._startCSSTransition();
    }
  }

  /**
   * Stop the animation.
   */
  stop() {
    if (this.animation) {
      this.animation.cancel();
      this.animation = null;
    }
    this.element.style.transition = "";
  }

  /**
   * Set the animation duration in milliseconds.
   * @param {number} duration - Duration in milliseconds
   */
  setDuration(duration) {
    this.duration = duration;
  }

  /**
   * Set the starting value for the animated property.
   * @param {any} value - Starting value
   */
  setStartValue(value) {
    this.startValue = value;
  }

  /**
   * Set the ending value for the animated property.
   * @param {any} value - Ending value
   */
  setEndValue(value) {
    this.endValue = value;
  }

  /**
   * Start animation using Web Animations API.
   * @private
   */
  _startWebAnimation() {
    const keyframes = [
      { [this.property]: this.startValue },
      { [this.property]: this.endValue },
    ];

    const options = {
      duration: this.duration,
      easing: "ease-in-out",
      fill: "forwards",
    };

    this.animation = this.element.animate(keyframes, options);
  }

  /**
   * Start animation using CSS transitions.
   * @private
   */
  _startCSSTransition() {
    // Set initial value
    if (this.startValue !== null) {
      this.element.style[this.property] = this.startValue;
    }

    // Set up transition
    this.element.style.transition = `${this.property} ${this.duration}ms ease-in-out`;

    // Trigger transition by setting end value
    if (this.endValue !== null) {
      // Use requestAnimationFrame to ensure the transition is applied
      requestAnimationFrame(() => {
        this.element.style[this.property] = this.endValue;
      });
    }
  }
}

/**
 * Web adapter for animation groups using coordinated CSS animations.
 * Implements the AnimationGroup protocol for web browsers.
 */
class WebAnimationGroupAdapter {
  /**
   * Initialize an empty animation group.
   */
  constructor() {
    this.animations = [];
  }

  /**
   * Add an animation to the group.
   * @param {WebPropertyAnimationAdapter} animation - Animation to add
   */
  addAnimation(animation) {
    if (animation instanceof WebPropertyAnimationAdapter) {
      this.animations.push(animation);
    } else {
      console.warn(
        "WebAnimationGroupAdapter: Expected WebPropertyAnimationAdapter"
      );
    }
  }

  /**
   * Start all animations in the group simultaneously.
   */
  start() {
    this.animations.forEach((animation) => animation.start());
  }

  /**
   * Stop all animations in the group.
   */
  stop() {
    this.animations.forEach((animation) => animation.stop());
  }
}

// Factory functions for creating web adapters

export function createPropertyAnimationAdapter(element, property) {
  return new WebPropertyAnimationAdapter(element, property);
}

// Export adapter classes
export {
  WebStackAdapter,
  WebOpacityEffectAdapter,
  WebPropertyAnimationAdapter,
  WebAnimationGroupAdapter,
};
