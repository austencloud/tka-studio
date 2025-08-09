<!--
PyToggle Component - Svelte Version
A custom toggle switch with smooth animations.
-->
<script lang="ts">
	interface Props {
		checked?: boolean;
		width?: number;
		bgColor?: string;
		activeColor?: string;
		circleColor?: string;
		disabled?: boolean;
	}

	let { 
		checked = false, 
		width = 50, 
		bgColor = "#00BCff", 
		activeColor = "#00BCff", 
		circleColor = "#FFFFFF",
		disabled = false
	}: Props = $props();

	// State
	let isChecked = $state(checked);

	// Handle click
	function handleToggle() {
		if (!disabled) {
			isChecked = !isChecked;
			// Dispatch custom event
			const event = new CustomEvent('stateChanged', { 
				detail: { checked: isChecked } 
			});
			document.dispatchEvent(event);
		}
	}

	// Export method for parent to control
	export function setChecked(value: boolean) {
		isChecked = value;
	}

	export function getChecked() {
		return isChecked;
	}

	// Computed styles
	let toggleWidth = $derived(`${width}px`);
	let toggleHeight = $derived(`${width * 0.6}px`);
	let circleSize = $derived(`${width * 0.45}px`);
	let circleOffset = $derived(isChecked ? `${width * 0.5}px` : '4px');
</script>

<button 
	class="py-toggle" 
	class:checked={isChecked}
	class:disabled
	{disabled}
	onclick={handleToggle}
	style="
		width: {toggleWidth}; 
		height: {toggleHeight};
		background-color: {isChecked ? activeColor : bgColor};
	"
	type="button"
	role="switch"
	aria-checked={isChecked}
>
	<div 
		class="toggle-circle" 
		style="
			width: {circleSize}; 
			height: {circleSize};
			background-color: {circleColor};
			transform: translateX({circleOffset});
		"
	></div>
</button>

<style>
	.py-toggle {
		position: relative;
		border: none;
		border-radius: 25px;
		cursor: pointer;
		padding: 0;
		transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
		outline: none;
		overflow: hidden;
	}

	.py-toggle:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.py-toggle:focus-visible {
		box-shadow: 0 0 0 2px rgba(0, 188, 255, 0.5);
	}

	.toggle-circle {
		border-radius: 50%;
		transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
		position: absolute;
		top: 50%;
		transform-origin: center;
		margin-top: calc(-1 * var(--circle-size) / 2);
	}
</style>
