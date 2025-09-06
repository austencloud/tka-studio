<!-- src/lib/components/MainWidget/MainWidget.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import ConstructTab from '$lib/components/ConstructTab/ConstructTab.svelte';
	import GenerateTabContent from '$lib/components/GenerateTab/components/GenerateTabContent.svelte';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';

	// State using Svelte 5 runes
	let activeMode = $state<'construct' | 'generate'>('construct');

	// Debug the current mode
	$effect(() => {
		console.log('MainWidget active mode:', activeMode);
	});

	// Listen for mode switch events
	onMount(() => {
		const handleModeSwitch = (event: CustomEvent) => {
			if (event.detail?.mode) {
				console.log('Mode switch event received:', event.detail.mode);
				activeMode = event.detail.mode;
				hapticFeedbackService.trigger('navigation');

			}
		};

		// Listen for the switch-mode event
		document.addEventListener('switch-mode', handleModeSwitch as EventListener);

		// Also listen for the action event with constructMode or generateMode
		const handleAction = (event: CustomEvent) => {
			if (event.detail?.id === 'constructMode') {
				console.log('Construct mode action received');
				activeMode = 'construct';
			} else if (event.detail?.id === 'generateMode') {
				console.log('Generate mode action received');
				activeMode = 'generate';
			}
		};

		document.addEventListener('action', handleAction as EventListener);

		return () => {
			document.removeEventListener('switch-mode', handleModeSwitch as EventListener);
			document.removeEventListener('action', handleAction as EventListener);
		};
	});
</script>

<div class="main-widget">
	{#if activeMode === 'construct'}
		<ConstructTab />
	{:else if activeMode === 'generate'}
		<div class="generate-container">
			<GenerateTabContent />
		</div>
	{/if}
</div>

<style>
	.main-widget {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}

	.generate-container {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}
</style>
