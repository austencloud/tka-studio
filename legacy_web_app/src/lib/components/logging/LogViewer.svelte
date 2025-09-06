<!--
  Log Viewer Component

  Displays logs from the memory transport in a filterable, searchable interface.
-->
<script lang="ts">
  import { getContext, onMount, onDestroy } from 'svelte';
  import { writable, derived, type Writable } from 'svelte/store';
  import {
    LogLevel,
    LogDomain,
    CONSOLE_COLORS,
    DOMAIN_COLORS,
    type LogEntry
  } from '$lib/core/logging';

  // Props
  export let maxHeight: string = '400px';
  export let showToolbar: boolean = true;
  export let showTimestamps: boolean = true;
  export let showSource: boolean = true;
  export let showDomain: boolean = true;
  export let autoScroll: boolean = true;
  export let initialLevel: LogLevel = LogLevel.INFO;

  // Get the logs from context
  const { logs } = getContext<{
    logs: Writable<LogEntry[]>;
  }>(Symbol('logger'));

  // Filter state
  const levelFilter = writable<LogLevel>(initialLevel);
  const domainFilter = writable<LogDomain | null>(null);
  const sourceFilter = writable<string>('');
  const searchQuery = writable<string>('');

  // Filtered logs
  const filteredLogs = derived(
    [logs, levelFilter, domainFilter, sourceFilter, searchQuery],
    ([$logs, $levelFilter, $domainFilter, $sourceFilter, $searchQuery]) => {
      return $logs.filter(log => {
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

          return message.includes(query) ||
                 source.includes(query) ||
                 domain.includes(query) ||
                 JSON.stringify(log.data).toLowerCase().includes(query);
        }

        return true;
      });
    }
  );

  // Reference to the log container for auto-scrolling
  let logContainer: HTMLDivElement;
  let isScrolledToBottom = true;

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

  // Export logs as JSON
  function exportLogs() {
    const json = JSON.stringify($logs, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `logs-${new Date().toISOString()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // Copy logs to clipboard
  function copyLogs() {
    const text = $filteredLogs.map(log => {
      let line = '';
      if (showTimestamps) line += `[${formatTimestamp(log.timestamp)}] `;
      line += `[${log.levelName.toUpperCase()}]`;
      if (showSource) line += ` [${log.source}]`;
      if (showDomain && log.domain) line += ` [${log.domain}]`;
      line += `: ${log.message}`;
      if (log.data) line += ` ${JSON.stringify(log.data)}`;
      return line;
    }).join('\n');

    navigator.clipboard.writeText(text);
  }
</script>

<div class="log-viewer">
  {#if showToolbar}
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

        <input
          type="text"
          placeholder="Filter by source..."
          bind:value={$sourceFilter}
        />

        <input
          type="text"
          placeholder="Search logs..."
          bind:value={$searchQuery}
        />
      </div>

      <div class="actions">
        <button on:click={clearLogs}>Clear</button>
        <button on:click={exportLogs}>Export</button>
        <button on:click={copyLogs}>Copy</button>
        <label>
          <input type="checkbox" bind:checked={autoScroll} />
          Auto-scroll
        </label>
      </div>
    </div>
  {/if}

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
        <div class="log-entry" data-level={log.levelName}>
          {#if showTimestamps}
            <span class="timestamp">{formatTimestamp(log.timestamp)}</span>
          {/if}

          <span
            class="level"
            style="color: {CONSOLE_COLORS[log.level]};"
          >
            {log.levelName.toUpperCase()}
          </span>

          {#if showSource}
            <span class="source">{log.source}</span>
          {/if}

          {#if showDomain && log.domain}
            <span
              class="domain"
              style="color: {DOMAIN_COLORS[log.domain]};"
            >
              {log.domain}
            </span>
          {/if}

          <span class="message">{log.message}</span>

          {#if log.duration !== undefined}
            <span
              class="duration"
              class:slow={log.duration > 200}
              class:medium={log.duration > 50 && log.duration <= 200}
              class:fast={log.duration <= 50}
            >
              {log.duration.toFixed(2)}ms
            </span>
          {/if}

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
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #f8f9fa;
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .toolbar {
    display: flex;
    justify-content: space-between;
    padding: 8px;
    border-bottom: 1px solid #ccc;
    background-color: #f0f0f0;
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
  }

  .log-entry {
    padding: 4px 0;
    border-bottom: 1px solid #eee;
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 8px;
  }

  .log-entry[data-level="error"],
  .log-entry[data-level="fatal"] {
    background-color: rgba(220, 53, 69, 0.1);
  }

  .log-entry[data-level="warn"] {
    background-color: rgba(255, 193, 7, 0.1);
  }

  .timestamp {
    color: #888;
  }

  .level {
    font-weight: bold;
  }

  .source {
    color: #0066cc;
    font-weight: bold;
  }

  .domain {
    font-style: italic;
  }

  .message {
    flex: 1;
    word-break: break-word;
  }

  .duration {
    font-weight: bold;
  }

  .duration.fast {
    color: #28a745;
  }

  .duration.medium {
    color: #ffc107;
  }

  .duration.slow {
    color: #dc3545;
  }

  .details {
    width: 100%;
    margin-top: 4px;
    margin-left: 16px;
    padding: 4px;
    background-color: #f0f0f0;
    border-radius: 4px;
    max-height: 200px;
    overflow: auto;
  }

  .error {
    color: #dc3545;
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

  select, input, button {
    font-size: 12px;
    padding: 4px;
  }
</style>
