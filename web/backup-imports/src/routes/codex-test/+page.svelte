<!--
  Standalone Codex Test Page
  
  Simple page to test codex functionality in isolation
-->
<script lang="ts">
  import CodexComponent from "$lib/components/codex/CodexComponent.svelte";

  console.log("🔧 Codex test page: Script loaded");

  // Simple handler for pictograph selection
  function handlePictographSelected(pictograph: any) {
    console.log("Pictograph selected:", pictograph);
  }

  console.log("🔧 Codex test page: Script setup complete");
</script>

<svelte:head>
  <title>Codex Test Page</title>
</svelte:head>

<div class="test-page">
  <h1>Codex Test Page</h1>
  <p>This is a standalone test page for the codex component.</p>

  <div class="codex-container">
    {#key "codex-test"}
      <CodexComponent
        isVisible={true}
        onPictographSelected={handlePictographSelected}
      />
    {/key}
  </div>
</div>

<style>
  .test-page {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .codex-container {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 2rem;
    background: #f9f9f9;
  }

  h1 {
    color: #333;
    margin-bottom: 1rem;
  }

  p {
    color: #666;
    margin-bottom: 1rem;
  }
</style>
