<!--
Generation Mode Toggle - Svelte Version
Toggle between freeform and circular generation modes using modern segmented control.
-->
<script lang="ts">
	import IOSToggle from '../../../ui/IOSToggle.svelte';

	type GenerationMode = 'FREEFORM' | 'CIRCULAR';

	interface Props {
		initialMode?: GenerationMode;
		onmodeChanged?: (mode: GenerationMode) => void;
	}

	let { initialMode = 'FREEFORM', onmodeChanged }: Props = $props();

	// State
	let currentMode = $state(initialMode);

	// Options for the segmented control
	const modeOptions = [
		{ value: 'FREEFORM', label: 'Freeform', icon: '🎯' },
		{ value: 'CIRCULAR', label: 'Circular', icon: '🔄' }
	];

	// Handle mode change
	function handleModeChange(newMode: string) {
		const mode = newMode as GenerationMode;
		currentMode = mode;
		onmodeChanged?.(mode);
	}

	// Public methods
	export function setMode(mode: GenerationMode) {
		currentMode = mode;
	}

	export function getMode(): GenerationMode {
		return currentMode;
	}
</script>

<IOSToggle
	value={currentMode}
	options={modeOptions}
	label="Generation Mode"
	onchange={handleModeChange}
	size="medium"
/>
