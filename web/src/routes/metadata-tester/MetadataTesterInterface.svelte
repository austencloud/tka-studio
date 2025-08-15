<!-- Main Metadata Tester Interface -->
<script lang="ts">
  import ThumbnailBrowser from "./components/ThumbnailBrowser.svelte";
  import MetadataDisplay from "./components/MetadataDisplay.svelte";
  import { createMetadataTesterState } from "./state/metadata-tester-state.svelte";

  // Initialize the metadata tester state
  const state = createMetadataTesterState();
</script>

<div class="metadata-tester-container">
  <header class="tester-header">
    <h1>🔍 TKA Metadata Tester</h1>
    <p>Test and validate PNG metadata extraction for sequence files</p>
  </header>

  <main class="tester-main">
    <!-- Left Panel: Thumbnail Browser -->
    <div class="panel thumbnail-browser">
      <ThumbnailBrowser {state} />
    </div>

    <!-- Right Panel: Metadata Display -->
    <div class="panel metadata-display">
      <MetadataDisplay {state} />
    </div>
  </main>
</div>

<style>
  .metadata-tester-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
    color: white;
    padding: 20px;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }

  .tester-header {
    text-align: center;
    margin-bottom: 30px;
  }

  .tester-header h1 {
    font-size: 2.5rem;
    margin: 0 0 10px 0;
    background: linear-gradient(45deg, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .tester-header p {
    font-size: 1.1rem;
    opacity: 0.8;
    margin: 0;
  }

  .tester-main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    height: calc(100vh - 180px);
  }

  .panel {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 20px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .thumbnail-browser {
    background: rgba(59, 130, 246, 0.05);
    border-color: rgba(59, 130, 246, 0.2);
  }

  .metadata-display {
    background: rgba(34, 197, 94, 0.05);
    border-color: rgba(34, 197, 94, 0.2);
  }

  /* Responsive design */
  @media (max-width: 1024px) {
    .tester-main {
      grid-template-columns: 1fr;
      grid-template-rows: 1fr 1fr;
    }
  }

  @media (max-width: 768px) {
    .metadata-tester-container {
      padding: 10px;
    }

    .tester-header h1 {
      font-size: 2rem;
    }

    .panel {
      padding: 15px;
    }
  }
</style>
