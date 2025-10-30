import { injectable } from "inversify";
import type {
  IGestureService,
  SwipeGestureConfig,
  SwipeGestureHandler,
  GestureDirection,
} from "../contracts/IGestureService";

interface SwipeGestureState {
  touchStartX: number;
  touchStartY: number;
  touchCurrentX: number;
  touchCurrentY: number;
  isDragging: boolean;
}

/**
 * Gesture Service Implementation
 *
 * Provides reusable touch gesture handling for common interaction patterns.
 */
@injectable()
export class GestureService implements IGestureService {

  createSwipeGestureHandler(config: SwipeGestureConfig): SwipeGestureHandler {
    const threshold = config.threshold ?? 100;

    const state: SwipeGestureState = {
      touchStartX: 0,
      touchStartY: 0,
      touchCurrentX: 0,
      touchCurrentY: 0,
      isDragging: false,
    };

    const handleTouchStart = (e: TouchEvent) => {
      state.touchStartX = e.touches[0].clientX;
      state.touchStartY = e.touches[0].clientY;
      state.touchCurrentX = state.touchStartX;
      state.touchCurrentY = state.touchStartY;
      state.isDragging = true;
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (!state.isDragging) return;

      state.touchCurrentX = e.touches[0].clientX;
      state.touchCurrentY = e.touches[0].clientY;

      const deltaX = state.touchCurrentX - state.touchStartX;
      const deltaY = state.touchCurrentY - state.touchStartY;

      // Determine if gesture matches configuration
      let shouldPreventDefault = false;
      let delta = 0;

      if (config.direction === 'vertical') {
        delta = deltaY;
        // Check if swipe is in the allowed direction
        if (config.dismissOrientation === 'down' && deltaY > 0) {
          shouldPreventDefault = true;
        } else if (config.dismissOrientation === 'up' && deltaY < 0) {
          shouldPreventDefault = true;
          delta = Math.abs(deltaY);
        }
      } else {
        delta = deltaX;
        // Check if swipe is in the allowed direction
        if (config.dismissOrientation === 'right' && deltaX > 0) {
          shouldPreventDefault = true;
        } else if (config.dismissOrientation === 'left' && deltaX < 0) {
          shouldPreventDefault = true;
          delta = Math.abs(deltaX);
        }
      }

      if (shouldPreventDefault) {
        e.preventDefault();
        config.onDrag?.(delta);
      }
    };

    const handleTouchEnd = () => {
      if (!state.isDragging) return;

      const deltaX = state.touchCurrentX - state.touchStartX;
      const deltaY = state.touchCurrentY - state.touchStartY;

      let delta = 0;
      let shouldDismiss = false;

      if (config.direction === 'vertical') {
        delta = deltaY;
        if (config.dismissOrientation === 'down' && delta > threshold) {
          shouldDismiss = true;
        } else if (config.dismissOrientation === 'up' && delta < -threshold) {
          shouldDismiss = true;
        }
      } else {
        delta = deltaX;
        if (config.dismissOrientation === 'right' && delta > threshold) {
          shouldDismiss = true;
        } else if (config.dismissOrientation === 'left' && delta < -threshold) {
          shouldDismiss = true;
        }
      }

      if (shouldDismiss) {
        config.onDismiss();
      } else {
        config.onSnapBack?.();
      }

      // Reset state
      state.isDragging = false;
      state.touchStartX = 0;
      state.touchStartY = 0;
      state.touchCurrentX = 0;
      state.touchCurrentY = 0;
    };

    return {
      handleTouchStart,
      handleTouchMove,
      handleTouchEnd,
    };
  }

  applyDragTransform(
    element: HTMLElement | null,
    delta: number,
    direction: GestureDirection
  ): void {
    if (!element) return;

    if (direction === 'vertical') {
      element.style.transform = `translateY(${delta}px)`;
    } else {
      element.style.transform = `translateX(${delta}px)`;
    }
  }

  snapBackTransform(
    element: HTMLElement | null,
    direction: GestureDirection,
    duration: number = 300
  ): void {
    if (!element) return;

    const transform = direction === 'vertical' ? 'translateY(0)' : 'translateX(0)';
    element.style.transform = transform;
    element.style.transition = `transform ${duration}ms cubic-bezier(0.34, 1.56, 0.64, 1)`;

    setTimeout(() => {
      if (element) {
        element.style.transition = '';
      }
    }, duration);
  }
}
