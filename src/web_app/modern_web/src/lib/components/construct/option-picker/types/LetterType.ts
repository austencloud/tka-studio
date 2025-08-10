/**
 * LetterType - Exact copy of desktop version
 *
 * Defines the 6 letter types and their groupings exactly as in the desktop app
 */

export class LetterType {
	static readonly TYPE1 = 'Type1';
	static readonly TYPE2 = 'Type2';
	static readonly TYPE3 = 'Type3';
	static readonly TYPE4 = 'Type4';
	static readonly TYPE5 = 'Type5';
	static readonly TYPE6 = 'Type6';

	static readonly ALL_TYPES = [
		LetterType.TYPE1,
		LetterType.TYPE2,
		LetterType.TYPE3,
		LetterType.TYPE4,
		LetterType.TYPE5,
		LetterType.TYPE6,
	];

	/**
	 * Get letter type from pictograph letter - exact copy from desktop
	 */
	static getLetterType(letter: string): string {
		const type1Letters = [
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
			'V',
		];
		const type2Letters = ['W', 'X', 'Y', 'Z', 'Σ', 'Δ', 'θ', 'Ω'];
		const type3Letters = ['W-', 'X-', 'Y-', 'Z-', 'Σ-', 'Δ-', 'θ-', 'Ω-'];
		const type4Letters = ['Φ', 'Ψ', 'Λ'];
		const type5Letters = ['Φ-', 'Ψ-', 'Λ-'];
		const type6Letters = ['α', 'β', 'Γ'];

		if (type1Letters.includes(letter)) return LetterType.TYPE1;
		if (type2Letters.includes(letter)) return LetterType.TYPE2;
		if (type3Letters.includes(letter)) return LetterType.TYPE3;
		if (type4Letters.includes(letter)) return LetterType.TYPE4;
		if (type5Letters.includes(letter)) return LetterType.TYPE5;
		if (type6Letters.includes(letter)) return LetterType.TYPE6;

		return LetterType.TYPE1; // Default fallback
	}

	/**
	 * Get type description and name - exact copy from desktop
	 */
	static getTypeDescription(letterType: string): { description: string; typeName: string } {
		const descriptions = {
			[LetterType.TYPE1]: { description: 'Dual-Shift', typeName: 'Type1' },
			[LetterType.TYPE2]: { description: 'Shift', typeName: 'Type2' },
			[LetterType.TYPE3]: { description: 'Cross-Shift', typeName: 'Type3' },
			[LetterType.TYPE4]: { description: 'Dash', typeName: 'Type4' },
			[LetterType.TYPE5]: { description: 'Dual-Dash', typeName: 'Type5' },
			[LetterType.TYPE6]: { description: 'Static', typeName: 'Type6' },
		};

		return (
			descriptions[letterType as keyof typeof descriptions] || {
				description: 'Unknown',
				typeName: 'Type ?',
			}
		);
	}

	/**
	 * Check if letter type is groupable (Types 4, 5, 6 are displayed horizontally)
	 */
	static isGroupableType(letterType: string): boolean {
		return [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6].includes(letterType);
	}

	/**
	 * Get colored HTML text for letter type descriptions - matches desktop styling
	 */
	static getColoredText(description: string): string {
		const colors = {
			Shift: '#6F2DA8',
			Dual: '#00b3ff',
			Dash: '#26e600',
			Cross: '#26e600',
			Static: '#eb7d00',
			'-': '#000000',
		};

		let coloredText = description;

		// Apply colors to each word
		Object.entries(colors).forEach(([word, color]) => {
			const regex = new RegExp(`\\b${word}\\b`, 'gi');
			coloredText = coloredText.replace(
				regex,
				`<span style="color: ${color};">${word}</span>`
			);
		});

		return coloredText;
	}

	/**
	 * Get legacy double border colors for each type (for buttons)
	 */
	static getLegacyColorPairs(letterType: string): { primary: string; secondary: string } {
		const colorPairs = {
			[LetterType.TYPE1]: { primary: '#36c3ff', secondary: '#6F2DA8' }, // Light blue + Purple
			[LetterType.TYPE2]: { primary: '#6F2DA8', secondary: '#6F2DA8' }, // Purple + Purple
			[LetterType.TYPE3]: { primary: '#26e600', secondary: '#6F2DA8' }, // Green + Purple
			[LetterType.TYPE4]: { primary: '#26e600', secondary: '#26e600' }, // Green + Green
			[LetterType.TYPE5]: { primary: '#00b3ff', secondary: '#26e600' }, // Blue + Green
			[LetterType.TYPE6]: { primary: '#eb7d00', secondary: '#eb7d00' }, // Orange + Orange
		};

		return (
			colorPairs[letterType as keyof typeof colorPairs] || {
				primary: '#666666',
				secondary: '#666666',
			}
		);
	}
}
