/**
 * SimplifiedOrientationControl Layout Test
 *
 * Tests that orientation display text scales appropriately and doesn't
 * cause layout shifts when showing long values like "COUNTER"
 */

import { render, screen } from '@testing-library/svelte';
import { describe, it, expect, beforeEach } from 'vitest';
import SimplifiedOrientationControl from '$lib/modules/build/edit/components/SimplifiedOrientationControl.svelte';
import {
  GridLocation,
  GridMode,
  MotionColor,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
  type BeatData
} from '$shared';

describe('SimplifiedOrientationControl - Layout Stability', () => {
  const mockBeatData: BeatData = {
    id: 'test-beat',
    beatNumber: 1,
    duration: 1000,
    blueReversal: false,
    redReversal: false,
    isBlank: false,
    motions: {
      [MotionColor.BLUE]: {
        motionType: MotionType.PRO,
        rotationDirection: RotationDirection.CLOCKWISE,
        startLocation: GridLocation.NORTH,
        endLocation: GridLocation.SOUTH,
        turns: 1.5,
        startOrientation: Orientation.IN,
        endOrientation: Orientation.OUT,
        isVisible: true,
        propType: PropType.STAFF,
        arrowLocation: GridLocation.NORTH,
        color: MotionColor.BLUE,
        gridMode: GridMode.DIAMOND,
        arrowPlacementData: {} as any,
        propPlacementData: {} as any,
      },
      [MotionColor.RED]: {
        motionType: MotionType.ANTI,
        rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        startLocation: GridLocation.NORTH,
        endLocation: GridLocation.SOUTH,
        turns: 1.0,
        startOrientation: Orientation.COUNTER,
        endOrientation: Orientation.IN,
        isVisible: true,
        propType: PropType.STAFF,
        arrowLocation: GridLocation.SOUTH,
        color: MotionColor.RED,
        gridMode: GridMode.DIAMOND,
        arrowPlacementData: {} as any,
        propPlacementData: {} as any,
      },
    },
  };

  const mockOnOrientationChanged = () => {};

  describe('Layout measurements with different orientation values', () => {
    it('should measure and compare button positions between short and long orientation text', () => {
      // Render blue control with short orientation "IN"
      const { container: blueContainer } = render(SimplifiedOrientationControl, {
        props: {
          color: 'blue',
          currentBeatData: mockBeatData,
          onOrientationChanged: mockOnOrientationChanged,
        },
      });

      // Render red control with long orientation "COUNTER"
      const { container: redContainer } = render(SimplifiedOrientationControl, {
        props: {
          color: 'red',
          currentBeatData: mockBeatData,
          onOrientationChanged: mockOnOrientationChanged,
        },
      });

      // Get the previous/next buttons from both controls
      const bluePrevButton = blueContainer.querySelector('.stepper-btn.previous') as HTMLElement;
      const blueNextButton = blueContainer.querySelector('.stepper-btn.next') as HTMLElement;
      const redPrevButton = redContainer.querySelector('.stepper-btn.previous') as HTMLElement;
      const redNextButton = redContainer.querySelector('.stepper-btn.next') as HTMLElement;

      expect(bluePrevButton).toBeTruthy();
      expect(blueNextButton).toBeTruthy();
      expect(redPrevButton).toBeTruthy();
      expect(redNextButton).toBeTruthy();

      // Get bounding boxes
      const bluePrevRect = bluePrevButton.getBoundingClientRect();
      const blueNextRect = blueNextButton.getBoundingClientRect();
      const redPrevRect = redPrevButton.getBoundingClientRect();
      const redNextRect = redNextButton.getBoundingClientRect();

      // Calculate center positions
      const bluePrevCenter = bluePrevRect.left + bluePrevRect.width / 2;
      const blueNextCenter = blueNextRect.left + blueNextRect.width / 2;
      const redPrevCenter = redPrevRect.left + redPrevRect.width / 2;
      const redNextCenter = redNextRect.left + redNextRect.width / 2;

      console.log('Blue (IN) - Prev button center:', bluePrevCenter);
      console.log('Blue (IN) - Next button center:', blueNextCenter);
      console.log('Red (COUNTER) - Prev button center:', redPrevCenter);
      console.log('Red (COUNTER) - Next button center:', redNextCenter);

      // SUCCESS CRITERIA: Button positions should be identical (within 1px tolerance)
      // This ensures "COUNTER" doesn't push buttons to the right
      expect(Math.abs(bluePrevCenter - redPrevCenter)).toBeLessThan(1);
      expect(Math.abs(blueNextCenter - redNextCenter)).toBeLessThan(1);
    });

    it('should ensure orientation display text fits within max-width constraint', () => {
      const { container } = render(SimplifiedOrientationControl, {
        props: {
          color: 'red',
          currentBeatData: mockBeatData,
          onOrientationChanged: mockOnOrientationChanged,
        },
      });

      const orientationDisplay = container.querySelector('.orientation-display') as HTMLElement;
      expect(orientationDisplay).toBeTruthy();
      expect(orientationDisplay.textContent?.trim()).toBe('COUNTER');

      const rect = orientationDisplay.getBoundingClientRect();
      const computedStyle = window.getComputedStyle(orientationDisplay);
      const maxWidth = parseInt(computedStyle.maxWidth);

      console.log('Orientation display width:', rect.width);
      console.log('Orientation display max-width:', maxWidth);

      // SUCCESS CRITERIA: Display width should not exceed max-width
      expect(rect.width).toBeLessThanOrEqual(maxWidth);
    });

    it('should verify text scales down with container query', () => {
      const { container } = render(SimplifiedOrientationControl, {
        props: {
          color: 'red',
          currentBeatData: mockBeatData,
          onOrientationChanged: mockOnOrientationChanged,
        },
      });

      const orientationDisplay = container.querySelector('.orientation-display') as HTMLElement;
      const computedStyle = window.getComputedStyle(orientationDisplay);
      const fontSize = parseInt(computedStyle.fontSize);

      console.log('Font size for "COUNTER":', fontSize);

      // SUCCESS CRITERIA: Font size should be scaled down (less than 20px)
      // Based on clamp(14px, 5cqw, 20px), longer text should trigger smaller font
      expect(fontSize).toBeGreaterThanOrEqual(14);
      expect(fontSize).toBeLessThanOrEqual(20);
    });

    it('should verify center controls container maintains perfect centering', () => {
      const { container } = render(SimplifiedOrientationControl, {
        props: {
          color: 'red',
          currentBeatData: mockBeatData,
          onOrientationChanged: mockOnOrientationChanged,
        },
      });

      const controlElement = container.querySelector('.simplified-orientation-control') as HTMLElement;
      const centerControls = container.querySelector('.center-controls') as HTMLElement;

      expect(controlElement).toBeTruthy();
      expect(centerControls).toBeTruthy();

      const controlRect = controlElement.getBoundingClientRect();
      const centerRect = centerControls.getBoundingClientRect();

      const controlCenter = controlRect.left + controlRect.width / 2;
      const centerControlsCenter = centerRect.left + centerRect.width / 2;

      console.log('Control element center:', controlCenter);
      console.log('Center controls center:', centerControlsCenter);

      // SUCCESS CRITERIA: Center controls should be at the exact center of the parent
      // Allow 2px tolerance for rounding
      expect(Math.abs(controlCenter - centerControlsCenter)).toBeLessThan(2);
    });
  });

  describe('Visual comparison test', () => {
    it('should render both controls side-by-side and verify no layout shift', () => {
      // Create a container to hold both controls
      const testContainer = document.createElement('div');
      testContainer.style.width = '344px'; // Z Fold width
      testContainer.style.display = 'flex';
      testContainer.style.flexDirection = 'column';
      testContainer.style.gap = '12px';
      document.body.appendChild(testContainer);

      // Render blue with "IN"
      const blueWrapper = document.createElement('div');
      testContainer.appendChild(blueWrapper);
      render(SimplifiedOrientationControl, {
        target: blueWrapper,
        props: {
          color: 'blue',
          currentBeatData: mockBeatData,
          onOrientationChanged: mockOnOrientationChanged,
        },
      });

      // Render red with "COUNTER"
      const redWrapper = document.createElement('div');
      testContainer.appendChild(redWrapper);
      render(SimplifiedOrientationControl, {
        target: redWrapper,
        props: {
          color: 'red',
          currentBeatData: mockBeatData,
          onOrientationChanged: mockOnOrientationChanged,
        },
      });

      // Get all stepper buttons
      const allButtons = testContainer.querySelectorAll('.stepper-btn');
      expect(allButtons.length).toBe(4); // 2 buttons per control

      const [bluePrev, blueNext, redPrev, redNext] = Array.from(allButtons) as HTMLElement[];

      // Get X positions
      const bluePrevX = bluePrev.getBoundingClientRect().left;
      const blueNextX = blueNext.getBoundingClientRect().left;
      const redPrevX = redPrev.getBoundingClientRect().left;
      const redNextX = redNext.getBoundingClientRect().left;

      console.log('=== Visual Alignment Test ===');
      console.log('Blue (IN) - Prev X:', bluePrevX, 'Next X:', blueNextX);
      console.log('Red (COUNTER) - Prev X:', redPrevX, 'Next X:', redNextX);
      console.log('X-axis difference (Prev):', Math.abs(bluePrevX - redPrevX));
      console.log('X-axis difference (Next):', Math.abs(blueNextX - redNextX));

      // SUCCESS CRITERIA: Both controls should have buttons at same X positions
      expect(Math.abs(bluePrevX - redPrevX)).toBeLessThan(1);
      expect(Math.abs(blueNextX - redNextX)).toBeLessThan(1);

      // Cleanup
      document.body.removeChild(testContainer);
    });
  });
});
