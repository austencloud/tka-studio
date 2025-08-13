<!-- Constructor Route -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { switchTab } from '$lib/state/appState.svelte';
	import MainApplication from '$components/MainApplication.svelte';

	onMount(async () => {
		// Navigate to construct tab
		switchTab('construct');
	});
</script>

<MainApplication />
