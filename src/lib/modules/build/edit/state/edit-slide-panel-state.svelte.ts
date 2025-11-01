/**
 * Edit Slide Panel State
 * Local UI state management for the EditSlidePanel component
 *
 * Manages:
 * - Touch gesture state for swipe-to-dismiss
 * - Adjustment panel state
 * - Panel element reference
 */

export type SwipeDirection = 'horizontal' | 'vertical';

export interface SwipeGestureState {
  touchStartX: number;
  touchCurrentX: number;
  touchStartY: number;
  touchCurrentY: number;
  isDragging: boolean;
}

export interface SwipeDismissOptions {
  threshold?: number;
  direction: SwipeDirection;
  onDismiss: () => void;
  onHaptic?: (type: 'selection' | 'warning') => void;
}

/**
 * Creates edit slide panel state
 */
export function createEditSlidePanelState() {
  // Touch gesture state
  let touchStartX = $state(0);
  let touchCurrentX = $state(0);
  let touchStartY = $state(0);
  let touchCurrentY = $state(0);
  let isDragging = $state(false);

  // Adjustment panel state
  let isAdjustmentPanelOpen = $state(false);
  let adjustedBeatData = $state<any | null>(null); // Type will be BeatData

  // Panel element reference
  let panelElement = $state<HTMLElement | null>(null);

  // ============================================================================
  // TOUCH GESTURE HANDLERS
  // ============================================================================

  function startGesture(event: TouchEvent): void {
    touchStartX = event.touches[0].clientX;
    touchCurrentX = touchStartX;
    touchStartY = event.touches[0].clientY;
    touchCurrentY = touchStartY;
    isDragging = true;
  }

  function updateGesture(event: TouchEvent, direction: SwipeDirection): void {
    if (!isDragging || !panelElement) return;

    touchCurrentX = event.touches[0].clientX;
    touchCurrentY = event.touches[0].clientY;

    if (direction === 'vertical') {
      // Bottom placement: Allow dragging downward
      const deltaY = touchCurrentY - touchStartY;
      if (deltaY > 0) {
        panelElement.style.transform = `translateY(${deltaY}px)`;
      }
    } else {
      // Side placement: Allow dragging to the right
      const deltaX = touchCurrentX - touchStartX;
      if (deltaX > 0) {
        panelElement.style.transform = `translateX(${deltaX}px)`;
      }
    }
  }

  function endGesture(options: SwipeDismissOptions): void {
    if (!isDragging || !panelElement) return;

    isDragging = false;
    const threshold = options.threshold ?? 100;

    if (options.direction === 'vertical') {
      // Bottom placement: Check vertical swipe distance
      const deltaY = touchCurrentY - touchStartY;
      if (deltaY > threshold) {
        // Swipe far enough - dismiss
        options.onHaptic?.('warning');
        options.onDismiss();
      } else {
        // Snap back
        snapBack();
      }
    } else {
      // Side placement: Check horizontal swipe distance
      const deltaX = touchCurrentX - touchStartX;
      if (deltaX > threshold) {
        // Swipe far enough - dismiss
        options.onHaptic?.('warning');
        options.onDismiss();
      } else {
        // Snap back
        snapBack();
      }
    }
  }

  function snapBack(): void {
    if (!panelElement) return;

    panelElement.style.transform = 'translate(0, 0)';
    panelElement.style.transition = 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';

    setTimeout(() => {
      if (panelElement) {
        panelElement.style.transition = '';
      }
    }, 300);
  }

  // ============================================================================
  // ADJUSTMENT PANEL ACTIONS
  // ============================================================================

  function openAdjustmentPanel(beatData: any): void {
    adjustedBeatData = beatData;
    isAdjustmentPanelOpen = true;
  }

  function closeAdjustmentPanel(): void {
    isAdjustmentPanelOpen = false;
    adjustedBeatData = null;
  }

  function updateAdjustedBeatData(beatData: any): void {
    adjustedBeatData = beatData;
  }

  // ============================================================================
  // EXPOSED STATE AND ACTIONS
  // ============================================================================

  return {
    // Gesture state (read-only access)
    get touchStartX() {
      return touchStartX;
    },
    get touchCurrentX() {
      return touchCurrentX;
    },
    get touchStartY() {
      return touchStartY;
    },
    get touchCurrentY() {
      return touchCurrentY;
    },
    get isDragging() {
      return isDragging;
    },

    // Adjustment panel state
    get isAdjustmentPanelOpen() {
      return isAdjustmentPanelOpen;
    },
    get adjustedBeatData() {
      return adjustedBeatData;
    },

    // Panel element
    get panelElement() {
      return panelElement;
    },
    set panelElement(element: HTMLElement | null) {
      panelElement = element;
    },

    // Gesture actions
    startGesture,
    updateGesture,
    endGesture,

    // Adjustment panel actions
    openAdjustmentPanel,
    closeAdjustmentPanel,
    updateAdjustedBeatData,
  };
}

export type EditSlidePanelState = ReturnType<typeof createEditSlidePanelState>;
