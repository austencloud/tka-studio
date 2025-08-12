<!-- Constructor Route - Auto-enters App Mode -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { enterAppMode } from '$lib/state/appModeState.svelte';
	import { switchTab } from '$lib/state/appState.svelte';
	import MainApplication from '$components/MainApplication.svelte';

	onMount(async () => {
		// Automatically enter app mode and switch to construct tab
		console.log('🔧 Constructor route accessed - entering app mode...');
		await enterAppMode();
		switchTab('construct');
	});
</script>

<MainApplication />
