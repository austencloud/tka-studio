<!-- SequenceCardNavigation.svelte - Navigation sidebar matching desktop modern styling -->
<script lang="ts">
	interface Props {
		selectedLength?: number;
		columnCount?: number;
		onlengthselected?: (length: number) => void;
		oncolumncountchanged?: (count: number) => void;
	}

	let { selectedLength = 16, columnCount = 2, onlengthselected, oncolumncountchanged }: Props = $props();

	// Length options matching desktop app exactly
	const lengthOptions = [
		{ value: 0, label: 'All' },
		{ value: 2, label: '2' },
		{ value: 3, label: '3' },
		{ value: 4, label: '4' },
		{ value: 5, label: '5' },
		{ value: 6, label: '6' },
		{ value: 8, label: '8' },
		{ value: 10, label: '10' },
		{ value: 12, label: '12' },
		{ value: 16, label: '16' },
	];

	// Column count options
	const columnOptions = [2, 3, 4, 5, 6];

	function handleLengthClick(length: number) {
		selectedLength = length;
		onlengthselected?.(length);
	}

	function handleColumnChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		const newCount = parseInt(target.value);
		columnCount = newCount;
		oncolumncountchanged?.(newCount);
	}
</script>

<div class="sequence-card-navigation">
	<!-- Sidebar Header -->
	<div class="sidebar-header">
		<h2 class="header-title">Sequence Length</h2>
		<p class="header-subtitle">Select a length to display</p>
	</div>

	<!-- Length Selection Scroll Area -->
	<div class="length-scroll-area">
		<div class="length-options">
			{#each lengthOptions as option (option.value)}
				<button
					class="length-button"
					class:selected={selectedLength === option.value}
					onclick={() => handleLengthClick(option.value)}
					title="Show sequences with {option.value === 0
						? 'any length'
						: `${option.value} beats`}"
				>
					{option.label}
				</button>
			{/each}
		</div>
	</div>

	<!-- Column Selector -->
	<div class="column-selector">
		<label class="column-label" for="column-select"> Preview Columns: </label>
		<select
			id="column-select"
			class="column-select"
			bind:value={columnCount}
			onchange={handleColumnChange}
		>
			{#each columnOptions as count}
				<option value={count}>{count}</option>
			{/each}
		</select>
	</div>
</div>

<style>
	.sequence-card-navigation {
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	border-radius: 16px;
	border: var(--glass-border);
	box-shadow: var(--shadow-glass);
	padding: 12px;
	display: flex;
	flex-direction: column;
	gap: 16px;
	height: 100%;
}

	/* Sidebar Header */
	.sidebar-header {
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	border-radius: 12px;
	border: var(--glass-border);
	box-shadow: var(--shadow-glass);
	padding: 16px;
	text-align: center;
}

	.header-title {
	margin: 0 0 4px 0;
	color: rgba(255, 255, 255, 0.95);
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
	font-size: 18px;
	font-weight: bold;
	letter-spacing: 0.5px;
}

	.header-subtitle {
	margin: 0;
	color: rgba(255, 255, 255, 0.8);
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
	font-size: 14px;
	font-style: italic;
}

	/* Length Selection Area */
	.length-scroll-area {
		flex: 1;
		overflow-y: auto;
		min-height: 0;
	}

	.length-options {
		display: flex;
		flex-direction: column;
		gap: 6px;
		padding: 6px;
	}

	.length-button {
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	border: var(--glass-border);
	border-radius: 12px;
	padding: 10px 14px;
	color: rgba(255, 255, 255, 0.9);
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
	font-weight: 500;
	font-size: 14px;
	text-align: center;
	cursor: pointer;
	transition: all var(--transition-normal);
	margin: 2px;
	box-shadow: var(--shadow-glass);
}

	.length-button:hover {
	background: var(--surface-hover);
	border: var(--glass-border-hover);
	transform: translateY(-2px);
	box-shadow: var(--shadow-glass-hover);
}

	.length-button.selected {
	background: var(--gradient-primary);
	border: 1px solid rgba(99, 102, 241, 0.6);
	color: white;
	font-weight: 600;
	box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
}

	.length-button:active {
		transform: translateY(0);
	}

	/* Column Selector */
	.column-selector {
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	border-radius: 12px;
	border: var(--glass-border);
	box-shadow: var(--shadow-glass);
	padding: 12px;
	display: flex;
	flex-direction: column;
	gap: 8px;
	flex-shrink: 0;
}

	.column-label {
	color: rgba(255, 255, 255, 0.9);
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
	font-weight: 500;
	font-size: 14px;
	margin: 0;
}

	.column-select {
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	border: var(--glass-border);
	border-radius: 10px;
	padding: 8px 12px;
	color: rgba(255, 255, 255, 0.9);
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
	font-size: 14px;
	min-height: 36px;
	cursor: pointer;
	appearance: none;
	background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23ffffff' viewBox='0 0 16 16'%3E%3Cpath d='M4 6l4 4 4-4'/%3E%3C/svg%3E");
	background-repeat: no-repeat;
	background-position: right 8px center;
	background-size: 16px;
	padding-right: 32px;
	box-shadow: var(--shadow-glass);
}

	.column-select:hover {
	background: var(--surface-hover);
	border: var(--glass-border-hover);
	box-shadow: var(--shadow-glass-hover);
}

	.column-select:focus {
	outline: none;
	border-color: rgba(99, 102, 241, 0.6);
	box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
}

	/* Custom scrollbar for length area */
	.length-scroll-area::-webkit-scrollbar {
		width: 8px;
	}

	.length-scroll-area::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.1);
		border-radius: 4px;
	}

	.length-scroll-area::-webkit-scrollbar-thumb {
		background: rgba(0, 0, 0, 0.3);
		border-radius: 4px;
	}

	.length-scroll-area::-webkit-scrollbar-thumb:hover {
		background: rgba(0, 0, 0, 0.5);
	}

	/* Responsive Design */
	@media (max-width: 1024px) {
		.sequence-card-navigation {
			flex-direction: row;
			height: auto;
		}

		.sidebar-header {
			flex-shrink: 0;
		}

		.length-scroll-area {
			flex: 1;
		}

		.length-options {
			flex-direction: row;
			flex-wrap: wrap;
			gap: 4px;
		}

		.length-button {
			flex: 1;
			min-width: 60px;
		}

		.column-selector {
			flex-shrink: 0;
			width: 160px;
		}
	}

	@media (max-width: 768px) {
		.sequence-card-navigation {
			flex-direction: column;
			gap: 12px;
		}

		.length-scroll-area {
			max-height: 120px;
		}

		.column-selector {
			width: auto;
		}

		.header-title {
			font-size: 16px;
		}

		.header-subtitle {
			font-size: 12px;
		}

		.length-button {
			padding: 8px 12px;
			font-size: 13px;
		}
	}
</style>
