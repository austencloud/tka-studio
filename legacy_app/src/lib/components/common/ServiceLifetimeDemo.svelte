<script lang="ts">
	import { onMount } from 'svelte';
	import { getService } from '$lib/core/di/serviceContext';
	import { SERVICE_TOKENS } from '$lib/core/di/ServiceTokens';
	import { IdGeneratorFormat } from '$lib/core/services/IdGenerator';
	import type { IdGenerator } from '$lib/core/services/IdGenerator';
	import { ErrorSeverity, type ErrorHandler } from '$lib/core/services/ErrorHandling';

	// A component that demonstrates the service lifetimes

	let errorHandler: ErrorHandler;
	let idGen1: IdGenerator;
	let idGen2: IdGenerator;

	// Generated IDs to show whether services are the same instance or different
	let ids1: string[] = [];
	let ids2: string[] = [];

	onMount(() => {
		// Get our services from DI
		errorHandler = getService<ErrorHandler>(SERVICE_TOKENS.ERROR_HANDLER); // singleton
		idGen1 = getService<IdGenerator>(SERVICE_TOKENS.ID_GENERATOR); // transient
		idGen2 = getService<IdGenerator>(SERVICE_TOKENS.ID_GENERATOR); // transient - should be different instance

		// Log that we've set up the component
		errorHandler.log({
			source: 'ServiceLifetimeDemo',
			message: 'Component initialized with services',
			severity: ErrorSeverity.INFO,
			context: {
				idGen1: idGen1 === idGen2 ? 'Same instance as idGen2' : 'Different instance from idGen2'
			}
		});

		// Generate some IDs to show
		for (let i = 0; i < 3; i++) {
			ids1.push(idGen1.next());
			ids2.push(idGen2.next());
		}
	});

	function generateMoreIds() {
		if (idGen1 && idGen2) {
			ids1 = [...ids1, idGen1.next()];
			ids2 = [...ids2, idGen2.next()];
		}
	}
</script>

<div class="service-lifetime-demo">
	<h3>Service Lifetime Demonstration</h3>

	<div class="lifetime-info">
		<div class="service-info">
			<h4>Transient Service #1</h4>
			<p>Each request for this service creates a new instance</p>
			<ul>
				{#each ids1 as id}
					<li>{id}</li>
				{/each}
			</ul>
		</div>

		<div class="service-info">
			<h4>Transient Service #2</h4>
			<p>This is a separate instance of the same service</p>
			<ul>
				{#each ids2 as id}
					<li>{id}</li>
				{/each}
			</ul>
		</div>
	</div>

	<button on:click={generateMoreIds}>Generate More IDs</button>
</div>

<style>
	.service-lifetime-demo {
		padding: 1rem;
		background-color: #f0f4f8;
		border-radius: 0.5rem;
		margin-bottom: 1rem;
	}

	.lifetime-info {
		display: flex;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.service-info {
		flex: 1;
		background-color: white;
		padding: 0.5rem 1rem;
		border-radius: 0.25rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	h4 {
		margin: 0 0 0.5rem 0;
		color: #2a4365;
	}

	button {
		background-color: #4299e1;
		color: white;
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 0.25rem;
		cursor: pointer;
		font-weight: 500;
	}

	button:hover {
		background-color: #3182ce;
	}

	ul {
		list-style-type: none;
		padding-left: 0;
		margin: 0.5rem 0;
	}

	li {
		font-family: monospace;
		padding: 0.25rem 0;
		border-bottom: 1px solid #edf2f7;
	}
</style>
