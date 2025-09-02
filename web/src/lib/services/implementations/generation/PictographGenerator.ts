/**
 * Movement Generator Service - Orchestrator (Refactored)
 *
 * Now acts as a lightweight orchestrator that delegates to specific letter generators.
 * Each letter has its own microservice generator following single responsibility principle.
 *
 * From 582 lines → ~100 lines by extracting letter-specific logic into microservices.
 */

import type {
  ILetterGeneratorFactory,
  IPictographGenerator,
} from "$contracts/generation-interfaces";
import type { PictographData } from "$domain";
import { inject, injectable } from "inversify";
import { TYPES } from "../../inversify/types";
import { LetterGeneratorFactory } from "./letter-generators/LetterGeneratorFactory";

@injectable()
export class PictographGenerator implements IPictographGenerator {
  private readonly letterGeneratorFactory: ILetterGeneratorFactory;

  constructor(
    @inject(TYPES.IPositionPatternService)
    patternService: import("../../contracts/generation-interfaces").IPositionPatternService,
    @inject(TYPES.IDirectionCalculator)
    positionCalculator: import("../../contracts/generation-interfaces").IDirectionCalculator,
    @inject(TYPES.IPictographValidatorService)
    validator: import("../../contracts/generation-interfaces").IPictographValidatorService
  ) {
    this.letterGeneratorFactory = new LetterGeneratorFactory(
      patternService,
      positionCalculator,
      validator
    );
  }

  // ===== ORCHESTRATION METHODS =====

  /**
   * Get movement set for any supported letter
   */
  getPictographDataByLetter(letter: string): PictographData | undefined {
    const generator = this.letterGeneratorFactory.createGenerator(letter);
    return generator?.generate();
  }

  /**
   * Get all movement sets for all supported letters
   */
  getAllPictographDatas(): PictographData[] {
    const supportedLetters = this.letterGeneratorFactory.getSupportedLetters();
    const PictographDatas: PictographData[] = [];

    for (const letter of supportedLetters) {
      const generator = this.letterGeneratorFactory.createGenerator(letter);
      if (generator) {
        PictographDatas.push(generator.generate());
      }
    }

    return PictographDatas;
  }

  /**
   * Get list of all supported letters
   */
  getSupportedLetters(): string[] {
    return this.letterGeneratorFactory.getSupportedLetters();
  }

  // ===== INDIVIDUAL LETTER METHODS (Legacy API Compatibility) =====
  // These delegate to the appropriate letter generators

  generateA(): PictographData[] {
    return [this.requireGenerator("A").generate()];
  }

  generateB(): PictographData[] {
    return [this.requireGenerator("B").generate()];
  }

  generateC(): PictographData[] {
    return [this.requireGenerator("C").generate()];
  }

  // TODO: Add remaining letters as generators are implemented
  generateD(): PictographData[] {
    return [this.generateBasicPattern("D")];
  }

  generateE(): PictographData[] {
    return [this.generateBasicPattern("E")];
  }

  generateF(): PictographData[] {
    return [this.generateBasicPattern("F")];
  }

  generateG(): PictographData[] {
    return [this.generateBasicPattern("G")];
  }

  generateH(): PictographData[] {
    return [this.generateBasicPattern("H")];
  }

  generateI(): PictographData[] {
    return [this.generateBasicPattern("I")];
  }

  generateJ(): PictographData[] {
    return [this.generateBasicPattern("J")];
  }

  generateK(): PictographData[] {
    return [this.generateBasicPattern("K")];
  }

  generateL(): PictographData[] {
    return [this.generateBasicPattern("L")];
  }

  generateM(): PictographData[] {
    return [this.generateBasicPattern("M")];
  }

  generateN(): PictographData[] {
    return [this.generateBasicPattern("N")];
  }

  generateO(): PictographData[] {
    return [this.generateBasicPattern("O")];
  }

  generateP(): PictographData[] {
    return [this.generateBasicPattern("P")];
  }

  generateQ(): PictographData[] {
    return [this.generateBasicPattern("Q")];
  }

  generateR(): PictographData[] {
    return [this.generateBasicPattern("R")];
  }

  generateS(): PictographData[] {
    return [this.generateBasicPattern("S")];
  }

  generateT(): PictographData[] {
    return [this.generateBasicPattern("T")];
  }

  generateU(): PictographData[] {
    return [this.generateBasicPattern("U")];
  }

  generateV(): PictographData[] {
    return [this.generateBasicPattern("V")];
  }

  generateW(): PictographData[] {
    return [this.generateBasicPattern("W")];
  }

  generateX(): PictographData[] {
    return [this.generateBasicPattern("X")];
  }

  generateY(): PictographData[] {
    return [this.generateBasicPattern("Y")];
  }

  generateZ(): PictographData[] {
    return [this.generateBasicPattern("Z")];
  }

  // Greek letters (TODO: implement specific generators)
  generateSigma(): PictographData[] {
    return [this.generateBasicPattern("Σ")];
  }

  generateDelta(): PictographData[] {
    return [this.generateBasicPattern("Δ")];
  }

  generateTheta(): PictographData[] {
    return [this.generateBasicPattern("θ")];
  }

  generateOmega(): PictographData[] {
    return [this.generateBasicPattern("Ω")];
  }

  generatePhi(): PictographData[] {
    return [this.generateBasicPattern("Φ")];
  }

  generatePsi(): PictographData[] {
    return [this.generateBasicPattern("Ψ")];
  }

  generateLambda(): PictographData[] {
    return [this.generateBasicPattern("Λ")];
  }

  generateAlpha(): PictographData[] {
    return [this.generateBasicPattern("α")];
  }

  generateBeta(): PictographData[] {
    return [this.generateBasicPattern("β")];
  }

  generateGamma(): PictographData[] {
    return [this.generateBasicPattern("Γ")];
  }

  // Dash variants (TODO: implement specific generators)
  generateWDash(): PictographData[] {
    return [this.generateBasicPattern("W-")];
  }

  generateXDash(): PictographData[] {
    return [this.generateBasicPattern("X-")];
  }

  generateYDash(): PictographData[] {
    return [this.generateBasicPattern("Y-")];
  }

  generateZDash(): PictographData[] {
    return [this.generateBasicPattern("Z-")];
  }

  generateSigmaDash(): PictographData[] {
    return [this.generateBasicPattern("Σ-")];
  }

  generateDeltaDash(): PictographData[] {
    return [this.generateBasicPattern("Δ-")];
  }

  generateThetaDash(): PictographData[] {
    return [this.generateBasicPattern("θ-")];
  }

  generateOmegaDash(): PictographData[] {
    return [this.generateBasicPattern("Ω-")];
  }

  generatePhiDash(): PictographData[] {
    return [this.generateBasicPattern("Φ-")];
  }

  generatePsiDash(): PictographData[] {
    return [this.generateBasicPattern("Ψ-")];
  }

  generateLambdaDash(): PictographData[] {
    return [this.generateBasicPattern("Λ-")];
  }

  // ===== PRIVATE HELPER METHODS =====

  private requireGenerator(letter: string) {
    const generator = this.letterGeneratorFactory.createGenerator(letter);
    if (!generator) {
      throw new Error(`No generator available for letter: ${letter}`);
    }
    return generator;
  }

  private generateBasicPattern(letter: string): PictographData {
    // Fallback for letters that don't have specific generators yet
    const generator = this.letterGeneratorFactory.createGenerator(letter);
    if (generator) {
      return generator.generate();
    }

    // This would implement a basic default pattern
    // For now, throw an error to indicate the generator needs to be implemented
    throw new Error(`Generator for letter ${letter} not yet implemented`);
  }

  // Utility methods required by interface
  getAllPictographs(): PictographData[] {
    const allPictographs: PictographData[] = [];

    // Add all generated pictographs
    allPictographs.push(...this.generateA());
    allPictographs.push(...this.generateB());
    allPictographs.push(...this.generateC());
    // Add more as needed...

    return allPictographs;
  }

  getPictographsByLetter(letter: string): PictographData[] | undefined {
    try {
      switch (letter.toUpperCase()) {
        case "A":
          return this.generateA();
        case "B":
          return this.generateB();
        case "C":
          return this.generateC();
        case "D":
          return this.generateD();
        case "E":
          return this.generateE();
        // Add more cases as needed...
        default:
          console.warn(
            `PictographGenerator: No generator for letter ${letter}`
          );
          return undefined;
      }
    } catch (error) {
      console.error(
        `Failed to generate pictographs for letter ${letter}:`,
        error
      );
      return undefined;
    }
  }
}
