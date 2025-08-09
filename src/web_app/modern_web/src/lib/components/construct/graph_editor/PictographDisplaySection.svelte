<!--
Pictograph Display Section - Svelte Version
Manages the top section of the graph editor containing the large pictograph display
and detailed information panel.
-->
<script lang="ts">
	import DetailedInfoPanel from './DetailedInfoPanel.svelte';

	// Types
	interface BeatData {
		beat: number;
		letter?: string;
		pictograph_data?: any;
		metadata?: Record<string, any>;
	}

	// Props
	interface Props {
		onPictographUpdated?: (beatIndex: number, beatData: BeatData) => void;
	}

	let { onPictographUpdated }: Props = $props();

	// State
	let currentBeatIndex: number | null = $state(null);
	let currentBeatData: BeatData | null = $state(null);
	let currentPictographSize = $state(280);

	// Responsive sizing configuration
	const minPictographSize = 200;
	const maxPictographSize = 500;
	const infoPanelMinWidth = 180;
	const infoPanelMaxWidth = 250;

	// Component references
	let pictographContainer: HTMLDivElement;
	let infoPanelRef: DetailedInfoPanel;

	// Calculate optimal pictograph size based on container
	function calculateOptimalPictographSize(containerWidth: number): number {
		if (containerWidth <= 0) {
			return currentPictographSize;
		}

		const reservedSpace = infoPanelMinWidth + 15 + 16; // info panel + spacing + margins
		const availableWidth = containerWidth - reservedSpace;

		return Math.max(minPictographSize, Math.min(maxPictographSize, availableWidth));
	}

	// Update pictograph size dynamically
	function updatePictographSize(newSize: number) {
		if (newSize === currentPictographSize) return;

		currentPictographSize = newSize;
		console.log('📐 [PICTOGRAPH_DISPLAY] Size updated to:', newSize);
	}

	// Handle container resize
	function handleResize() {
		if (pictographContainer) {
			const containerWidth = pictographContainer.offsetWidth;
			const newSize = calculateOptimalPictographSize(containerWidth);

			if (Math.abs(newSize - currentPictographSize) > 5) {
				updatePictographSize(newSize);
			}
		}
	}

	// Public methods
	export function updateDisplay(beatIndex: number, beatData: BeatData | null) {
		currentBeatIndex = beatIndex;
		currentBeatData = beatData;

		console.log('🖼️ [PICTOGRAPH_DISPLAY] Display updated for beat:', beatIndex);

		// Update pictograph component (placeholder for now)
		if (beatData?.pictograph_data) {
			// TODO: Update actual pictograph component when available
			onPictographUpdated?.(beatIndex, beatData);
		}

		// Update information panel
		if (infoPanelRef) {
			infoPanelRef.updateBeatInfo(beatIndex, beatData);
		}
	}

	export function updatePictographOnly(beatIndex: number, beatData: BeatData) {
		if (beatData?.pictograph_data) {
			// TODO: Update only pictograph component when available
			onPictographUpdated?.(beatIndex, beatData);
			console.log('🖼️ [PICTOGRAPH_DISPLAY] Pictograph-only update:', beatData.letter);
		}
	}

	export function updateInfoPanelOnly(beatIndex: number, beatData: BeatData | null) {
		if (infoPanelRef) {
			infoPanelRef.updateBeatInfo(beatIndex, beatData);
		}
	}

	export function clearDisplay() {
		updateDisplay(-1, null);
	}

	export function getCurrentBeatData(): BeatData | null {
		return currentBeatData;
	}

	export function getCurrentBeatIndex(): number | null {
		return currentBeatIndex;
	}

	// Set up resize observer
	$effect(() => {
		if (typeof window !== 'undefined' && pictographContainer) {
			const resizeObserver = new ResizeObserver(handleResize);
			resizeObserver.observe(pictographContainer);

			return () => {
				resizeObserver.disconnect();
			};
		}
	});
</script>

<div class="pictograph-display-section">
	<!-- Left side: Large square pictograph display -->
	<div class="pictograph-container" bind:this={pictographContainer}>
		<div class="pictograph-wrapper">
			<div
				class="pictograph-placeholder"
				style="width: {currentPictographSize}px; height: {currentPictographSize}px;"
			>
				{#if currentBeatData?.letter}
					<div class="beat-letter">{currentBeatData.letter}</div>
				{:else}
					<div class="placeholder-text">Pictograph View</div>
				{/if}
			</div>
		</div>
	</div>

	<!-- Right side: Detailed information panel -->
	<div class="info-panel-container">
		<DetailedInfoPanel bind:this={infoPanelRef} />
	</div>
</div>

<style>
	.pictograph-display-section {
		display: flex;
		height: 100%;
		gap: 15px;
		padding: 10px;
	}

	.pictograph-container {
		flex: 2; /* Takes 2/3 of available space */
		display: flex;
		align-items: center;
		justify-content: center;
		min-width: 200px;
	}

	.pictograph-wrapper {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.pictograph-placeholder {
		background: rgba(255, 255, 255, 0.1);
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		backdrop-filter: blur(5px);
		transition: all 0.3s ease;
		position: relative;
	}

	.pictograph-placeholder:hover {
		background: rgba(255, 255, 255, 0.15);
		border-color: rgba(255, 255, 255, 0.4);
	}

	.beat-letter {
		font-size: 2rem;
		font-weight: bold;
		color: rgba(255, 255, 255, 0.9);
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
	}

	.placeholder-text {
		font-size: 1.2rem;
		color: rgba(255, 255, 255, 0.7);
		text-align: center;
		font-weight: 500;
	}

	.info-panel-container {
		flex: 1; /* Takes 1/3 of available space */
		min-width: 180px;
		max-width: 250px;
		display: flex;
		flex-direction: column;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.pictograph-display-section {
			flex-direction: column;
			gap: 10px;
		}

		.pictograph-container {
			flex: none;
			height: 200px;
		}

		.info-panel-container {
			flex: 1;
			max-width: none;
		}

		.beat-letter {
			font-size: 1.5rem;
		}

		.placeholder-text {
			font-size: 1rem;
		}
	}
</style>
