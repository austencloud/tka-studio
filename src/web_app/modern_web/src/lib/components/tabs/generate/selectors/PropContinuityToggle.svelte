<!--
Prop Continuity Toggle - Svelte Version
Simple toggle between random and continuous prop behavior.
-->
<script lang="ts">
	import PyToggle from './PyToggle.svelte';

	type PropContinuity = 'RANDOM' | 'CONTINUOUS';

	interface Props {
		initialValue?: PropContinuity;
	}

	let { initialValue = 'CONTINUOUS' }: Props = $props();

	// State
	let currentValue = $state(initialValue);
	let toggleRef: PyToggle;

	// Derived
	let isContinuous = $derived(currentValue === 'CONTINUOUS');

	// Handle toggle change
	function handleToggleChange(event: CustomEvent) {
		const isChecked = event.detail.checked;
		currentValue = isChecked ? 'CONTINUOUS' : 'RANDOM';

		// Dispatch value change
		const changeEvent = new CustomEvent('valueChanged', {
			detail: { value: currentValue },
		});
		document.dispatchEvent(changeEvent);
	}

	// Handle label clicks
	function selectRandom() {
		if (currentValue !== 'RANDOM') {
			currentValue = 'RANDOM';
			toggleRef?.setChecked(false);

			const changeEvent = new CustomEvent('valueChanged', {
				detail: { value: currentValue },
			});
			document.dispatchEvent(changeEvent);
		}
	}

	function selectContinuous() {
		if (currentValue !== 'CONTINUOUS') {
			currentValue = 'CONTINUOUS';
			toggleRef?.setChecked(true);

			const changeEvent = new CustomEvent('valueChanged', {
				detail: { value: currentValue },
			});
			document.dispatchEvent(changeEvent);
		}
	}

	// Public methods
	export function setValue(value: PropContinuity) {
		currentValue = value;
		toggleRef?.setChecked(value === 'CONTINUOUS');
	}

	export function getValue(): PropContinuity {
		return currentValue;
	}
</script>

<div class="prop-continuity-toggle">
	<div class="header-label">Prop Continuity:</div>

	<div class="control-layout">
		<button
			class="mode-label"
			class:active={!isContinuous}
			onclick={selectRandom}
			type="button"
		>
			Random
		</button>

		<PyToggle
			bind:this={toggleRef}
			checked={isContinuous}
			width={60}
			bgColor="#00BCff"
			activeColor="#00BCff"
			circleColor="#DDD"
			onstateChanged={handleToggleChange}
		/>

		<button
			class="mode-label"
			class:active={isContinuous}
			onclick={selectContinuous}
			type="button"
		>
			Continuous
		</button>
	</div>
</div>

<style>
	.prop-continuity-toggle {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;
		padding: 8px 0;
	}

	.header-label {
		color: rgba(255, 255, 255, 0.9);
		font-size: 16px;
		font-weight: 500;
		text-align: center;
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
		color: white;
		font-weight: bold;
	}
</style>
