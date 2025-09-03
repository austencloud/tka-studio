<!--
  Export Test Page

  This page provides a UI for testing the pictograph export functionality.
-->
<script lang="ts">
	import EnhancedExportTester from '$lib/components/Pictograph/export/SequenceImageExportTester.svelte';

	let activeTab: 'single-beat' | 'sequence' | 'enhanced' = 'single-beat';

	function showTab(tab: 'single-beat' | 'sequence' | 'enhanced') {
		activeTab = tab;
	}
</script>

<div class="export-test-page">
	<h1>Pictograph Export Testing</h1>
	<div class="tabs">

		<button
			class="tab-button"
			class:active={activeTab === 'enhanced'}
			on:click={() => showTab('enhanced')}
		>
			Enhanced Export
		</button>
	</div>

	{#if activeTab === 'enhanced'}
		<div id="enhanced" class="tab-content">
			<EnhancedExportTester />
		</div>
	{/if}
</div>

<style>
	.export-test-page {
		padding: 1rem;
		max-width: 1200px;
		margin: 0 auto;
	}

	h1 {
		margin-bottom: 1rem;
		text-align: center;
	}

	.tabs {
		display: flex;
		gap: 1rem;
		margin-bottom: 1rem;
		justify-content: center;
	}

	.tab-button {
		padding: 0.5rem 1rem;
		background-color: #f0f0f0;
		border: 1px solid #ccc;
		border-radius: 4px;
		cursor: pointer;
		font-weight: bold;
	}

	.tab-button:hover {
		background-color: #e0e0e0;
	}

	.tab-button.active {
		background-color: #4caf50;
		color: white;
		border-color: #388e3c;
	}

	.tab-content {
		border: 1px solid #ccc;
		border-radius: 4px;
		padding: 1rem;
	}
</style>
