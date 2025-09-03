<!-- src/lib/components/Pictograph/components/StyledBorderOverlay.svelte -->
<script lang="ts">
	import { LetterType } from '$lib/types/LetterType';
	import type { Letter } from '$lib/types/Letter';
	import type { PictographData } from '$lib/types/PictographData';

	// Props using Svelte 5 runes
	const props = $props<{
		pictographData: PictographData;
		isEnabled?: boolean;
		isGold?: boolean;
	}>();

	// Constants
	const GOLD = '#FFD700';
	const OUTER_BORDER_WIDTH = 2;
	const INNER_BORDER_WIDTH = 2;

	// Border colors map for different letter types
	const BORDER_COLORS = {
		[LetterType.Type1.folderName]: ['#36c3ff', '#6F2DA8'], // Cyan, Purple
		[LetterType.Type2.folderName]: ['#6F2DA8', '#6F2DA8'], // Purple, Purple
		[LetterType.Type3.folderName]: ['#26e600', '#6F2DA8'], // Green, Purple
		[LetterType.Type4.folderName]: ['#26e600', '#26e600'], // Green, Green
		[LetterType.Type5.folderName]: ['#00b3ff', '#26e600'], // Cyan, Green
		[LetterType.Type6.folderName]: ['#eb7d00', '#eb7d00'], // Orange, Orange
		[LetterType.Type7.folderName]: ['#6F2DA8', '#36c3ff'], // Purple, Cyan
		[LetterType.Type8.folderName]: ['#26e600', '#36c3ff'], // Green, Cyan
		[LetterType.Type9.folderName]: ['#eb7d00', '#36c3ff'] // Orange, Cyan
	};

	// Compute border colors based on props
	function getBorderColors() {
		// Default to no border
		if (!props.isEnabled) {
			return { primary: null, secondary: null };
		}

		// Gold border takes precedence
		if (props.isGold) {
			return { primary: GOLD, secondary: GOLD };
		}

		// Get colors based on letter type
		const letter = props.pictographData?.letter as Letter | null;
		if (!letter) {
			return { primary: null, secondary: null };
		}

		const letterType = LetterType.getLetterType(letter);
		if (!letterType) {
			return { primary: null, secondary: null };
		}

		const [primary, secondary] = BORDER_COLORS[letterType.folderName] || ['#000000', '#000000'];
		return {
			primary,
			secondary: primary !== secondary ? secondary : null
		};
	}

	// Use separate derived values to avoid TypeScript issues
	const { primary, secondary } = $derived(getBorderColors());
	const showBorder = $derived(!!primary);
	const outerWidth = $derived(OUTER_BORDER_WIDTH);
	const innerWidth = $derived(INNER_BORDER_WIDTH);
</script>

{#if showBorder}
	<div class="border-overlay">
		<div class="outer-border" style="border-color: {primary}; border-width: {outerWidth}px;">
			{#if secondary}
				<div
					class="inner-border"
					style="border-color: {secondary}; border-width: {innerWidth}px;"
				></div>
			{/if}
		</div>
	</div>
{/if}

<style>
	.border-overlay {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		z-index: 10;
	}

	.outer-border {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		box-sizing: border-box;
		border-style: solid;
		border-radius: 4px;
	}

	.inner-border {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		box-sizing: border-box;
		border-style: solid;
		border-radius: 2px;
	}
</style>
