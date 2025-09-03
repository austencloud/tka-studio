import { DIAMOND, BOX } from '$lib/types/Constants';

const diamondLayer1Files = import.meta.glob(
	'$lib/data/arrow_placement/diamond/special/from_layer1/*_placements.json',
	{ eager: true }
);
const diamondLayer2Files = import.meta.glob(
	'$lib/data/arrow_placement/diamond/special/from_layer2/*_placements.json',
	{ eager: true }
);
const diamondLayer3Blue1Red2Files = import.meta.glob(
	'$lib/data/arrow_placement/diamond/special/from_layer3_blue1_red2/*_placements.json',
	{ eager: true }
);
const diamondLayer3Blue2Red1Files = import.meta.glob(
	'$lib/data/arrow_placement/diamond/special/from_layer3_blue2_red1/*_placements.json',
	{ eager: true }
);

const boxLayer1Files = import.meta.glob(
	'$lib/data/arrow_placement/box/special/from_layer1/*_placements.json',
	{ eager: true }
);
const boxLayer2Files = import.meta.glob(
	'$lib/data/arrow_placement/box/special/from_layer2/*_placements.json',
	{ eager: true }
);
const boxLayer3Blue1Red2Files = import.meta.glob(
	'$lib/data/arrow_placement/box/special/from_layer3_blue1_red2/*_placements.json',
	{ eager: true }
);
const boxLayer3Blue2Red1Files = import.meta.glob(
	'$lib/data/arrow_placement/box/special/from_layer3_blue2_red1/*_placements.json',
	{ eager: true }
);

export class SpecialPlacementLoader {
	private static instance: SpecialPlacementLoader;
	private placementsByFolder: Record<string, Record<string, Record<string, any>>> = {};

	private constructor() {
		this.loadPlacements();
	}

	public static getInstance(): SpecialPlacementLoader {
		if (!SpecialPlacementLoader.instance) {
			SpecialPlacementLoader.instance = new SpecialPlacementLoader();
		}
		return SpecialPlacementLoader.instance;
	}

	private loadPlacements(): void {
		this.placementsByFolder[DIAMOND] = {
			from_layer1: this.processFiles(diamondLayer1Files),
			from_layer2: this.processFiles(diamondLayer2Files),
			from_layer3_blue1_red2: this.processFiles(diamondLayer3Blue1Red2Files),
			from_layer3_blue2_red1: this.processFiles(diamondLayer3Blue2Red1Files)
		};

		this.placementsByFolder[BOX] = {
			from_layer1: this.processFiles(boxLayer1Files),
			from_layer2: this.processFiles(boxLayer2Files),
			from_layer3_blue1_red2: this.processFiles(boxLayer3Blue1Red2Files),
			from_layer3_blue2_red1: this.processFiles(boxLayer3Blue2Red1Files)
		};
	}

	private getLayerFolder(oriKey: string, turnsTuple: string = ''): string {
		if (oriKey.includes('layer1')) {
			return 'from_layer1';
		} else if (oriKey.includes('layer3')) {
			return 'from_layer3_blue1_red2';
		}
		return 'NOT_FOUND';
	}

	private processFiles(files: Record<string, any>): Record<string, any> {
		const result: Record<string, any> = {};

		Object.entries(files).forEach(([path, module]) => {
			const letterMatch = path.match(/\/([^\/]+)_placements\.json$/);
			if (!letterMatch || !letterMatch[1]) return;

			const letter = letterMatch[1];
			const moduleData = module.default || module;

			result[letter] = moduleData;
		});

		return result;
	}

	public getAdjustmentForLetter(
		gridMode: string,
		oriKey: string,
		letter: string,
		turnsTuple: string,
		arrowKey: string
	): [number, number] | null {
		if (letter !== 'Q') {
			const letterData =
				this.placementsByFolder[gridMode]?.[this.getLayerFolder(oriKey, turnsTuple)]?.[letter];
			const actualLetterData = letterData?.[letter] || letterData;

			const matchedTuple = Object.keys(actualLetterData || {}).find(
				(key) => key === turnsTuple || key.replace(/\s/g, '') === turnsTuple.replace(/\s/g, '')
			);

			if (matchedTuple) {
				const placements = actualLetterData[matchedTuple];
				return (
					placements?.[arrowKey] ||
					placements?.[arrowKey.trim()] ||
					Object.entries(placements || {}).find(([key]) => key.trim() === arrowKey.trim())?.[1] ||
					null
				);
			}
			return null;
		}

		const folder = this.getLayerFolder(oriKey, turnsTuple);
		const letterData = this.placementsByFolder[gridMode]?.[folder]?.[letter];

		if (!letterData) {
			return null;
		}

		const actualLetterData = letterData[letter] || letterData;

		const matchedTuple = Object.keys(actualLetterData).find(
			(key) => key === turnsTuple || key.replace(/\s/g, '') === turnsTuple.replace(/\s/g, '')
		);

		if (!matchedTuple) {
			return null;
		}

		const placements = actualLetterData[matchedTuple];

		if (!placements) {
			return null;
		}

		const adjustment =
			placements[arrowKey] ||
			placements[arrowKey.trim()] ||
			Object.entries(placements).find(([key]) => key.trim() === arrowKey.trim())?.[1];

		return adjustment || null;
	}

	public loadOrReturnSpecialPlacements(): Record<string, Record<string, Record<string, any>>> {
		return this.placementsByFolder;
	}

	public reload(): void {
		this.loadPlacements();
	}
}
