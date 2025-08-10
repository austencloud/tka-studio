<!-- StartPositionPicker.svelte - Modern implementation updated for proper OptionPicker integration -->
<script lang="ts">
	import type { BeatData } from '$domain/BeatData';
	import type { PictographData } from '$domain/PictographData';
	import { GridMode, Location, MotionType } from '$domain/enums';
	import { getLetterBorderColor } from '$lib/utils/letterTypeUtils';
	import { resolve } from '$services/bootstrap';
	import type { IPictographRenderingService, IStartPositionService } from '$services/interfaces';
	import { onMount } from 'svelte';
	import ModernPictograph from '../pictograph/Pictograph.svelte';

	// Props using runes
	const { gridMode = 'diamond', onStartPositionSelected = () => {} } = $props<{
		gridMode?: 'diamond' | 'box';
		onStartPositionSelected?: (position: BeatData) => void;
	}>();

	// Runes-based reactive state (replacing legacy stores)
	let startPositionPictographs = $state<PictographData[]>([]);
	let selectedStartPos = $state<PictographData | null>(null);
	let isLoading = $state(true);
	let loadingError = $state(false);
	let isTransitioning = $state(false);

	// Modern services (replacing legacy service calls)
	let startPositionService = $state<IStartPositionService | null>(null);
	let pictographRenderingService = $state<IPictographRenderingService | null>(null);

	// Resolve services when container is ready
	$effect(() => {
		try {
			// Try to resolve services, but handle gracefully if container not ready
			if (!startPositionService) {
				try {
					startPositionService = resolve('IStartPositionService');
				} catch {
					// Container not ready yet, will retry on next effect run
					return;
				}
			}
			if (!pictographRenderingService) {
				try {
					pictographRenderingService = resolve('IPictographRenderingService');
				} catch {
					// Container not ready yet, will retry on next effect run
					return;
				}
			}
		} catch (error) {
			console.error('StartPositionPicker: Failed to resolve services:', error);
			// Services will remain null and component will handle gracefully
		}
	});

	// Load available start positions (modernized from legacy)
	async function loadStartPositions() {
		isLoading = true;
		loadingError = false;

		try {
			// Use modern service to get start positions
			if (!startPositionService) {
				throw new Error('StartPositionService not available');
			}
			const startPositions = await startPositionService.getDefaultStartPositions(gridMode);
			startPositionPictographs = startPositions;
		} catch (error) {
			console.error('❌ Error loading start positions:', error);
			loadingError = true;
			startPositionPictographs = [];
		} finally {
			isLoading = false;
		}
	}

	// Handle start position selection (modernized from legacy with proper data format)
	async function handleSelect(startPosPictograph: PictographData) {
		try {
			// Show transition state
			isTransitioning = true;

			// **CRITICAL: Create the data format that OptionPicker expects**
			// Based on legacy analysis, OptionPicker looks for:
			// 1. localStorage 'start_position' with endPos field
			// 2. Proper pictograph data structure

			// Extract end position from the pictograph data
			const endPosition = extractEndPosition(startPosPictograph);

			// Create start position data in the format the OptionPicker expects (like legacy)
			const startPositionData = {
				// CRITICAL: Include endPos field for OptionPicker
				endPos: endPosition,
				// Include the full pictograph data
				pictograph_data: {
					...startPosPictograph,
					// Ensure static motion types for start positions
					motions: {
						blue: startPosPictograph.motions?.blue
							? {
									...startPosPictograph.motions.blue,
									motion_type: MotionType.STATIC,
									end_loc: startPosPictograph.motions.blue.start_loc,
									end_ori: startPosPictograph.motions.blue.start_ori,
									turns: 0,
								}
							: null,
						red: startPosPictograph.motions?.red
							? {
									...startPosPictograph.motions.red,
									motion_type: MotionType.STATIC,
									end_loc: startPosPictograph.motions.red.start_loc,
									end_ori: startPosPictograph.motions.red.start_ori,
									turns: 0,
								}
							: null,
					},
				},
				// Additional legacy-compatible fields
				letter: startPosPictograph.letter,
				gridMode: gridMode,
				isStartPosition: true,
			};

			// Create start position beat data for internal use
			const startPositionBeat: BeatData = {
				id: crypto.randomUUID(),
				beat_number: 0,
				duration: 1.0,
				blue_reversal: false,
				red_reversal: false,
				is_blank: false,
				pictograph_data: startPosPictograph,
				metadata: {
					endPos: endPosition,
				},
			};

			// Update selected state
			selectedStartPos = startPosPictograph;

			// **CRITICAL: Save to localStorage in the format OptionPicker expects**
			try {
				localStorage.setItem('start_position', JSON.stringify(startPositionData));
			} catch (error) {
				console.error('Failed to save start position to localStorage:', error);
			}

			// **NEW: Preload options BEFORE triggering the transition**
			// This ensures options are ready when the option picker fades in
			try {
				console.log('🚀 Preloading options for seamless transition...');

				// Import and use the OptionDataService to preload options
				const { OptionDataService } = await import(
					'$services/implementations/OptionDataService'
				);
				const optionDataService = new OptionDataService();
				await optionDataService.initialize();

				const preloadedOptions = await optionDataService.getNextOptionsFromEndPosition(
					endPosition,
					gridMode === 'diamond' ? GridMode.DIAMOND : GridMode.BOX,
					{}
				);

				console.log(
					`✅ Preloaded ${preloadedOptions?.length || 0} options for seamless transition`
				);

				// Store the preloaded options so OptionPicker can use them immediately
				localStorage.setItem('preloaded_options', JSON.stringify(preloadedOptions || []));
			} catch (preloadError) {
				console.warn('Failed to preload options, will load normally:', preloadError);
				// Continue with normal flow even if preload fails
			}

			// Use modern service to set start position
			if (startPositionService) {
				await startPositionService.setStartPosition(startPositionBeat);
			}

			// Call callback to notify parent component
			onStartPositionSelected(startPositionBeat);

			// **CRITICAL: Emit event that OptionPicker is listening for**
			const event = new CustomEvent('start-position-selected', {
				detail: {
					startPosition: startPositionData,
					endPosition: endPosition,
					isTransitioning: true,
					preloadedOptions: true, // Signal that options are preloaded
				},
				bubbles: true,
			});
			document.dispatchEvent(event);
		} catch (error) {
			console.error('❌ Error selecting start position:', error);
			isTransitioning = false;
		}
	}

	/**
	 * Extract end position from pictograph data
	 * This determines where the start position ends, which becomes the starting point for next options
	 */
	function extractEndPosition(pictographData: PictographData): string {
		// For start positions, the end position is typically the same as start position
		// since they're static motions, but we need to map to position keys that exist in CSV

		// Default mappings based on legacy desktop patterns
		const defaultEndPositions: Record<string, string> = {
			α: 'alpha1', // Alpha start position ends at alpha1
			β: 'beta5', // Beta start position ends at beta5
			γ: 'gamma11', // Gamma start position ends at gamma11
		};

		// Try to get from letter first
		if (pictographData.letter && defaultEndPositions[pictographData.letter]) {
			return defaultEndPositions[pictographData.letter]!;
		}

		// Try to extract from motion data
		if (pictographData.motions?.blue?.end_loc) {
			return mapLocationToPosition(pictographData.motions.blue.end_loc);
		}
		if (pictographData.motions?.red?.end_loc) {
			return mapLocationToPosition(pictographData.motions.red.end_loc);
		}

		// Default fallback
		return 'alpha1';
	}

	/**
	 * Map location enum to position string for CSV lookup
	 */
	function mapLocationToPosition(location: Location): string {
		// Basic mapping - this would need to be enhanced based on actual position system
		const locationMap: Record<string, string> = {
			SOUTH: 'alpha1',
			NORTH: 'alpha1',
			EAST: 'gamma11',
			WEST: 'alpha1',
			// Add more mappings as needed
		};

		const locationStr = typeof location === 'string' ? location : String(location || '');
		return locationMap[locationStr.toUpperCase()] || 'alpha1';
	}

	// Initialize on mount
	onMount(() => {
		loadStartPositions();
	});

	// Reload when grid mode changes
	$effect(() => {
		if (gridMode) {
			loadStartPositions();
		}
	});
</script>

<div class="start-pos-picker" data-testid="start-position-picker">
	{#if isLoading}
		<div class="loading-container">
			<div class="loading-spinner"></div>
			<p class="loading-text">Loading Start Positions...</p>
		</div>
	{:else if loadingError}
		<div class="error-container">
			<p>Unable to load start positions. Please try refreshing the page.</p>
			<button
				class="refresh-button"
				onclick={() => {
					if (typeof window !== 'undefined') window.location.reload();
				}}
			>
				Refresh
			</button>
		</div>
	{:else if startPositionPictographs.length === 0}
		<div class="error-container">
			<p>No valid start positions found for the current configuration.</p>
		</div>
	{:else}
		<div class="pictograph-row">
			{#each startPositionPictographs as pictograph (pictograph.id)}
				<div
					class="pictograph-container"
					class:selected={selectedStartPos?.id === pictograph.id}
					role="button"
					tabindex="0"
					style:--letter-border-color={getLetterBorderColor(pictograph.letter || null)}
					onclick={() => handleSelect(pictograph)}
					onkeydown={(e) => {
						if (e.key === 'Enter' || e.key === ' ') {
							e.preventDefault();
							handleSelect(pictograph);
						}
					}}
				>
					<!-- Render pictograph using ModernPictograph component -->
					<div class="pictograph-wrapper">
						<ModernPictograph
							pictographData={pictograph}
							debug={false}
							showLoadingIndicator={false}
						/>
					</div>

					<!-- Position label (from legacy) -->
					<div class="position-label">
						{pictograph.letter || 'Start Position'}
					</div>
				</div>
			{/each}
		</div>
	{/if}

	<!-- Loading overlay during transition (from legacy) -->
	{#if isTransitioning}
		<div class="loading-overlay">
			<div class="loading-spinner"></div>
			<p>Loading options...</p>
		</div>
	{/if}
</div>

<style>
	.start-pos-picker {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100%;
		width: 100%;
		min-height: 300px;
		padding: 20px 0;
		position: relative;
	}

	.loading-container,
	.error-container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100%;
		width: 100%;
		flex: 1;
	}

	.error-container {
		background-color: rgba(255, 220, 220, 0.7);
		padding: 20px;
		border-radius: var(--border-radius);
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid var(--muted);
		border-top: 4px solid var(--primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.loading-text {
		margin-top: 20px;
		font-size: 1.2rem;
		color: var(--muted-foreground);
		animation: pulse 1.5s infinite ease-in-out;
	}

	@keyframes pulse {
		0%,
		100% {
			opacity: 0.6;
		}
		50% {
			opacity: 1;
		}
	}

	.refresh-button {
		margin-top: 15px;
		padding: 10px 20px;
		background: var(--primary);
		color: var(--primary-foreground);
		border: none;
		border-radius: var(--border-radius);
		cursor: pointer;
		font-size: 1rem;
	}

	.refresh-button:hover {
		background: var(--primary-hover, var(--primary));
		opacity: 0.9;
	}

	.pictograph-row {
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		align-items: center;
		width: 90%;
		gap: 3%;
		margin: auto;
		flex: 0 0 auto;
		padding: 2rem 0;
	}

	.pictograph-container {
		width: 25%;
		aspect-ratio: 1 / 1;
		height: auto;
		position: relative;
		cursor: pointer;
		transition: all 0.2s ease-in-out;
		border: 2px solid transparent;
		border-radius: var(--border-radius);
		padding: 0;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.pictograph-container:hover {
		transform: scale(1.05);
		border-color: var(--letter-border-color, var(--primary));
		box-shadow: var(--shadow-lg);
	}

	.pictograph-container.selected {
		border-color: var(--letter-border-color, var(--primary));
		background: var(--primary) / 10;
	}

	.pictograph-wrapper {
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
	}

	.position-label {
		position: absolute;
		bottom: -25px;
		left: 50%;
		transform: translateX(-50%);
		font-size: var(--font-size-sm);
		font-weight: 500;
		color: var(--foreground);
		text-align: center;
		white-space: nowrap;
	}

	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.9);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		border-radius: var(--border-radius);
		z-index: 1000;
	}

	.loading-overlay .loading-spinner {
		width: 32px;
		height: 32px;
		margin-bottom: var(--spacing-md);
	}

	.loading-overlay p {
		color: var(--foreground);
		font-size: 1.1rem;
		margin: 0;
	}

	@media (max-width: 768px) {
		.pictograph-row {
			flex-direction: column;
			gap: var(--spacing-lg);
		}

		.pictograph-container {
			width: 80%;
			max-width: 200px;
		}
	}
</style>
