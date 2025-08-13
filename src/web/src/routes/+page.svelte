
<script lang="ts">
	import { onMount } from 'svelte';
	import { switchTab } from '$lib/state/appState.svelte';
	import MainApplication from '$components/MainApplication.svelte';

	onMount(async () => {
		// Go to constructor tab on startup
		switchTab('construct');
	});
</script>

<MainApplication />
