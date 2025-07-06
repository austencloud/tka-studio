<!-- src/lib/components/SequenceWorkbench/BeatFrame/SelectionBorderOverlay.svelte -->
<script lang="ts">
	import { LetterType } from '../../types/LetterType.js';
	import type { Letter } from '@tka/domain';
	import type { PictographData } from '../types/PictographData.js';

	// Props using Svelte 5 runes
	const props = $props<{
		pictographData: PictographData;
		isSelected: boolean;
	}>();

	// Constants for border styling
	const BORDER_WIDTH = 3;
	const GLOW_RADIUS = 4;

	// Border colors map for different letter types
	const BORDER_COLORS = {
		[LetterType.Type1.folderName]: '#36c3ff', // Cyan
		[LetterType.Type2.folderName]: '#6F2DA8', // Purple
		[LetterType.Type3.folderName]: '#26e600', // Green
		[LetterType.Type4.folderName]: '#26e600', // Green
		[LetterType.Type5.folderName]: '#00b3ff', // Cyan
		[LetterType.Type6.folderName]: '#eb7d00', // Orange
		[LetterType.Type7.folderName]: '#6F2DA8', // Purple
		[LetterType.Type8.folderName]: '#26e600', // Green
		[LetterType.Type9.folderName]: '#eb7d00'  // Orange
	};

	// Default color if letter type not found
	const DEFAULT_COLOR = '#ffcc00'; // Gold

	// Compute border color based on letter type
	function getBorderColor(): string {
		if (!props.isSelected) {
			return 'transparent';
		}

		const letter = props.pictographData?.letter as Letter | null;
		if (!letter) {
			return DEFAULT_COLOR;
		}

		const letterType = LetterType.getLetterType(letter);
		if (!letterType) {
			return DEFAULT_COLOR;
		}

		return BORDER_COLORS[letterType.folderName] || DEFAULT_COLOR;
	}

	// Use derived values for reactive updates
	const borderColor = $derived(getBorderColor());
	const showBorder = $derived(props.isSelected);
	const borderWidth = $derived(BORDER_WIDTH);
	const glowRadius = $derived(GLOW_RADIUS);
</script>

{#if showBorder}
	<div 
		class="selection-border"
		style="
			--border-color: {borderColor};
			--border-width: {borderWidth}px;
			--glow-radius: {glowRadius}px;
		"
	></div>
{/if}

<style>
	.selection-border {
		position: absolute;
		inset: 2px; /* Inset from the edges of the pictograph */
		border-radius: 6px; /* Slightly rounded corners */
		border: var(--border-width) solid var(--border-color);
		box-shadow: 
			0 0 var(--glow-radius) var(--border-color),
			inset 0 0 var(--glow-radius) var(--border-color);
		pointer-events: none; /* Let events pass through to the pictograph */
		z-index: 5; /* Above the pictograph but below other overlays */
		animation: pulse 2s infinite ease-in-out;
	}

	@keyframes pulse {
		0% {
			box-shadow: 
				0 0 var(--glow-radius) var(--border-color),
				inset 0 0 var(--glow-radius) var(--border-color);
		}
		50% {
			box-shadow: 
				0 0 calc(var(--glow-radius) * 2) var(--border-color),
				inset 0 0 calc(var(--glow-radius) * 1.5) var(--border-color);
		}
		100% {
			box-shadow: 
				0 0 var(--glow-radius) var(--border-color),
				inset 0 0 var(--glow-radius) var(--border-color);
		}
	}
</style>
