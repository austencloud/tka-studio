// src/lib/components/OptionPicker/utils/headerUtils.ts

/**
 * Map of internal type keys (like Type1) to their display descriptions.
 * IMPORTANT: Ensure this map is complete and accurate for all types.
 */
export const letterTypeDescriptions: Record<string, string> = {
	Type1: 'Dual-Shift',
	Type2: 'Shift',
	Type3: 'Cross-Shift',
	Type4: 'Dash',
	Type5: 'Dual-Dash',
	Type6: 'Static',
	'Unknown Type': 'Unknown',
	// Descriptions for other potential sorting groups
	alpha: 'Alpha',
	beta: 'Beta',
	gamma: 'Gamma',
	Continuous: 'Continuous',
	'One Reversal': 'One Reversal',
	'Two Reversals': 'Two Reversals'
};

/**
 * Map of keywords found in descriptions to their desired CSS color.
 */
export const headerTextColors: Record<string, string> = {
	Shift: '#6F2DA8', // Purple
	Dual: '#00b3ff', // Blue
	Dash: '#26e600', // Green
	Cross: '#26e600', // Green
	Static: '#eb7d00', // Orange
	// '-': '#000000', // Default hyphen color (usually black/dark grey)
	Continuous: '#008000', // Green
	One: '#eb7d00', // Orange
	Two: '#ff0000', // Red
	Reversal: '#6F2DA8', // Purple
	Reversals: '#6F2DA8', // Purple
	Alpha: '#000000', // Black
	Beta: '#000000', // Black
	Gamma: '#000000' // Black
};

/**
 * Inner helper to style individual words/parts based on the color map.
 * @param text The word or part to style.
 * @returns An HTML string with a styled span.
 */
function formatStyledPart(text: string): string {
	if (text === '-') return `<span style="font-weight: normal;">-</span>`; // Style hyphen differently
	const color = headerTextColors[text] || 'black'; // Default color
	const fontWeight = 'bold'; // Bold for description parts
	return `<span style="color: ${color}; font-weight: ${fontWeight};">${text}</span>`;
}

/**
 * Formats the header text based on the group key.
 * Produces "Type X - [Styled Description]" for Type keys,
 * or just the styled description for other keys.
 * @param key The group key (e.g., "Type1", "Continuous").
 * @returns An HTML string ready for {@html}.
 */
export function formatStyledHeader(key: string): string {
	const description = letterTypeDescriptions[key] || key; // Get description or use key

	// Check if the key follows the "TypeX" pattern
	const typeMatch = key.match(/^Type(\d)$/);
	if (typeMatch) {
		const typeNumber = typeMatch[1];
		// Style only the description part after splitting
		const styledDescription = description.split(/(-)/).map(formatStyledPart).join('');
		// Return "Type X - [Styled Description]"
		return `<span style="color: #333; font-weight: normal;">Type ${typeNumber} - </span>${styledDescription}`;
	} else {
		// For other keys (like 'alpha', 'Continuous'), style the whole description
		return description.split(/(-)/).map(formatStyledPart).join('');
	}
}
