<!-- Quick action buttons for common debugging scenarios -->
<script lang="ts">
	import type { ArrowDebugState } from '../state/arrow-debug-state.svelte';
	import { createGridData } from '$lib/domain/GridData';
	import { GridMode, ArrowType, MotionType, RotationDirection, Location, Orientation, GridPosition } from '$lib/domain/enums';

	interface Props {
		state: ArrowDebugState;
	}

	let { state }: Props = $props();

	// Common test scenarios
	const testScenarios = [
		{
			name: 'Pro Motion Test',
			description: 'Blue Pro 1T CW, Red Anti 1T CCW',
			letter: 'A',
			setup: () => createTestPictograph('A', 'pro', 'anti', 1, 1)
		},
		{
			name: 'Static Test',
			description: 'Both Static 0.5T',
			letter: 'B', 
			setup: () => createTestPictograph('B', 'static', 'static', 0.5, 0.5)
		},
		{
			name: 'Float Test',
			description: 'Blue Float FL, Red Dash 0T',
			letter: 'C',
			setup: () => createTestPictograph('C', 'float', 'dash', 'fl', 0)
		},
		{
			name: 'Complex Test',
			description: 'Blue Pro 2.5T CW, Red Anti 1.5T CCW',
			letter: 'D',
			setup: () => createTestPictograph('D', 'pro', 'anti', 2.5, 1.5)
		}
	];

	function createTestPictograph(
		letter: string,
		blueMotion: string,
		redMotion: string,
		blueTurns: number | string,
		redTurns: number | string
	) {
		// Map string motion types to enum values
		const mapMotionType = (motion: string): MotionType => {
			switch (motion.toLowerCase()) {
				case 'pro': return MotionType.PRO;
				case 'anti': return MotionType.ANTI;
				case 'static': return MotionType.STATIC;
				case 'float': return MotionType.FLOAT;
				case 'dash': return MotionType.DASH;
				default: return MotionType.STATIC;
			}
		};
		return {
			id: `test_${letter.toLowerCase()}`,
			letter,
			grid_mode: 'diamond',
			start_position: GridPosition.ALPHA1,
			end_position: GridPosition.ALPHA3,
			beat: 1,
			is_blank: false,
			is_mirrored: false,
			grid_data: createGridData({ grid_mode: GridMode.DIAMOND }),
			props: {},
			metadata: {},
			motions: {
				blue: {
					motion_type: mapMotionType(blueMotion),
					start_ori: blueMotion === 'pro' ? Orientation.IN : blueMotion === 'anti' ? Orientation.OUT : Orientation.IN,
					end_ori: blueMotion === 'pro' ? Orientation.OUT : blueMotion === 'anti' ? Orientation.IN : Orientation.OUT,
					start_loc: Location.NORTH,
					end_loc: Location.SOUTH,
					prop_rot_dir: RotationDirection.CLOCKWISE,
					turns: typeof blueTurns === 'string' && blueTurns.toLowerCase() === 'fl' ? 'fl' as const : Number(blueTurns),
					is_visible: true
				},
				red: {
					motion_type: mapMotionType(redMotion),
					start_ori: redMotion === 'pro' ? Orientation.IN : redMotion === 'anti' ? Orientation.OUT : Orientation.IN,
					end_ori: redMotion === 'pro' ? Orientation.OUT : redMotion === 'anti' ? Orientation.IN : Orientation.OUT,
					start_loc: Location.NORTH,
					end_loc: Location.SOUTH,
					prop_rot_dir: RotationDirection.COUNTER_CLOCKWISE,
					turns: typeof redTurns === 'string' && redTurns.toLowerCase() === 'fl' ? 'fl' as const : Number(redTurns),
					is_visible: true
				}
			},
			arrows: {
				blue: {
					id: 'blue_arrow',
					color: 'blue',
					arrow_type: ArrowType.BLUE,
					is_visible: true,
					is_selected: false,
					position_x: 0,
					position_y: 0,
					rotation_angle: 0,
					is_mirrored: false,
					motion_type: blueMotion,
					location: 'center',
					start_orientation: blueMotion === 'pro' ? 'in' : 'out',
					end_orientation: blueMotion === 'pro' ? 'out' : 'in',
					rotation_direction: 'cw',
					turns: typeof blueTurns === 'number' ? blueTurns : 0
				},
				red: {
					id: 'red_arrow',
					color: 'red',
					arrow_type: ArrowType.RED,
					is_visible: true,
					is_selected: false,
					position_x: 0,
					position_y: 0,
					rotation_angle: 0,
					is_mirrored: false,
					motion_type: redMotion,
					location: 'center',
					start_orientation: redMotion === 'pro' ? 'in' : 'out',
					end_orientation: redMotion === 'pro' ? 'out' : 'in',
					rotation_direction: 'ccw',
					turns: typeof redTurns === 'number' ? redTurns : 0
				}
			}
		};
	}

	async function loadTestScenario(scenario: typeof testScenarios[0]) {
		try {
			const testPictograph = scenario.setup();
			
			// Add to available pictographs if not already there
			const existing = state.availablePictographs.find(p => p.letter === testPictograph.letter);
			if (!existing) {
				state.availablePictographs = [...state.availablePictographs, testPictograph];
			}
			
			// Select the test pictograph
			state.selectedPictograph = testPictograph;
			
			// Reset step-by-step mode to beginning
			if (state.stepByStepMode) {
				state.currentStep = 0;
			}
			
			console.log(`Loaded test scenario: ${scenario.name}`);
		} catch (error) {
			console.error(`Failed to load test scenario ${scenario.name}:`, error);
		}
	}

	function resetToBeginning() {
		state.currentStep = 0;
	}

	function jumpToEnd() {
		state.currentStep = state.maxSteps;
	}

	async function runFullAnalysis() {
		if (!state.selectedPictograph) return;
		
		// Reset and run step by step with delays for visualization
		state.currentStep = 0;
		
		for (let step = 0; step <= state.maxSteps; step++) {
			state.currentStep = step;
			await new Promise(resolve => setTimeout(resolve, 800)); // 800ms delay between steps
		}
	}
</script>

<div class="quick-actions">
	<h4>🚀 Quick Test Scenarios</h4>
	
	<div class="scenarios-grid">
		{#each testScenarios as scenario}
			<button 
				class="scenario-btn"
				onclick={() => loadTestScenario(scenario)}
				disabled={state.isCalculating}
			>
				<div class="scenario-name">{scenario.name}</div>
				<div class="scenario-desc">{scenario.description}</div>
			</button>
		{/each}
	</div>

	<div class="action-buttons">
		<button 
			class="action-btn reset"
			onclick={resetToBeginning}
			disabled={state.isCalculating || !state.stepByStepMode}
		>
			⏮️ Reset
		</button>
		
		<button 
			class="action-btn analyze"
			onclick={runFullAnalysis}
			disabled={state.isCalculating || !state.selectedPictograph || !state.stepByStepMode}
		>
			🔍 Auto Analyze
		</button>
		
		<button 
			class="action-btn jump"
			onclick={jumpToEnd}
			disabled={state.isCalculating || !state.stepByStepMode}
		>
			⏭️ Jump to End
		</button>
	</div>
</div>

<style>
	.quick-actions {
		background: rgba(0, 0, 0, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		padding: 15px;
	}

	h4 {
		margin: 0 0 12px 0;
		color: #34d399;
		font-size: 0.9rem;
		border-bottom: 1px solid rgba(52, 211, 153, 0.2);
		padding-bottom: 6px;
	}

	.scenarios-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 8px;
		margin-bottom: 15px;
	}

	.scenario-btn {
		background: rgba(52, 211, 153, 0.1);
		border: 1px solid rgba(52, 211, 153, 0.3);
		border-radius: 6px;
		padding: 10px;
		color: white;
		cursor: pointer;
		transition: all 0.2s ease;
		text-align: left;
	}

	.scenario-btn:hover:not(:disabled) {
		background: rgba(52, 211, 153, 0.2);
		border-color: #34d399;
		transform: translateY(-1px);
	}

	.scenario-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
		transform: none;
	}

	.scenario-name {
		font-weight: 600;
		font-size: 0.85rem;
		color: #34d399;
		margin-bottom: 2px;
	}

	.scenario-desc {
		font-size: 0.75rem;
		color: #a3a3a3;
		line-height: 1.2;
	}

	.action-buttons {
		display: flex;
		gap: 6px;
	}

	.action-btn {
		flex: 1;
		padding: 8px 12px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		background: rgba(0, 0, 0, 0.4);
		color: white;
		font-size: 0.8rem;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.action-btn:hover:not(:disabled) {
		background: rgba(255, 255, 255, 0.1);
	}

	.action-btn:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}

	.action-btn.reset {
		border-color: rgba(239, 68, 68, 0.5);
	}

	.action-btn.reset:hover:not(:disabled) {
		background: rgba(239, 68, 68, 0.1);
		border-color: #ef4444;
	}

	.action-btn.analyze {
		border-color: rgba(251, 191, 36, 0.5);
	}

	.action-btn.analyze:hover:not(:disabled) {
		background: rgba(251, 191, 36, 0.1);
		border-color: #fbbf24;
	}

	.action-btn.jump {
		border-color: rgba(34, 197, 94, 0.5);
	}

	.action-btn.jump:hover:not(:disabled) {
		background: rgba(34, 197, 94, 0.1);
		border-color: #22c55e;
	}
</style>
