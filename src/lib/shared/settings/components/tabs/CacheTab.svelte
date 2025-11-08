<!--
  CacheTab.svelte - Cache Diagnostics for Settings Panel

  Simple, functional cache diagnostics that work WITHOUT authentication
-->
<script lang="ts">
  import {
    diagnoseCacheState,
    nuclearCacheClear,
    type CacheDiagnostics,
  } from "$shared/auth";
  import { auth } from "$shared/auth";
  import { onMount } from "svelte";

  let diagnostics = $state<CacheDiagnostics | null>(null);
  let loading = $state(false);
  let clearing = $state(false);

  async function runDiagnostics() {
    loading = true;
    try {
      diagnostics = await diagnoseCacheState();
    } catch (error) {
      console.error("Failed to run diagnostics:", error);
      alert("Failed to run diagnostics. Check console.");
    } finally {
      loading = false;
    }
  }

  async function clearCache() {
    if (
      !confirm(
        "⚠️ NUCLEAR CACHE CLEAR ⚠️\n\n" +
          "This will DELETE ALL cached data and reload the page.\n\n" +
          "Continue?"
      )
    ) {
      return;
    }

    clearing = true;
    try {
      await nuclearCacheClear();
      setTimeout(() => {
        window.location.reload();
      }, 1000);
    } catch (error) {
      console.error("Failed to clear cache:", error);
      alert("Failed to clear cache. Check console.");
      clearing = false;
    }
  }

  onMount(() => {
    runDiagnostics();
  });

  const hasOldProject = $derived(
    diagnostics?.indexedDBDatabases.some((db) =>
      db.includes("the-kinetic-constructor")
    ) || false
  );
</script>

<div class="cache-tab">
  <div class="section">
    <h3>🔍 Cache Diagnostics</h3>

    <div class="firebase-info">
      <p><strong>Current Project:</strong></p>
      <code>{auth.app.options.projectId}</code>
    </div>

    {#if diagnostics}
      <div class="stats">
        <div class="stat">
          <span>IndexedDB:</span>
          <strong>{diagnostics.indexedDBDatabases.length}</strong>
        </div>
        <div class="stat">
          <span>localStorage:</span>
          <strong>{diagnostics.localStorageKeys.length}</strong>
        </div>
        <div class="stat">
          <span>Cookies:</span>
          <strong>{diagnostics.cookies.length}</strong>
        </div>
      </div>

      {#if hasOldProject}
        <div class="alert error">
          <strong>🚨 OLD PROJECT DETECTED!</strong>
          <p>
            Found "the-kinetic-constructor" data. This WILL cause auth failures!
          </p>
          <p>Click "Clear Cache" below to fix.</p>
        </div>
      {:else}
        <div class="alert success">
          <strong>✅ Cache is clean</strong>
          <p>No old project data detected.</p>
        </div>
      {/if}

      <details>
        <summary>View Database List</summary>
        <ul class="db-list">
          {#each diagnostics.indexedDBDatabases as db}
            <li class:old={db.includes("the-kinetic-constructor")}>
              {db}
              {#if db.includes("the-kinetic-constructor")}
                <span class="badge">OLD</span>
              {/if}
            </li>
          {/each}
        </ul>
      </details>
    {/if}

    <div class="actions">
      <button class="btn secondary" onclick={runDiagnostics} disabled={loading}>
        {loading ? "Scanning..." : "🔍 Refresh"}
      </button>

      <button class="btn danger" onclick={clearCache} disabled={clearing}>
        {clearing ? "Clearing..." : "💣 Clear Cache"}
      </button>
    </div>

    <div class="help">
      <p><strong>When to clear cache:</strong></p>
      <ul>
        <li>Google/Facebook sign-in fails</li>
        <li>App stuck on "Setting up services..."</li>
        <li>Old project alert shown above</li>
      </ul>
    </div>
  </div>
</div>

<style>
  .cache-tab {
    padding: 20px;
    color: rgba(255, 255, 255, 0.9);
  }

  .section {
    max-width: 600px;
  }

  h3 {
    font-size: 20px;
    margin-bottom: 16px;
    color: white;
  }

  .firebase-info {
    background: rgba(255, 255, 255, 0.05);
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 16px;
  }

  .firebase-info p {
    margin: 0 0 4px 0;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
  }

  code {
    background: rgba(0, 0, 0, 0.3);
    padding: 4px 8px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.95);
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin-bottom: 16px;
  }

  .stat {
    background: rgba(255, 255, 255, 0.05);
    padding: 12px;
    border-radius: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .stat span {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
  }

  .stat strong {
    font-size: 18px;
    color: white;
  }

  .alert {
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 16px;
  }

  .alert.error {
    background: rgba(239, 68, 68, 0.1);
    border: 2px solid rgba(239, 68, 68, 0.5);
  }

  .alert.error strong {
    color: #ef4444;
  }

  .alert.success {
    background: rgba(34, 197, 94, 0.1);
    border: 2px solid rgba(34, 197, 94, 0.5);
  }

  .alert.success strong {
    color: #22c55e;
  }

  .alert p {
    margin: 4px 0 0 0;
    font-size: 14px;
  }

  details {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 16px;
  }

  summary {
    cursor: pointer;
    font-weight: 600;
    user-select: none;
  }

  .db-list {
    list-style: none;
    padding: 0;
    margin: 12px 0 0 0;
  }

  .db-list li {
    padding: 6px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 4px;
    margin-bottom: 4px;
    font-family: monospace;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .db-list li.old {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #ef4444;
  }

  .badge {
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 4px;
    background: #ef4444;
    color: white;
    font-weight: 600;
  }

  .actions {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
  }

  .btn {
    padding: 10px 16px;
    border-radius: 6px;
    border: none;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }

  .btn.secondary:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.15);
  }

  .btn.danger {
    background: #ef4444;
    color: white;
  }

  .btn.danger:hover:not(:disabled) {
    background: #dc2626;
  }

  .help {
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 8px;
    padding: 12px;
  }

  .help strong {
    color: #3b82f6;
  }

  .help ul {
    margin: 8px 0 0 0;
    padding-left: 20px;
  }

  .help li {
    font-size: 13px;
    margin-bottom: 4px;
  }

  @media (max-width: 600px) {
    .cache-tab {
      padding: 16px;
    }

    .actions {
      flex-direction: column;
    }

    .btn {
      width: 100%;
    }
  }
</style>
