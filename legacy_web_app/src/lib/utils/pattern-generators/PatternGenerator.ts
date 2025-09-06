// Position mappings define the blue and red locations for each position
const positionMappings = {
	alpha: {
		alpha1: { blue: 's', red: 'n' },
		alpha3: { blue: 'w', red: 'e' },
		alpha5: { blue: 'n', red: 's' },
		alpha7: { blue: 'e', red: 'w' }
	},
	beta: {
		beta1: { blue: 'n', red: 'n' },
		beta3: { blue: 'e', red: 'e' },
		beta5: { blue: 's', red: 's' },
		beta7: { blue: 'w', red: 'w' }
	},
	gamma: {
		gamma1: { blue: 'w', red: 'n' },
		gamma3: { blue: 'n', red: 'e' },
		gamma5: { blue: 'e', red: 's' },
		gamma7: { blue: 's', red: 'w' },
		gamma9: { blue: 'e', red: 'n' },
		gamma11: { blue: 's', red: 'e' },
		gamma13: { blue: 'w', red: 's' },
		gamma15: { blue: 'n', red: 'w' }
	}
} as const;

// Define type for position mapping
type PositionSystem = keyof typeof positionMappings;
type PositionKey<T extends PositionSystem> = keyof (typeof positionMappings)[T];
type LocationPoint = { blue: string; red: string };

// Define cardinal direction cycle (clockwise order)
const locationCycle = ['n', 'e', 's', 'w'];

// Define position cycles
const positionCycles = {
	alpha: {
		cw: ['alpha3', 'alpha5', 'alpha7', 'alpha1'],
		ccw: ['alpha3', 'alpha1', 'alpha7', 'alpha5']
	},
	beta: {
		cw: ['beta3', 'beta5', 'beta7', 'beta1'],
		ccw: ['beta3', 'beta1', 'beta7', 'beta5']
	},
	gamma: {
		cw1: ['gamma3', 'gamma5', 'gamma7', 'gamma1'],
		ccw1: ['gamma3', 'gamma1', 'gamma7', 'gamma5'],
		cw2: ['gamma11', 'gamma13', 'gamma15', 'gamma9'],
		ccw2: ['gamma11', 'gamma9', 'gamma15', 'gamma13'],
		quarter1: [
			['gamma3', 'gamma13'],
			['gamma5', 'gamma15'],
			['gamma7', 'gamma9'],
			['gamma1', 'gamma11']
		],
		quarter2: [
			['gamma11', 'gamma5'],
			['gamma13', 'gamma7'],
			['gamma15', 'gamma1'],
			['gamma9', 'gamma3']
		]
	}
};

// Calculate end location based on start location, motion type, and rotation direction
function calculateEndLocation(startLoc: string, motion: string, rotDir: string): string {
	if (motion === 'static') return startLoc;
	if (motion === 'dash') {
		// Dash goes to opposite location
		const index = locationCycle.indexOf(startLoc);
		return locationCycle[(index + 2) % 4];
	}

	const index = locationCycle.indexOf(startLoc);
	if (rotDir === 'cw') {
		return locationCycle[(index + 1) % 4];
	} else if (rotDir === 'ccw') {
		return locationCycle[(index + 3) % 4]; // -1 in modular arithmetic
	} else {
		return startLoc; // No rotation (no_rot)
	}
}

// Pattern row interface
export interface PatternRow {
	letter: string;
	startPos: string;
	endPos: string;
	timing: string;
	direction: string;
	blueMotion: string;
	blueRotDir: string;
	blueStartLoc: string;
	blueEndLoc: string;
	redMotion: string;
	redRotDir: string;
	redStartLoc: string;
	redEndLoc: string;
}

// Pattern row parameters interface
export interface PatternParams {
	letter: string;
	startPos: string;
	endPos: string;
	timing: string;
	direction: string;
	blueMotion: string;
	blueRotDir: string;
	redMotion: string;
	redRotDir: string;
}

// Generate a pattern row
export function generatePatternRow(params: PatternParams): PatternRow {
	const {
		letter,
		startPos,
		endPos,
		timing,
		direction,
		blueMotion,
		blueRotDir,
		redMotion,
		redRotDir
	} = params;

	// Get start locations from position mappings
	const startSystem = startPos.match(/^([a-z]+)/)![1] as PositionSystem;
	const systemMap = positionMappings[startSystem];

	// Type guard to ensure startPos exists in the system map
	if (!(startPos in systemMap)) {
		throw new Error(`Invalid start position '${startPos}' for system '${startSystem}'`);
	}

	// Need to use bracket notation with type assertion
	// We know this is safe because we checked startPos is in systemMap
	const mapping = systemMap[startPos as keyof typeof systemMap] as LocationPoint;
	const blueStartLoc = mapping.blue;
	const redStartLoc = mapping.red;

	// Calculate end locations
	const blueEndLoc = calculateEndLocation(blueStartLoc, blueMotion, blueRotDir);
	const redEndLoc = calculateEndLocation(redStartLoc, redMotion, redRotDir);

	return {
		letter,
		startPos,
		endPos,
		timing,
		direction,
		blueMotion,
		blueRotDir,
		blueStartLoc,
		blueEndLoc,
		redMotion,
		redRotDir,
		redStartLoc,
		redEndLoc
	};
}

// Format pattern for CSV output
export function formatPatternCSV(pattern: PatternRow): string {
	return `${pattern.letter},${pattern.startPos},${pattern.endPos},${pattern.timing},${pattern.direction},${pattern.blueMotion},${pattern.blueRotDir},${pattern.blueStartLoc},${pattern.blueEndLoc},${pattern.redMotion},${pattern.redRotDir},${pattern.redStartLoc},${pattern.redEndLoc}`;
}

// Format pattern for display
export function formatPatternDisplay(pattern: PatternRow): string {
	return (
		`${pattern.letter}: ${pattern.startPos} → ${pattern.endPos}, ` +
		`timing=${pattern.timing}, direction=${pattern.direction}, ` +
		`blue: ${pattern.blueMotion}/${pattern.blueRotDir} (${pattern.blueStartLoc}→${pattern.blueEndLoc}), ` +
		`red: ${pattern.redMotion}/${pattern.redRotDir} (${pattern.redStartLoc}→${pattern.redEndLoc})`
	);
}

export { positionMappings, locationCycle, positionCycles };
