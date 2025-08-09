<!--
CAP Type Selector - Svelte Version
Grid of buttons for selecting circular arrangement pattern types.
-->
<script lang="ts">
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
	}

	let { initialValue = 'STRICT_ROTATED' }: Props = $props();

	// State
	let currentValue = $state(initialValue);

	// CAP type data: [cap_type, display_text, row, col]
	const capTypes: Array<{
		type: CAPType;
		text: string;
		row: number;
		col: number;
	}> = [
		{ type: 'STRICT_ROTATED', text: "Rotated", row: 0, col: 0 },
		{ type: 'STRICT_MIRRORED', text: "Mirrored", row: 0, col: 1 },
		{ type: 'STRICT_SWAPPED', text: "Swapped", row: 0, col: 2 },
		{ type: 'STRICT_COMPLEMENTARY', text: "Complementary", row: 0, col: 3 },
		{ type: 'MIRRORED_SWAPPED', text: "Mirrored / Swapped", row: 1, col: 0 },
		{ type: 'SWAPPED_COMPLEMENTARY', text: "Swapped / Complementary", row: 1, col: 1 },
		{ type: 'ROTATED_COMPLEMENTARY', text: "Rotated / Complementary", row: 1, col: 2 },
		{ type: 'MIRRORED_COMPLEMENTARY', text: "Mirrored / Complementary", row: 1, col: 3 },
		{ type: 'ROTATED_SWAPPED', text: "Rotated / Swapped", row: 2, col: 0 },
		{ type: 'MIRRORED_ROTATED', text: "Mirrored / Rotated", row: 2, col: 1 },
		{ type: 'MIRRORED_COMPLEMENTARY_ROTATED', text: "Mir / Comp / Rot", row: 2, col: 2 }
	];

	// Handle button click
	function selectCapType(capType: CAPType) {
		if (capType !== currentValue) {
			currentValue = capType;
			
			// Dispatch value change
			const event = new CustomEvent('valueChanged', { 
				detail: { value: capType } 
			});
			document.dispatchEvent(event);
		}
	}

	// Public methods
	export function setValue(value: CAPType) {
		currentValue = value;
	}

	export function getValue(): CAPType {
		return currentValue;
	}

	// Group cap types by row for rendering
	type CAPTypeItem = typeof capTypes[0];
	const groupedTypes: CAPTypeItem[][] = (() => {
		const groups: CAPTypeItem[][] = [[], [], []];
		capTypes.forEach(capType => {
			groups[capType.row].push(capType);
		});
		return groups;
	})();
</script>

<div class="cap-type-selector">
	<div class="header-label">CAP Type:</div>
	
	<div class="grid-container">
		<div class="button-grid">
			{#each groupedTypes as row, rowIndex}
				<div class="grid-row">
					{#each row as { type, text }}
						<button 
							class="cap-button" 
							class:checked={currentValue === type}
							onclick={() => selectCapType(type)}
							type="button"
						>
							{text}
						</button>
					{/each}
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.cap-type-selector {
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

	.grid-container {
		display: flex;
		justify-content: center;
	}

	.button-grid {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.grid-row {
		display: flex;
		gap: 4px;
		justify-content: center;
	}

	.cap-button {
		width: 120px;
		height: 32px;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		color: rgba(255, 255, 255, 0.9);
		font-size: 10px;
		font-weight: 500;
		padding: 4px 8px;
		cursor: pointer;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
	}

	.cap-button:hover:not(.checked) {
		background: rgba(255, 255, 255, 0.15);
		border-color: rgba(255, 255, 255, 0.3);
	}

	.cap-button.checked {
		background: rgba(70, 130, 255, 0.8);
		border-color: rgba(70, 130, 255, 0.9);
		color: white;
		font-weight: 600;
	}
</style>
