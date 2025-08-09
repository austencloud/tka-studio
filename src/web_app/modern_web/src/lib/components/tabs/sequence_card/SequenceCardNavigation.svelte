<!-- SequenceCardNavigation.svelte - Navigation sidebar matching desktop modern styling -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher<{
		lengthSelected: number;
		columnCountChanged: number;
	}>();

	interface Props {
		selectedLength?: number;
		columnCount?: number;
	}

	let { selectedLength = 16, columnCount = 2 }: Props = $props();

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
		dispatch('lengthSelected', length);
	}

	function handleColumnChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		const newCount = parseInt(target.value);
		columnCount = newCount;
		dispatch('columnCountChanged', newCount);
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
		background: linear-gradient(to bottom, rgba(71, 85, 105, 0.4), rgba(51, 65, 85, 0.6));
		border-radius: 12px;
		border: 1px solid rgba(100, 116, 139, 0.3);
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 16px;
		height: 100%;
	}

	/* Sidebar Header */
	.sidebar-header {
		background: linear-gradient(to bottom, rgba(71, 85, 105, 0.5), rgba(51, 65, 85, 0.7));
		border-radius: 10px;
		border: 1px solid rgba(100, 116, 139, 0.4);
		padding: 16px;
		text-align: center;
	}

	.header-title {
		margin: 0 0 4px 0;
		color: #f8fafc;
		font-size: 18px;
		font-weight: bold;
		letter-spacing: 0.5px;
	}

	.header-subtitle {
		margin: 0;
		color: #f8fafc;
		font-size: 14px;
		font-style: italic;
		opacity: 0.9;
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
		background: linear-gradient(to bottom, rgba(71, 85, 105, 0.3), rgba(51, 65, 85, 0.5));
		border: 1px solid rgba(100, 116, 139, 0.4);
		border-radius: 10px;
		padding: 10px 14px;
		color: #f8fafc;
		font-weight: 500;
		font-size: 14px;
		text-align: center;
		cursor: pointer;
		transition: all 0.2s ease;
		margin: 2px;
	}

	.length-button:hover {
		background: linear-gradient(to bottom, rgba(100, 116, 139, 0.4), rgba(71, 85, 105, 0.6));
		border: 1px solid rgba(148, 163, 184, 0.5);
		transform: translateY(-1px);
	}

	.length-button.selected {
		background: linear-gradient(to bottom, #3b82f6, #2563eb);
		border: 1px solid #60a5fa;
		color: white;
		font-weight: 600;
		box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
	}

	.length-button:active {
		transform: translateY(0);
	}

	/* Column Selector */
	.column-selector {
		background: rgba(71, 85, 105, 0.3);
		border-radius: 8px;
		border: 1px solid rgba(100, 116, 139, 0.4);
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 8px;
		flex-shrink: 0;
	}

	.column-label {
		color: #f8fafc;
		font-weight: 500;
		font-size: 14px;
		margin: 0;
	}

	.column-select {
		background: rgba(71, 85, 105, 0.6);
		border: 1px solid rgba(100, 116, 139, 0.5);
		border-radius: 8px;
		padding: 8px 12px;
		color: #f8fafc;
		font-size: 14px;
		min-height: 36px;
		cursor: pointer;
		appearance: none;
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23f8fafc' viewBox='0 0 16 16'%3E%3Cpath d='M4 6l4 4 4-4'/%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 8px center;
		background-size: 16px;
		padding-right: 32px;
	}

	.column-select:hover {
		background-color: rgba(100, 116, 139, 0.7);
		border-color: rgba(148, 163, 184, 0.6);
	}

	.column-select:focus {
		outline: none;
		border-color: #60a5fa;
		box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.3);
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
