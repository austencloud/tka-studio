<script lang="ts">
	import type { BeatDebugInfo, DebugModalState, BeatOverride } from '../../types/debug.js';
	import type { SequenceDebugger } from '../../core/debug/sequence-debugger.js';
	import BeatSelector from './BeatSelector.svelte';
	import EditorControls from './EditorControls.svelte';
	import AttributeEditor from './AttributeEditor.svelte';
	import InterpretationDisplay from './InterpretationDisplay.svelte';
	import ValidationDisplay from './ValidationDisplay.svelte';
	import ComparisonView from './ComparisonView.svelte';

	// Props
	let {
		debugHistory = [],
		modalState,
		sequenceDebugger = null,
		onOverrideApply = () => {}
	}: {
		debugHistory?: BeatDebugInfo[];
		modalState: DebugModalState;
		sequenceDebugger?: SequenceDebugger | null;
		onOverrideApply?: (_overrides: any) => void;
	} = $props();

	// State
	let selectedBeat = $state<number | null>(null);
	let selectedProp = $state<'blue' | 'red' | null>(null);
	let editMode = $state<'view' | 'edit' | 'compare'>('view');
	let originalAttributes = $state<any>(null);
	let modifiedAttributes = $state<any>(null);

	// Computed values
	let currentBeatData = $derived(() => {
		if (selectedBeat === null) return null;
		return debugHistory.find((beat) => beat.beatNumber === selectedBeat);
	});

	let currentPropData = $derived(() => {
		const beatData = currentBeatData();
		if (!beatData || !selectedProp) return null;
		return selectedProp === 'blue' ? beatData.blueProps : beatData.redProps;
	});

	// Watch for modal state changes - only update if different to prevent loops
	$effect(() => {
		if (modalState.selectedBeat !== null && modalState.selectedBeat !== selectedBeat) {
			selectedBeat = modalState.selectedBeat;
		}
		if (modalState.selectedProp !== null && modalState.selectedProp !== selectedProp) {
			selectedProp = modalState.selectedProp;
		}
	});

	// Initialize edit mode when beat/prop is selected - only when changing to view mode
	$effect(() => {
		const propData = currentPropData();
		if (propData && editMode === 'view' && (!originalAttributes || !modifiedAttributes)) {
			originalAttributes = { ...propData.attributes };
			modifiedAttributes = { ...propData.attributes };
		}
	});

	function handleBeatSelect(beatNumber: number): void {
		selectedBeat = beatNumber;
		selectedProp = null;
		editMode = 'view';
	}

	function handlePropSelect(prop: 'blue' | 'red'): void {
		selectedProp = prop;
		editMode = 'view';

		const propData = currentPropData();
		if (propData) {
			originalAttributes = { ...propData.attributes };
			modifiedAttributes = { ...propData.attributes };
		}
	}

	function startEdit(): void {
		editMode = 'edit';
	}

	function cancelEdit(): void {
		editMode = 'view';
		if (originalAttributes) {
			modifiedAttributes = { ...originalAttributes };
		}
	}

	function saveEdit(): void {
		if (!selectedBeat || !selectedProp || !modifiedAttributes) return;

		const override: BeatOverride = {
			beatNumber: selectedBeat,
			enabled: true,
			...(selectedProp === 'blue'
				? { blueOverrides: modifiedAttributes }
				: { redOverrides: modifiedAttributes })
		};

		// Apply override
		const currentOverrides = sequenceDebugger?.getOverrides() || {
			beatOverrides: new Map(),
			globalOverrides: {}
		};
		currentOverrides.beatOverrides.set(selectedBeat, override);

		onOverrideApply({ beatOverrides: currentOverrides.beatOverrides });

		editMode = 'view';
	}

	function toggleCompareMode(): void {
		editMode = editMode === 'compare' ? 'view' : 'compare';
	}

	function resetToOriginal(): void {
		if (originalAttributes) {
			modifiedAttributes = { ...originalAttributes };
		}
	}

	function handleAttributeChange(key: string, value: any): void {
		if (modifiedAttributes) {
			modifiedAttributes = { ...modifiedAttributes, [key]: value };
		}
	}
</script>

<div class="beat-editor">
	<!-- Beat and Prop Selection -->
	<BeatSelector
		{debugHistory}
		{selectedBeat}
		{selectedProp}
		onBeatSelect={handleBeatSelect}
		onPropSelect={handlePropSelect}
	/>

	{#if currentBeatData() && currentPropData()}
		{@const propData = currentPropData()}

		<!-- Editor Controls -->
		<EditorControls
			{editMode}
			onStartEdit={startEdit}
			onSaveEdit={saveEdit}
			onCancelEdit={cancelEdit}
			onResetToOriginal={resetToOriginal}
			onToggleCompare={toggleCompareMode}
		/>

		<!-- Attribute Editor -->
		<AttributeEditor
			{editMode}
			attributes={modifiedAttributes}
			onAttributeChange={handleAttributeChange}
		/>

		<!-- Interpretation Analysis -->
		<InterpretationDisplay {propData} />

		<!-- Validation Results -->
		<ValidationDisplay {propData} />

		<!-- Comparison Mode -->
		<ComparisonView {originalAttributes} {modifiedAttributes} isVisible={editMode === 'compare'} />
	{:else}
		<div class="no-selection">
			<p>Select a beat and prop to begin editing</p>
		</div>
	{/if}
</div>

<style>
	.beat-editor {
		display: flex;
		flex-direction: column;
		height: 100%;
		padding: 1rem;
		gap: 1rem;
		overflow-y: auto;
	}

	.no-selection {
		text-align: center;
		padding: 2rem;
		color: var(--color-text-secondary);
		background: var(--color-surface-elevated);
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.beat-editor {
			padding: 0.5rem;
		}
	}
</style>
