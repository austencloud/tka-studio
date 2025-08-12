<!--
CAP Type Selector - Svelte Version
Simple row of 4 toggleable buttons for selecting circular arrangement pattern types.
-->
<script lang="ts">
	type CAPComponent = 'ROTATED' | 'MIRRORED' | 'SWAPPED' | 'COMPLEMENTARY';

	// Legacy CAP types for backward compatibility
	type CAPType =
		| 'STRICT_ROTATED'
		| 'STRICT_MIRRORED'
		| 'STRICT_SWAPPED'
		| 'STRICT_COMPLEMENTARY'
		| 'MIRRORED_SWAPPED'
		| 'SWAPPED_COMPLEMENTARY'
		| 'ROTATED_COMPLEMENTARY'
		| 'MIRRORED_COMPLEMENTARY'
		| 'ROTATED_SWAPPED'
		| 'MIRRORED_ROTATED'
		| 'MIRRORED_COMPLEMENTARY_ROTATED';

	interface Props {
		initialValue?: CAPType;
		onvalueChanged?: (value: CAPType) => void;
	}

	let { initialValue = 'STRICT_ROTATED', onvalueChanged }: Props = $props();

	// State - track which components are selected
	let selectedComponents = $state(new Set<CAPComponent>());

	// Component data with colors and icons
	const capComponents: Array<{
		component: CAPComponent;
		label: string;
		icon: string;
		color: string;
	}> = [
		{ component: 'ROTATED', label: 'Rotated', icon: '🔄', color: '#36c3ff' },
		{ component: 'MIRRORED', label: 'Mirrored', icon: '🪞', color: '#6F2DA8' },
		{ component: 'SWAPPED', label: 'Swapped', icon: '🔀', color: '#26e600' },
		{ component: 'COMPLEMENTARY', label: 'Complementary', icon: '🎨', color: '#eb7d00' },
	];

	// Convert legacy CAP type to component set
	function capTypeToComponents(capType: CAPType): Set<CAPComponent> {
		const components = new Set<CAPComponent>();

		if (capType.includes('ROTATED')) components.add('ROTATED');
		if (capType.includes('MIRRORED')) components.add('MIRRORED');
		if (capType.includes('SWAPPED')) components.add('SWAPPED');
		if (capType.includes('COMPLEMENTARY')) components.add('COMPLEMENTARY');

		// Handle strict types (single component)
		if (capType === 'STRICT_ROTATED') components.add('ROTATED');
		if (capType === 'STRICT_MIRRORED') components.add('MIRRORED');
		if (capType === 'STRICT_SWAPPED') components.add('SWAPPED');
		if (capType === 'STRICT_COMPLEMENTARY') components.add('COMPLEMENTARY');

		return components;
	}

	// Convert component set to legacy CAP type
	function componentsToCapType(components: Set<CAPComponent>): CAPType {
		const sorted = Array.from(components).sort();

		// Single components (strict)
		if (sorted.length === 1) {
			switch (sorted[0]) {
				case 'ROTATED':
					return 'STRICT_ROTATED';
				case 'MIRRORED':
					return 'STRICT_MIRRORED';
				case 'SWAPPED':
					return 'STRICT_SWAPPED';
				case 'COMPLEMENTARY':
					return 'STRICT_COMPLEMENTARY';
			}
		}

		// Two components
		if (sorted.length === 2) {
			const key = sorted.join('_');
			switch (key) {
				case 'MIRRORED_SWAPPED':
					return 'MIRRORED_SWAPPED';
				case 'COMPLEMENTARY_SWAPPED':
					return 'SWAPPED_COMPLEMENTARY';
				case 'COMPLEMENTARY_ROTATED':
					return 'ROTATED_COMPLEMENTARY';
				case 'COMPLEMENTARY_MIRRORED':
					return 'MIRRORED_COMPLEMENTARY';
				case 'ROTATED_SWAPPED':
					return 'ROTATED_SWAPPED';
				case 'MIRRORED_ROTATED':
					return 'MIRRORED_ROTATED';
			}
		}

		// Three components
		if (
			sorted.length === 3 &&
			sorted.includes('MIRRORED') &&
			sorted.includes('COMPLEMENTARY') &&
			sorted.includes('ROTATED')
		) {
			return 'MIRRORED_COMPLEMENTARY_ROTATED';
		}

		// Default fallback
		return 'STRICT_ROTATED';
	}

	// Initialize from legacy CAP type
	$effect(() => {
		selectedComponents = capTypeToComponents(initialValue);
	});

	// Handle component toggle
	function toggleComponent(component: CAPComponent) {
		const newComponents = new Set(selectedComponents);

		if (newComponents.has(component)) {
			newComponents.delete(component);
			// Ensure at least one component is selected
			if (newComponents.size === 0) {
				newComponents.add(component);
			}
		} else {
			newComponents.add(component);
		}

		selectedComponents = newComponents;
		const capType = componentsToCapType(newComponents);
		onvalueChanged?.(capType);
	}

	// Public methods
	export function setValue(value: CAPType) {
		selectedComponents = capTypeToComponents(value);
	}

	export function getValue(): CAPType {
		return componentsToCapType(selectedComponents);
	}
</script>

<div class="cap-type-selector">
	<div class="header-label">CAP Components:</div>

	<div class="button-layout">
		{#each capComponents as { component, label, icon, color }}
			<button
				class="cap-button"
				class:checked={selectedComponents.has(component)}
				onclick={() => toggleComponent(component)}
				style="
					{selectedComponents.has(component)
					? `background: ${color}; border-color: ${color}; color: white;`
					: `border-color: ${color}; color: ${color};`}
				"
				type="button"
			>
				<span class="button-icon">{icon}</span>
				<span class="button-label">{label}</span>
			</button>
		{/each}
	</div>
</div>

<style>
	.cap-type-selector {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 12px;
		padding: 8px 0;
	}

	.header-label {
		color: rgba(255, 255, 255, 0.9);
		font-size: 14px;
		font-weight: 500;
		text-align: center;
	}

	.button-layout {
		display: flex;
		gap: 8px;
		flex-wrap: wrap;
		justify-content: center;
		max-width: 100%;
	}

	.cap-button {
		flex: 1;
		min-width: 0;
		max-width: 120px;
		height: 44px;
		background: rgba(255, 255, 255, 0.05);
		border: 2px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		color: rgba(255, 255, 255, 0.7);
		font-size: 12px;
		font-weight: 500;
		padding: 6px 8px;
		cursor: pointer;
		transition: all 0.2s ease;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 2px;
		text-align: center;
		white-space: nowrap;
		overflow: hidden;
	}

	.cap-button:hover:not(.checked) {
		background: rgba(255, 255, 255, 0.1);
		transform: translateY(-1px);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
	}

	.cap-button.checked {
		font-weight: 600;
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	}

	.button-icon {
		font-size: 16px;
		line-height: 1;
	}

	.button-label {
		font-size: 10px;
		line-height: 1.2;
		font-weight: inherit;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.button-layout {
			gap: 6px;
		}

		.cap-button {
			min-width: 70px;
			max-width: 90px;
			height: 40px;
			padding: 4px 6px;
		}

		.button-icon {
			font-size: 14px;
		}

		.button-label {
			font-size: 9px;
		}
	}
</style>
