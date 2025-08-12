
<script lang="ts">
	import { onMount } from 'svelte';
	import { enterAppMode } from '$lib/state/appModeState.svelte';
	import { switchTab } from '$lib/state/appState.svelte';
	import MainApplication from '$components/MainApplication.svelte';

	onMount(async () => {
		// Enter app mode and go to constructor
		console.log('🔧 Root route accessed - entering app mode...');
		await enterAppMode();
		switchTab('construct');
	});
</script>

<MainApplication />
