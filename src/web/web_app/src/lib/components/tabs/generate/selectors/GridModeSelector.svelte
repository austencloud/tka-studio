<!--
Grid Mode Selector - Svelte Version
A compact control using segmented control for selecting between Diamond and Box grid modes.
-->
<script lang="ts">
	import IOSToggle from '../../../ui/IOSToggle.svelte';

	type GridMode = 'DIAMOND' | 'BOX';

	interface Props {
		initialMode?: GridMode;
		onvalueChanged?: (value: GridMode) => void;
	}

	let { initialMode = 'DIAMOND', onvalueChanged }: Props = $props();

	// State
	let currentMode = $state(initialMode);

	// Options for the segmented control
	const gridOptions = [
		{ value: 'DIAMOND', label: 'Diamond', icon: '◆' },
		{ value: 'BOX', label: 'Box', icon: '⬜' },
	];

	// Handle mode change
	function handleModeChange(newMode: string) {
		const mode = newMode as GridMode;
		currentMode = mode;
		onvalueChanged?.(mode);
	}

	// Public methods
	export function setValue(mode: GridMode) {
		currentMode = mode;
	}

	export function resetToDefault() {
		setValue('DIAMOND');
	}
</script>

<IOSToggle
	value={currentMode}
	options={gridOptions}
	label="Grid Mode"
	onchange={handleModeChange}
	size="medium"
/>
