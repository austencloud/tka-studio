import type { CodexLetterMapping, CodexLetterRow } from "../../domain";

export interface ICodexCodexLetterMappingRepo {
  initialize(): Promise<void>;

  getLetterMapping(letter: string): CodexLetterMapping | null;

  getLetterRows(): CodexLetterRow[];

  getAllLetters(): string[];

  isValidLetter(letter: string): boolean;
}
