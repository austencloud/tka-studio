import { Letter } from './Letter';

export class LetterType {
	static Type1 = new LetterType(
		[
			'A',
			'B',
			'C',
			'D',
			'E',
			'F',
			'G',
			'H',
			'I',
			'J',
			'K',
			'L',
			'M',
			'N',
			'O',
			'P',
			'Q',
			'R',
			'S',
			'T',
			'U',
			'V'
		],
		'Dual-Shift',
		'Type1'
	);
	static Type2 = new LetterType(['W', 'X', 'Y', 'Z', 'Σ', 'Δ', 'θ', 'Ω'], 'Shift', 'Type2');
	static Type3 = new LetterType(
		['W-', 'X-', 'Y-', 'Z-', 'Σ-', 'Δ-', 'θ-', 'Ω-'],
		'Cross-Shift',
		'Type3'
	);
	static Type4 = new LetterType(['Φ', 'Ψ', 'Λ'], 'Dash', 'Type4');
	static Type5 = new LetterType(['Φ-', 'Ψ-', 'Λ-'], 'Dual-Dash', 'Type5');
	static Type6 = new LetterType(['α', 'β', 'Γ'], 'Static', 'Type6');
	static Type7 = new LetterType(['ζ', 'η'], 'Skewed', 'Type7');
	static Type8 = new LetterType(['μ', 'ν'], 'TauShift', 'Type8');
	static Type9 = new LetterType(['τ', '⊕'], 'Centric', 'Type9');

	static AllTypes = [
		LetterType.Type1,
		LetterType.Type2,
		LetterType.Type3,
		LetterType.Type4,
		LetterType.Type5,
		LetterType.Type6,
		LetterType.Type7,
		LetterType.Type8,
		LetterType.Type9
	];

	private constructor(
		public letters: string[],
		public description: string,
		public folderName: string
	) {}

	static getLetterType(letter: Letter): LetterType | null {
		const letterStr = letter.toString();
		for (const type of LetterType.AllTypes) {
			if (type.letters.includes(letterStr)) {
				return type;
			}
		}
		return null;
	}
}
