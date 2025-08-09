<!--
Dual Orientation Picker - Svelte Version
Provides dual blue/red orientation selection panels for start position configuration.
-->
<script lang="ts">
	// Types
	interface BeatData {
		beat: number;
		letter?: string;
		pictograph_data?: any;
		metadata?: Record<string, any>;
	}

	enum Orientation {
		IN = 'in',
		OUT = 'out',
		CLOCK = 'clock',
		COUNTER = 'counter',
	}

	// Props
	interface Props {
		onOrientationChanged?: (color: string, orientation: Orientation) => void;
		onBeatDataUpdated?: (beatData: BeatData) => void;
	}

	let { onOrientationChanged, onBeatDataUpdated }: Props = $props();

	// State
	let currentBeatData: BeatData | null = $state(null);
	let blueOrientation: Orientation = $state(Orientation.IN);
	let redOrientation: Orientation = $state(Orientation.IN);

	// Available orientations
	const orientations = [Orientation.IN, Orientation.OUT, Orientation.CLOCK, Orientation.COUNTER];

	// Handle orientation selection
	function setOrientation(color: 'blue' | 'red', orientation: Orientation) {
		if (color === 'blue') {
			blueOrientation = orientation;
		} else {
			redOrientation = orientation;
		}

		onOrientationChanged?.(color, orientation);
		console.log('🧭 [ORIENTATION_PICKER]', color, 'orientation set to:', orientation);
	}

	// Public methods
	export function setBeatData(beatData: BeatData | null) {
		currentBeatData = beatData;

		if (beatData) {
			// Extract current orientations from beat data
			if (beatData.pictograph_data?.motions?.blue) {
				const blueOri = beatData.pictograph_data.motions.blue.start_ori;
				if (blueOri) {
					try {
						blueOrientation =
							typeof blueOri === 'string'
								? Orientation[blueOri.toUpperCase() as keyof typeof Orientation] ||
									Orientation.IN
								: blueOri;
					} catch {
						blueOrientation = Orientation.IN;
					}
				} else {
					blueOrientation = Orientation.IN;
				}
			} else {
				blueOrientation = Orientation.IN;
			}

			if (beatData.pictograph_data?.motions?.red) {
				const redOri = beatData.pictograph_data.motions.red.start_ori;
				if (redOri) {
					try {
						redOrientation =
							typeof redOri === 'string'
								? Orientation[redOri.toUpperCase() as keyof typeof Orientation] ||
									Orientation.IN
								: redOri;
					} catch {
						redOrientation = Orientation.IN;
					}
				} else {
					redOrientation = Orientation.IN;
				}
			} else {
				redOrientation = Orientation.IN;
			}
		} else {
			// Reset to defaults
			blueOrientation = Orientation.IN;
			redOrientation = Orientation.IN;
		}

		console.log('🧭 [ORIENTATION_PICKER] Beat data set, orientations:', {
			blue: blueOrientation,
			red: redOrientation,
		});
	}

	export function getBlueOrientation(): Orientation {
		return blueOrientation;
	}

	export function getRedOrientation(): Orientation {
		return redOrientation;
	}

	export function setBlueOrientation(orientation: Orientation) {
		setOrientation('blue', orientation);
	}

	export function setRedOrientation(orientation: Orientation) {
		setOrientation('red', orientation);
	}

	export function resetOrientations() {
		setOrientation('blue', Orientation.IN);
		setOrientation('red', Orientation.IN);
	}

	export function getCurrentBeatData(): BeatData | null {
		return currentBeatData;
	}
</script>

<div class="dual-orientation-picker">
	<!-- Blue orientation picker (left side) -->
	<div class="orientation-panel blue-panel">
		<div class="panel-header">
			<h4>Blue Orientation</h4>
		</div>

		<!-- Current orientation display -->
		<div class="current-orientation blue-display">
			{blueOrientation.toUpperCase()}
		</div>

		<!-- Orientation selection buttons -->
		<div class="orientation-buttons">
			{#each orientations as orientation}
				<button
					class="orientation-btn blue-btn"
					class:active={blueOrientation === orientation}
					onclick={() => setOrientation('blue', orientation)}
					type="button"
				>
					{orientation.toUpperCase()}
				</button>
			{/each}
		</div>
	</div>

	<!-- Red orientation picker (right side) -->
	<div class="orientation-panel red-panel">
		<div class="panel-header">
			<h4>Red Orientation</h4>
		</div>

		<!-- Current orientation display -->
		<div class="current-orientation red-display">
			{redOrientation.toUpperCase()}
		</div>

		<!-- Orientation selection buttons -->
		<div class="orientation-buttons">
			{#each orientations as orientation}
				<button
					class="orientation-btn red-btn"
					class:active={redOrientation === orientation}
					onclick={() => setOrientation('red', orientation)}
					type="button"
				>
					{orientation.toUpperCase()}
				</button>
			{/each}
		</div>
	</div>
</div>

<style>
	.dual-orientation-picker {
		display: flex;
		height: 100%;
		gap: 10px;
		padding: 0;
	}

	.orientation-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 10px;
		padding: 10px;
		gap: 8px;
		backdrop-filter: blur(8px);
	}

	.blue-panel {
		border-color: rgba(0, 102, 204, 0.4);
		background: rgba(0, 102, 204, 0.05);
	}

	.red-panel {
		border-color: rgba(204, 0, 0, 0.4);
		background: rgba(204, 0, 0, 0.05);
	}

	.panel-header {
		text-align: center;
		margin-bottom: 4px;
	}

	.panel-header h4 {
		margin: 0;
		font-size: 0.9rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.9);
	}

	.current-orientation {
		background: rgba(255, 255, 255, 0.9);
		border-radius: 6px;
		padding: 12px;
		text-align: center;
		font-weight: bold;
		font-size: 1rem;
		min-height: 20px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.blue-display {
		border: 2px solid #0066cc;
		color: #0066cc;
	}

	.red-display {
		border: 2px solid #cc0000;
		color: #cc0000;
	}

	.orientation-buttons {
		display: flex;
		flex-wrap: wrap;
		gap: 5px;
		flex: 1;
	}

	.orientation-btn {
		flex: 1;
		min-width: 45px;
		height: 35px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		background: rgba(255, 255, 255, 0.1);
		color: rgba(255, 255, 255, 0.9);
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.orientation-btn:hover {
		background: rgba(255, 255, 255, 0.2);
		border-color: rgba(255, 255, 255, 0.5);
	}

	.blue-btn.active {
		background: rgba(0, 102, 204, 0.8);
		border-color: #0066cc;
		color: white;
	}

	.blue-btn.active:hover {
		background: rgba(0, 102, 204, 0.9);
	}

	.red-btn.active {
		background: rgba(204, 0, 0, 0.8);
		border-color: #cc0000;
		color: white;
	}

	.red-btn.active:hover {
		background: rgba(204, 0, 0, 0.9);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.dual-orientation-picker {
			flex-direction: column;
			gap: 8px;
		}

		.orientation-panel {
			flex: none;
			min-height: 120px;
		}

		.panel-header h4 {
			font-size: 0.8rem;
		}

		.current-orientation {
			padding: 8px;
			font-size: 0.9rem;
		}

		.orientation-btn {
			height: 30px;
			font-size: 0.7rem;
		}
	}
</style>
