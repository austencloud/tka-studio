<!--
Grid Mode Selector - Svelte Version
A compact control using PyToggle for selecting between Diamond and Box grid modes.
-->
<script lang="ts">
	import PyToggle from './PyToggle.svelte';

	interface Props {
		initialMode?: 'DIAMOND' | 'BOX';
	}

	let { initialMode = 'DIAMOND' }: Props = $props();

	// State
	let currentMode = $state(initialMode);
	let toggleRef: PyToggle;

	// Derived
	let isBoxMode = $derived(currentMode === 'BOX');

	// Handle toggle change
	function handleToggleChange(event: CustomEvent) {
		const isChecked = event.detail.checked;
		currentMode = isChecked ? 'BOX' : 'DIAMOND';

		// Dispatch value change
		const changeEvent = new CustomEvent('valueChanged', {
			detail: { value: currentMode },
		});
		document.dispatchEvent(changeEvent);
	}

	// Handle label clicks
	function selectDiamond() {
		if (currentMode !== 'DIAMOND') {
			currentMode = 'DIAMOND';
			toggleRef?.setChecked(false);

			const changeEvent = new CustomEvent('valueChanged', {
				detail: { value: currentMode },
			});
			document.dispatchEvent(changeEvent);
		}
	}

	function selectBox() {
		if (currentMode !== 'BOX') {
			currentMode = 'BOX';
			toggleRef?.setChecked(true);

			const changeEvent = new CustomEvent('valueChanged', {
				detail: { value: currentMode },
			});
			document.dispatchEvent(changeEvent);
		}
	}

	// Public methods
	export function setValue(mode: 'DIAMOND' | 'BOX') {
		currentMode = mode;
		toggleRef?.setChecked(mode === 'BOX');
	}

	export function resetToDefault() {
		setValue('DIAMOND');
	}
</script>

<div class="grid-mode-selector">
	<div class="header-label">Grid Mode:</div>

	<div class="control-layout">
		<button class="mode-label" class:active={!isBoxMode} onclick={selectDiamond} type="button">
			Diamond
		</button>

		<PyToggle
			bind:this={toggleRef}
			checked={isBoxMode}
			width={50}
			bgColor="#00BCff"
			activeColor="#00BCff"
			circleColor="#FFFFFF"
			onstateChanged={handleToggleChange}
		/>

		<button class="mode-label" class:active={isBoxMode} onclick={selectBox} type="button">
			Box
		</button>
	</div>
</div>

<style>
	.grid-mode-selector {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;
		padding: 8px 0;
	}

	.header-label {
		color: rgba(255, 255, 255, 0.9);
		font-size: 14px;
		font-weight: 500;
		text-align: center;
	}

	.control-layout {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.mode-label {
		color: rgba(255, 255, 255, 0.6);
		background: transparent;
		border: none;
		font-size: 18px;
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
		color: rgba(255, 255, 255, 1);
		font-weight: bold;
	}
</style>
