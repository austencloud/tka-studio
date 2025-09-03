<script lang="ts">
	import Pictograph from '$lib/components/Pictograph/Pictograph.svelte';
	import type { BeatData } from './BeatData';
	import { defaultPictographData } from '$lib/components/Pictograph/utils/defaultPictographData';
	import StyledBorderOverlay from '$lib/components/Pictograph/components/StyledBorderOverlay.svelte';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';

	// Props using Svelte 5 runes
	const props = $props<{
		beat: BeatData;
		onClick: () => void;
		isStartPosition?: boolean;
	}>();

	// Default values for optional props
	const isStartPosition = $derived(props.isStartPosition ?? false);

	// Derived values
	const pictographData = $derived(props.beat?.pictographData || defaultPictographData);
	const isFilled = $derived(props.beat?.filled ?? false);
	const beatNumber = $derived(props.beat?.beatNumber ?? 0);

	// State
	let showBorder = $state(false);

	// Handle the click event
	function handleClick(event: MouseEvent) {
		event.stopPropagation();

		// Provide haptic feedback when selecting a beat
		if (typeof window !== 'undefined' && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		props.onClick();
	}

	function handleMouseEnter() {
		showBorder = true;
	}

	function handleMouseLeave() {
		showBorder = false;
	}
</script>

<button
	class="beat"
	class:filled={isFilled}
	onclick={handleClick}
	onmouseenter={handleMouseEnter}
	onmouseleave={handleMouseLeave}
	aria-label={`Beat ${beatNumber}`}
>
	<div class="pictograph-wrapper">
		<Pictograph {pictographData} {beatNumber} {isStartPosition} showLoadingIndicator={false} />
		<StyledBorderOverlay {pictographData} isEnabled={showBorder} />
	</div>
</button>

<style>
	.beat {
		width: 100%;
		height: 100%;
		background-color: transparent;
		border: none;
		padding: 0;
		margin: 0;
		cursor: pointer;
		transition: transform 0.2s ease;
		display: flex;
		justify-content: center;
		align-items: center;
		border-radius: 4px;
		min-width: 100%;
		min-height: 100%;
		box-sizing: border-box;
		overflow: visible;
		transform-origin: center center;
	}

	.pictograph-wrapper {
		position: relative;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
