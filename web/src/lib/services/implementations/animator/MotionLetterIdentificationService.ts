/**
 * Motion Letter Identification Service
 *
 * Reverse-lookup TKA letters from motion parameters.
 * Takes current animator parameters and identifies the corresponding TKA letter.
 */

import type { LetterMapping } from "$domain";
import { GridMode } from "$domain";
import { injectable } from "inversify";
import type { MotionTestParams } from "./MotionParameterService";

export interface LetterIdentificationResult {
  letter: string | null;
  confidence: "exact" | "partial" | "none";
  matchedParameters: string[];
  missingParameters: string[];
}

export interface IMotionLetterIdentificationService {
  identifyLetter(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ): LetterIdentificationResult;
  getAvailableLetters(): string[];
}

@injectable()
export class MotionLetterIdentificationService
  implements IMotionLetterIdentificationService
{
  private letterMappings: Record<string, LetterMapping> = {};
  private isInitialized = false;

  constructor() {
    this.initializeLetterMappings();
  }

  /**
   * Initialize letter mappings from the configuration
   */
  private async initializeLetterMappings() {
    try {
      // Load letter mappings from the configuration file
      const response = await fetch("/config/codex/letter-mappings.json");
      if (!response.ok) {
        throw new Error(
          `Failed to load letter mappings: ${response.statusText}`
        );
      }

      const config = await response.json();
      this.letterMappings = config.letters || {};
      this.isInitialized = true;

      console.log(
        "✅ MotionLetterIdentificationService: Letter mappings loaded",
        {
          letterCount: Object.keys(this.letterMappings).length,
          availableLetters: Object.keys(this.letterMappings).slice(0, 10), // Show first 10
        }
      );
    } catch (error) {
      console.error(
        "❌ MotionLetterIdentificationService: Failed to load letter mappings:",
        error
      );
      this.letterMappings = {};
      this.isInitialized = true; // Set to true to prevent infinite loading
    }
  }

  /**
   * Identify the TKA letter that matches the current motion parameters
   */
  identifyLetter(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ): LetterIdentificationResult {
    if (!this.isInitialized) {
      return {
        letter: null,
        confidence: "none",
        matchedParameters: [],
        missingParameters: ["Service not initialized"],
      };
    }

    console.log("🔍 [LETTER ID] Identifying letter for motion parameters:", {
      blue: blueParams,
      red: redParams,
      gridMode,
    });

    // Convert motion parameters to the format used in letter mappings
    const motionSignature = this.createMotionSignature(
      blueParams,
      redParams,
      gridMode
    );

    console.log("🔍 [LETTER ID] Created motion signature:", motionSignature);

    // Find matching letter
    let bestMatch: LetterIdentificationResult = {
      letter: null,
      confidence: "none",
      matchedParameters: [],
      missingParameters: [],
    };

    for (const [letter, mapping] of Object.entries(this.letterMappings)) {
      const matchResult = this.compareMotionSignature(
        motionSignature,
        mapping,
        letter
      );

      if (matchResult.confidence === "exact") {
        console.log(`✅ [LETTER ID] Exact match found: ${letter}`);
        return matchResult;
      }

      if (
        matchResult.confidence === "partial" &&
        bestMatch.confidence !== "exact"
      ) {
        if (
          bestMatch.confidence === "none" ||
          matchResult.matchedParameters.length >
            bestMatch.matchedParameters.length
        ) {
          bestMatch = matchResult;
        }
      }
    }

    if (bestMatch.letter) {
      console.log(
        `🔍 [LETTER ID] Best partial match: ${bestMatch.letter} (${bestMatch.matchedParameters.length} matches)`
      );
    } else {
      console.log("❌ [LETTER ID] No matching letter found");
    }

    return bestMatch;
  }

  /**
   * Create a motion signature from motion parameters
   */
  private createMotionSignature(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ) {
    // Determine start and end positions based on motion parameters
    const startPosition = this.determineStartPosition(
      blueParams,
      redParams,
      gridMode
    );
    const endPosition = this.determineEndPosition(
      blueParams,
      redParams,
      gridMode
    );

    return {
      startPosition,
      endPosition,
      blueMotion: this.normalizeMotionType(blueParams.motionType),
      redMotion: this.normalizeMotionType(redParams.motionType),
      blueStartLocation: blueParams.startLocation.toLowerCase(),
      blueEndLocation: blueParams.endLocation.toLowerCase(),
      redStartLocation: redParams.startLocation.toLowerCase(),
      redEndLocation: redParams.endLocation.toLowerCase(),
      blueStartOrientation: blueParams.startOrientation.toLowerCase(),
      blueEndOrientation: blueParams.endOrientation.toLowerCase(),
      redStartOrientation: redParams.startOrientation.toLowerCase(),
      redEndOrientation: redParams.endOrientation.toLowerCase(),
    };
  }

  /**
   * Determine start position based on motion parameters
   */
  private determineStartPosition(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    _gridMode: GridMode
  ): string {
    // This is a simplified position determination
    // In a full implementation, this would use the same logic as the pictograph generation
    const blueStart = blueParams.startLocation.toLowerCase();
    const redStart = redParams.startLocation.toLowerCase();

    // Map location combinations to positions
    const locationToPosition: Record<string, string> = {
      "s,n": "alpha1",
      "sw,ne": "alpha2",
      "w,e": "alpha3",
      "nw,se": "alpha4",
      "n,s": "alpha5",
      "ne,sw": "alpha6",
      "e,w": "alpha7",
      "se,nw": "alpha8",
      "n,n": "beta1",
      "ne,ne": "beta2",
      "e,e": "beta3",
      "se,se": "beta4",
      "s,s": "beta5",
      "sw,sw": "beta6",
      "w,w": "beta7",
      "nw,nw": "beta8",
      "w,n": "gamma1",
      "nw,ne": "gamma2",
      "n,e": "gamma3",
      "ne,se": "gamma4",
      "e,s": "gamma5",
      "se,sw": "gamma6",
      "s,w": "gamma7",
      "sw,nw": "gamma8",
      "e,n": "gamma9",
      "se,ne": "gamma10",
      "s,e": "gamma11",
      "sw,se": "gamma12",
      "w,s": "gamma13",
      "nw,sw": "gamma14",
      "n,w": "gamma15",
      "ne,nw": "gamma16",
    };

    const key = `${blueStart},${redStart}`;
    return locationToPosition[key] || "alpha1"; // Default fallback
  }

  /**
   * Determine end position based on motion parameters
   */
  private determineEndPosition(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    _gridMode: GridMode
  ): string {
    const blueEnd = blueParams.endLocation.toLowerCase();
    const redEnd = redParams.endLocation.toLowerCase();

    // Map location combinations to positions
    const locationToPosition: Record<string, string> = {
      "s,n": "alpha1",
      "sw,ne": "alpha2",
      "w,e": "alpha3",
      "nw,se": "alpha4",
      "n,s": "alpha5",
      "ne,sw": "alpha6",
      "e,w": "alpha7",
      "se,nw": "alpha8",
      "n,n": "beta1",
      "ne,ne": "beta2",
      "e,e": "beta3",
      "se,se": "beta4",
      "s,s": "beta5",
      "sw,sw": "beta6",
      "w,w": "beta7",
      "nw,nw": "beta8",
      "w,n": "gamma1",
      "nw,ne": "gamma2",
      "n,e": "gamma3",
      "ne,se": "gamma4",
      "e,s": "gamma5",
      "se,sw": "gamma6",
      "s,w": "gamma7",
      "sw,nw": "gamma8",
      "e,n": "gamma9",
      "se,ne": "gamma10",
      "s,e": "gamma11",
      "sw,se": "gamma12",
      "w,s": "gamma13",
      "nw,sw": "gamma14",
      "n,w": "gamma15",
      "ne,nw": "gamma16",
    };

    const key = `${blueEnd},${redEnd}`;
    return locationToPosition[key] || "alpha3"; // Default fallback
  }

  /**
   * Normalize motion type to match letter mapping format
   */
  private normalizeMotionType(motionType: string): string {
    const normalized = motionType.toLowerCase();
    // Map motion types to letter mapping format
    const motionMap: Record<string, string> = {
      pro: "pro",
      anti: "anti",
      float: "float",
      dash: "dash",
      static: "static",
    };
    return motionMap[normalized] || normalized;
  }

  /**
   * Compare motion signature with letter mapping
   */
  private compareMotionSignature(
    signature: Record<string, string>,
    mapping: LetterMapping,
    letter: string
  ): LetterIdentificationResult {
    const matchedParameters: string[] = [];
    const missingParameters: string[] = [];

    // Check core parameters
    const coreParams = [
      {
        key: "startPosition",
        signatureKey: "startPosition",
        mappingKey: "startPosition" as keyof LetterMapping,
      },
      {
        key: "endPosition",
        signatureKey: "endPosition",
        mappingKey: "endPosition" as keyof LetterMapping,
      },
      {
        key: "blueMotion",
        signatureKey: "blueMotion",
        mappingKey: "blueMotionType" as keyof LetterMapping,
      },
      {
        key: "redMotion",
        signatureKey: "redMotion",
        mappingKey: "redMotionType" as keyof LetterMapping,
      },
    ];

    for (const param of coreParams) {
      const mappingValue = mapping[param.mappingKey];
      const signatureValue = signature[param.signatureKey];

      if (mappingValue && signatureValue) {
        if (mappingValue.toLowerCase() === signatureValue.toLowerCase()) {
          matchedParameters.push(param.key);
        } else {
          missingParameters.push(
            `${param.key}: expected ${mappingValue}, got ${signatureValue}`
          );
        }
      } else if (mappingValue) {
        missingParameters.push(`${param.key}: missing in signature`);
      }
    }

    // Determine confidence
    let confidence: "exact" | "partial" | "none" = "none";

    if (missingParameters.length === 0 && matchedParameters.length >= 4) {
      confidence = "exact";
    } else if (matchedParameters.length >= 2) {
      confidence = "partial";
    }

    return {
      letter: confidence !== "none" ? letter : null,
      confidence,
      matchedParameters,
      missingParameters,
    };
  }

  /**
   * Get all available letters
   */
  getAvailableLetters(): string[] {
    return Object.keys(this.letterMappings);
  }
}
