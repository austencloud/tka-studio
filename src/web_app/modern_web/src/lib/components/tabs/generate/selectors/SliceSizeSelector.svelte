<!--
Slice Size Selector - Svelte Version
Simple toggle between halved and quartered slice sizes for circular mode.
-->
<script lang="ts">
	import PyToggle from './PyToggle.svelte';

	type SliceSize = 'HALVED' | 'QUARTERED';

	interface Props {
		initialValue?: SliceSize;
	}

	let { initialValue = 'HALVED' }: Props = $props();

	// State
	let currentValue = $state(initialValue);
	let toggleRef: PyToggle;

	// Derived
	let isQuartered = $derived(currentValue === 'QUARTERED');

	// Handle toggle change
	function handleToggleChange(event: CustomEvent) {
		const isChecked = event.detail.checked;
		currentValue = isChecked ? 'QUARTERED' : 'HALVED';
		
		// Dispatch value change
		const changeEvent = new CustomEvent('valueChanged', { 
			detail: { value: currentValue } 
		});
		document.dispatchEvent(changeEvent);
	}

	// Handle label clicks
	function selectHalved() {
		if (currentValue !== 'HALVED') {
			currentValue = 'HALVED';
			toggleRef?.setChecked(false);
			
			const changeEvent = new CustomEvent('valueChanged', { 
				detail: { value: currentValue } 
			});
			document.dispatchEvent(changeEvent);
		}
	}

	function selectQuartered() {
		if (currentValue !== 'QUARTERED') {
			currentValue = 'QUARTERED';
			toggleRef?.setChecked(true);
			
			const changeEvent = new CustomEvent('valueChanged', { 
				detail: { value: currentValue } 
			});
			document.dispatchEvent(changeEvent);
		}
	}

	// Public methods
	export function setValue(value: SliceSize) {
		currentValue = value;
		toggleRef?.setChecked(value === 'QUARTERED');
	}

	export function getValue(): SliceSize {
		return currentValue;
	}
</script>

<div class="slice-size-selector">
	<div class="control-layout">
		<button 
			class="mode-label" 
			class:active={!isQuartered}
			onclick={selectHalved}
			type="button"
		>
			Halved
		</button>
		
		<PyToggle 
			bind:this={toggleRef}
			checked={isQuartered}
			width={60}
			bgColor="#00BCff"
			activeColor="#00BCff"
			circleColor="#DDD"
			onstateChanged={handleToggleChange}
		/>
		
		<button 
			class="mode-label" 
			class:active={isQuartered}
			onclick={selectQuartered}
			type="button"
		>
			Quartered
		</button>
	</div>
</div>

<style>
	.slice-size-selector {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 8px 0;
	}

	.control-layout {
		display: flex;
		align-items: center;
		gap: 12px;
	}

	.mode-label {
		color: gray;
		background: transparent;
		border: none;
		font-size: 14px;
		font-weight: normal;
		cursor: pointer;
		padding: 4px 8px;
		border-radius: 4px;
		transition: all 0.2s ease;
	}

	.mode-label:hover {
		background: rgba(255, 255, 255, 0.05);
	}

	.mode-label.active {
		color: white;
		font-weight: bold;
	}
</style>
