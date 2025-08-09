<!--
Generation Mode Toggle - Svelte Version
Simple toggle between freeform and circular generation modes.
-->
<script lang="ts">
	import PyToggle from './PyToggle.svelte';

	type GenerationMode = 'FREEFORM' | 'CIRCULAR';

	interface Props {
		initialMode?: GenerationMode;
	}

	let { initialMode = 'FREEFORM' }: Props = $props();

	// State
	let currentMode = $state(initialMode);
	let toggleRef: PyToggle;

	// Derived
	let isCircularMode = $derived(currentMode === 'CIRCULAR');

	// Handle toggle change
	function handleToggleChange(event: CustomEvent) {
		const isChecked = event.detail.checked;
		currentMode = isChecked ? 'CIRCULAR' : 'FREEFORM';
		
		// Dispatch mode change
		const changeEvent = new CustomEvent('modeChanged', { 
			detail: { mode: currentMode } 
		});
		document.dispatchEvent(changeEvent);
	}

	// Handle label clicks
	function selectFreeform() {
		if (currentMode !== 'FREEFORM') {
			currentMode = 'FREEFORM';
			toggleRef?.setChecked(false);
			
			const changeEvent = new CustomEvent('modeChanged', { 
				detail: { mode: currentMode } 
			});
			document.dispatchEvent(changeEvent);
		}
	}

	function selectCircular() {
		if (currentMode !== 'CIRCULAR') {
			currentMode = 'CIRCULAR';
			toggleRef?.setChecked(true);
			
			const changeEvent = new CustomEvent('modeChanged', { 
				detail: { mode: currentMode } 
			});
			document.dispatchEvent(changeEvent);
		}
	}

	// Public methods
	export function setMode(mode: GenerationMode) {
		currentMode = mode;
		toggleRef?.setChecked(mode === 'CIRCULAR');
	}

	export function getMode(): GenerationMode {
		return currentMode;
	}
</script>

<div class="generation-mode-toggle">
	<div class="header-label">Generation Mode:</div>
	
	<div class="control-layout">
		<button 
			class="mode-label" 
			class:active={!isCircularMode}
			onclick={selectFreeform}
			type="button"
		>
			Freeform
		</button>
		
		<PyToggle 
			bind:this={toggleRef}
			checked={isCircularMode}
			width={60}
			bgColor="#00BCff"
			activeColor="#00BCff"
			circleColor="#DDD"
			onstateChanged={handleToggleChange}
		/>
		
		<button 
			class="mode-label" 
			class:active={isCircularMode}
			onclick={selectCircular}
			type="button"
		>
			Circular
		</button>
	</div>
</div>

<style>
	.generation-mode-toggle {
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
