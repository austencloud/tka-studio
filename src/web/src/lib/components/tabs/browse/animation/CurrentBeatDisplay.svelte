<!--
Current Beat Display Component

Shows current beat information including letter and motion details.
-->
<script lang="ts">
	// Props
	const {
		currentBeat = 0,
		sequenceData = null
	} = $props<{
		currentBeat?: number;
		sequenceData?: any;
	}>();

	// Computed current beat data
	let currentBeatData = $derived(
		sequenceData?.beats && sequenceData.beats[Math.floor(currentBeat)] 
			? sequenceData.beats[Math.floor(currentBeat)]
			: null
	);
</script>

{#if currentBeatData}
	<div class="current-beat-display">
		<h5>
			Beat {Math.floor(currentBeat) + 1}: {currentBeatData.pictograph_data?.letter || ''}
		</h5>

		{#if currentBeatData.pictograph_data?.motions}
			<div class="motions-display">
				<div class="motion blue-motion">
					<h6>Blue Prop</h6>
					<div class="motion-info">
						<span class="location">
							{currentBeatData.pictograph_data.motions.blue?.start_loc} →
							{currentBeatData.pictograph_data.motions.blue?.end_loc}
						</span>
						<span class="motion-type">
							{currentBeatData.pictograph_data.motions.blue?.motion_type}
						</span>
					</div>
				</div>

				<div class="motion red-motion">
					<h6>Red Prop</h6>
					<div class="motion-info">
						<span class="location">
							{currentBeatData.pictograph_data.motions.red?.start_loc} →
							{currentBeatData.pictograph_data.motions.red?.end_loc}
						</span>
						<span class="motion-type">
							{currentBeatData.pictograph_data.motions.red?.motion_type}
						</span>
					</div>
				</div>
			</div>
		{/if}
	</div>
{/if}

<style>
	.current-beat-display {
		background: linear-gradient(135deg, 
			rgba(255, 255, 255, 0.08) 0%, 
			rgba(255, 255, 255, 0.04) 100%);
		border: 1px solid rgba(255, 255, 255, 0.1);
		padding: 1.25rem;
		border-radius: 16px;
		backdrop-filter: blur(15px);
		box-shadow: 
			0 4px 16px rgba(0, 0, 0, 0.1),
			inset 0 1px 0 rgba(255, 255, 255, 0.1);
	}

	.current-beat-display h5 {
		margin: 0 0 1rem 0;
		font-size: 1.125rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.motions-display {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.motion {
		padding: 1rem;
		border-radius: 12px;
		border-left: 4px solid;
		background: rgba(255, 255, 255, 0.04);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.08);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.motion:hover {
		background: rgba(255, 255, 255, 0.08);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	.blue-motion {
		border-left-color: #60a5fa;
		box-shadow: inset 4px 0 0 #60a5fa;
	}

	.red-motion {
		border-left-color: #f87171;
		box-shadow: inset 4px 0 0 #f87171;
	}

	.motion h6 {
		margin: 0 0 0.75rem 0;
		font-size: 0.875rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.9);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.motion-info {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		font-size: 0.8125rem;
	}

	.location {
		font-weight: 500;
		color: rgba(255, 255, 255, 0.85);
	}

	.motion-type {
		color: rgba(255, 255, 255, 0.6);
		text-transform: capitalize;
		font-style: italic;
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.motion {
			transition: none;
		}
	}
</style>
