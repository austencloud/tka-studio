<!--
PictographDemo.svelte - Demo component for testing modern pictograph rendering

This component demonstrates the modern pictograph system with sample data,
allowing you to test different configurations and see the rendering in action.
-->
<script lang="ts">
	import { ModernPictograph } from '$lib/components/pictograph';
	import type { BeatData, PictographData } from '$lib/domain';
	import { createBeatData, createPictographData } from '$lib/domain';

	// Demo state using runes
	let selectedDemo = $state('simple');
	let debugMode = $state(false);
	let gridMode = $state<'diamond' | 'box'>('diamond');
	let showControls = $state(true);

	// Sample pictograph data for different demos
	const samplePictographs = $derived(() => {
		return {
			simple: createPictographData({
				letter: 'A',
				grid_data: { mode: gridMode },
				arrows: {
					blue: {
						id: 'blue-arrow',
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
						metadata: {}
					},
					red: {
						id: 'red-arrow',
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
						metadata: {}
					}
				},
				props: {
					blue: {
						id: 'blue-prop',
						prop_type: 'staff',
						color: 'blue',
						location: 'n',
						coordinates: null,
						rotation_angle: 0,
						svg_center: null,
						metadata: {}
					},
					red: {
						id: 'red-prop',
						prop_type: 'staff',
						color: 'red',
						location: 's',
						coordinates: null,
						rotation_angle: 180,
						svg_center: null,
						metadata: {}
					}
				}
			}),

			complex: createPictographData({
				letter: 'Φ',
				grid_data: { mode: gridMode },
				arrows: {
					blue: {
						id: 'blue-arrow-complex',
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
						metadata: {}
					},
					red: {
						id: 'red-arrow-complex',
						arrow_type: 'red',
						color: 'red',
						motion_type: 'dash',
						location: 'sw',
						start_orientation: 'in',
						end_orientation: 'out',
						rotation_direction: 'counter_clockwise',
						turns: 0.5,
						is_mirrored: false,
						coordinates: null,
						rotation_angle: 225,
						svg_center: null,
						svg_mirrored: false,
						metadata: {}
					}
				}
			}),

			empty: createPictographData({
				grid_data: { mode: gridMode },
				is_blank: true
			})
		};
	});

	// Create sample beat data
	const sampleBeats = $derived(() => {
		return {
			withPictograph: createBeatData({
				beat_number: 1,
				pictograph_data: samplePictographs()[selectedDemo],
				is_blank: false
			}),
			blank: createBeatData({
				beat_number: 2,
				is_blank: true
			})
		};
	});

	// Demo selection options
	const demoOptions = [
		{ value: 'simple', label: 'Simple (A with basic arrows)' },
		{ value: 'complex', label: 'Complex (Φ with float/dash)' },
		{ value: 'empty', label: 'Empty (Grid only)' }
	];

	function handlePictographClick() {
		console.log('Pictograph clicked!', selectedDemo);
	}
</script>

<div class="pictograph-demo">
	<h2>Modern Pictograph Demo</h2>
	
	{#if showControls}
		<!-- Demo Controls -->
		<div class="controls" data-testid="demo-controls">
			<div class="control-group">
				<label>Demo Type:</label>
				<select bind:value={selectedDemo} data-testid="demo-selector">
					{#each demoOptions as option}
						<option value={option.value}>{option.label}</option>
					{/each}
				</select>
			</div>

			<div class="control-group">
				<label>Grid Mode:</label>
				<select bind:value={gridMode} data-testid="grid-mode-selector">
					<option value="diamond">Diamond</option>
					<option value="box">Box</option>
				</select>
			</div>

			<div class="control-group">
				<label>
					<input type="checkbox" bind:checked={debugMode} data-testid="debug-mode-checkbox" />
					Debug Mode
				</label>
			</div>

			<div class="control-group">
				<label>
					<input type="checkbox" bind:checked={showControls} />
					Show Controls
				</label>
			</div>
		</div>
	{/if}

	<!-- Pictograph Display -->
	<div class="demo-grid">
		<!-- Direct Pictograph Data Demo -->
		<div class="demo-item" data-testid="direct-pictograph-demo">
			<h3>Direct Pictograph Data</h3>
			<div class="pictograph-wrapper" data-testid="main-pictograph">
				<ModernPictograph
					pictographData={samplePictographs()[selectedDemo]}
					width={300}
					height={300}
					onClick={handlePictographClick}
					debug={debugMode}
				/>
			</div>
		</div>

		<!-- Beat Data Demo -->
		<div class="demo-item" data-testid="beat-data-demo">
			<h3>From Beat Data</h3>
			<div class="pictograph-wrapper">
				<ModernPictograph
					beatData={sampleBeats().withPictograph}
					width={300}
					height={300}
					beatNumber={1}
					onClick={handlePictographClick}
					debug={debugMode}
				/>
			</div>
		</div>

		<!-- Different Sizes Demo -->
		<div class="demo-item">
			<h3>Different Sizes</h3>
			<div class="size-demo">
				<div class="size-item" data-testid="small-pictograph">
					<h4>Small (150px)</h4>
					<ModernPictograph
						pictographData={samplePictographs()[selectedDemo]}
						width={150}
						height={150}
						debug={false}
					/>
				</div>
				<div class="size-item" data-testid="medium-pictograph">
					<h4>Medium (200px)</h4>
					<ModernPictograph
						pictographData={samplePictographs()[selectedDemo]}
						width={200}
						height={200}
						debug={false}
					/>
				</div>
				<div class="size-item" data-testid="large-pictograph">
					<h4>Large (400px)</h4>
					<ModernPictograph
						pictographData={samplePictographs()[selectedDemo]}
						width={400}
						height={400}
						debug={false}
					/>
				</div>
			</div>
		</div>

		<!-- Blank Beat Demo -->
		<div class="demo-item" data-testid="blank-beat-demo">
			<h3>Blank Beat</h3>
			<div class="pictograph-wrapper">
				<ModernPictograph
					beatData={sampleBeats().blank}
					width={300}
					height={300}
					beatNumber={2}
					debug={debugMode}
				/>
			</div>
		</div>
	</div>

	<!-- Info Panel -->
	<div class="info-panel">
		<h3>Current Configuration</h3>
		<ul>
			<li><strong>Demo:</strong> {demoOptions.find(opt => opt.value === selectedDemo)?.label}</li>
			<li><strong>Grid Mode:</strong> {gridMode}</li>
			<li><strong>Debug:</strong> {debugMode ? 'Enabled' : 'Disabled'}</li>
			<li><strong>Components:</strong> ModernPictograph, Grid, Prop, Arrow, TKAGlyph</li>
			<li><strong>Reactivity:</strong> Pure Svelte 5 Runes</li>
		</ul>

		<div class="data-preview">
			<h4>Sample Data Structure</h4>
			<pre><code>{JSON.stringify(samplePictographs()[selectedDemo], null, 2).substring(0, 500)}...</code></pre>
		</div>
	</div>

	<!-- Toggle Controls Button -->
	{#if !showControls}
		<button class="toggle-controls" onclick={() => showControls = true}>
			Show Controls
		</button>
	{/if}
</div>

<style>
	.pictograph-demo {
		padding: 2rem;
		max-width: 1400px;
		margin: 0 auto;
		font-family: 'Inter', system-ui, sans-serif;
	}

	h2 {
		color: #1f2937;
		margin-bottom: 2rem;
		text-align: center;
	}

	.controls {
		display: flex;
		gap: 1rem;
		margin-bottom: 2rem;
		padding: 1rem;
		background: #f8fafc;
		border-radius: 8px;
		flex-wrap: wrap;
	}

	.control-group {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.control-group label {
		font-weight: 500;
		color: #374151;
	}

	.control-group select,
	.control-group input[type="checkbox"] {
		padding: 0.25rem 0.5rem;
		border: 1px solid #d1d5db;
		border-radius: 4px;
	}

	.demo-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
		gap: 2rem;
		margin-bottom: 2rem;
	}

	.demo-item {
		border: 1px solid #e5e7eb;
		border-radius: 12px;
		padding: 1.5rem;
		background: white;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	.demo-item h3 {
		margin: 0 0 1rem 0;
		color: #1f2937;
		font-size: 1.25rem;
	}

	.pictograph-wrapper {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 300px;
	}

	.size-demo {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		align-items: center;
	}

	.size-item {
		text-align: center;
	}

	.size-item h4 {
		margin: 0 0 0.5rem 0;
		color: #6b7280;
		font-size: 0.875rem;
	}

	.info-panel {
		background: #f8fafc;
		border-radius: 12px;
		padding: 1.5rem;
		border: 1px solid #e5e7eb;
	}

	.info-panel h3 {
		margin: 0 0 1rem 0;
		color: #1f2937;
	}

	.info-panel ul {
		list-style: none;
		padding: 0;
		margin: 0 0 1rem 0;
	}

	.info-panel li {
		padding: 0.25rem 0;
		color: #4b5563;
	}

	.data-preview {
		margin-top: 1rem;
	}

	.data-preview h4 {
		margin: 0 0 0.5rem 0;
		color: #374151;
	}

	.data-preview pre {
		background: #1f2937;
		color: #e5e7eb;
		padding: 1rem;
		border-radius: 6px;
		overflow-x: auto;
		font-size: 0.75rem;
		margin: 0;
	}

	.toggle-controls {
		position: fixed;
		top: 1rem;
		right: 1rem;
		padding: 0.5rem 1rem;
		background: #3b82f6;
		color: white;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.toggle-controls:hover {
		background: #2563eb;
	}
</style>
