<script lang="ts">
	import { ModernPictograph } from '$lib/components/pictograph';
	import type { BeatData } from '$lib/domain';
	import { beatFrameService } from '$lib/services/BeatFrameService.svelte';

	interface Props {
		beat: BeatData;
		index: number;
		isSelected?: boolean;
		isHovered?: boolean;
		onClick?: (index: number) => void;
		onDoubleClick?: (index: number) => void;
		onHover?: (index: number) => void;
		onLeave?: () => void;
	}

	let {
		beat,
		index,
		isSelected = false,
		isHovered = false,
		onClick,
		onDoubleClick,
		onHover,
		onLeave,
	}: Props = $props();

	const config = $derived(beatFrameService.config);
	const displayText = $derived(
		beat.is_blank && !beat.pictograph_data
			? (beat.beat_number ?? index + 1).toString()
			: (beat.pictograph_data?.letter ??
					beat.metadata?.letter ??
					(beat.beat_number ?? index + 1).toString())
	);

	function handleClick() {
		onClick?.(index);
	}

	function handleDoubleClick() {
		onDoubleClick?.(index);
	}

	function handleMouseEnter() {
		onHover?.(index);
	}

	function handleMouseLeave() {
		onLeave?.();
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			onClick?.(index);
		}
	}
</script>

<div
	class="beat-view"
	class:selected={isSelected}
	class:hovered={isHovered}
	class:blank={beat.is_blank}
	class:has-pictograph={beat.pictograph_data != null}
	style:width="{config.beatSize}px"
	style:height="{config.beatSize}px"
	style="position: relative; display: flex; align-items: center; justify-content: center;"
	onclick={handleClick}
	ondblclick={handleDoubleClick}
	onkeypress={handleKeyPress}
	onmouseenter={handleMouseEnter}
	onmouseleave={handleMouseLeave}
	role="button"
	tabindex="0"
	aria-label="Beat {beat.beat_number ?? index + 1}"
>
	<div class="beat-content">
		{#if beat.pictograph_data}
			<!-- Render actual pictograph using ModernPictograph component -->
			<div class="pictograph-container">
				<ModernPictograph
					beatData={beat}
					width={config.beatSize - 8}
					height={config.beatSize - 8}
					onClick={handleClick}
					debug={false}
				/>
			</div>
		{:else}
			<div class="beat-number">
				{displayText}
			</div>
		{/if}
	</div>

	{#if beat.blue_reversal || beat.red_reversal}
		<div class="reversal-indicators">
			{#if beat.blue_reversal}
				<div class="reversal blue"></div>
			{/if}
			{#if beat.red_reversal}
				<div class="reversal red"></div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.beat-view {
		position: relative;
		border: 1px solid #d0d7de;
		border-radius: 6px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: border-color 0.15s ease;
		background: transparent;
		user-select: none;
	}

	.beat-view:hover,
	.beat-view.hovered {
		border-color: #6ea8fe;
	}

	.beat-view.selected {
		border-color: #28a745;
		box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2);
	}

	.beat-view.blank {
		background: #f8f9fa;
		border-style: dashed;
	}

	.beat-view.has-pictograph {
		background: transparent;
	}

	.beat-content {
		text-align: center;
		font-weight: 600;
	}

	.beat-number {
		font-size: 16px;
		color: #6c757d;
	}

	.pictograph-container {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
		border-radius: 4px;
		overflow: hidden;
	}

	.pictograph-container :global(.modern-pictograph) {
		border: none;
		border-radius: 4px;
	}

	.reversal-indicators {
		position: absolute;
		top: 4px;
		right: 4px;
		display: flex;
		gap: 2px;
	}

	.reversal {
		width: 8px;
		height: 8px;
		border-radius: 50%;
	}

	.reversal.blue {
		background: #007bff;
	}

	.reversal.red {
		background: #dc3545;
	}

	/* Focus styles for accessibility */
	.beat-view:focus {
		outline: none;
		border-color: #007bff;
		box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
	}
</style>
