/**
 * Arrow Placement Key Service
 * 
 * Generates placement keys for arrow positioning lookups.
 * Simplified version of the desktop PlacementKeyGenerator logic.
 */

import type { MotionData } from '@tka/schemas';
import type { MotionType, Orientation, PictographData } from '../interfaces';

export interface IArrowPlacementKeyService {
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    availableKeys: string[]
  ): string;
  
  generateBasicKey(motionType: MotionType): string;
}

export class ArrowPlacementKeyService implements IArrowPlacementKeyService {
  
  // Letter condition mappings from desktop
  private readonly dashLetterConditions = {
    TYPE3: ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
    TYPE5: ["Φ-", "Ψ-", "Λ-"]
  };

  /**
   * Generate placement key based on motion data and pictograph context
   */
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    availableKeys: string[]
  ): string {
    const motionType = this.normalizeMotionType(motionData.motionType);
    const letter = pictographData.letter;
    
    console.log(`Generating placement key for ${motionType}, letter: ${letter}`);
    
    // Generate candidate keys in order of preference
    const candidateKeys = this.generateCandidateKeys(motionData, pictographData);
    
    // Select the first available key from candidates
    for (const key of candidateKeys) {
      if (availableKeys.includes(key)) {
        console.log(`Selected placement key: ${key}`);
        return key;
      }
    }
    
    // Fallback to motion type
    const fallback = motionType;
    console.log(`No specific key found, using fallback: ${fallback}`);
    return fallback;
  }

  /**
   * Generate basic key for motion type (fallback)
   */
  generateBasicKey(motionType: MotionType): string {
    return motionType;
  }

  /**
   * Generate candidate keys in order of preference
   */
  private generateCandidateKeys(
    motionData: MotionData,
    pictographData: PictographData
  ): string[] {
    const motionType = this.normalizeMotionType(motionData.motionType);
    const letter = pictographData.letter;
    
    const candidates: string[] = [];
    
    if (letter) {
      // Generate letter-specific keys
      const letterSuffix = this.getLetterSuffix(letter);
      
      // Try different layer combinations with letter
      candidates.push(`${motionType}_to_layer1_alpha${letterSuffix}`);
      candidates.push(`${motionType}_to_layer2_alpha${letterSuffix}`);
      candidates.push(`${motionType}_to_layer1_beta${letterSuffix}`);
      candidates.push(`${motionType}_to_layer2_beta${letterSuffix}`);
      candidates.push(`${motionType}_to_layer1_gamma${letterSuffix}`);
      candidates.push(`${motionType}_to_layer2_gamma${letterSuffix}`);
      
      // Try radial layer3 combinations
      candidates.push(`${motionType}_to_radial_layer3_alpha${letterSuffix}`);
      candidates.push(`${motionType}_to_radial_layer3_beta${letterSuffix}`);
      candidates.push(`${motionType}_to_radial_layer3_gamma${letterSuffix}`);
      
      // Try nonradial layer3 combinations  
      candidates.push(`${motionType}_to_nonradial_layer3_alpha${letterSuffix}`);
      candidates.push(`${motionType}_to_nonradial_layer3_beta${letterSuffix}`);
      candidates.push(`${motionType}_to_nonradial_layer3_gamma${letterSuffix}`);
    }
    
    // Try basic layer combinations without letter
    candidates.push(`${motionType}_to_layer1_alpha`);
    candidates.push(`${motionType}_to_layer2_alpha`);
    candidates.push(`${motionType}_to_layer1_beta`);
    candidates.push(`${motionType}_to_layer2_beta`);
    candidates.push(`${motionType}_to_layer1_gamma`);
    candidates.push(`${motionType}_to_layer2_gamma`);
    
    // Try radial layer3 without letter
    candidates.push(`${motionType}_to_radial_layer3_alpha`);
    candidates.push(`${motionType}_to_radial_layer3_beta`);
    candidates.push(`${motionType}_to_radial_layer3_gamma`);
    
    // Try nonradial layer3 without letter
    candidates.push(`${motionType}_to_nonradial_layer3_alpha`);
    candidates.push(`${motionType}_to_nonradial_layer3_beta`);
    candidates.push(`${motionType}_to_nonradial_layer3_gamma`);
    
    // Finally, just motion type
    candidates.push(motionType);
    
    return candidates;
  }

  /**
   * Get letter suffix for placement key
   */
  private getLetterSuffix(letter: string): string {
    if (!letter) {
      return '';
    }
    
    // Check if letter needs dash handling (TYPE3/TYPE5)
    const allDashLetters = [
      ...this.dashLetterConditions.TYPE3,
      ...this.dashLetterConditions.TYPE5
    ];
    
    if (allDashLetters.includes(letter)) {
      // Remove dash and add "_dash" suffix: "W-" → "_W_dash"
      const baseString = letter.slice(0, -1);
      return `_${baseString}_dash`;
    }
    
    // Regular letter: "A" → "_A"
    return `_${letter}`;
  }

  /**
   * Normalize motion type to standard format
   */
  private normalizeMotionType(motionType: any): MotionType {
    if (typeof motionType === 'string') {
      const normalized = motionType.toLowerCase();
      if (['pro', 'anti', 'float', 'dash', 'static'].includes(normalized)) {
        return normalized as MotionType;
      }
    }
    
    // Handle enum objects
    if (motionType && typeof motionType === 'object' && motionType.value) {
      return this.normalizeMotionType(motionType.value);
    }
    
    console.warn(`Invalid motion type: ${motionType}, defaulting to 'pro'`);
    return 'pro';
  }

  /**
   * Debug method to show all candidate keys
   */
  debugCandidateKeys(
    motionData: MotionData,
    pictographData: PictographData
  ): string[] {
    const candidates = this.generateCandidateKeys(motionData, pictographData);
    console.log('Candidate placement keys:', candidates);
    return candidates;
  }
}
