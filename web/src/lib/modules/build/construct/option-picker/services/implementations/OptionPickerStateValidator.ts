/**
 * Option Picker State Validation Service
 *
 * Centralized validation logic for state transitions and business rules.
 */

import { injectable } from 'inversify';
import type { PictographData } from '$shared';
import { OptionPickerErrors } from '../../domain/errors/OptionPickerError';

export interface IOptionPickerStateValidator {
  /**
   * Validate sequence change parameters
   */
  validateSequenceChange(
    sequence: PictographData[], 
    containerWidth: number, 
    containerHeight: number
  ): { isValid: boolean; error?: string };

  /**
   * Validate option selection
   */
  validateOptionSelection(
    option: PictographData, 
    availableOptions: PictographData[]
  ): { isValid: boolean; error?: string };

  /**
   * Validate container dimensions
   */
  validateContainerDimensions(
    width: number, 
    height: number
  ): { isValid: boolean; error?: string };

  /**
   * Validate sequence for option loading
   */
  validateSequenceForOptions(
    sequence: PictographData[]
  ): { isValid: boolean; error?: string };
}

@injectable()
export class OptionPickerStateValidator implements IOptionPickerStateValidator {

  validateSequenceChange(
    sequence: PictographData[], 
    containerWidth: number, 
    containerHeight: number
  ): { isValid: boolean; error?: string } {
    
    // Check sequence validity
    const sequenceValidation = this.validateSequenceForOptions(sequence);
    if (!sequenceValidation.isValid) {
      return sequenceValidation;
    }

    // Check container dimensions
    const dimensionsValidation = this.validateContainerDimensions(containerWidth, containerHeight);
    if (!dimensionsValidation.isValid) {
      return dimensionsValidation;
    }

    return { isValid: true };
  }

  validateOptionSelection(
    option: PictographData, 
    availableOptions: PictographData[]
  ): { isValid: boolean; error?: string } {
    
    if (!option) {
      return { 
        isValid: false, 
        error: 'Option cannot be null or undefined' 
      };
    }

    if (!option.letter) {
      return { 
        isValid: false, 
        error: 'Option must have a valid letter identifier' 
      };
    }

    if (!availableOptions.includes(option)) {
      return { 
        isValid: false, 
        error: 'Selected option is not in the available options list' 
      };
    }

    return { isValid: true };
  }

  validateContainerDimensions(
    width: number, 
    height: number
  ): { isValid: boolean; error?: string } {
    
    if (width <= 0) {
      return { 
        isValid: false, 
        error: 'Container width must be greater than 0' 
      };
    }

    if (height <= 0) {
      return { 
        isValid: false, 
        error: 'Container height must be greater than 0' 
      };
    }

    if (width < 200) {
      return { 
        isValid: false, 
        error: 'Container width is too small (minimum: 200px)' 
      };
    }

    if (height < 100) {
      return { 
        isValid: false, 
        error: 'Container height is too small (minimum: 100px)' 
      };
    }

    return { isValid: true };
  }

  validateSequenceForOptions(
    sequence: PictographData[]
  ): { isValid: boolean; error?: string } {
    
    if (!Array.isArray(sequence)) {
      return { 
        isValid: false, 
        error: 'Sequence must be an array' 
      };
    }

    if (sequence.length === 0) {
      return { 
        isValid: false, 
        error: 'Sequence cannot be empty' 
      };
    }

    // Validate that the last beat has proper end position data
    const lastBeat = sequence[sequence.length - 1];
    if (!lastBeat) {
      return { 
        isValid: false, 
        error: 'Last beat in sequence is invalid' 
      };
    }

    if (!lastBeat.motions?.blue || !lastBeat.motions?.red) {
      return { 
        isValid: false, 
        error: 'Last beat must have complete motion data for both hands' 
      };
    }

    if (!lastBeat.motions.blue.endLocation || !lastBeat.motions.red.endLocation) {
      return { 
        isValid: false, 
        error: 'Last beat must have end location data for both hands' 
      };
    }

    return { isValid: true };
  }
}
