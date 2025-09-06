import { getLetterType, Letter } from "../domain/enums/Letter";

/**
 * Get the full image path for a letter based on its type
 * URL-encodes the filename to match browser fetch behavior
 */
export function getLetterImagePath(letter: Letter): string {
  const letterType = getLetterType(letter);
  const filename = letter;
  // URL-encode the filename to match what the browser will actually request
  const encodedFilename = encodeURIComponent(filename);
  return `/images/letters_trimmed/${letterType}/${encodedFilename}.svg`;
}
