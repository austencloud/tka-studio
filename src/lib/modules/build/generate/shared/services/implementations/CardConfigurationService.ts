import type { UIGenerationConfig } from "../../../state/generate-config.svelte";
import { DifficultyLevel } from "../../domain/models";
import type {
    CardDescriptor,
    CardHandlers,
    ICardConfigurationService
} from "../contracts/ICardConfigurationService";

/**
 * Implementation of ICardConfigurationService
 * Builds card descriptor arrays with conditional rendering and responsive grid layouts
 */
export class CardConfigurationService implements ICardConfigurationService {
	/**
	 * Build card descriptors array for rendering
	 * Extracted from CardBasedSettingsContainer to separate business logic from presentation
	 */
	buildCardDescriptors(
		config: UIGenerationConfig,
		currentLevel: DifficultyLevel,
		isFreeformMode: boolean,
		handlers: CardHandlers,
		headerFontSize: string,
		allowedIntensityValues: number[],
		isGenerating: boolean = false
	): CardDescriptor[] {
		const cardList: CardDescriptor[] = [];
		let cardIndex = 0;

		// Determine layout based on level
		const isBeginnerLevel = currentLevel === DifficultyLevel.BEGINNER;
		const shouldShowTurnIntensity = currentLevel !== DifficultyLevel.BEGINNER;

		// Row 1: Always visible cards (Level, Length, Generation Mode)
		// These cards are STABLE and never resize
		cardList.push({
			id: "level",
			props: {
				currentLevel,
				onLevelChange: handlers.handleLevelChange,
				cardIndex: cardIndex++,
				headerFontSize
			},
			gridColumnSpan: 2 // Always 2 cols - stable
		});

		cardList.push({
			id: "length",
			props: {
				currentLength: config.length,
				onLengthChange: handlers.handleLengthChange,
				color: "#3b82f6",
				cardIndex: cardIndex++,
				headerFontSize
			},
			gridColumnSpan: 2 // Always 2 cols - stable
		});

		cardList.push({
			id: "generation-mode",
			props: {
				currentMode: config.mode,
				onModeChange: handlers.handleGenerationModeChange,
				color: "#8b5cf6",
				cardIndex: cardIndex++,
				headerFontSize
			},
			gridColumnSpan: 2 // Always 2 cols - LOCKED TOP-RIGHT
		});

		// Row 2: Grid Mode and Prop Continuity
		// Expand to 3 cols each in Beginner mode (any type - Freeform or Circular)
		cardList.push({
			id: "grid-mode",
			props: {
				currentMode: config.gridMode,
				onModeChange: handlers.handleGridModeChange,
				color: "#10b981",
				cardIndex: cardIndex++,
				headerFontSize
			},
			gridColumnSpan: isBeginnerLevel ? 3 : 2 // Expands in any Beginner mode
		});

		cardList.push({
			id: "prop-continuity",
			props: {
				currentContinuity: config.propContinuity,
				onContinuityChange: handlers.handlePropContinuityChange,
				color: "#06b6d4",
				cardIndex: cardIndex++,
				headerFontSize
			},
			gridColumnSpan: isBeginnerLevel ? 3 : 2 // Expands in any Beginner mode
		});

		// Conditional: Turn Intensity (only when level !== BEGINNER)
		// Fills the last spot in Row 2 alongside Grid and PropCont
		if (shouldShowTurnIntensity) {
			cardList.push({
				id: "turn-intensity",
				props: {
					currentIntensity: config.turnIntensity,
					allowedValues: allowedIntensityValues,
					onIntensityChange: handlers.handleTurnIntensityChange,
					cardIndex: cardIndex++,
					headerFontSize
				},
				gridColumnSpan: 2 // Always 2 columns (1/3 of row)
			});
		}

		// Row 3: Circular mode only cards (Slice Size + CAP Type)
		// Determine if slice size selection is needed
		// Mirrored, Swapped, and Complementary CAPs only support halved mode
		const capTypeAllowsSliceChoice =
			!config.capType?.includes("mirrored") &&
			!config.capType?.includes("swapped") &&
			!config.capType?.includes("complementary");

		// Conditional: Slice Size (only in Circular mode AND when CAP type allows choice)
		if (!isFreeformMode && capTypeAllowsSliceChoice) {
			cardList.push({
				id: "slice-size",
				props: {
					currentSliceSize: config.sliceSize,
					onSliceSizeChange: handlers.handleSliceSizeChange,
					color: "#ec4899",
					cardIndex: cardIndex++,
					headerFontSize
				},
				gridColumnSpan: 2
			});
		}

		// Conditional: CAP Type (only in Circular mode)
		// Shares row 3 with SliceSize if shown: SliceSize=2 cols, CAP=4 cols
		// Takes full row if SliceSize hidden: CAP=6 cols
		if (!isFreeformMode) {
			cardList.push({
				id: "cap-type",
				props: {
					currentCAPType: config.capType,
					onCAPTypeChange: handlers.handleCAPTypeChange,
					shadowColor: "30deg 75% 55%", // Orange shadow
					cardIndex: cardIndex++,
					headerFontSize
				},
				gridColumnSpan: capTypeAllowsSliceChoice ? 4 : 6 // Expands to full row when slice size hidden
			});
		}

		// Generate Button Card - always at the end, spans full width
		if (handlers.handleGenerateClick) {
			cardList.push({
				id: "generate-button",
				props: {
					isGenerating,
					onGenerateClicked: handlers.handleGenerateClick,
					config // Pass the config so the button can convert it to GenerationOptions
				},
				gridColumnSpan: 6 // Full width
			});
		}

		return cardList;
	}
}
