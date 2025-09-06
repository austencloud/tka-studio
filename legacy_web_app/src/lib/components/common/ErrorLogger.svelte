<script lang="ts">
	import { onMount } from 'svelte';
	import { getService } from '$lib/core/di/serviceContext';
	import { SERVICE_TOKENS } from '$lib/core/di/ServiceTokens';
	import { ErrorSeverity, type ErrorHandler } from '$lib/core/services/ErrorHandling';

	export let componentName = 'ErrorLogger';

	let errorHandler: ErrorHandler;

	onMount(() => {
		errorHandler = getService<ErrorHandler>(SERVICE_TOKENS.ERROR_HANDLER);

		// Log that component mounted successfully
		errorHandler.log({
			source: componentName,
			message: 'Component initialized successfully',
			severity: ErrorSeverity.INFO
		});
	});

	function logError(message: string) {
		if (errorHandler) {
			errorHandler.log({
				source: componentName,
				message,
				severity: ErrorSeverity.ERROR
			});
		}
	}
</script>

<div class="error-logger">
	<slot {logError}></slot>
</div>
