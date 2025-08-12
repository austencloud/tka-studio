/**
 * Utility functions for handling pictograph data
 */
import type { PictographData } from '$lib/types/PictographData';

/**
 * Creates a safe copy of pictograph data that can be serialized to JSON
 * This prevents issues with circular references and non-serializable objects
 * 
 * @param data The pictograph data to copy
 * @returns A safe copy of the pictograph data
 */
export function createSafePictographCopy(data: PictographData | null): PictographData | null {
  if (!data) return null;
  
  try {
    // Create a shallow copy first
    const safeCopy: PictographData = { ...data };
    
    // Handle motion objects which might contain circular references
    safeCopy.redMotion = null;
    safeCopy.blueMotion = null;
    safeCopy.motions = [];
    
    // Handle SVG data in arrow data
    if (safeCopy.redArrowData?.svgData) {
      // Create a safe copy without DOM elements
      const originalSvgData = safeCopy.redArrowData.svgData;
      safeCopy.redArrowData = {
        ...safeCopy.redArrowData,
        svgData: { ...originalSvgData }
      };
      
      // Remove DOM elements and non-serializable properties
      if ((safeCopy.redArrowData.svgData as any).element) {
        (safeCopy.redArrowData.svgData as any).element = null;
      }
      if ((safeCopy.redArrowData.svgData as any).paths) {
        (safeCopy.redArrowData.svgData as any).paths = null;
      }
    }
    
    if (safeCopy.blueArrowData?.svgData) {
      // Create a safe copy without DOM elements
      const originalSvgData = safeCopy.blueArrowData.svgData;
      safeCopy.blueArrowData = {
        ...safeCopy.blueArrowData,
        svgData: { ...originalSvgData }
      };
      
      // Remove DOM elements and non-serializable properties
      if ((safeCopy.blueArrowData.svgData as any).element) {
        (safeCopy.blueArrowData.svgData as any).element = null;
      }
      if ((safeCopy.blueArrowData.svgData as any).paths) {
        (safeCopy.blueArrowData.svgData as any).paths = null;
      }
    }
    
    // Handle grid data which might contain non-serializable objects
    if (safeCopy.gridData) {
      // Create a safe copy of grid data
      safeCopy.gridData = { ...safeCopy.gridData };
      
      // Remove any potential circular references or DOM elements
      if ((safeCopy.gridData as any).element) {
        (safeCopy.gridData as any).element = null;
      }
    }
    
    // Handle prop data which might contain non-serializable objects
    if (safeCopy.redPropData) {
      safeCopy.redPropData = { ...safeCopy.redPropData };
      if ((safeCopy.redPropData as any).element) {
        (safeCopy.redPropData as any).element = null;
      }
    }
    
    if (safeCopy.bluePropData) {
      safeCopy.bluePropData = { ...safeCopy.bluePropData };
      if ((safeCopy.bluePropData as any).element) {
        (safeCopy.bluePropData as any).element = null;
      }
    }
    
    return safeCopy;
  } catch (error) {
    console.error('Error creating safe pictograph copy:', error);
    return null;
  }
}

/**
 * Creates a safe copy of a beat with pictograph data that can be serialized to JSON
 * 
 * @param beat The beat data to copy
 * @returns A safe copy of the beat data
 */
export function createSafeBeatCopy(beat: any): any {
  if (!beat) return null;
  
  try {
    // Create a shallow copy first
    const safeCopy = { ...beat };
    
    // Handle pictograph data
    if (safeCopy.pictographData) {
      safeCopy.pictographData = createSafePictographCopy(safeCopy.pictographData);
    }
    
    return safeCopy;
  } catch (error) {
    console.error('Error creating safe beat copy:', error);
    return null;
  }
}
