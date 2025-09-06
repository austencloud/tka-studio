<!--
  Simple Log Viewer Component

  A simplified log viewer that doesn't rely on context.
-->
<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { writable, derived } from 'svelte/store';
	import {
		LogLevel,
		LogDomain,
		CONSOLE_COLORS,
		DOMAIN_COLORS,
		logger,
		type LogEntry
	} from '$lib/core/logging';

	// Props
	export let maxHeight: string = '400px';

	// State
	const logs = writable<LogEntry[]>([]);
	const levelFilter = writable<LogLevel>(LogLevel.INFO);
	const domainFilter = writable<LogDomain | null>(null);
	const sourceFilter = writable<string>('');
	const searchQuery = writable<string>('');

	// Filtered logs
	const filteredLogs = derived(
		[logs, levelFilter, domainFilter, sourceFilter, searchQuery],
		([$logs, $levelFilter, $domainFilter, $sourceFilter, $searchQuery]) => {
			return $logs.filter((log) => {
				// Filter by level
				if (log.level < $levelFilter) return false;

				// Filter by domain
				if ($domainFilter && log.domain !== $domainFilter) return false;

				// Filter by source
				if ($sourceFilter && !log.source.includes($sourceFilter)) return false;

				// Filter by search query
				if ($searchQuery) {
					const query = $searchQuery.toLowerCase();
					const message = log.message.toLowerCase();
					const source = log.source.toLowerCase();
					const domain = log.domain?.toLowerCase() || '';

					return (
						message.includes(query) ||
						source.includes(query) ||
						domain.includes(query) ||
						JSON.stringify(log.data).toLowerCase().includes(query)
					);
				}

				return true;
			});
		}
	);

	// Reference to the log container for auto-scrolling
	let logContainer: HTMLDivElement;
	let isScrolledToBottom = true;
	let autoScroll = true;

	// Auto-scroll when new logs are added
	$: if (autoScroll && isScrolledToBottom && logContainer && $filteredLogs.length > 0) {
		setTimeout(() => {
			logContainer.scrollTop = logContainer.scrollHeight;
		}, 0);
	}

	// Handle scroll events to determine if we're at the bottom
	function handleScroll() {
		if (logContainer) {
			const { scrollTop, scrollHeight, clientHeight } = logContainer;
			isScrolledToBottom = Math.abs(scrollHeight - clientHeight - scrollTop) < 10;
		}
	}

	// Format timestamp
	function formatTimestamp(timestamp: number): string {
		const date = new Date(timestamp);
		return date.toISOString().split('T')[1].split('.')[0];
	}

	// Clear logs
	function clearLogs() {
		logs.set([]);
	}

	// Memory transport callback
	function handleNewLog(entry: LogEntry) {
		logs.update((currentLogs) => {
			// Keep only the last 1000 logs to prevent memory issues
			const newLogs = [...currentLogs, entry];
			if (newLogs.length > 1000) {
				return newLogs.slice(newLogs.length - 1000);
			}
			return newLogs;
		});
	}

	// Set up logging
	onMount(() => {
		// Add a memory transport to the logger
		const memoryTransport = {
			name: 'memory',
			log: handleNewLog
		};

		// Configure logger with our transport
		logger.setConfig({
			transports: [memoryTransport],
			minLevel: LogLevel.DEBUG
		});

		// Log that we've initialized
		logger.info('Log viewer initialized', {
			domain: LogDomain.SYSTEM
		});

		// Generate some test logs
		logger.debug('This is a debug message', { domain: LogDomain.SYSTEM });
		logger.info('This is an info message', { domain: LogDomain.SYSTEM });
		logger.warn('This is a warning message', { domain: LogDomain.SYSTEM });
		logger.error('This is an error message', { domain: LogDomain.SYSTEM });
	});
</script>

<div class="log-viewer">
	<div class="toolbar">
		<div class="filters">
			<select bind:value={$levelFilter}>
				<option value={LogLevel.TRACE}>TRACE</option>
				<option value={LogLevel.DEBUG}>DEBUG</option>
				<option value={LogLevel.INFO}>INFO</option>
				<option value={LogLevel.WARN}>WARN</option>
				<option value={LogLevel.ERROR}>ERROR</option>
				<option value={LogLevel.FATAL}>FATAL</option>
			</select>

			<select bind:value={$domainFilter}>
				<option value={null}>All Domains</option>
				{#each Object.values(LogDomain) as domain}
					<option value={domain}>{domain}</option>
				{/each}
			</select>

			<input type="text" placeholder="Filter by source..." bind:value={$sourceFilter} />

			<input type="text" placeholder="Search logs..." bind:value={$searchQuery} />
		</div>

		<div class="actions">
			<button on:click={clearLogs}>Clear</button>
			<label>
				<input type="checkbox" bind:checked={autoScroll} />
				Auto-scroll
			</label>
		</div>
	</div>

	<div
		class="log-container"
		bind:this={logContainer}
		on:scroll={handleScroll}
		style="max-height: {maxHeight};"
	>
		{#if $filteredLogs.length === 0}
			<div class="empty-state">No logs to display</div>
		{:else}
			{#each $filteredLogs as log (log.id)}
				<div
					class="log-entry"
					data-level={log.level === LogLevel.ERROR
						? 'error'
						: log.level === LogLevel.WARN
							? 'warn'
							: 'info'}
				>
					<span class="timestamp">{formatTimestamp(log.timestamp)}</span>

					<span class="level" style="color: {CONSOLE_COLORS[log.level]};">
						{LogLevel[log.level].toUpperCase()}
					</span>

					<span class="source">{log.source}</span>

					{#if log.domain}
						<span class="domain" style="color: {DOMAIN_COLORS[log.domain]};">
							{log.domain}
						</span>
					{/if}

					<span class="message">{log.message}</span>

					{#if log.data || log.error}
						<div class="details">
							{#if log.data}
								<pre>{JSON.stringify(log.data, null, 2)}</pre>
							{/if}

							{#if log.error}
								<div class="error">
									<div class="error-message">{log.error.message}</div>
									{#if log.error.stack}
										<pre class="error-stack">{log.error.stack}</pre>
									{/if}
								</div>
							{/if}
						</div>
					{/if}
				</div>
			{/each}
		{/if}
	</div>
</div>

<style>
	.log-viewer {
		font-family: monospace;
		font-size: 12px;
		border: 1px solid #444;
		border-radius: 4px;
		background-color: #1e1e1e;
		color: #e0e0e0;
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		overflow: hidden;
		box-sizing: border-box;
	}

	.toolbar {
		display: flex;
		justify-content: space-between;
		padding: 8px;
		border-bottom: 1px solid #444;
		background-color: #2a2a2a;
	}

	.filters {
		display: flex;
		gap: 8px;
	}

	.actions {
		display: flex;
		gap: 8px;
		align-items: center;
	}

	.log-container {
		overflow-y: auto;
		padding: 8px;
		flex: 1;
		height: calc(100% - 40px);
		box-sizing: border-box;
	}

	.log-entry {
		padding: 4px 0;
		border-bottom: 1px solid #333;
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 8px;
	}

	.log-entry[data-level='error'] {
		background-color: rgba(220, 53, 69, 0.2);
	}

	.log-entry[data-level='warn'] {
		background-color: rgba(255, 193, 7, 0.2);
	}

	.timestamp {
		color: #888;
	}

	.level {
		font-weight: bold;
	}

	.source {
		color: #4da6ff;
		font-weight: bold;
	}

	.domain {
		font-style: italic;
	}

	.message {
		flex: 1;
		word-break: break-word;
	}

	.details {
		width: 100%;
		margin-top: 4px;
		margin-left: 16px;
		padding: 4px;
		background-color: #2a2a2a;
		border-radius: 4px;
		max-height: 200px;
		overflow: auto;
	}

	.error {
		color: #ff6b6b;
	}

	.error-message {
		font-weight: bold;
	}

	.error-stack {
		font-size: 11px;
		margin-top: 4px;
		white-space: pre-wrap;
	}

	.empty-state {
		padding: 16px;
		text-align: center;
		color: #888;
	}

	pre {
		margin: 0;
		white-space: pre-wrap;
	}

	select,
	input,
	button {
		font-size: 12px;
		padding: 4px;
		background-color: #333;
		color: #e0e0e0;
		border: 1px solid #555;
		border-radius: 3px;
	}

	select:focus,
	input:focus,
	button:focus {
		outline: none;
		border-color: #4da6ff;
	}

	button {
		cursor: pointer;
	}

	button:hover {
		background-color: #444;
	}

	label {
		display: flex;
		align-items: center;
		gap: 4px;
	}
</style>
