<!--
Detailed Info Panel - Svelte Version
Displays detailed information about the selected beat including metadata and properties.
-->
<script lang="ts">
	// Types
	interface BeatData {
		beat: number;
		letter?: string;
		pictograph_data?: any;
		metadata?: Record<string, any>;
	}

	// State
	let currentBeatIndex: number | null = $state(null);
	let currentBeatData: BeatData | null = $state(null);

	// Derived information
	let displayInfo = $derived(() => {
		if (!currentBeatData) {
			return {
				title: 'No Selection',
				details: [],
			};
		}

		const isStartPosition =
			currentBeatIndex === -1 ||
			currentBeatData.metadata?.is_start_position ||
			currentBeatData.beat === 0 ||
			currentBeatData.letter === 'α';

		const title = isStartPosition ? 'Start Position' : `Beat ${currentBeatData.beat}`;

		const details = [];

		// Beat letter
		if (currentBeatData.letter) {
			details.push({
				label: 'Letter',
				value: currentBeatData.letter,
				important: true,
			});
		}

		// Beat number
		if (!isStartPosition) {
			details.push({
				label: 'Beat #',
				value: currentBeatData.beat.toString(),
				important: false,
			});
		}

		// Motion information
		if (currentBeatData.pictograph_data?.motions) {
			const motions = currentBeatData.pictograph_data.motions;

			if (motions.blue) {
				details.push({
					label: 'Blue Motion',
					value: motions.blue.motion_type || 'Unknown',
					important: false,
				});

				if (motions.blue.turns !== undefined) {
					details.push({
						label: 'Blue Turns',
						value: motions.blue.turns.toString(),
						important: false,
					});
				}
			}

			if (motions.red) {
				details.push({
					label: 'Red Motion',
					value: motions.red.motion_type || 'Unknown',
					important: false,
				});

				if (motions.red.turns !== undefined) {
					details.push({
						label: 'Red Turns',
						value: motions.red.turns.toString(),
						important: false,
					});
				}
			}
		}

		// Grid mode
		if (currentBeatData.pictograph_data?.grid_mode) {
			details.push({
				label: 'Grid Mode',
				value: currentBeatData.pictograph_data.grid_mode,
				important: false,
			});
		}

		// Metadata information
		if (currentBeatData.metadata) {
			Object.entries(currentBeatData.metadata).forEach(([key, value]) => {
				if (key !== 'is_start_position' && value !== null && value !== undefined) {
					details.push({
						label: key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
						value: String(value),
						important: false,
					});
				}
			});
		}

		return { title, details };
	});

	// Public methods
	export function updateBeatInfo(beatIndex: number, beatData: BeatData | null) {
		currentBeatIndex = beatIndex;
		currentBeatData = beatData;

		console.log('ℹ️ [INFO_PANEL] Updated with beat:', beatIndex, beatData?.letter);
	}

	export function clearInfo() {
		currentBeatIndex = null;
		currentBeatData = null;
	}
</script>

<div class="detailed-info-panel">
	<div class="panel-header">
		<h3 class="panel-title">{displayInfo.title}</h3>
	</div>

	<div class="panel-content">
		{#if displayInfo.details.length > 0}
			<div class="info-list">
				{#each displayInfo.details as detail}
					<div class="info-item" class:important={detail.important}>
						<div class="info-label">{detail.label}:</div>
						<div class="info-value">{detail.value}</div>
					</div>
				{/each}
			</div>
		{:else}
			<div class="empty-state">
				<div class="empty-icon">📊</div>
				<div class="empty-text">Select a beat to view details</div>
			</div>
		{/if}
	</div>
</div>

<style>
	.detailed-info-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		backdrop-filter: blur(8px);
		overflow: hidden;
	}

	.panel-header {
		flex-shrink: 0;
		padding: 12px 16px 8px 16px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		background: rgba(255, 255, 255, 0.05);
	}

	.panel-title {
		margin: 0;
		font-size: 1.1rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
		text-align: center;
	}

	.panel-content {
		flex: 1;
		padding: 12px 16px;
		overflow-y: auto;
	}

	.info-list {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.info-item {
		display: flex;
		flex-direction: column;
		gap: 2px;
		padding: 8px;
		border-radius: 6px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		transition: all 0.2s ease;
	}

	.info-item:hover {
		background: rgba(255, 255, 255, 0.08);
		border-color: rgba(255, 255, 255, 0.15);
	}

	.info-item.important {
		background: rgba(70, 130, 255, 0.15);
		border-color: rgba(70, 130, 255, 0.3);
	}

	.info-item.important:hover {
		background: rgba(70, 130, 255, 0.2);
		border-color: rgba(70, 130, 255, 0.4);
	}

	.info-label {
		font-size: 0.75rem;
		font-weight: 500;
		color: rgba(255, 255, 255, 0.7);
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}

	.info-value {
		font-size: 0.9rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
		word-break: break-word;
	}

	.important .info-value {
		color: rgba(70, 130, 255, 1);
		font-size: 1rem;
		font-weight: 700;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		text-align: center;
		color: rgba(255, 255, 255, 0.6);
		gap: 8px;
	}

	.empty-icon {
		font-size: 2rem;
		opacity: 0.5;
	}

	.empty-text {
		font-size: 0.9rem;
		font-weight: 500;
	}

	/* Custom scrollbar for info list */
	.panel-content::-webkit-scrollbar {
		width: 6px;
	}

	.panel-content::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 3px;
	}

	.panel-content::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.2);
		border-radius: 3px;
	}

	.panel-content::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 255, 255, 0.3);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.panel-header {
			padding: 10px 12px 6px 12px;
		}

		.panel-title {
			font-size: 1rem;
		}

		.panel-content {
			padding: 10px 12px;
		}

		.info-item {
			padding: 6px;
		}

		.info-label {
			font-size: 0.7rem;
		}

		.info-value {
			font-size: 0.8rem;
		}

		.important .info-value {
			font-size: 0.9rem;
		}
	}
</style>
