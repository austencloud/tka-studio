/**
 * Element Finder
 *
 * This module provides functions for finding the BeatFrame element in the DOM.
 * It uses multiple strategies to ensure the element can be found reliably.
 */

import type { ElementContext } from '../../context/ElementContext';
import { logger } from '$lib/core/logging';

/**
 * Find the BeatFrame element in the DOM using multiple strategies
 *
 * @param beatFrameContext Optional context that may contain the element
 * @returns The found element or null if not found
 */
export function findBeatFrameElement(
  beatFrameContext?: ElementContext | null
): HTMLElement | null {
  logger.debug('ElementFinder: Actively searching for BeatFrame element in DOM');

  // First try from context (most reliable)
  if (beatFrameContext) {
    const contextElement = beatFrameContext.getElement();
    if (contextElement) {
      logger.debug('ElementFinder: Found element from context');
      return contextElement;
    }
  }

  // Try to find the element by class or ID
  const byClass = document.querySelector('.beat-frame') as HTMLElement | null;
  if (byClass) {
    logger.debug('ElementFinder: Found element by class .beat-frame');
    return byClass;
  }

  // Try by specific container selectors
  const byContainer = document.querySelector(
    '.sequence-container .beat-frame-container'
  ) as HTMLElement | null;
  if (byContainer) {
    logger.debug('ElementFinder: Found element by container selector');
    return byContainer;
  }

  // Try to find element with SVGs inside (more generic approach)
  const svgContainers = Array.from(document.querySelectorAll('.sequence-widget svg')).map((svg) =>
    svg.closest('.sequence-widget > div')
  );
  if (svgContainers.length > 0 && svgContainers[0] instanceof HTMLElement) {
    logger.debug('ElementFinder: Found container with SVGs');
    return svgContainers[0] as HTMLElement;
  }

  // Try more aggressive selectors as a last resort
  const alternativeElement =
    document.querySelector('.sequence-widget') ||
    document.querySelector('.sequence-container') ||
    document.querySelector('.sequence');

  if (alternativeElement instanceof HTMLElement) {
    logger.debug('ElementFinder: Found alternative element:', alternativeElement);
    return alternativeElement;
  }

  logger.debug('ElementFinder: Could not find BeatFrame element in DOM');
  return null;
}

/**
 * Set up an event listener for the beatframe-element-available event
 *
 * @param callback Function to call when the element is available
 * @returns Cleanup function to remove the event listener
 */
export function listenForBeatFrameElement(
  callback: (element: HTMLElement) => void
): () => void {
  const handleElementAvailable = (event: CustomEvent) => {
    if (event.detail?.element) {
      logger.debug('ElementFinder: Got element from event');
      callback(event.detail.element);
    }
  };

  document.addEventListener(
    'beatframe-element-available',
    handleElementAvailable as EventListener
  );

  return () => {
    document.removeEventListener(
      'beatframe-element-available',
      handleElementAvailable as EventListener
    );
  };
}
