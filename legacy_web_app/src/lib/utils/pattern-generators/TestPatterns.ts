import {
	generateAllPatterns,
	generatePatternsForLetter,
	formatPatternDisplay,
	formatPatternCSV,
	letterGenerators,
	type Pattern
} from './index';

/**
 * Test the pattern generation system by generating and displaying patterns
 * for all implemented letters or a specific subset.
 */
export function testPatternGenerators(
	options: {
		letters?: string[];
		outputFormat?: 'display' | 'csv';
		maxSamplesPerLetter?: number;
		groupByLetter?: boolean;
	} = {}
): string {
	const {
		letters,
		outputFormat = 'display',
		maxSamplesPerLetter = 5, // Set default value to fix the error
		groupByLetter = true
	} = options;

	let patterns: Pattern[];
	const formatter = outputFormat === 'csv' ? formatPatternCSV : formatPatternDisplay;
	let output = '';

	// Generate patterns for all letters or just the specified ones
	if (letters && letters.length > 0) {
		patterns = [];
		letters.forEach((letter) => {
			patterns.push(...generatePatternsForLetter(letter));
		});
	} else {
		patterns = generateAllPatterns();
	}

	// Count total patterns
	output += `Generated ${patterns.length} patterns\n\n`;

	if (groupByLetter) {
		// Group patterns by letter
		const letterGroups: Record<string, any[]> = {};
		patterns.forEach((pattern) => {
			if (!letterGroups[pattern.letter]) {
				letterGroups[pattern.letter] = [];
			}
			letterGroups[pattern.letter].push(pattern);
		});

		// Output patterns by letter with limited samples
		Object.keys(letterGroups).forEach((letter) => {
			const letterPatterns = letterGroups[letter];
			output += `\nLetter ${letter} (${letterPatterns.length} patterns):\n`;

			letterPatterns.slice(0, maxSamplesPerLetter).forEach((pattern, i) => {
				output += `  ${i + 1}. ${formatter(pattern)}\n`;
			});

			if (letterPatterns.length > maxSamplesPerLetter) {
				output += `  ... (${letterPatterns.length - maxSamplesPerLetter} more patterns)\n`;
			}
		});
	} else {
		// Output all patterns with a limit
		const maxTotal = 20;
		patterns.slice(0, maxTotal).forEach((pattern, i) => {
			output += `${i + 1}. ${formatter(pattern)}\n`;
		});

		if (patterns.length > maxTotal) {
			output += `... (${patterns.length - maxTotal} more patterns)\n`;
		}
	}

	// Output statistics
	output += `\nImplemented ${Object.keys(letterGenerators).length} letter generators\n`;

	return output;
}

/**
 * Generate a CSV string of all patterns for export
 */
export function generatePatternsCsv(): string {
	const patterns = generateAllPatterns();
	let csv =
		'letter,start_pos,end_pos,timing,direction,blue_motion_type,blue_prop_rot_dir,blue_start_loc,blue_end_loc,red_motion_type,red_prop_rot_dir,red_start_loc,red_end_loc\n';

	patterns.forEach((pattern) => {
		csv += formatPatternCSV(pattern) + '\n';
	});

	return csv;
}

/**
 * Main function to run pattern generation and testing
 */
export function main() {
	// Test all implemented generators
	console.log('======= GENERATED PATTERNS =======');
	console.log(testPatternGenerators());

	// Test specific letters
	console.log('\n\n======= TESTING SPECIFIC LETTERS =======');
	console.log(
		testPatternGenerators({
			letters: ['A', 'F', 'M', 'X', 'Alpha', 'Omega'],
			maxSamplesPerLetter: 2
		})
	);

	// Generate CSV output for a sample
	console.log('\n\n======= CSV SAMPLE OUTPUT =======');
	const csvSample = generatePatternsCsv().split('\n').slice(0, 11).join('\n');
	console.log(csvSample + '\n... (more rows)');
}

// Uncomment to run the test program
// main();
