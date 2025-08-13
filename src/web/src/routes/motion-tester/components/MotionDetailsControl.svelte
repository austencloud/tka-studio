<script lang="ts">
	import { MotionParameterService } from '../services/MotionParameterService';

	interface Props {
		propLabel: string;
		propColor: string;
		startLocation: string;
		endLocation: string;
		motionType: string;
		turns: number;
		startOrientation: string;
		onMotionTypeChange: (motionType: string) => void;
		onTurnsChange: (turns: number) => void;
		onStartOrientationChange: (orientation: string) => void;
	}

	let { 
		propLabel,
		propColor,
		startLocation,
		endLocation,
		motionType,
		turns,
		startOrientation,
		onMotionTypeChange,
		onTurnsChange,
		onStartOrientationChange
	}: Props = $props();

	const motionService = new MotionParameterService();
	
	// Simplified orientation options (no cardinal directions)
	const orientations = [
		{ value: 'in', label: 'In' },
		{ value: 'out', label: 'Out' },
		{ value: 'clock', label: 'Clock' },
		{ value: 'counter', label: 'Counter' }
	];

	// Get available motion types based on locations
	let availableMotionTypes = $derived(motionService.getAvailableMotionTypes(startLocation, endLocation));

	function incrementTurns() {
		onTurnsChange(Math.min(10, turns + 0.5));
	}

	function decrementTurns() {
		onTurnsChange(Math.max(0, turns - 0.5));
	}
</script>

<div class="motion-details-control">
	<div class="prop-controls-row">
		<div class="prop-header" style="color: {propColor}">
			{propLabel}
		</div>
		<div class="control-group">
			<label for="{propLabel}-motion-type">Motion:</label>
			<select 
				id="{propLabel}-motion-type"
				value={motionType}
				onchange={(e) => onMotionTypeChange(e.currentTarget.value)}
			>
				{#each availableMotionTypes as type}
					<option value={type}>{type.toUpperCase()}</option>
				{/each}
			</select>
		</div>
		<div class="control-group">
			<span class="control-label">Turns:</span>
			<div class="turns-control" role="group" aria-label="Turns control">
				<button onclick={decrementTurns} aria-label="Decrease turns">−</button>
				<span class="turns-value" aria-live="polite">{turns}</span>
				<button onclick={incrementTurns} aria-label="Increase turns">+</button>
			</div>
		</div>
		<div class="control-group">
			<label for="{propLabel}-start-ori">Start Ori:</label>
			<select
				id="{propLabel}-start-ori"
				value={startOrientation}
				onchange={(e) => onStartOrientationChange(e.currentTarget.value)}
			>
				{#each orientations as ori}
					<option value={ori.value}>{ori.label}</option>
				{/each}
			</select>
		</div>
	</div>
</div>

<style>
	.motion-details-control {
		width: 100%;
	}

	.prop-controls-row {
		display: flex;
		align-items: center;
		gap: 12px;
		flex-wrap: wrap;
	}

	.prop-header {
		font-weight: 600;
		font-size: 0.9rem;
		min-width: 60px;
	}

	.control-group {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 0.8rem;
	}

	.control-group label {
		color: #c7d2fe;
		font-size: 0.75rem;
		min-width: 50px;
	}

	.control-group select {
		padding: 4px 6px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 3px;
		background: rgba(255, 255, 255, 0.1);
		color: white;
		font-size: 11px;
		min-width: 70px;
	}

	.control-group select option {
		background: #312e81;
		color: white;
	}

	.turns-control {
		display: flex;
		align-items: center;
		gap: 4px;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 3px;
		padding: 2px;
	}

	.turns-control button {
		background: rgba(99, 102, 241, 0.3);
		border: none;
		color: white;
		width: 20px;
		height: 20px;
		border-radius: 2px;
		cursor: pointer;
		font-size: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.turns-control button:hover {
		background: rgba(99, 102, 241, 0.5);
	}

	.turns-value {
		color: white;
		font-size: 11px;
		min-width: 20px;
		text-align: center;
	}
</style>
