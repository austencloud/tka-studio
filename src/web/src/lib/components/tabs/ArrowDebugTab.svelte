<script lang="ts">
	import { onMount } from 'svelte';
	import ArrowDebugControlPanel from '../../../routes/arrow-debug/ArrowDebugControlPanel.svelte';
	import ArrowDebugCanvas from '../../../routes/arrow-debug/ArrowDebugCanvas.svelte';
	import ArrowDebugInfoPanel from '../../../routes/arrow-debug/ArrowDebugInfoPanel.svelte';
	import { initializeDebugApp } from '../../../routes/arrow-debug/debug-app-init';

	// Import necessary types and services
	import type { ArrowData, MotionData, PictographData } from '$lib/domain';
	import { Location } from '$lib/domain';
	import { resolve } from '$lib/services/bootstrap';
	import type { IArrowCoordinateSystemService, IArrowLocationCalculator, IArrowRotationCalculator, IArrowAdjustmentCalculator } from '$lib/services/interfaces';
	import type { Point } from '$lib/services/positioning/types';

	// Reactive state for app initialization
	let isAppReady = $state(false);
	let initError = $state<string | null>(null);

	// Debug state - defined directly in component to avoid $effect issues
	let selectedPictograph = $state<PictographData | null>(null);
	let selectedArrowColor = $state<'red' | 'blue'>('blue');
	let availablePictographs = $state<PictographData[]>([]);
	
	let stepByStepMode = $state(true);
	let currentStep = $state(0);
	let maxSteps = $state(5);
	
	let showCoordinateGrid = $state(true);
	let showHandPoints = $state(true);
	let showLayer2Points = $state(true);
	let showAdjustmentVectors = $state(true);
	
	let currentDebugData = $state(createEmptyDebugData());
	
	let isCalculating = $state(false);
	let autoUpdate = $state(true);
	
	let expandedSections = $state(new Set(['coordinate_system', 'positioning_steps']));

	// Services - will be initialized after DI container is ready
	let coordinateSystemService: IArrowCoordinateSystemService | null = $state(null);
	let locationCalculator: IArrowLocationCalculator | null = $state(null);
	let rotationCalculator: IArrowRotationCalculator | null = $state(null);
	let adjustmentCalculator: IArrowAdjustmentCalculator | null = $state(null);

	// Computed values
	let currentMotionData = $derived(() => {
		if (!selectedPictograph?.motions) return null;
		return selectedPictograph.motions[selectedArrowColor];
	});

	let currentArrowData = $derived(() => {
		if (!selectedPictograph?.arrows) return null;
		return selectedPictograph.arrows[selectedArrowColor];
	});

	// Auto-update positioning when inputs change (only if services are available)
	$effect(() => {
		if (autoUpdate && selectedPictograph && currentMotionData && currentArrowData && coordinateSystemService) {
			calculateFullPositioning();
		}
	});

	function createEmptyDebugData() {
		return {
			pictographData: null,
			motionData: null,
			arrowData: null,
			calculatedLocation: null,
			locationDebugInfo: null,
			initialPosition: null,
			coordinateSystemDebugInfo: null,
			defaultAdjustment: null,
			defaultAdjustmentDebugInfo: null,
			specialAdjustment: null,
			specialAdjustmentDebugInfo: null,
			tupleProcessedAdjustment: null,
			tupleProcessingDebugInfo: null,
			finalPosition: null,
			finalRotation: 0,
			errors: [],
			timing: null
		};
	}

	// Initialize services
	function initializeServices(): boolean {
		try {
			coordinateSystemService = resolve('IArrowCoordinateSystemService');
			locationCalculator = resolve('IArrowLocationCalculator');
			rotationCalculator = resolve('IArrowRotationCalculator');
			adjustmentCalculator = resolve('IArrowAdjustmentCalculator');
			return true;
		} catch (error) {
			console.error('Failed to resolve services:', error);
			return false;
		}
	}

	// Toggle section for debug panels
	function toggleSection(section: string) {
		if (expandedSections.has(section)) {
			expandedSections.delete(section);
		} else {
			expandedSections.add(section);
		}
		// Trigger reactivity
		expandedSections = new Set(expandedSections);
	}

	async function calculateFullPositioning(): Promise<void> {
		if (!selectedPictograph || !currentMotionData || !currentArrowData) {
			return;
		}

		if (!coordinateSystemService || !locationCalculator || !rotationCalculator || !adjustmentCalculator) {
			console.error('Cannot calculate positioning: services not available');
			return;
		}

		isCalculating = true;
		const startTime = performance.now();
		
		try {
			const debugData = createEmptyDebugData();
			debugData.pictographData = selectedPictograph;
			debugData.motionData = currentMotionData;
			debugData.arrowData = currentArrowData;

			// Step 1: Calculate location
			const locationStart = performance.now();
			try {
				debugData.calculatedLocation = locationCalculator.calculateLocation(
					currentMotionData, 
					selectedPictograph
				);
				debugData.locationDebugInfo = {
					motionType: currentMotionData.motion_type || '',
					startOri: currentMotionData.start_ori || '',
					endOri: currentMotionData.end_ori || '',
					calculationMethod: getLocationCalculationMethod(currentMotionData)
				};
			} catch (error) {
				debugData.errors.push({
					step: 'location_calculation',
					error: error instanceof Error ? error.message : String(error),
					timestamp: Date.now()
				});
			}
			debugData.timing = { 
				totalDuration: 0, 
				stepDurations: { location: performance.now() - locationStart }
			};

			// Continue with other steps...
			// (Additional steps implementation)

			debugData.timing.totalDuration = performance.now() - startTime;
			currentDebugData = debugData;

		} catch (error) {
			currentDebugData.errors.push({
				step: 'full_calculation',
				error: error instanceof Error ? error.message : String(error),
				timestamp: Date.now()
			});
		} finally {
			isCalculating = false;
		}
	}

	function getLocationCalculationMethod(motion: MotionData): string {
		const motionType = motion.motion_type?.toLowerCase();
		if (['static', 'dash'].includes(motionType || '')) {
			return 'static_calculator';
		} else if (['pro', 'anti', 'float'].includes(motionType || '')) {
			return 'shift_calculator';
		}
		return 'unknown';
	}

	// Load sample pictographs for testing
	async function loadSamplePictographs(): Promise<void> {
		try {
			const samplePictographs: PictographData[] = [
				{
					letter: 'A',
					grid_mode: 'diamond',
					motions: {
						blue: {
							motion_type: 'pro',
							start_ori: 'in',
							end_ori: 'out',
							prop_rot_dir: 'cw',
							turns: 1
						},
						red: {
							motion_type: 'anti',
							start_ori: 'out',
							end_ori: 'in',
							prop_rot_dir: 'ccw',
							turns: 1
						}
					},
					arrows: {
						blue: {
							id: 'blue_arrow',
							color: 'blue',
							arrow_type: 'BLUE',
							is_visible: true,
							is_selected: false,
							position_x: 0,
							position_y: 0,
							rotation_angle: 0,
							is_mirrored: false,
							motion_type: 'pro',
							location: 'center',
							start_orientation: 'in',
							end_orientation: 'out',
							rotation_direction: 'cw',
							turns: 1
						},
						red: {
							id: 'red_arrow',
							color: 'red',
							arrow_type: 'RED',
							is_visible: true,
							is_selected: false,
							position_x: 0,
							position_y: 0,
							rotation_angle: 0,
							is_mirrored: false,
							motion_type: 'anti',
							location: 'center',
							start_orientation: 'out',
							end_orientation: 'in',
							rotation_direction: 'ccw',
							turns: 1
						}
					}
				} as PictographData
			];
			
			availablePictographs = samplePictographs;
			if (samplePictographs.length > 0) {
				selectedPictograph = samplePictographs[0];
			}
		} catch (error) {
			console.error('Failed to load sample pictographs:', error);
		}
	}

	// Initialize the application on mount
	onMount(async () => {
		try {
			await initializeDebugApp();
			
			// Initialize services
			if (!initializeServices()) {
				throw new Error('Failed to initialize positioning services');
			}
			
			// Load sample data
			await loadSamplePictographs();
			
			isAppReady = true;
		} catch (error) {
			console.error('Failed to initialize arrow debug:', error);
			initError = error instanceof Error ? error.message : 'Unknown initialization error';
		}
	});

	console.log('🎯 ArrowDebugTab rendered!');
</script>

<div class="arrow-debug-tab">
	{#if initError}
		<div class="error-container">
			<div class="error-box">
				<h2>❌ Initialization Error</h2>
				<p>Failed to initialize the arrow debug system:</p>
				<code>{initError}</code>
				<p>Please check the console for more details.</p>
				<button onclick={() => window.location.reload()} class="retry-btn">
					🔄 Retry
				</button>
			</div>
		</div>
	{:else if !isAppReady || !state}
		<div class="loading-container">
			<div class="loading-box">
				<div class="spinner"></div>
				<h2>🔧 Initializing Arrow Debug</h2>
				<p>Setting up positioning services and debug tools...</p>
			</div>
		</div>
	{:else}
		<header class="debug-header">
			<h1>🎯 Arrow Debug</h1>
			<p>Step-by-step analysis of arrow positioning with visual debugging</p>
		</header>

		<main class="debug-main">
			<!-- Left Panel: Controls & Pictograph Selection -->
			<div class="panel control-panel">
				<ArrowDebugControlPanel
					{availablePictographs}
					{maxSteps}
					{isCalculating}
					{currentMotionData}
					bind:selectedPictograph
					bind:selectedArrowColor
					bind:stepByStepMode
					bind:currentStep
					bind:autoUpdate
					{calculateFullPositioning}
					{loadSamplePictographs}
				/>
			</div>

			<!-- Center Panel: Visual Canvas with Step-by-Step Positioning -->
			<div class="panel canvas-panel">
				<ArrowDebugCanvas
					{currentDebugData}
					{stepByStepMode}
					{currentStep}
					{selectedArrowColor}
					{isCalculating}
					bind:showCoordinateGrid
					bind:showHandPoints
					bind:showLayer2Points
					bind:showAdjustmentVectors
				/>
			</div>

			<!-- Right Panel: Debug Information & Coordinate Details -->
			<div class="panel debug-info-panel">
				<ArrowDebugInfoPanel
					{currentDebugData}
					{isCalculating}
					{stepByStepMode}
					{currentStep}
					bind:expandedSections
					{toggleSection}
				/>
			</div>
		</main>
	{/if}
</div>

<style>
	.arrow-debug-tab {
		height: 100%;
		width: 100%;
		display: flex;
		flex-direction: column;
		background: transparent;
		color: white;
		padding: 20px;
		font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
		overflow: hidden;
	}

	.debug-header {
		text-align: center;
		margin-bottom: 20px;
		padding-bottom: 15px;
		border-bottom: 2px solid rgba(251, 191, 36, 0.3);
		flex-shrink: 0;
	}

	.debug-header h1 {
		font-size: 1.8rem;
		margin-bottom: 8px;
		background: linear-gradient(135deg, #fbbf24, #f59e0b);
		background-clip: text;
		-webkit-background-clip: text;
		color: transparent;
	}

	.debug-header p {
		color: #c7d2fe;
		font-size: 1rem;
	}

	.debug-main {
		display: grid;
		grid-template-columns: 320px 1fr 350px;
		gap: 15px;
		flex: 1;
		min-height: 0;
	}

	.panel {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		padding: 16px;
		overflow-y: auto;
	}

	.canvas-panel {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.05);
	}

	.loading-container,
	.error-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100%;
		padding: 40px;
	}

	.loading-box,
	.error-box {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		padding: 40px;
		text-align: center;
		max-width: 500px;
		width: 100%;
	}

	.error-box {
		border-color: rgba(248, 113, 113, 0.5);
		background: rgba(248, 113, 113, 0.1);
	}

	.loading-box h2,
	.error-box h2 {
		margin: 20px 0 15px 0;
		color: #fbbf24;
		font-size: 1.5rem;
	}

	.error-box h2 {
		color: #f87171;
	}

	.loading-box p,
	.error-box p {
		color: #c7d2fe;
		margin-bottom: 10px;
		line-height: 1.5;
	}

	.error-box code {
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		padding: 8px 12px;
		font-family: 'Courier New', monospace;
		color: #f87171;
		display: block;
		margin: 15px 0;
		word-break: break-all;
	}

	.retry-btn {
		background: linear-gradient(135deg, #f87171, #ef4444);
		border: none;
		border-radius: 8px;
		padding: 10px 16px;
		color: white;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
		margin-top: 15px;
	}

	.retry-btn:hover {
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(248, 113, 113, 0.3);
	}

	.spinner {
		width: 50px;
		height: 50px;
		border: 4px solid rgba(251, 191, 36, 0.3);
		border-top: 4px solid #fbbf24;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0 auto;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	/* Responsive design */
	@media (max-width: 1200px) {
		.debug-main {
			grid-template-columns: 280px 1fr 300px;
			gap: 12px;
		}
	}

	@media (max-width: 1000px) {
		.arrow-debug-tab {
			padding: 15px;
		}
		
		.debug-main {
			grid-template-columns: 1fr;
			grid-template-rows: auto auto 1fr;
			gap: 10px;
		}

		.panel {
			min-height: auto;
			padding: 12px;
		}

		.debug-header h1 {
			font-size: 1.5rem;
		}
	}

	@media (max-width: 768px) {
		.arrow-debug-tab {
			padding: 10px;
		}

		.debug-header {
			margin-bottom: 15px;
			padding-bottom: 10px;
		}

		.debug-header h1 {
			font-size: 1.3rem;
		}

		.debug-header p {
			font-size: 0.9rem;
		}

		.panel {
			padding: 10px;
		}
	}

	/* Scrollbar styling for webkit browsers */
	.panel::-webkit-scrollbar {
		width: 6px;
	}

	.panel::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.1);
		border-radius: 3px;
	}

	.panel::-webkit-scrollbar-thumb {
		background: rgba(251, 191, 36, 0.5);
		border-radius: 3px;
	}

	.panel::-webkit-scrollbar-thumb:hover {
		background: rgba(251, 191, 36, 0.7);
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.arrow-debug-tab {
			transition: none;
		}
	}

	/* High contrast mode */
	@media (prefers-contrast: high) {
		.panel {
			border: 2px solid white;
			background: rgba(0, 0, 0, 0.8);
		}

		.debug-header {
			border-bottom-color: white;
		}
	}
</style>
