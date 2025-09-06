/**
 * Letter Generator Factory
 *
 * Creates appropriate letter generators for each letter.
 * Handles registration and instantiation of all letter generators.
 */


import { Type1Generator } from "./Type1/Type1Generator";
import type { BaseLetterGenerator } from "./BaseLetterGenerator";
import type { IPositionPatternService, IDirectionCalculator, IPictographValidatorService, ILetterGeneratorFactory, ILetterGenerator } from "../../contracts/generate-contracts";

type LetterGeneratorConstructor = new (
  letter: string,
  patternService: IPositionPatternService,
  positionCalculator: IDirectionCalculator,
  validator: IPictographValidatorService
) => BaseLetterGenerator;

export class LetterGeneratorFactory implements ILetterGeneratorFactory {
  private readonly generatorClasses = new Map<
    string,
    LetterGeneratorConstructor
  >();

  constructor(
    private readonly patternService: IPositionPatternService,
    private readonly positionCalculator: IDirectionCalculator,
    private readonly validator: IPictographValidatorService
  ) {
    this.registerGenerators();
  }

  createGenerator(letter: string): ILetterGenerator | null {
    const GeneratorClass = this.generatorClasses.get(letter.toUpperCase());
    if (!GeneratorClass) {
      return null;
    }

    return new GeneratorClass(
      letter.toUpperCase(),
      this.patternService,
      this.positionCalculator,
      this.validator
    );
  }

  getSupportedLetters(): string[] {
    return Array.from(this.generatorClasses.keys()).sort();
  }

  private registerGenerators(): void {
    // Register all Type 1 letters (A-V) with the unified Type1Generator
    const type1Letters = Type1Generator.getSupportedLetters();
    for (const letter of type1Letters) {
      this.generatorClasses.set(letter, Type1Generator);
    }

    // TODO: Add Type 2 generators
    // Type 2 - Gamma to Alpha letters (W, X)
    // Type 2 - Gamma to Beta letters (Y, Z)

    // TODO: Add Greek letters and dash variants
  }
}
