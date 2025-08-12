<script lang="ts">
  import { onMount } from 'svelte'
  import { launcherState } from '../lib/stores/launcher.svelte.js'
  import VersionCard from '../lib/components/VersionCard.svelte'
  import {
    RefreshCw,
    Settings,
    GitCompare,
    Terminal,
    Monitor,
    Zap,
    AlertCircle,
    CheckCircle2
  } from 'lucide-svelte'

  let showSettings = $state(false)

  onMount(() => {
    // Set up effects and initialize launcher state
    launcherState.setupEffects()
    launcherState.initialize()
  })

  async function handleRefresh() {
    await launcherState.refreshVersions()
  }

  function handleCompareSelected() {
    if (launcherState.selectedVersions.length === 2) {
      const [v1, v2] = launcherState.selectedVersions
      launcherState.compareVersions(v1, v2)
    }
  }

  function handleStartAll() {
    launcherState.availableVersions.forEach(version => {
      if (version.status === 'available') {
        launcherState.startVersion(version.id)
      }
    })
  }

  function handleStopAll() {
    launcherState.runningVersions.forEach(version => {
      launcherState.stopVersion(version.id)
    })
  }
</script>

<svelte:head>
  <title>Kinetic Constructor Launcher</title>
  <meta name="description" content="Version management dashboard for Kinetic Constructor" />
</svelte:head>

<div class="min-h-screen bg-gray-50">
  <!-- Header -->
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="logo">
          <Zap class="logo-icon" />
          <div>
            <h1 class="text-2xl font-bold">Kinetic Constructor</h1>
            <p class="text-sm text-gray-500">Version Launcher</p>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <!-- Status indicators -->
          <div class="flex items-center gap-6 text-sm">
            <div class="flex items-center gap-2">
              <CheckCircle2 size={16} class="text-green-500" />
              <span class="text-gray-600 font-medium">
                {launcherState.availableVersions.length} Available
              </span>
            </div>
            <div class="flex items-center gap-2">
              <Zap size={16} class="text-blue-500" />
              <span class="text-gray-600 font-medium">
                {launcherState.runningVersions.length} Running
              </span>
            </div>
          </div>

          <!-- Actions -->
          <button
            onclick={handleRefresh}
            class="btn btn-secondary"
            disabled={launcherState.isLoading}
            title="Refresh versions"
          >
            <RefreshCw size={16} class={launcherState.isLoading ? 'animate-spin' : ''} />
          </button>

          <button
            onclick={() => showSettings = true}
            class="btn btn-secondary"
            title="Settings"
          >
            <Settings size={16} />
          </button>
        </div>
      </div>
    </div>
  </header>

  <!-- Main content -->
  <main class="container p-8">
    <!-- Error display -->
    {#if launcherState.error}
      <div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <div class="flex items-center gap-3">
          <AlertCircle class="text-red-500" size={20} />
          <div>
            <h3 class="text-sm font-medium text-red-800">Error</h3>
            <p class="text-sm text-red-700">{launcherState.error}</p>
          </div>
          <button
            onclick={() => launcherState.clearError()}
            class="ml-auto text-red-500 hover:text-red-700"
          >
            ×
          </button>
        </div>
      </div>
    {/if}

    <!-- Quick actions -->
    <div class="mb-8 animate-slide-in">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-gray-900">Quick Actions</h2>
        <div class="flex items-center gap-3">
          {#if launcherState.selectedVersions.length === 2}
            <button
              onclick={handleCompareSelected}
              class="btn btn-primary"
              disabled={!launcherState.canCompare}
            >
              <GitCompare size={16} />
              Compare Selected
            </button>
          {/if}
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <button
          onclick={handleStartAll}
          class="btn btn-success"
          disabled={launcherState.availableVersions.filter(v => v.status === 'available').length === 0}
        >
          <Zap size={16} />
          Start All Available
        </button>

        <button
          onclick={handleStopAll}
          class="btn btn-error"
          disabled={launcherState.runningVersions.length === 0}
        >
          <Monitor size={16} />
          Stop All Running
        </button>

        <button
          onclick={() => launcherState.toggleLogs()}
          class="btn btn-secondary"
          disabled={launcherState.runningVersions.length === 0}
        >
          <Terminal size={16} />
          {launcherState.showLogs ? 'Hide' : 'Show'} Logs
        </button>

        <button
          onclick={() => launcherState.togglePerformanceMetrics()}
          class="btn btn-secondary"
        >
          <Monitor size={16} />
          {launcherState.settings.showPerformanceMetrics ? 'Hide' : 'Show'} Metrics
        </button>
      </div>
    </div>

    <!-- Loading state -->
    {#if launcherState.isLoading && launcherState.versions.length === 0}
      <div class="text-center py-16 animate-fade-in">
        <RefreshCw class="animate-spin mx-auto mb-6 text-primary" size={64} />
        <h3 class="text-xl font-semibold text-gray-700 mb-2">Detecting versions...</h3>
        <p class="text-gray-500">Scanning workspace for available applications</p>
      </div>
    {:else}
      <!-- Versions grid -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900">
            Available Versions
            <span class="text-lg font-normal text-gray-500">({launcherState.versions.length})</span>
          </h2>
        </div>

        {#if launcherState.versions.length === 0}
          <div class="text-center py-16 bg-white rounded-xl border border-gray-200 shadow-sm animate-fade-in">
            <AlertCircle class="mx-auto mb-6 text-gray-400" size={64} />
            <h3 class="text-xl font-semibold text-gray-900 mb-3">No versions found</h3>
            <p class="text-gray-500 mb-6 max-w-md mx-auto">
              Make sure your project structure follows the expected layout with apps in the correct directories.
            </p>
            <button onclick={handleRefresh} class="btn btn-primary btn-lg">
              <RefreshCw size={18} />
              Refresh Workspace
            </button>
          </div>
        {:else}
          <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
            {#each launcherState.versions as version (version.id)}
              <VersionCard
                {version}
                metrics={launcherState.performanceMetrics.get(version.id)}
                isSelected={launcherState.selectedVersions.includes(version.id)}
              />
            {/each}
          </div>
        {/if}
      </div>
    {/if}
  </main>
</div>


