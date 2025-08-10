/**
 * Core Service Interfaces for TKA V2 Modern
 *
 * These interfaces define the contract for all application services,
 * following the service-oriented architecture pattern from the desktop app.
 */

import type { ArrowData, BeatData, MotionData, PictographData, SequenceData } from '$lib/domain';
import { GridMode as DomainGridMode } from '$lib/domain';

// Re-export domain types for convenience
export type { BeatData, MotionData, PictographData, SequenceData };

// ============================================================================
// SEQUENCE SERVICES
// ============================================================================

export interface SequenceCreateRequest {
	name: string;
	length: number;
	gridMode?: DomainGridMode;
	propType?: string;
}

export interface ValidationResult {
	isValid: boolean;
	errors: string[];
}

export interface ISequenceService {
	createSequence(request: SequenceCreateRequest): Promise<SequenceData>;
	updateBeat(sequenceId: string, beatIndex: number, beatData: BeatData): Promise<void>;
	setSequenceStartPosition(sequenceId: string, startPosition: BeatData): Promise<void>;
	deleteSequence(id: string): Promise<void>;
	getSequence(id: string): Promise<SequenceData | null>;
	getAllSequences(): Promise<SequenceData[]>;
}

export interface ISequenceDomainService {
	validateCreateRequest(request: SequenceCreateRequest): ValidationResult;
	createSequence(request: SequenceCreateRequest): SequenceData;
	updateBeat(sequence: SequenceData, beatIndex: number, beatData: BeatData): SequenceData;
	calculateSequenceWord(sequence: SequenceData): string;
}

// ============================================================================
// PICTOGRAPH SERVICES
// ============================================================================

export interface IPictographService {
	renderPictograph(data: PictographData): Promise<SVGElement>;
	updateArrow(pictographId: string, arrowData: ArrowData): Promise<PictographData>;
}

export interface IPictographRenderingService {
	renderPictograph(data: PictographData): Promise<SVGElement>;
	renderBeat(beat: BeatData): Promise<SVGElement>;
}

// ============================================================================
// PERSISTENCE SERVICES
// ============================================================================

export interface IPersistenceService {
	saveSequence(sequence: SequenceData): Promise<void>;
	loadSequence(id: string): Promise<SequenceData | null>;
	loadAllSequences(): Promise<SequenceData[]>;
	deleteSequence(id: string): Promise<void>;
}

// ============================================================================
// GENERATION SERVICES
// ============================================================================

export interface GenerationOptions {
	length: number;
	gridMode: DomainGridMode;
	propType: string;
	difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export interface ISequenceGenerationService {
	generateSequence(options: GenerationOptions): Promise<SequenceData>;
}

export interface IMotionGenerationService {
	generateMotion(
		color: 'blue' | 'red',
		options: GenerationOptions,
		previousBeats: BeatData[]
	): Promise<MotionData>;
}

// ============================================================================
// ARROW POSITIONING SERVICES
// ============================================================================

export interface ArrowPosition {
	x: number;
	y: number;
	rotation: number;
}

export interface LegacyArrowData {
	id: string;
	color: 'blue' | 'red';
	motionType: MotionType;
	location: Location;
	startOrientation: Orientation;
	endOrientation: Orientation;
	propRotDir: PropRotDir;
	turns: number;
	isMirrored: boolean;
	coords?: Coordinates;
	rotAngle?: number;
	svgCenter?: Coordinates;
	svgMirrored?: boolean;
}

export interface GridData {
	mode: DomainGridMode;
	allLayer2PointsNormal: Record<string, GridPoint>;
	allHandPointsNormal: Record<string, GridPoint>;
}

export interface GridPoint {
	coordinates: Coordinates;
}

export interface Coordinates {
	x: number;
	y: number;
}

export interface ArrowPlacementConfig {
	pictographData: PictographData;
	gridData: GridData;
	checker?: unknown;
}

// Arrow positioning enums
export type MotionType = 'pro' | 'anti' | 'float' | 'dash' | 'static';
export type Location = 'n' | 'ne' | 'e' | 'se' | 's' | 'sw' | 'w' | 'nw' | 'center';
export type Orientation = 'in' | 'out' | 'clock' | 'counter';
export type PropRotDir = 'cw' | 'ccw' | 'no_rot' | 'clockwise' | 'counter_clockwise';
export type HandRotDir = 'cw_shift' | 'ccw_shift';
export type GridMode = DomainGridMode;

export interface IArrowPositioningService {
	calculateArrowPosition(
		arrowData: ArrowData,
		pictographData: PictographData,
		gridData: GridData
	): Promise<ArrowPosition>;

	calculateAllArrowPositions(
		pictographData: PictographData,
		gridData: GridData
	): Promise<Map<string, ArrowPosition>>;

	calculateRotationAngle(motion: MotionData, location: Location, isMirrored: boolean): number;

	shouldMirrorArrow(motion: MotionData): boolean;
}

// ============================================================================
// PROP RENDERING SERVICES
// ============================================================================

export interface PropData {
	id: string;
	propType: string;
	color: 'blue' | 'red';
	location: Location;
	position: Coordinates;
	rotation: number;
}

export interface PropPosition {
	x: number;
	y: number;
	rotation: number;
}

export interface IPropRenderingService {
	renderProp(
		propType: string,
		color: 'blue' | 'red',
		motionData: MotionData,
		gridMode: GridMode
	): Promise<SVGElement>;

	calculatePropPosition(
		motionData: MotionData,
		color: 'blue' | 'red',
		gridMode: GridMode
	): Promise<PropPosition>;

	loadPropSVG(propType: string, color: 'blue' | 'red'): Promise<string>;

	getSupportedPropTypes(): string[];
}

// ============================================================================
// ARROW PLACEMENT SERVICES
// ============================================================================

export interface IArrowPlacementDataService {
	getDefaultAdjustment(
		motionType: MotionType,
		placementKey: string,
		turns: number | string,
		gridMode: GridMode
	): Promise<{ x: number; y: number }>;

	getAvailablePlacementKeys(motionType: MotionType, gridMode: GridMode): Promise<string[]>;

	isLoaded(): boolean;
	loadPlacementData(): Promise<void>;
}

export interface IArrowPlacementKeyService {
	generatePlacementKey(
		motionData: MotionData,
		pictographData: PictographData,
		availableKeys: string[]
	): string;

	generateBasicKey(motionType: MotionType): string;
}

// ============================================================================
// APPLICATION SERVICES
// ============================================================================

export interface IApplicationInitializationService {
	initialize(): Promise<void>;
}

export interface ISettingsService {
	currentSettings: AppSettings;
	updateSetting<K extends keyof AppSettings>(key: K, value: AppSettings[K]): Promise<void>;
	loadSettings(): Promise<void>;
}

// ============================================================================
// EXPORT SERVICES
// ============================================================================

export interface ExportOptions {
	beatSize: number;
	spacing: number;
	includeTitle: boolean;
	includeMetadata: boolean;
}

export interface IExportService {
	exportSequenceAsImage(sequence: SequenceData, options: ExportOptions): Promise<Blob>;
	exportSequenceAsJson(sequence: SequenceData): Promise<string>;
}

// ============================================================================
// CONSTRUCT TAB SERVICES
// ============================================================================

export interface IConstructTabCoordinationService {
	setupComponentCoordination(components: Record<string, unknown>): void;
	handleSequenceModified(sequence: SequenceData): Promise<void>;
	handleStartPositionSet(startPosition: BeatData): Promise<void>;
	handleBeatAdded(beatData: BeatData): Promise<void>;
	handleGenerationRequest(config: Record<string, unknown>): Promise<void>;
	handleUITransitionRequest(targetPanel: string): Promise<void>;
}

export interface IOptionDataService {
	getNextOptions(
		currentSequence: SequenceData,
		filters?: OptionFilters
	): Promise<PictographData[]>;
	filterOptionsByDifficulty(options: PictographData[], level: DifficultyLevel): PictographData[];
	validateOptionCompatibility(option: PictographData, sequence: SequenceData): ValidationResult;
	getAvailableMotionTypes(): MotionType[];
}

export interface IStartPositionService {
	getAvailableStartPositions(propType: string, gridMode: GridMode): Promise<BeatData[]>;
	setStartPosition(startPosition: BeatData): Promise<void>;
	validateStartPosition(position: BeatData): ValidationResult;
	getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]>;
}

// Additional types for the new services
export interface OptionFilters {
	difficulty?: DifficultyLevel;
	motionTypes?: MotionType[];
	minTurns?: number;
	maxTurns?: number;
}

export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';

// ============================================================================
// SERVICE REGISTRY
// ============================================================================

export type ServiceInterface<T> = {
	readonly name: string;
	readonly _type?: T;
};

// Helper function to define service interfaces
export function defineService<T>(name: string): ServiceInterface<T> {
	return { name } as ServiceInterface<T>;
}

// Note: Service interface constants are defined in bootstrap.ts to avoid circular dependencies

// ============================================================================
// DEVICE DETECTION SERVICES
// ============================================================================

export interface DeviceCapabilities {
	/** Primary input method - determines UI interaction patterns */
	primaryInput: 'touch' | 'mouse' | 'hybrid';

	/** Screen size category for layout decisions */
	screenSize: 'mobile' | 'tablet' | 'desktop';

	/** Whether device has touch capability */
	hasTouch: boolean;

	/** Whether device has precise pointer (mouse/trackpad) */
	hasPrecisePointer: boolean;

	/** Whether device has keyboard */
	hasKeyboard: boolean;

	/** Viewport dimensions */
	viewport: {
		width: number;
		height: number;
	};

	/** Pixel density ratio */
	pixelRatio: number;
}

export interface ResponsiveSettings {
	/** Minimum touch target size in pixels */
	minTouchTarget: number;

	/** Preferred spacing between interactive elements */
	elementSpacing: number;

	/** Whether scrolling is acceptable in current context */
	allowScrolling: boolean;

	/** Layout density preference */
	layoutDensity: 'compact' | 'comfortable' | 'spacious';

	/** Font size scaling factor */
	fontScaling: number;
}

export interface IDeviceDetectionService {
	/** Get current device capabilities */
	getCapabilities(): DeviceCapabilities;

	/** Get responsive settings based on device */
	getResponsiveSettings(): ResponsiveSettings;

	/** Check if device is primarily touch-based */
	isTouchPrimary(): boolean;

	/** Check if layout should prioritize touch targets */
	shouldOptimizeForTouch(): boolean;

	/** Listen for device capability changes (screen rotation, etc.) */
	onCapabilitiesChanged(callback: (capabilities: DeviceCapabilities) => void): () => void;

	/** Get breakpoint for current viewport */
	getCurrentBreakpoint(): 'mobile' | 'tablet' | 'desktop' | 'large-desktop';
}

// ============================================================================
// APPLICATION SETTINGS
// ============================================================================

export interface AppSettings {
	theme: 'light' | 'dark';
	gridMode: DomainGridMode;
	showBeatNumbers: boolean;
	autoSave: boolean;
	exportQuality: 'low' | 'medium' | 'high';
	workbenchColumns: number;
	userName?: string;
	propType?: string;
	backupFrequency?: string;
	enableFades?: boolean;
	animationsEnabled?: boolean; // Simple animation control
	growSequence?: boolean;
	numBeats?: number;
	beatLayout?: string;
	// Background settings
	backgroundType?:
		| 'snowfall'
		| 'nightSky'
		| 'aurora'
		| 'auroraBorealis'
		| 'starfield'
		| 'bubbles';
	backgroundQuality?: 'high' | 'medium' | 'low' | 'minimal';
	backgroundEnabled?: boolean;
	visibility?: {
		TKA?: boolean;
		Reversals?: boolean;
		Positions?: boolean;
		Elemental?: boolean;
		VTG?: boolean;
		nonRadialPoints?: boolean;
	};
	imageExport?: {
		includeStartPosition?: boolean;
		addReversalSymbols?: boolean;
		addBeatNumbers?: boolean;
		addDifficultyLevel?: boolean;
		addWord?: boolean;
		addInfo?: boolean;
		addUserInfo?: boolean;
	};
}
