<script lang="ts">
	import { getContext } from 'svelte';
	import type { PictographData } from '$lib/types/PictographData';
	import { optionPickerContainer } from '$lib/state/stores/optionPicker/optionPickerContainer';
	import { LAYOUT_CONTEXT_KEY, type LayoutContext } from '../layoutContext';
	import Pictograph from '$lib/components/Pictograph/Pictograph.svelte';
	import StyledBorderOverlay from '$lib/components/Pictograph/components/StyledBorderOverlay.svelte';

	// Props using Svelte 5 runes
	const props = $props<{
		pictographData: PictographData;
		isPartOfTwoItems?: boolean;
	}>();

	// Default values for optional props
	const isPartOfTwoItems = $derived(props.isPartOfTwoItems ?? false);

	// Consume context
	const layoutContext = getContext<LayoutContext>(LAYOUT_CONTEXT_KEY);

	// Reactive state using Svelte 5 runes
	const isMobileDevice = $derived($layoutContext.isMobile);
	const scaleFactor = $derived($layoutContext.layoutConfig.scaleFactor);
	const isSelected = $derived(
		optionPickerContainer.state.selectedPictograph === props.pictographData
	);
	const ariaLabel = $derived(`Select option ${props.pictographData.letter || 'Unnamed'}`);

	// We'll use a key to force re-render when pictograph data changes
	const pictographKey = $derived(
		`${props.pictographData.letter || ''}-${props.pictographData.startPos || ''}-${props.pictographData.endPos || ''}`
	);

	// Show border state
	let showBorder = $state(false);

	function handleSelect() {
		optionPickerContainer.selectOption(props.pictographData);
	}

	function handleMouseEnter() {
		showBorder = true;
	}

	function handleMouseLeave() {
		showBorder = false;
	}
</script>

<div
	class="option"
	class:mobile={isMobileDevice}
	class:selected={isSelected}
	class:two-item-option={isPartOfTwoItems}
	role="button"
	tabindex="0"
	onclick={handleSelect}
	onkeydown={(e) => e.key === 'Enter' && handleSelect()}
	onmouseenter={handleMouseEnter}
	onmouseleave={handleMouseLeave}
	aria-label={ariaLabel}
	aria-pressed={isSelected}
>
	<div class="pictograph-container" style="transform: scale({scaleFactor})">
		{#key pictographKey}
			<div class="pictograph-wrapper">
				<Pictograph pictographData={props.pictographData} />
				<StyledBorderOverlay
					pictographData={props.pictographData}
					isEnabled={showBorder || isSelected}
					isGold={isSelected}
				/>
			</div>
		{/key}
	</div>
</div>

<style>
	.option {
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
		transition:
			transform 0.2s ease-in-out,
			background-color 0.2s ease;
		border-radius: 6px;
		outline: none;
	}
	.pictograph-container {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100%;
		transition: transform 0.2s ease-in-out;
	}
	.pictograph-wrapper {
		position: relative;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	/* In Option.svelte */
	.option:hover {
		transform: scale(1.1); /* Bump this up from 1.05 */
		background-color: rgba(243, 244, 246, 0.5);
		z-index: 20; /* Add this to ensure it rises above siblings */
	}
	.option:active {
		transform: scale(0.98);
	}
	.option.selected {
		background-color: rgba(56, 161, 105, 0.1);
	}
	.option.two-item-option {
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
	}
	.option.two-item-option:hover {
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	}
	.option.mobile {
		transition: transform 0.15s ease-in-out;
	}
	.option.mobile:hover {
		transform: scale(1.03);
	}
	.option:focus-visible {
		box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.6);
		z-index: 11;
	}
</style>
