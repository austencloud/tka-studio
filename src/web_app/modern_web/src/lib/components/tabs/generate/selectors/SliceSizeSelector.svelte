<!--
Slice Size Selector - Svelte Version
Beautiful iOS-style toggle between halved and quartered slice sizes for circular mode.
-->
<script lang="ts">
	import IOSToggle from '../../../ui/IOSToggle.svelte';

	type SliceSize = 'HALVED' | 'QUARTERED';

	interface Props {
		initialValue?: SliceSize;
		onvalueChanged?: (value: SliceSize) => void;
	}

	let { initialValue = 'HALVED', onvalueChanged }: Props = $props();

	// State
	let currentValue = $state(initialValue);

	// Options for the iOS toggle
	const sliceSizeOptions = [
		{ value: 'HALVED', label: 'Halved', icon: '◗' },
		{ value: 'QUARTERED', label: 'Quartered', icon: '◐' }
	];

	// Handle value change
	function handleValueChange(newValue: string) {
		const value = newValue as SliceSize;
		currentValue = value;
		onvalueChanged?.(value);
	}

	// Public methods
	export function setValue(value: SliceSize) {
		currentValue = value;
	}

	export function getValue(): SliceSize {
		return currentValue;
	}
</script>

<IOSToggle
	value={currentValue}
	options={sliceSizeOptions}
	label="Slice Size"
	onchange={handleValueChange}
	size="medium"
/>
