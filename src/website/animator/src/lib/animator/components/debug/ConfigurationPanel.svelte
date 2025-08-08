<script lang="ts">
	import type { SequenceData, PropState, PropAttributes } from '../../types/core.js';
	import type { BeatDebugInfo } from '../../types/debug.js';
	import { AnimationEngine } from '../../core/engine/animation-engine.js';
	import AnimatorCanvas from '../canvas/AnimatorCanvas.svelte';

	// Props
	let {
		sequenceData = null,
		debugHistory = [],
		onBeatSelect = () => {},
		onParameterChange = () => {}
	}: {
		sequenceData?: SequenceData | null;
		debugHistory?: BeatDebugInfo[];
		onBeatSelect?: (_beatNumber: number) => void;
		onParameterChange?: (
			_beatNumber: number,
			_prop: 'blue' | 'red',
			_changes: Partial<PropAttributes>
		) => void;
	} = $props();

	// State for interactive testing
	let selectedBeat = $state<number | null>(null);
	let selectedProp = $state<'blue' | 'red' | null>(null);
	let isPlaying = $state(false);
	let editingParameters = $state<Partial<PropAttributes>>({});
	let markedCorrect = $state<Set<string>>(new Set());
	let markedIncorrect = $state<Set<string>>(new Set());

	// Animation engine for single-beat playback
	let miniEngine = new AnimationEngine();
	let blueProp = $state<PropState>({ centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 });
	let redProp = $state<PropState>({ centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 });

	// Initialize mini engine when sequence data changes
	$effect(() => {
		if (sequenceData) {
			miniEngine.initialize(sequenceData);
			updateMiniAnimation();
		}
	});

	// Update mini animation when selected beat changes
	$effect(() => {
		if (selectedBeat !== null) {
			updateMiniAnimation();
		}
	});

	function updateMiniAnimation(): void {
		if (selectedBeat === null || !sequenceData) return;

		// Calculate state for the selected beat
		miniEngine.calculateState(selectedBeat);
		blueProp = miniEngine.getBluePropState();
		redProp = miniEngine.getRedPropState();
	}

	function handleBeatClick(beatNumber: number): void {
		selectedBeat = beatNumber;
		selectedProp = null;
		editingParameters = {};
		onBeatSelect(beatNumber);

		// Play single beat animation
		playSingleBeat(beatNumber);
	}

	function playSingleBeat(beatNumber: number): void {
		if (!sequenceData) return;

		isPlaying = true;
		const startTime = performance.now();
		const duration = 1000; // 1 second for single beat

		function animate(currentTime: number): void {
			const elapsed = currentTime - startTime;
			const progress = Math.min(elapsed / duration, 1);

			// Interpolate within the beat
			const beatTime = beatNumber + progress;
			miniEngine.calculateState(beatTime);
			blueProp = miniEngine.getBluePropState();
			redProp = miniEngine.getRedPropState();

			if (progress < 1 && isPlaying) {
				requestAnimationFrame(animate);
			} else {
				isPlaying = false;
			}
		}

		requestAnimationFrame(animate);
	}

	function handlePropSelect(prop: 'blue' | 'red'): void {
		selectedProp = prop;

		// Load current parameters for editing
		if (selectedBeat !== null && debugHistory.length > 0) {
			const beatInfo = debugHistory.find((b) => b.beatNumber === selectedBeat);
			if (beatInfo) {
				const propInfo = prop === 'blue' ? beatInfo.blueProps : beatInfo.redProps;
				editingParameters = { ...propInfo.attributes };
			}
		}
	}

	function handleParameterEdit(key: keyof PropAttributes, value: any): void {
		editingParameters = { ...editingParameters, [key]: value };

		// Apply changes and update mini animation
		if (selectedBeat !== null && selectedProp) {
			onParameterChange(selectedBeat, selectedProp, { [key]: value });
			updateMiniAnimation();
		}
	}

	function markAsCorrect(beatNumber: number, prop: 'blue' | 'red'): void {
		const key = `${beatNumber}-${prop}`;
		markedCorrect.add(key);
		markedIncorrect.delete(key);
	}

	function markAsIncorrect(beatNumber: number, prop: 'blue' | 'red'): void {
		const key = `${beatNumber}-${prop}`;
		markedIncorrect.add(key);
		markedCorrect.delete(key);
	}

	function getValidationStatus(beatNumber: number): 'valid' | 'warning' | 'error' {
		const beatInfo = debugHistory.find((b) => b.beatNumber === beatNumber);
		if (!beatInfo) return 'valid';

		const hasErrors =
			beatInfo.blueProps.validation.errors.length > 0 ||
			beatInfo.redProps.validation.errors.length > 0;
		const hasWarnings =
			beatInfo.blueProps.validation.warnings.length > 0 ||
			beatInfo.redProps.validation.warnings.length > 0;

		if (hasErrors) return 'error';
		if (hasWarnings) return 'warning';
		return 'valid';
	}

	function getOrientationChain(): Array<{
		beat: number;
		blueStart: string | number;
		blueEnd: string | number;
		redStart: string | number;
		redEnd: string | number;
		blueValid: boolean;
		redValid: boolean;
	}> {
		return debugHistory.map((beat) => ({
			beat: beat.beatNumber,
			blueStart: beat.blueProps.attributes.start_ori || 0,
			blueEnd: beat.blueProps.attributes.end_ori || 0,
			redStart: beat.redProps.attributes.start_ori || 0,
			redEnd: beat.redProps.attributes.end_ori || 0,
			blueValid: beat.blueProps.validation.orientationContinuity.isValid,
			redValid: beat.redProps.validation.orientationContinuity.isValid
		}));
	}
</script>

<div class="motion-testing-panel">
	<!-- Header with Status Indicator -->
	<div class="panel-header">
		<h3>🔧 Interactive Motion Testing & Calibration</h3>
		<div class="status-indicator {getValidationStatus(selectedBeat || 0)}">
			{#if getValidationStatus(selectedBeat || 0) === 'valid'}✓{:else if getValidationStatus(selectedBeat || 0) === 'warning'}⚠{:else}✗{/if}
		</div>
	</div>

	<!-- Main Content Area -->
	<div class="main-content">
		<!-- Left Side: Animation Steps Table -->
		<div class="steps-section">
			<h4>Animation Steps</h4>
			<div class="steps-table-container">
				<table class="steps-table">
					<thead>
						<tr>
							<th>Beat</th>
							<th>Blue Motion</th>
							<th>Red Motion</th>
							<th>Status</th>
							<th>Actions</th>
						</tr>
					</thead>
					<tbody>
						{#each debugHistory as beat (beat.beatNumber)}
							<tr
								class="beat-row {getValidationStatus(beat.beatNumber)}"
								class:selected={selectedBeat === beat.beatNumber}
								onclick={() => handleBeatClick(beat.beatNumber)}
							>
								<td class="beat-number">{beat.beatNumber}</td>
								<td class="motion-info">
									<div class="motion-type">{beat.blueProps.attributes.motion_type}</div>
									<div class="orientation">
										{beat.blueProps.attributes.start_ori} → {beat.blueProps.attributes.end_ori}
									</div>
									<div class="turns">Turns: {beat.blueProps.attributes.turns}</div>
								</td>
								<td class="motion-info">
									<div class="motion-type">{beat.redProps.attributes.motion_type}</div>
									<div class="orientation">
										{beat.redProps.attributes.start_ori} → {beat.redProps.attributes.end_ori}
									</div>
									<div class="turns">Turns: {beat.redProps.attributes.turns}</div>
								</td>
								<td class="status-cell">
									{#if getValidationStatus(beat.beatNumber) === 'valid'}✅
									{:else if getValidationStatus(beat.beatNumber) === 'warning'}⚠️
									{:else}❌{/if}
								</td>
								<td class="actions">
									<button
										class="action-btn play"
										onclick={(e) => {
											e.stopPropagation();
											playSingleBeat(beat.beatNumber);
										}}
										title="Play this beat"
									>
										▶️
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>

		<!-- Right Side: Mini Animation Viewer -->
		<div class="mini-viewer-section">
			<h4>Beat Preview</h4>
			<div class="mini-canvas-container">
				<AnimatorCanvas {blueProp} {redProp} width={300} height={300} gridVisible={true} />
				{#if isPlaying}
					<div class="playing-indicator">▶️ Playing Beat {selectedBeat}</div>
				{/if}
			</div>
		</div>
	</div>

	<!-- Parameter Editing Panel (shown when beat is selected) -->
	{#if selectedBeat !== null}
		<div class="parameter-panel">
			<h4>Beat {selectedBeat} Parameters</h4>

			<!-- Prop Selector -->
			<div class="prop-selector">
				<button
					class="prop-btn blue"
					class:active={selectedProp === 'blue'}
					onclick={() => handlePropSelect('blue')}
				>
					🔵 Blue Prop
				</button>
				<button
					class="prop-btn red"
					class:active={selectedProp === 'red'}
					onclick={() => handlePropSelect('red')}
				>
					🔴 Red Prop
				</button>
			</div>

			<!-- Parameter Controls (shown when prop is selected) -->
			{#if selectedProp && editingParameters}
				<div class="parameter-controls">
					<div class="control-group">
						<label for="motion-type">Motion Type:</label>
						<select
							id="motion-type"
							value={editingParameters.motion_type}
							onchange={(e) =>
								handleParameterEdit('motion_type', (e.target as HTMLSelectElement).value)}
						>
							<option value="pro">Pro</option>
							<option value="anti">Anti</option>
							<option value="static">Static</option>
							<option value="dash">Dash</option>
						</select>
					</div>

					<div class="control-group">
						<label for="rotation-dir">Rotation Direction:</label>
						<select
							id="rotation-dir"
							value={editingParameters.prop_rot_dir}
							onchange={(e) =>
								handleParameterEdit('prop_rot_dir', (e.target as HTMLSelectElement).value)}
						>
							<option value="clockwise">Clockwise</option>
							<option value="counterclockwise">Counterclockwise</option>
							<option value="no_rot">No Rotation</option>
						</select>
					</div>

					<div class="control-group">
						<label for="turns">Turns:</label>
						<input
							id="turns"
							type="number"
							min="0"
							max="10"
							step="0.5"
							value={editingParameters.turns}
							oninput={(e) =>
								handleParameterEdit('turns', parseFloat((e.target as HTMLInputElement).value))}
						/>
					</div>

					<div class="control-group">
						<label for="start-ori">Start Orientation:</label>
						<input
							id="start-ori"
							type="number"
							min="0"
							max="7"
							step="1"
							value={editingParameters.start_ori}
							oninput={(e) =>
								handleParameterEdit('start_ori', parseInt((e.target as HTMLInputElement).value))}
						/>
					</div>

					<div class="control-group">
						<label for="end-ori">End Orientation:</label>
						<input
							id="end-ori"
							type="number"
							min="0"
							max="7"
							step="1"
							value={editingParameters.end_ori}
							oninput={(e) =>
								handleParameterEdit('end_ori', parseInt((e.target as HTMLInputElement).value))}
						/>
					</div>

					<!-- Validation Actions -->
					<div class="validation-actions">
						<button
							class="mark-btn correct"
							onclick={() =>
								selectedBeat !== null && selectedProp && markAsCorrect(selectedBeat, selectedProp)}
						>
							✅ Mark as Correct
						</button>
						<button
							class="mark-btn incorrect"
							onclick={() =>
								selectedBeat !== null &&
								selectedProp &&
								markAsIncorrect(selectedBeat, selectedProp)}
						>
							❌ Mark as Incorrect
						</button>
					</div>
				</div>
			{/if}
		</div>
	{/if}

	<!-- Orientation Continuity Debugging -->
	{#if debugHistory.length > 0}
		<div class="orientation-chain-section">
			<h4>Orientation Continuity Chain</h4>
			<div class="orientation-chain">
				{#each getOrientationChain() as chainItem, index}
					<div class="chain-item" class:invalid={!chainItem.blueValid || !chainItem.redValid}>
						<div class="beat-label">Beat {chainItem.beat}</div>
						<div class="prop-orientations">
							<div class="blue-ori" class:invalid={!chainItem.blueValid}>
								🔵 {chainItem.blueStart} → {chainItem.blueEnd}
							</div>
							<div class="red-ori" class:invalid={!chainItem.redValid}>
								🔴 {chainItem.redStart} → {chainItem.redEnd}
							</div>
						</div>
						{#if index < getOrientationChain().length - 1}
							<div class="chain-arrow">→</div>
						{/if}
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	.motion-testing-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		gap: 1rem;
		overflow: hidden;
	}

	.panel-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem;
		border-bottom: 1px solid var(--color-border);
		background: var(--color-surface-elevated);
	}

	.panel-header h3 {
		margin: 0;
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.status-indicator {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 24px;
		height: 24px;
		border-radius: 50%;
		font-weight: bold;
		font-size: 0.875rem;
	}

	.status-indicator.valid {
		background: #10b981;
		color: white;
	}

	.status-indicator.warning {
		background: #f59e0b;
		color: white;
	}

	.status-indicator.error {
		background: #ef4444;
		color: white;
	}

	.main-content {
		display: grid;
		grid-template-columns: 2fr 1fr;
		gap: 1rem;
		flex: 1;
		overflow: hidden;
		padding: 0 1rem;
	}

	.steps-section {
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.steps-section h4 {
		margin: 0 0 0.5rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.steps-table-container {
		flex: 1;
		overflow: auto;
		border: 1px solid var(--color-border);
		border-radius: 8px;
		background: var(--color-surface-elevated);
	}

	.steps-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.875rem;
	}

	.steps-table th {
		background: var(--color-surface);
		color: var(--color-text-secondary);
		font-weight: 600;
		padding: 0.75rem 0.5rem;
		text-align: left;
		border-bottom: 1px solid var(--color-border);
		position: sticky;
		top: 0;
		z-index: 1;
	}

	.steps-table td {
		padding: 0.5rem;
		border-bottom: 1px solid var(--color-border);
		vertical-align: top;
	}

	.beat-row {
		cursor: pointer;
		transition: background-color 0.2s ease;
	}

	.beat-row:hover {
		background: var(--color-surface-hover);
	}

	.beat-row.selected {
		background: rgba(59, 130, 246, 0.1);
		border-left: 3px solid var(--color-primary);
	}

	.beat-row.error {
		background: rgba(239, 68, 68, 0.05);
	}

	.beat-row.warning {
		background: rgba(245, 158, 11, 0.05);
	}

	.beat-number {
		font-weight: 600;
		color: var(--color-text);
	}

	.motion-info {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.motion-type {
		font-weight: 600;
		color: var(--color-primary);
	}

	.orientation {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
	}

	.turns {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
	}

	.status-cell {
		text-align: center;
		font-size: 1rem;
	}

	.actions {
		text-align: center;
	}

	.action-btn {
		background: none;
		border: none;
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		transition: background-color 0.2s ease;
		font-size: 1rem;
	}

	.action-btn:hover {
		background: var(--color-surface-hover);
	}

	.mini-viewer-section {
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.mini-viewer-section h4 {
		margin: 0 0 0.5rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.mini-canvas-container {
		position: relative;
		border: 1px solid var(--color-border);
		border-radius: 8px;
		background: var(--color-surface-elevated);
		padding: 1rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
	}

	.playing-indicator {
		position: absolute;
		top: 8px;
		left: 8px;
		background: rgba(0, 0, 0, 0.7);
		color: white;
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		font-size: 0.75rem;
		font-weight: 500;
	}

	.parameter-panel {
		margin: 0 1rem;
		padding: 1rem;
		background: var(--color-surface-elevated);
		border: 1px solid var(--color-border);
		border-radius: 8px;
	}

	.parameter-panel h4 {
		margin: 0 0 1rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.prop-selector {
		display: flex;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}

	.prop-btn {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		padding: 0.5rem 1rem;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.875rem;
		font-weight: 500;
	}

	.prop-btn:hover {
		background: var(--color-surface-hover);
	}

	.prop-btn.active {
		background: var(--color-primary);
		color: white;
		border-color: var(--color-primary);
	}

	.parameter-controls {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1rem;
	}

	.control-group {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.control-group label {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-text);
	}

	.control-group select,
	.control-group input {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 4px;
		padding: 0.5rem;
		color: var(--color-text);
		font-size: 0.875rem;
	}

	.validation-actions {
		grid-column: 1 / -1;
		display: flex;
		gap: 0.5rem;
		margin-top: 1rem;
	}

	.mark-btn {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		padding: 0.5rem 1rem;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.875rem;
		font-weight: 500;
	}

	.mark-btn:hover {
		background: var(--color-surface-hover);
	}

	.mark-btn.correct {
		border-color: #10b981;
		color: #10b981;
	}

	.mark-btn.correct:hover {
		background: rgba(16, 185, 129, 0.1);
	}

	.mark-btn.incorrect {
		border-color: #ef4444;
		color: #ef4444;
	}

	.mark-btn.incorrect:hover {
		background: rgba(239, 68, 68, 0.1);
	}

	.orientation-chain-section {
		margin: 0 1rem 1rem 1rem;
		padding: 1rem;
		background: var(--color-surface-elevated);
		border: 1px solid var(--color-border);
		border-radius: 8px;
	}

	.orientation-chain-section h4 {
		margin: 0 0 1rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.orientation-chain {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		align-items: center;
	}

	.chain-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
		padding: 0.75rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		min-width: 120px;
	}

	.chain-item.invalid {
		border-color: #ef4444;
		background: rgba(239, 68, 68, 0.05);
	}

	.beat-label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		text-transform: uppercase;
	}

	.prop-orientations {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		text-align: center;
	}

	.blue-ori,
	.red-ori {
		font-size: 0.875rem;
		font-weight: 500;
	}

	.blue-ori.invalid,
	.red-ori.invalid {
		color: #ef4444;
		font-weight: 600;
	}

	.chain-arrow {
		font-size: 1.25rem;
		color: var(--color-text-secondary);
		margin: 0 0.5rem;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.main-content {
			grid-template-columns: 1fr;
			grid-template-rows: 1fr auto;
		}

		.parameter-controls {
			grid-template-columns: 1fr;
		}

		.orientation-chain {
			flex-direction: column;
			align-items: stretch;
		}

		.chain-arrow {
			transform: rotate(90deg);
			margin: 0.5rem 0;
		}
	}
</style>
