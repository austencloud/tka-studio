/**
 * Utility functions for working with BeatFrame elements in the DOM
 */

/**
 * Verifies that BeatFrame elements are fully loaded and ready for rendering
 * @returns boolean indicating if BeatFrame elements are ready
 */
export function verifyBeatFrameElements(): boolean {
  const beatFrameElement = document.querySelector('.beat-frame-container');
  if (!beatFrameElement) {
    console.log('⚠️ BeatFrame element not found during verification');
    return false;
  }

  // Check for SVG elements
  const svgElements = beatFrameElement.querySelectorAll('svg');
  console.log(`🔍 BeatFrame verification: Found ${svgElements.length} SVG elements`);

  // Check for arrows and other critical elements
  const arrowElements = beatFrameElement.querySelectorAll('.arrow-path, .arrow-head');
  const propElements = beatFrameElement.querySelectorAll('.pictograph-prop');

  console.log(`🔍 BeatFrame verification details:`, {
    svgCount: svgElements.length,
    arrowCount: arrowElements.length,
    propCount: propElements.length
  });

  // Consider it valid if we have SVGs and either arrows or props
  return svgElements.length > 0 && (arrowElements.length > 0 || propElements.length > 0);
}

/**
 * Creates a temporary element for rendering the BeatFrame
 * @param width Width of the temporary element
 * @param height Height of the temporary element
 * @returns The created temporary element
 */
export function createTemporaryRenderElement(width: number, height: number): HTMLDivElement {
  const tempElement = document.createElement('div');
  tempElement.style.position = 'absolute';
  tempElement.style.left = '-9999px';
  tempElement.style.width = `${width}px`;
  tempElement.style.height = `${height}px`;
  tempElement.className = 'temp-beat-frame-clone';
  document.body.appendChild(tempElement);
  return tempElement;
}

/**
 * Clones the BeatFrame content into a temporary element for rendering
 * @param tempElement The temporary element to clone into
 * @returns boolean indicating success
 */
export function cloneBeatFrameContent(tempElement: HTMLDivElement): boolean {
  const beatFrameElement = document.querySelector('.beat-frame-container');
  if (!beatFrameElement) {
    console.error('Could not find BeatFrame element in the DOM');
    return false;
  }

  // Clone the BeatFrame content into our temporary element
  tempElement.innerHTML = beatFrameElement.innerHTML;

  // Force a layout calculation to ensure all elements are properly rendered
  tempElement.getBoundingClientRect();

  // Ensure SVG elements are properly cloned and visible
  const clonedSvgs = tempElement.querySelectorAll('svg');
  clonedSvgs.forEach((svg) => {
    // Ensure SVG has proper dimensions
    if (!svg.getAttribute('width') || svg.getAttribute('width') === '0') {
      svg.setAttribute('width', '100%');
    }
    if (!svg.getAttribute('height') || svg.getAttribute('height') === '0') {
      svg.setAttribute('height', '100%');
    }
    // Force visibility
    svg.style.visibility = 'visible';
    svg.style.display = 'block';
  });

  return clonedSvgs.length > 0;
}

/**
 * Logs detailed information about the BeatFrame element
 */
export function logBeatFrameDetails(): void {
  const beatFrameElement = document.querySelector('.beat-frame-container');
  if (!beatFrameElement) {
    console.error('Could not find BeatFrame element in the DOM');
    return;
  }

  // Verify BeatFrame has necessary elements
  const svgElements = beatFrameElement.querySelectorAll('svg');
  const arrowElements = beatFrameElement.querySelectorAll('.arrow-path, .arrow-head');
  const propElements = beatFrameElement.querySelectorAll('.pictograph-prop');

  // Log detailed information about what we found
  console.log('Found BeatFrame element with details:', {
    element: beatFrameElement,
    svgCount: svgElements.length,
    arrowCount: arrowElements.length,
    propCount: propElements.length,
    html: beatFrameElement.innerHTML.substring(0, 200) + '...' // Log a preview of the HTML
  });

  // Warn if we're missing expected elements
  if (svgElements.length === 0 || (arrowElements.length === 0 && propElements.length === 0)) {
    console.warn('⚠️ BeatFrame may be missing critical elements for rendering');
  }
}

/**
 * Removes a temporary element from the DOM
 * @param element The element to remove
 */
export function removeTemporaryElement(element: HTMLDivElement): void {
  if (element && element.parentNode) {
    document.body.removeChild(element);
  }
}
