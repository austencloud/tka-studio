<!--
BeatView Demo Test Route

Test route for E2E BeatView testing with multiple beats and interactions.
-->
<script lang="ts">
	import BeatView from '$lib/components/workbench/BeatView.svelte';
	import { createBeatData, createPictographData } from '$lib/domain';

	// Create sample beats for testing
	const beats = [
		// Beat with pictograph
		createBeatData({
			beat_number: 1,
			pictograph_data: createPictographData({
				letter: 'A',
				grid_data: { mode: 'diamond' },
				arrows: {
					blue: {
						id: 'blue-arrow-1',
						arrow_type: 'blue',
						color: 'blue',
						motion_type: 'pro',
						location: 'n',
						start_orientation: 'in',
						end_orientation: 'out',
						rotation_direction: 'clockwise',
						turns: 1,
						is_mirrored: false,
						coordinates: null,
						rotation_angle: 0,
						svg_center: null,
						svg_mirrored: false,
						metadata: {},
					},
					red: {
						id: 'red-arrow-1',
						arrow_type: 'red',
						color: 'red',
						motion_type: 'anti',
						location: 's',
						start_orientation: 'in',
						end_orientation: 'out',
						rotation_direction: 'counter_clockwise',
						turns: 1,
						is_mirrored: false,
						coordinates: null,
						rotation_angle: 180,
						svg_center: null,
						svg_mirrored: false,
						metadata: {},
					},
				},
			}),
		}),

		// Blank beat
		createBeatData({
			beat_number: 2,
			is_blank: true,
		}),

		// Beat with complex pictograph
		createBeatData({
			beat_number: 3,
			pictograph_data: createPictographData({
				letter: 'Φ',
				grid_data: { mode: 'box' },
				arrows: {
					blue: {
						id: 'blue-arrow-3',
						arrow_type: 'blue',
						color: 'blue',
						motion_type: 'float',
						location: 'ne',
						start_orientation: 'out',
						end_orientation: 'in',
						rotation_direction: 'clockwise',
						turns: 2.5,
						is_mirrored: true,
						coordinates: null,
						rotation_angle: 45,
						svg_center: null,
						svg_mirrored: true,
						metadata: {},
					},
				},
			}),
		}),

		// Beat with reversals
		createBeatData({
			beat_number: 4,
			blue_reversal: true,
			red_reversal: true,
			is_blank: true,
		}),
	];

	// State for testing interactions
	let selectedBeatIndex = -1;
	let hoveredBeatIndex = -1;
	let clickHistory: number[] = [];

	function handleBeatClick(index: number) {
		selectedBeatIndex = index;
		clickHistory = [...clickHistory, index];
		console.log('Beat clicked:', index);
	}

	function handleBeatDoubleClick(index: number) {
		console.log('Beat double-clicked:', index);
		// Toggle selection on double click
		selectedBeatIndex = selectedBeatIndex === index ? -1 : index;
	}

	function handleBeatHover(index: number) {
		hoveredBeatIndex = index;
	}

	function handleBeatLeave() {
		hoveredBeatIndex = -1;
	}
</script>

<svelte:head>
	<title>BeatView Demo Test</title>
</svelte:head>

<main class="test-page">
	<div class="test-wrapper" data-testid="beat-view-demo-test">
		<h1>BeatView Integration Test</h1>

		<!-- Control Panel -->
		<div class="controls" data-testid="controls-panel">
			<div class="control-item">
				<strong>Selected Beat:</strong>
				{selectedBeatIndex === -1 ? 'None' : selectedBeatIndex}
			</div>
			<div class="control-item">
				<strong>Hovered Beat:</strong>
				{hoveredBeatIndex === -1 ? 'None' : hoveredBeatIndex}
			</div>
			<div class="control-item">
				<strong>Click History:</strong> [{clickHistory.join(', ')}]
			</div>
			<button
				onclick={() => {
					selectedBeatIndex = -1;
					hoveredBeatIndex = -1;
					clickHistory = [];
				}}
			>
				Reset
			</button>
		</div>

		<!-- Beat Grid -->
		<div class="beat-grid" data-testid="beat-grid">
			{#each beats as beat, index}
				<div class="beat-wrapper" data-testid="beat-view-{index}">
					<div class="beat-label">Beat {beat.beat_number}</div>
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
					<div class="beat-info">
						<div>Type: {beat.is_blank ? 'Blank' : 'Pictograph'}</div>
						{#if beat.blue_reversal || beat.red_reversal}
							<div>
								Reversals:
								{#if beat.blue_reversal}Blue{/if}
								{#if beat.blue_reversal && beat.red_reversal}
									&
								{/if}
								{#if beat.red_reversal}Red{/if}
							</div>
						{/if}
					</div>
				</div>
			{/each}
		</div>

		<!-- Test Actions -->
		<div class="test-actions" data-testid="test-actions">
			<h2>Test Actions</h2>
			<div class="action-buttons">
				<button onclick={() => handleBeatClick(0)} data-testid="select-beat-0">
					Select Beat 0
				</button>
				<button onclick={() => handleBeatClick(1)} data-testid="select-beat-1">
					Select Beat 1
				</button>
				<button onclick={() => handleBeatHover(2)} data-testid="hover-beat-2">
					Hover Beat 2
				</button>
				<button onclick={() => handleBeatLeave()} data-testid="clear-hover">
					Clear Hover
				</button>
			</div>
		</div>


	</div>
</main>

<style>
	.test-page {
		padding: 1rem;
		min-height: 100vh;
		background: #f8fafc;
		font-family: 'Inter', system-ui, sans-serif;
	}

	.test-wrapper {
		max-width: 1200px;
		margin: 0 auto;
		background: white;
		border-radius: 8px;
		padding: 2rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	h1,
	h2 {
		color: #1f2937;
		margin-bottom: 1rem;
	}

	.controls {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		align-items: center;
		padding: 1rem;
		background: #f8fafc;
		border-radius: 6px;
		margin-bottom: 2rem;
		border: 1px solid #e5e7eb;
	}

	.control-item {
		font-size: 0.875rem;
		color: #4b5563;
	}

	.control-item strong {
		color: #1f2937;
	}

	button {
		padding: 0.5rem 1rem;
		background: #3b82f6;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-weight: 500;
	}

	button:hover {
		background: #2563eb;
	}

	.beat-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 2rem;
		margin-bottom: 2rem;
	}

	.beat-wrapper {
		text-align: center;
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		padding: 1rem;
		background: #fafbfc;
	}

	.beat-label {
		font-weight: 600;
		color: #1f2937;
		margin-bottom: 0.5rem;
	}

	.beat-info {
		margin-top: 0.5rem;
		font-size: 0.75rem;
		color: #6b7280;
	}

	.test-actions {
		margin-bottom: 2rem;
		padding: 1rem;
		background: #f0f9ff;
		border-radius: 6px;
		border: 1px solid #bae6fd;
	}

	.action-buttons {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}


</style>
