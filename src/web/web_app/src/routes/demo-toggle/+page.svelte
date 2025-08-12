<!--
Demo page to showcase the new iOS-style toggle component
-->
<script lang="ts">
	import IOSToggle from '$lib/components/ui/IOSToggle.svelte';

	// Demo states
	let generationMode = $state('FREEFORM');
	let gridMode = $state('DIAMOND');
	let propContinuity = $state('CONTINUOUS');

	// Options
	const generationOptions = [
		{ value: 'FREEFORM', label: 'Freeform', icon: '🎯' },
		{ value: 'CIRCULAR', label: 'Circular', icon: '🔄' },
	];

	const gridOptions = [
		{ value: 'DIAMOND', label: 'Diamond', icon: '◆' },
		{ value: 'BOX', label: 'Box', icon: '⬜' },
	];

	const continuityOptions = [
		{ value: 'RANDOM', label: 'Random', icon: '🎲' },
		{ value: 'CONTINUOUS', label: 'Continuous', icon: '🔗' },
	];

	// Handlers
	function handleGenerationModeChange(value: string) {
		generationMode = value;
		console.log('Generation mode changed to:', value);
	}

	function handleGridModeChange(value: string) {
		gridMode = value;
		console.log('Grid mode changed to:', value);
	}

	function handleContinuityChange(value: string) {
		propContinuity = value;
		console.log('Prop continuity changed to:', value);
	}
</script>

<svelte:head>
	<title>Toggle Demo - TKA Modern Web</title>
</svelte:head>

<div class="demo-page">
	<div class="demo-container">
		<h1>Beautiful iOS-Style Toggle Controls</h1>
		<p>Elegant toggle switches that replace the old confusing toggle + label pattern</p>

		<div class="demo-section">
			<h2>Before vs After</h2>
			<div class="comparison">
				<div class="before">
					<h3>❌ Old Pattern (Confusing)</h3>
					<p>Toggle switch with clickable labels on both sides</p>
					<div class="old-toggle-mockup">
						<span class="label">Freeform</span>
						<div class="toggle-switch"></div>
						<span class="label">Circular</span>
					</div>
					<p class="issue">Issues: 3 clickable areas, unclear interaction model</p>
				</div>

				<div class="after">
					<h3>✅ New Pattern (Clear)</h3>
					<p>Beautiful iOS-style toggle with clear labels</p>
					<IOSToggle
						value={generationMode}
						options={generationOptions}
						label="Generation Mode"
						onchange={handleGenerationModeChange}
						size="medium"
					/>
					<p class="benefit">
						Benefits: Single interaction, elegant design, clear feedback
					</p>
				</div>
			</div>
		</div>

		<div class="demo-section">
			<h2>All Toggle Controls</h2>
			<div class="controls-grid">
				<div class="control-demo">
					<IOSToggle
						value={generationMode}
						options={generationOptions}
						label="Generation Mode"
						onchange={handleGenerationModeChange}
						size="medium"
					/>
					<p>Current: {generationMode}</p>
				</div>

				<div class="control-demo">
					<IOSToggle
						value={gridMode}
						options={gridOptions}
						label="Grid Mode"
						onchange={handleGridModeChange}
						size="medium"
					/>
					<p>Current: {gridMode}</p>
				</div>

				<div class="control-demo">
					<IOSToggle
						value={propContinuity}
						options={continuityOptions}
						label="Prop Continuity"
						onchange={handleContinuityChange}
						size="medium"
					/>
					<p>Current: {propContinuity}</p>
				</div>
			</div>
		</div>

		<div class="demo-section">
			<h2>Size Variants</h2>
			<div class="size-demos">
				<IOSToggle
					value={generationMode}
					options={generationOptions}
					label="Small Size"
					onchange={handleGenerationModeChange}
					size="small"
				/>

				<IOSToggle
					value={generationMode}
					options={generationOptions}
					label="Medium Size"
					onchange={handleGenerationModeChange}
					size="medium"
				/>

				<IOSToggle
					value={generationMode}
					options={generationOptions}
					label="Large Size"
					onchange={handleGenerationModeChange}
					size="large"
				/>
			</div>
		</div>

		<div class="demo-section">
			<h2>Benefits</h2>
			<ul class="benefits-list">
				<li>
					✅ <strong>Single interaction model</strong> - Only the toggle itself is clickable
				</li>
				<li>
					✅ <strong>Beautiful iOS design</strong> - Smooth animations and elegant appearance
				</li>
				<li>
					✅ <strong>Clear visual feedback</strong> - Labels show which option is active
				</li>
				<li>✅ <strong>Familiar pattern</strong> - Users recognize this from iOS/macOS</li>
				<li>✅ <strong>Accessible</strong> - Proper ARIA roles and keyboard navigation</li>
				<li>✅ <strong>Responsive</strong> - Works perfectly on touch and mouse devices</li>
				<li>✅ <strong>No confusion</strong> - Labels are visual only, not clickable</li>
			</ul>
		</div>
	</div>
</div>

<style>
	.demo-page {
		min-height: 100vh;
		background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
		color: white;
		padding: 2rem;
	}

	.demo-container {
		max-width: 1200px;
		margin: 0 auto;
	}

	h1 {
		text-align: center;
		font-size: 2.5rem;
		margin-bottom: 1rem;
		background: linear-gradient(45deg, #4facfe, #00f2fe);
		background-clip: text;
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
	}

	.demo-section {
		margin: 3rem 0;
		padding: 2rem;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.comparison {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 2rem;
		margin-top: 1rem;
	}

	.before,
	.after {
		padding: 1.5rem;
		border-radius: 8px;
	}

	.before {
		background: rgba(255, 0, 0, 0.1);
		border: 1px solid rgba(255, 0, 0, 0.3);
	}

	.after {
		background: rgba(0, 255, 0, 0.1);
		border: 1px solid rgba(0, 255, 0, 0.3);
	}

	.old-toggle-mockup {
		display: flex;
		align-items: center;
		gap: 12px;
		margin: 1rem 0;
		padding: 1rem;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 6px;
	}

	.toggle-switch {
		width: 60px;
		height: 30px;
		background: #333;
		border-radius: 15px;
		position: relative;
	}

	.toggle-switch::after {
		content: '';
		position: absolute;
		width: 26px;
		height: 26px;
		background: white;
		border-radius: 50%;
		top: 2px;
		left: 2px;
	}

	.label {
		color: rgba(255, 255, 255, 0.7);
		cursor: pointer;
		padding: 4px 8px;
		border-radius: 4px;
	}

	.controls-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 2rem;
		margin-top: 1rem;
	}

	.control-demo {
		padding: 1.5rem;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		text-align: center;
	}

	.size-demos {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		align-items: center;
		margin-top: 1rem;
	}

	.benefits-list {
		list-style: none;
		padding: 0;
	}

	.benefits-list li {
		margin: 1rem 0;
		padding: 0.5rem 0;
		font-size: 1.1rem;
	}

	.issue {
		color: #ff6b6b;
		font-style: italic;
		margin-top: 1rem;
	}

	.benefit {
		color: #51cf66;
		font-style: italic;
		margin-top: 1rem;
	}

	@media (max-width: 768px) {
		.comparison {
			grid-template-columns: 1fr;
		}

		.controls-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
