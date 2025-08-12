/**
 * Core Service Interfaces for TKA V2 Modern
 *
 * These interfaces define the contract for all application services,
 * following the service-oriented architecture pattern from the desktop app.
 */

import type { ArrowData, BeatData, MotionData, PictographData, SequenceData } from '$lib/domain';
import { GridMode as DomainGridMode } from '$lib/domain';
import type {
	BrowseDisplayState,
	BrowseLoadingState,
	BrowseSequenceMetadata,
	FilterType,
	FilterValue,
	SortMethod,
} from '$lib/domain/browse';

// ============================================================================
// ADVANCED BROWSE SERVICES
// ============================================================================

// Re-export types from service implementations
export type {
	DeleteConfirmationData,
	DeleteResult,
	IDeleteService,
} from './implementations/DeleteService';
export type { IFavoritesService } from './implementations/FavoritesService';
export type {
	BrowseState,
	FilterState,
	IFilterPersistenceService,
} from './implementations/FilterPersistenceService';
export type {
	INavigationService,
	NavigationItem,
	NavigationSection,
} from './implementations/NavigationService';
export type {
	ISectionService,
	SectionConfiguration,
	SequenceSection,
} from './implementations/SectionService';

// Re-export domain types for convenience
export type {
	BeatData,
	BrowseDisplayState,
	BrowseLoadingState,
	BrowseSequenceMetadata,
	FilterType,
	FilterValue,
	MotionData,
	PictographData,
	SequenceData,
	SortMethod,
};

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
// SERVICE CONSTANTS
// ============================================================================

// Sequence Card Service Interface Constants
export const ISequenceCardImageServiceInterface = defineService<ISequenceCardImageService>('ISequenceCardImageService');
export const ISequenceCardLayoutServiceInterface = defineService<ISequenceCardLayoutService>('ISequenceCardLayoutService');
export const ISequenceCardPageServiceInterface = defineService<ISequenceCardPageService>('ISequenceCardPageService');
export const ISequenceCardBatchServiceInterface = defineService<ISequenceCardBatchService>('ISequenceCardBatchService');
export const ISequenceCardCacheServiceInterface = defineService<ISequenceCardCacheService>('ISequenceCardCacheService');
export const IEnhancedExportServiceInterface = defineService<IEnhancedExportService>('IEnhancedExportService');

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
// BROWSE SERVICES
// ============================================================================

export interface IBrowseService {
	loadSequenceMetadata(): Promise<BrowseSequenceMetadata[]>;
	applyFilter(
		sequences: BrowseSequenceMetadata[],
		filterType: FilterType,
		filterValue: FilterValue
	): Promise<BrowseSequenceMetadata[]>;
	sortSequences(
		sequences: BrowseSequenceMetadata[],
		sortMethod: SortMethod
	): Promise<BrowseSequenceMetadata[]>;
	groupSequencesIntoSections(
		sequences: BrowseSequenceMetadata[],
		sortMethod: SortMethod
	): Promise<Record<string, BrowseSequenceMetadata[]>>;
	getUniqueValues(field: keyof BrowseSequenceMetadata): Promise<string[]>;
	getFilterOptions(filterType: FilterType): Promise<string[]>;
}

export interface IThumbnailService {
	getThumbnailUrl(sequenceId: string, thumbnailPath: string): string;
	preloadThumbnail(sequenceId: string, thumbnailPath: string): Promise<void>;
	getThumbnailMetadata(sequenceId: string): Promise<{ width: number; height: number } | null>;
	clearThumbnailCache(): void;
}

export interface ISequenceIndexService {
	loadSequenceIndex(): Promise<BrowseSequenceMetadata[]>;
	buildSearchIndex(sequences: BrowseSequenceMetadata[]): Promise<void>;
	searchSequences(query: string): Promise<BrowseSequenceMetadata[]>;
	refreshIndex(): Promise<void>;
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
	// Sequence Card Settings
	sequenceCard?: {
		defaultColumnCount?: number;
		defaultLayoutMode?: 'grid' | 'list' | 'printable';
		enableTransparency?: boolean;
		cacheEnabled?: boolean;
		cacheSizeLimit?: number;
		exportQuality?: 'low' | 'medium' | 'high';
		exportFormat?: 'PNG' | 'JPG' | 'WebP';
		defaultPaperSize?: 'A4' | 'Letter' | 'Legal' | 'Tabloid';
	};
}

// ============================================================================
// SEQUENCE CARD SERVICES
// ============================================================================

// Import sequence card types
export type {
	LayoutConfig,
	ExportOptions,
	SequenceCardExportSettings,
	DeviceCapabilities,
	PrintLayoutOptions,
	CacheEntry,
	CacheConfig,
	ProgressInfo,
	ValidationResult,
	ExportResult
} from '$lib/domain/sequenceCard';

export interface ISequenceCardImageService {
	/**
	 * Generate a high-quality image for a single sequence card
	 */
	generateSequenceCardImage(sequence: SequenceData, options: ExportOptions): Promise<Blob>;
	
	/**
	 * Generate images for multiple sequences in batch
	 */
	generateBatchImages(
		sequences: SequenceData[], 
		options: ExportOptions,
		onProgress?: (progress: ProgressInfo) => void
	): Promise<ExportResult[]>;
	
	/**
	 * Get cached image for a sequence
	 */
	getCachedImage(sequenceId: string, options: ExportOptions): Promise<Blob | null>;
	
	/**
	 * Preload images for a set of sequences
	 */
	preloadImages(sequences: SequenceData[], options: ExportOptions): Promise<void>;
	
	/**
	 * Clear image cache
	 */
	clearImageCache(): Promise<void>;
	
	/**
	 * Get cache statistics
	 */
	getCacheStats(): Promise<{ size: number; count: number; hitRate: number }>;
}

export interface ISequenceCardLayoutService {
	/**
	 * Calculate optimal grid layout for given constraints
	 */
	calculateOptimalLayout(
		containerWidth: number,
		containerHeight: number,
		cardCount: number,
		preferredColumns?: number
	): LayoutConfig;
	
	/**
	 * Calculate responsive layout based on device capabilities
	 */
	getResponsiveLayout(
		deviceCapabilities: DeviceCapabilities,
		cardCount: number
	): LayoutConfig;
	
	/**
	 * Calculate column layout for specific column count
	 */
	calculateColumnLayout(
		columnCount: number,
		containerWidth: number,
		cardAspectRatio?: number
	): { cardWidth: number; cardHeight: number; spacing: number };
	
	/**
	 * Get layout for printable pages
	 */
	getPrintableLayout(
		printOptions: PrintLayoutOptions,
		cardCount: number
	): LayoutConfig;
	
	/**
	 * Validate layout constraints
	 */
	validateLayoutConstraints(layout: LayoutConfig): ValidationResult;
	
	/**
	 * Get optimal column count for container size
	 */
	getOptimalColumnCount(containerWidth: number, cardAspectRatio?: number): number;
}

export interface ISequenceCardPageService {
	/**
	 * Generate a complete page with multiple sequence cards
	 */
	generatePage(
		sequences: SequenceData[],
		layout: LayoutConfig,
		options: ExportOptions
	): Promise<HTMLElement>;
	
	/**
	 * Generate printable page as image
	 */
	generatePrintablePage(
		sequences: SequenceData[],
		printOptions: PrintLayoutOptions
	): Promise<Blob>;
	
	/**
	 * Generate PDF with multiple pages
	 */
	generatePDF(
		sequences: SequenceData[],
		printOptions: PrintLayoutOptions
	): Promise<Blob>;
	
	/**
	 * Calculate pagination for sequences
	 */
	calculatePagination(
		sequences: SequenceData[],
		itemsPerPage: number
	): SequenceData[][];
	
	/**
	 * Generate page preview
	 */
	generatePagePreview(
		sequences: SequenceData[],
		layout: LayoutConfig
	): Promise<string>; // Returns data URL
}

export interface ISequenceCardBatchService {
	/**
	 * Process large batch of sequences with memory management
	 */
	processBatch(
		sequences: SequenceData[],
		options: SequenceCardExportSettings,
		onProgress?: (progress: ProgressInfo) => void
	): Promise<ExportResult[]>;
	
	/**
	 * Estimate processing time for batch
	 */
	estimateProcessingTime(
		sequences: SequenceData[],
		options: ExportOptions
	): Promise<number>; // milliseconds
	
	/**
	 * Check memory requirements for batch
	 */
	getMemoryRequirements(
		sequences: SequenceData[],
		options: ExportOptions
	): Promise<number>; // bytes
	
	/**
	 * Cancel running batch operation
	 */
	cancelBatch(): void;
	
	/**
	 * Get optimal batch size for current system
	 */
	getOptimalBatchSize(): Promise<number>;
}

export interface ISequenceCardCacheService {
	/**
	 * Store image in cache
	 */
	storeImage(
		sequenceId: string,
		imageBlob: Blob,
		options: ExportOptions
	): Promise<void>;
	
	/**
	 * Retrieve image from cache
	 */
	retrieveImage(
		sequenceId: string,
		options: ExportOptions
	): Promise<Blob | null>;
	
	/**
	 * Check if image is cached
	 */
	isImageCached(
		sequenceId: string,
		options: ExportOptions
	): Promise<boolean>;
	
	/**
	 * Clear all cached images
	 */
	clearCache(): Promise<void>;
	
	/**
	 * Clear cache entries older than specified date
	 */
	clearOldEntries(olderThan: Date): Promise<void>;
	
	/**
	 * Get cache statistics
	 */
	getCacheStats(): Promise<{
		entryCount: number;
		totalSize: number;
		hitRate: number;
		oldestEntry?: Date;
	}>;
	
	/**
	 * Optimize cache (remove least recently used items)
	 */
	optimizeCache(): Promise<void>;
	
	/**
	 * Set cache configuration
	 */
	setCacheConfig(config: Partial<CacheConfig>): Promise<void>;
}

// Enhanced Export Service with sequence card support
export interface IEnhancedExportService extends IExportService {
	/**
	 * Export multiple sequence cards as individual images
	 */
	exportSequenceCardsAsImages(
		sequences: SequenceData[],
		options: ExportOptions
	): Promise<Blob[]>;
	
	/**
	 * Export sequence cards as printable PDF
	 */
	exportSequenceCardsAsPDF(
		sequences: SequenceData[],
		layoutOptions: PrintLayoutOptions
	): Promise<Blob>;
	
	/**
	 * Export single sequence card with advanced options
	 */
	exportSingleSequenceCard(
		sequence: SequenceData,
		options: ExportOptions
	): Promise<Blob>;
	
	/**
	 * Export sequence cards as ZIP archive
	 */
	exportSequenceCardsAsZip(
		sequences: SequenceData[],
		options: ExportOptions,
		filename?: string
	): Promise<Blob>;
	
	/**
	 * Get available export formats
	 */
	getAvailableFormats(): string[];
	
	/**
	 * Get default export options for sequence cards
	 */
	getDefaultSequenceCardExportOptions(): ExportOptions;
}
