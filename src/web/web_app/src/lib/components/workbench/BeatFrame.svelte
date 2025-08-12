<script lang="ts">
	import type { BeatData } from '$lib/domain';
	import { beatFrameService } from '$lib/services/BeatFrameService.svelte';
	import { createEventDispatcher } from 'svelte';
	import BeatView from './BeatView.svelte';

	interface Props {
		beats: ReadonlyArray<BeatData> | BeatData[];
		startPosition?: BeatData | null;
		selectedBeatIndex?: number;
		onBeatClick?: (index: number) => void;
		onBeatDoubleClick?: (index: number) => void;
		onStartClick?: () => void;
		isScrollable?: boolean;
	}

	let {
		beats,
		startPosition = null,
		selectedBeatIndex = -1,
		onBeatClick,
		onBeatDoubleClick,
		onStartClick,
		isScrollable = false,
	}: Props = $props();

	const config = $derived(beatFrameService.config);
	const hoveredBeatIndex = $derived(beatFrameService.hoveredBeatIndex);
	const frameDimensions = $derived(beatFrameService.calculateFrameDimensions(beats.length));

	const dispatch = createEventDispatcher<{ naturalheightchange: { height: number } }>();

	// TODO: Add responsive sizing later once core functionality is stable
	// For now, use fixed sizing to avoid infinite loops

	// Emit natural height whenever calculated frame dimensions change
	$effect(() => {
		if (frameDimensions?.height != null) {
			dispatch('naturalheightchange', { height: frameDimensions.height });
		}
	});

	function handleBeatClick(index: number) {
		onBeatClick?.(index);
	}

	function handleBeatDoubleClick(index: number) {
		onBeatDoubleClick?.(index);
	}

	function handleBeatHover(index: number) {
		beatFrameService.setHoveredBeat(index);
	}

	function handleBeatLeave() {
		beatFrameService.clearHoveredBeat();
	}
</script>

<div class="beat-frame-container" class:scrollable-active={isScrollable}>
	<div class="beat-frame-scroll">
		<div
			class="beat-frame"
			style:width="{frameDimensions.width}px"
			style:height="{frameDimensions.height}px"
		>
			<!-- Start Position tile at [0,0] when enabled -->
			{#if config.hasStartTile}
				<div
					class="start-tile"
					class:has-pictograph={startPosition?.pictograph_data}
					style:width="{config.beatSize}px"
					style:height="{config.beatSize}px"
					title="Start Position"
					role="button"
					tabindex="0"
					onclick={() => onStartClick?.()}
					onkeydown={(e) => {
						if (e.key === 'Enter' || e.key === ' ') {
							e.preventDefault();
							onStartClick?.();
						}
					}}
					aria-label="Start Position"
				>
					{#if startPosition?.pictograph_data}
						<!-- Display actual start position pictograph -->
						<BeatView
							beat={startPosition}
							index={-1}
							isSelected={false}
							isHovered={false}
						/>
					{:else}
						<!-- Default START label when no start position is set -->
						<div class="start-label">START</div>
					{/if}
				</div>
			{/if}

			{#each beats as beat, index}
				{@const position = beatFrameService.calculateBeatPosition(index)}
				<div
					class="beat-container"
					style:left="{position.x}px"
					style:top="{position.y}px"
					style:width="{config.beatSize}px"
					style:height="{config.beatSize}px"
				>
					<BeatView
						{beat}
						{index}
						isSelected={index === selectedBeatIndex}
						isHovered={index === hoveredBeatIndex}
						onClick={handleBeatClick}
						onDoubleClick={handleBeatDoubleClick}
						onHover={handleBeatHover}
						onLeave={handleBeatLeave}
					/>
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.beat-frame-container {
		position: relative;
		background: transparent;
		border-radius: 12px;
		overflow: hidden;

		border: 1px solid rgba(0, 0, 0, 0.1);
	}

	.beat-frame-scroll {
		overflow: auto;
		background: rgba(255, 255, 255, 0.02);
		display: flex;
		justify-content: center; /* center like Qt AlignCenter */
	}

	/* Scroll mode parity with legacy */
	.beat-frame-container.scrollable-active {
		height: 100%;
		overflow: hidden; /* inner scroll element handles y-scroll */
	}

	.beat-frame-container.scrollable-active .beat-frame-scroll {
		overflow-y: auto;
		overflow-x: hidden;
		align-items: flex-start;
		padding-right: 8px; /* space for scrollbar */
	}

	.beat-frame-container.scrollable-active .beat-frame-scroll::-webkit-scrollbar {
		width: 8px;
		height: 8px;
	}
	.beat-frame-container.scrollable-active .beat-frame-scroll::-webkit-scrollbar-track {
		background: transparent;
	}
	.beat-frame-container.scrollable-active .beat-frame-scroll::-webkit-scrollbar-thumb {
		background-color: rgba(0, 0, 0, 0.3);
		border-radius: 4px;
	}

	.beat-frame {
		position: relative;
		margin: 0; /* legacy parity: no padding/margins on grid area */
		padding: 0;
	}

	.beat-container,
	.start-tile {
		/* zero gaps between cells for parity */
		margin: 0;
	}

	.start-tile {
		position: absolute;
		left: 0;
		top: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 8px;
		font-weight: 700;
		letter-spacing: 0.5px;
	}

	/* Empty start tile styling */
	.start-tile:not(.has-pictograph) {
		border: 2px dashed #ced4da;
		background: #f8f9fa;
		color: #6c757d;
	}

	/* Start tile with pictograph - no border, no background */
	.start-tile.has-pictograph {
		border: none;
	}

	.start-label {
		font-size: 14px;
	}

	.beat-container {
		position: absolute;
		transition: all 0.2s ease;
	}

	/* Subtle grid pattern for parity feel */
	.beat-frame::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-image: radial-gradient(
			circle at 1px 1px,
			rgba(0, 0, 0, 0.05) 1px,
			transparent 0
		);
		background-size: 20px 20px;
		pointer-events: none;
		border-radius: inherit;
	}
</style>
