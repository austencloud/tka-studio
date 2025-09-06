<script lang="ts">
	import { useService } from '$lib/core/di/useService';
	import { SERVICE_TOKENS } from '$lib/core/di/ServiceTokens';
	import type { BackgroundService } from '$lib/core/services/BackgroundService';
	import type { ErrorHandler } from '$lib/core/services/ErrorHandling';
	import { ErrorSeverity } from '$lib/core/services/ErrorHandling';

	// Use our services via the hook
	const { service: backgroundService, isReady: backgroundReady } = useService<BackgroundService>(
		SERVICE_TOKENS.BACKGROUND_SERVICE
	);
	const { service: errorHandler, isReady: errorReady } = useService<ErrorHandler>(
		SERVICE_TOKENS.ERROR_HANDLER
	);

	// Component props
	export let onBackgroundChange: (type: string) => void = () => {};

	// Component state
	let availableBackgrounds: string[] = [];
	let currentBackground = '';

	// Load available backgrounds when services are ready
	$: if ($backgroundReady) {
		availableBackgrounds = $backgroundService!.getAvailableBackgrounds();
		currentBackground = $backgroundService!.getCurrentBackground();
	}

	function handleBackgroundChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		const type = target.value;
		currentBackground = type;

		// Log change with DI error handler
		if ($errorReady) {
			$errorHandler!.log({
				source: 'BackgroundSettings',
				message: `Background changed to: ${type}`,
				severity: ErrorSeverity.INFO
			});
		}

		// Notify parent component
		onBackgroundChange(type);
	}

	// Function to get a user-friendly display name for each background
	function getDisplayName(type: string): string {
		switch (type) {
			case 'snowfall':
				return 'Snowfall';
			case 'nightSky':
				return 'Night Sky';

			default:
				return type;
		}
	}
</script>

<div class="background-settings">
	<h3>Background Settings</h3>

	{#if $backgroundReady}
		<div class="setting-group">
			<label for="background-type">Background Type:</label>
			<select id="background-type" value={currentBackground} on:change={handleBackgroundChange}>
				{#each availableBackgrounds as type}
					<option value={type}>{getDisplayName(type)}</option>
				{/each}
			</select>
		</div>
	{:else}
		<p>Loading background options...</p>
	{/if}
</div>

<style>
	.background-settings {
		padding: 1rem;
		background-color: #f5f5f5;
		border-radius: 0.5rem;
	}

	.setting-group {
		margin-bottom: 0.5rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	select {
		padding: 0.25rem 0.5rem;
		border-radius: 0.25rem;
	}
</style>
