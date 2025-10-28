import type { UIGenerationConfig } from "../../../state/generate-config.svelte";
import type { DifficultyLevel } from "../../domain/models";

/**
 * Card descriptor for rendering in the UI
 * Contains all necessary information to render a specific card component
 */
export interface CardDescriptor {
	/** Unique identifier for the card (used as key in Svelte's each block) */
	id: string;
	/** Props to pass to the card component */
	props: Record<string, any>;
	/** Number of grid columns this card should span (1-6) */
	gridColumnSpan: number;
}

/**
 * Handlers for card interactions
 * Passed from parent component to wire up event callbacks
 */
export interface CardHandlers {
	handleLevelChange: (level: DifficultyLevel) => void;
	handleLengthChange: (length: number) => void;
	handleTurnIntensityChange: (intensity: number) => void;
	handlePropContinuityChange: (continuity: string) => void;
	handleGridModeChange: (mode: any) => void;
	handleGenerationModeChange: (mode: any) => void;
	handleCAPTypeChange: (capType: any) => void;
	handleSliceSizeChange: (sliceSize: any) => void;
	handleGenerateClick?: () => Promise<void>;
}

/**
 * Service for building card configuration arrays
 * Encapsulates the complex logic for determining which cards to display and how they should be laid out
 */
export interface ICardConfigurationService {
	/**
	 * Build an array of card descriptors based on current configuration
	 * Handles conditional rendering logic (e.g., turn intensity only shown for non-beginner levels)
	 * Calculates grid spans and responsive layouts
	 *
	 * @param config - Current generation configuration
	 * @param currentLevel - Current difficulty level
	 * @param isFreeformMode - Whether in freeform mode (vs circular mode)
	 * @param handlers - Event handlers for card interactions
	 * @param headerFontSize - Calculated header font size to pass to cards
	 * @param allowedIntensityValues - Allowed turn intensity values for current level
	 * @param isGenerating - Whether generation is currently in progress
	 * @returns Array of card descriptors ready for rendering
	 */
	buildCardDescriptors(
		config: UIGenerationConfig,
		currentLevel: DifficultyLevel,
		isFreeformMode: boolean,
		handlers: CardHandlers,
		headerFontSize: string,
		allowedIntensityValues: number[],
		isGenerating?: boolean
	): CardDescriptor[];
}
