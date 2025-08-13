<script lang="ts">
	import type { MotionTesterState } from './state/motion-tester-state.svelte.ts';

	interface Props {
		state: MotionTesterState;
	}

	let { state }: Props = $props();

	// Helper function to determine motion type based on start/end locations
	function getMotionType(startLoc: string, endLoc: string): string {
		if (startLoc === endLoc) {
			return 'static'; // Same location = static
		}

		// Check if it's a dash motion (opposite locations)
		const opposites = [
			['n', 's'], ['s', 'n'],
			['e', 'w'], ['w', 'e']
		];

		for (const [start, end] of opposites) {
			if (startLoc === start && endLoc === end) {
				return 'dash';
			}
		}

		// Adjacent locations = shift motion (pro/anti/float)
		return 'pro'; // Default to pro for shift motions
	}

	// Helper function to get available motion types for a start/end pair
	function getAvailableMotionTypes(startLoc: string, endLoc: string): string[] {
		const motionType = getMotionType(startLoc, endLoc);

		if (motionType === 'static') {
			return ['static'];
		} else if (motionType === 'dash') {
			return ['dash'];
		} else {
			// Shift motions can be pro, anti, or float
			return ['pro', 'anti', 'float'];
		}
	}

	// Location options for visual selector
	const locations = ['n', 'e', 's', 'w'];
	const motionTypes = ['pro', 'anti', 'float', 'dash'];
	const orientations = ['in', 'out', 'clock', 'counter'];

	// Visual position mapping for location display in the path grid
	const locationPositions: Record<string, any> = {
		n: { top: '15%', left: '50%', transform: 'translateX(-50%)' },
		e: { top: '50%', right: '15%', transform: 'translateY(-50%)' },
		s: { bottom: '15%', left: '50%', transform: 'translateX(-50%)' },
		w: { top: '50%', left: '15%', transform: 'translateY(-50%)' }
	};

	// Get motion description for display
	function getMotionDescription(startLoc: string, endLoc: string, motionType: string, turns: number): string {
		const direction = startLoc === endLoc ? 'STATIC' : `${startLoc.toUpperCase()}→${endLoc.toUpperCase()}`;
		const rotation = getRotationDirection(startLoc, endLoc, motionType, turns);
		return `${direction} ${motionType.toUpperCase()} ${turns}T ${rotation}`;
	}

	// Get rotation direction for display
	function getRotationDirection(startLoc: string, endLoc: string, motionType: string, turns: number): string {
		if (startLoc === endLoc) return 'NO_ROT';
		if (motionType === 'dash') return 'NO_ROT';
		if (turns === 0) return 'NO_ROT';

		// Simplified rotation logic for display
		const clockwisePairs = [['n', 'e'], ['e', 's'], ['s', 'w'], ['w', 'n']];
		const isClockwise = clockwisePairs.some(([start, end]) => start === startLoc && end === endLoc);

		if (motionType === 'pro') {
			return isClockwise ? 'CW' : 'CCW';
		} else {
			return isClockwise ? 'CCW' : 'CW';
		}
	}

	// Handle location selection with smart logic
	function handleLocationClick(prop: 'blue' | 'red', location: string) {
		const params = prop === 'blue' ? state.blueMotionParams : state.redMotionParams;

		if (params.startLoc === location) {
			// Clicking start location makes it the end location
			if (prop === 'blue') {
				state.updateBlueMotionParam('endLoc', location);
			} else {
				state.updateRedMotionParam('endLoc', location);
			}
		} else if (params.endLoc === location) {
			// Clicking end location makes it the start location
			if (prop === 'blue') {
				state.updateBlueMotionParam('startLoc', location);
			} else {
				state.updateRedMotionParam('startLoc', location);
			}
		} else {
			// Clicking empty location makes it the end location
			if (prop === 'blue') {
				state.updateBlueMotionParam('endLoc', location);
			} else {
				state.updateRedMotionParam('endLoc', location);
			}
		}
	}

</script>

<div class="motion-params-panel">
	<h2>🎯 Motion Designer</h2>

	<!-- Blue Prop Motion Card -->
	<div class="motion-card blue-card">
		<div class="card-header">
			<div class="prop-indicator blue">
				<span class="prop-icon">🔵</span>
				<span class="prop-label">Blue Prop</span>
			</div>
			<div class="motion-summary">
				{getMotionDescription(
					state.blueMotionParams.startLoc,
					state.blueMotionParams.endLoc,
					state.blueMotionParams.motionType,
					state.blueMotionParams.turns
				)}
			</div>
		</div>

		<!-- Location Selectors -->
		<div class="location-selectors">
			<div class="location-group">
				<label for="blue-start-location">Start Location</label>
				<select id="blue-start-location" bind:value={state.blueMotionParams.startLoc}>
					{#each locations as location}
						<option value={location}>{location.toUpperCase()}</option>
					{/each}
				</select>
			</div>
			<div class="location-group">
				<label for="blue-end-location">End Location</label>
				<select id="blue-end-location" bind:value={state.blueMotionParams.endLoc}>
					{#each locations as location}
						<option value={location}>{location.toUpperCase()}</option>
					{/each}
				</select>
			</div>
		</div>

		<!-- Motion Parameters -->
		<div class="motion-params">
			<div class="param-group">
				<label>Motion Type</label>
				<div class="motion-type-selector" role="group" aria-label="Blue prop motion type">
					{#each motionTypes as type}
						<button
							class="motion-type-btn {state.blueMotionParams.motionType === type ? 'active' : ''}"
							onclick={() => state.updateBlueMotionParam('motionType', type)}
						>
							{type.toUpperCase()}
						</button>
					{/each}
				</div>
			</div>

			<div class="param-row">
				<div class="param-group">
					<span class="param-label">Turns</span>
					<div class="turns-control" role="group" aria-label="Blue prop turns">
						<button onclick={() => state.updateBlueMotionParam('turns', Math.max(0, state.blueMotionParams.turns - 1))}>−</button>
						<span class="turns-value">{state.blueMotionParams.turns}</span>
						<button onclick={() => state.updateBlueMotionParam('turns', state.blueMotionParams.turns + 1)}>+</button>
					</div>
				</div>

				<div class="param-group">
					<label for="blue-start-orientation">Start Orientation</label>
					<select id="blue-start-orientation" bind:value={state.blueMotionParams.startOri}>
						{#each orientations as orientation}
							<option value={orientation}>{orientation.charAt(0).toUpperCase() + orientation.slice(1)}</option>
						{/each}
					</select>
				</div>
			</div>
		</div>
	</div>
	<!-- Red Prop Motion Card -->
	<div class="motion-card red-card">
		<div class="card-header">
			<div class="prop-indicator red">
				<span class="prop-icon">🔴</span>
				<span class="prop-label">Red Prop</span>
			</div>
			<div class="motion-summary">
				{getMotionDescription(
					state.redMotionParams.startLoc,
					state.redMotionParams.endLoc,
					state.redMotionParams.motionType,
					state.redMotionParams.turns
				)}
			</div>
		</div>

		<!-- Location Selectors -->
		<div class="location-selectors">
			<div class="location-group">
				<label for="red-start-location">Start Location</label>
				<select id="red-start-location" bind:value={state.redMotionParams.startLoc}>
					{#each locations as location}
						<option value={location}>{location.toUpperCase()}</option>
					{/each}
				</select>
			</div>
			<div class="location-group">
				<label for="red-end-location">End Location</label>
				<select id="red-end-location" bind:value={state.redMotionParams.endLoc}>
					{#each locations as location}
						<option value={location}>{location.toUpperCase()}</option>
					{/each}
				</select>
			</div>
		</div>

		<!-- Motion Parameters -->
		<div class="motion-params">
			<div class="param-group">
				<span class="param-label">Motion Type</span>
				<div class="motion-type-selector" role="group" aria-label="Red prop motion type">
					{#each motionTypes as type}
						<button
							class="motion-type-btn {state.redMotionParams.motionType === type ? 'active' : ''}"
							onclick={() => state.updateRedMotionParam('motionType', type)}
						>
							{type.toUpperCase()}
						</button>
					{/each}
				</div>
			</div>

			<div class="param-row">
				<div class="param-group">
					<label>Turns</label>
					<div class="turns-control">
						<button onclick={() => state.updateRedMotionParam('turns', Math.max(0, state.redMotionParams.turns - 1))}>−</button>
						<span class="turns-value">{state.redMotionParams.turns}</span>
						<button onclick={() => state.updateRedMotionParam('turns', state.redMotionParams.turns + 1)}>+</button>
					</div>
				</div>

				<div class="param-group">
					<label>Start Orientation</label>
					<select bind:value={state.redMotionParams.startOri} onchange={(e) => state.updateRedMotionParam('startOri', e.target.value)}>
						{#each orientations as orientation}
							<option value={orientation}>{orientation.charAt(0).toUpperCase() + orientation.slice(1)}</option>
						{/each}
					</select>
				</div>
			</div>
		</div>
	</div>

	<!-- Quick Test Section -->
	<div class="quick-tests-section">
		<h3>⚡ Quick Tests</h3>
		<div class="quick-tests">
			<button class="quick-test-btn" onclick={() => {
				state.updateBlueMotionParam('startLoc', 'n');
				state.updateBlueMotionParam('endLoc', 'e');
				state.updateBlueMotionParam('motionType', 'pro');
				state.updateBlueMotionParam('turns', 1);
			}}>N→E PRO</button>
			<button class="quick-test-btn" onclick={() => {
				state.updateBlueMotionParam('startLoc', 'e');
				state.updateBlueMotionParam('endLoc', 'w');
				state.updateBlueMotionParam('motionType', 'dash');
				state.updateBlueMotionParam('turns', 0);
			}}>E→W DASH</button>
			<button class="quick-test-btn" onclick={() => {
				state.updateBlueMotionParam('startLoc', 's');
				state.updateBlueMotionParam('endLoc', 'w');
				state.updateBlueMotionParam('motionType', 'anti');
				state.updateBlueMotionParam('turns', 1);
			}}>S→W ANTI</button>
			<button class="quick-test-btn" onclick={() => {
				state.updateBlueMotionParam('startLoc', 'n');
				state.updateBlueMotionParam('endLoc', 's');
				state.updateBlueMotionParam('motionType', 'float');
				state.updateBlueMotionParam('turns', 0);
			}}>N→S FLOAT</button>
		</div>
	</div>

</div>

<style>
	.motion-params-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		gap: 20px;
		padding: 20px;
		box-sizing: border-box;
		overflow-y: auto;
	}

	h2 {
		margin: 0 0 20px 0;
		color: #e0e7ff;
		font-size: 1.3rem;
		font-weight: 700;
		text-align: center;
		background: linear-gradient(135deg, #6366f1, #8b5cf6);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	/* Motion Card Styles */
	.motion-card {
		background: linear-gradient(135deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.1));
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 20px;
		margin-bottom: 20px;
		backdrop-filter: blur(10px);
		transition: all 0.3s ease;
	}

	.motion-card:hover {
		border-color: rgba(255, 255, 255, 0.2);
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
	}

	.blue-card {
		border-left: 4px solid #60a5fa;
	}

	.red-card {
		border-left: 4px solid #f87171;
	}

	/* Card Header */
	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20px;
		padding-bottom: 15px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.prop-indicator {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.prop-icon {
		font-size: 1.2rem;
	}

	.prop-label {
		font-weight: 600;
		color: #e0e7ff;
		font-size: 1.1rem;
	}

	.motion-summary {
		background: rgba(99, 102, 241, 0.2);
		border: 1px solid rgba(99, 102, 241, 0.3);
		border-radius: 8px;
		padding: 8px 16px;
		color: #c7d2fe;
		font-size: 13px;
		font-weight: 600;
		font-family: 'Courier New', monospace;
	}

	/* Location Selectors */
	.location-selectors {
		margin-bottom: 20px;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 15px;
	}

	.location-group {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.location-group label {
		color: #c7d2fe;
		font-size: 14px;
		font-weight: 600;
	}

	.location-group select {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		color: white;
		padding: 10px 12px;
		font-size: 14px;
		transition: all 0.2s ease;
	}

	.location-group select:focus {
		outline: none;
		border-color: rgba(99, 102, 241, 0.5);
		box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
	}

	/* Motion Parameters */
	.motion-params {
		display: flex;
		flex-direction: column;
		gap: 15px;
	}

	.param-group {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.param-group label {
		color: #c7d2fe;
		font-size: 14px;
		font-weight: 600;
	}

	.motion-type-selector {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;
	}

	.motion-type-btn {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		color: #e0e7ff;
		padding: 10px 15px;
		cursor: pointer;
		font-size: 13px;
		font-weight: 600;
		transition: all 0.2s ease;
	}

	.motion-type-btn:hover {
		background: rgba(99, 102, 241, 0.2);
		border-color: rgba(99, 102, 241, 0.4);
	}

	.motion-type-btn.active {
		background: rgba(99, 102, 241, 0.4);
		border-color: rgba(99, 102, 241, 0.6);
		box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
	}

	.param-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 15px;
	}

	.turns-control {
		display: flex;
		align-items: center;
		gap: 10px;
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		padding: 8px;
	}

	.turns-control button {
		background: rgba(99, 102, 241, 0.3);
		border: 1px solid rgba(99, 102, 241, 0.5);
		border-radius: 4px;
		color: white;
		width: 30px;
		height: 30px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		font-size: 16px;
		font-weight: bold;
		transition: all 0.2s ease;
	}

	.turns-control button:hover {
		background: rgba(99, 102, 241, 0.5);
		transform: scale(1.1);
	}

	.turns-value {
		color: white;
		font-weight: 600;
		min-width: 30px;
		text-align: center;
		font-size: 16px;
	}

	.param-group select {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		color: white;
		padding: 10px 12px;
		font-size: 14px;
		transition: all 0.2s ease;
	}

	.param-group select:focus {
		outline: none;
		border-color: rgba(99, 102, 241, 0.5);
		box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
	}

	/* Quick Tests */
	.quick-tests-section {
		background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05));
		border: 1px solid rgba(34, 197, 94, 0.2);
		border-radius: 12px;
		padding: 20px;
		margin-top: 10px;
	}

	.quick-tests-section h3 {
		margin: 0 0 15px 0;
		color: #bbf7d0;
		font-size: 1rem;
		font-weight: 600;
	}

	.quick-tests {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 10px;
	}

	.quick-test-btn {
		background: rgba(34, 197, 94, 0.2);
		border: 1px solid rgba(34, 197, 94, 0.3);
		border-radius: 6px;
		color: #bbf7d0;
		padding: 12px 16px;
		cursor: pointer;
		font-size: 13px;
		font-weight: 600;
		transition: all 0.2s ease;
	}

	.quick-test-btn:hover {
		background: rgba(34, 197, 94, 0.3);
		border-color: rgba(34, 197, 94, 0.5);
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
	}
</style>
