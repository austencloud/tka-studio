<script lang="ts">
  let status = "Click button to start simple test";
  let downloadUrl = "";

  async function runSimpleTest() {
    status = "Finding SVG from BeatGrid...";

    // Open main app in new window
    const appWindow = window.open("http://localhost:5173/", "_blank");
    if (!appWindow) {
      status = "ERROR: Could not open app window";
      return;
    }

    // Wait for app to load
    await new Promise((resolve) => setTimeout(resolve, 3000));

    status = "App loaded, creating sequence...";

    // Wait a bit more for sequence creation
    await new Promise((resolve) => setTimeout(resolve, 2000));

    status = "Capturing SVG...";

    try {
      // Get SVG from the beat grid in the opened window
      const beatGrid = appWindow.document.querySelector('[class*="beat-grid"]');
      if (!beatGrid) {
        status = "ERROR: No beat grid found";
        appWindow.close();
        return;
      }

      const svg = beatGrid.querySelector("svg");
      if (!svg) {
        status = "ERROR: No SVG found";
        appWindow.close();
        return;
      }

      const bbox = svg.getBBox();
      status = `SVG found! BBox: ${bbox.width}×${bbox.height}, right=${bbox.x + bbox.width}, bottom=${bbox.y + bbox.height}`;

      // Clone the SVG
      const svgClone = svg.cloneNode(true) as SVGSVGElement;

      // Convert to blob and then to image
      const svgString = new XMLSerializer().serializeToString(svgClone);
      const svgBlob = new Blob([svgString], { type: "image/svg+xml" });
      const url = URL.createObjectURL(svgBlob);

      // Create image
      const img = new Image();
      img.onload = () => {
        status = "Converting to canvas...";

        // Create canvas with EXACT same size as SVG viewBox
        const canvas = document.createElement("canvas");
        canvas.width = 950;
        canvas.height = 950;

        const ctx = canvas.getContext("2d");
        if (!ctx) {
          status = "ERROR: Canvas context failed";
          URL.revokeObjectURL(url);
          appWindow.close();
          return;
        }

        // White background
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, 950, 950);

        // Draw image at exact size
        ctx.drawImage(img, 0, 0, 950, 950);

        // Create download
        canvas.toBlob(
          (blob) => {
            if (blob) {
              downloadUrl = URL.createObjectURL(blob);
              status = `✅ SUCCESS! Ready to download. Canvas: ${canvas.width}×${canvas.height}px`;
            }
            URL.revokeObjectURL(url);
            appWindow.close();
          },
          "image/jpeg",
          0.95
        );
      };

      img.onerror = () => {
        status = "ERROR: Image load failed";
        URL.revokeObjectURL(url);
        appWindow.close();
      };

      img.src = url;
    } catch (error) {
      status = `ERROR: ${error}`;
      appWindow.close();
    }
  }

  function download() {
    if (!downloadUrl) return;
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = "simple-export-test.jpg";
    link.click();
  }
</script>

<div class="page">
  <h1>🧪 Simple Export Test</h1>
  <p class="subtitle">
    Bypasses all composition logic - just grabs SVG and converts it
  </p>

  <div class="status-box">
    <strong>Status:</strong>
    <div class="status">{status}</div>
  </div>

  <div class="instructions">
    <h2>What this test does:</h2>
    <ol>
      <li>Opens the main TKA Studio app in a new window</li>
      <li>Waits for it to load and create a sequence</li>
      <li>Grabs the SVG directly from the BeatGrid</li>
      <li>Converts it to a 950×950px canvas</li>
      <li>Exports as JPEG</li>
    </ol>
    <p><strong>This completely bypasses:</strong></p>
    <ul>
      <li>ImageCompositionService</li>
      <li>BeatRenderingService</li>
      <li>LayoutCalculationService</li>
      <li>All composition logic</li>
    </ul>
    <p>
      <strong>Result:</strong> If this STILL shows clipping, the problem is in the
      Pictograph component itself or the SVG→Canvas conversion.
    </p>
  </div>

  <div class="actions">
    <button onclick={runSimpleTest} class="primary">
      🚀 Run Simple Test
    </button>
    <button onclick={download} disabled={!downloadUrl} class="secondary">
      💾 Download Result
    </button>
  </div>
</div>

<style>
  .page {
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
    background: #1a1a2e;
    color: #eee;
    min-height: 100vh;
  }

  h1 {
    color: #4ecca3;
    margin-bottom: 0.5rem;
  }

  .subtitle {
    color: #aaa;
    font-style: italic;
    margin-bottom: 2rem;
  }

  .status-box {
    background: #16213e;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    border-left: 4px solid #4ecca3;
  }

  .status {
    margin-top: 0.5rem;
    font-family: monospace;
    color: #4ecca3;
    font-size: 1.1rem;
  }

  .instructions {
    background: #16213e;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
  }

  .instructions h2 {
    color: #4ecca3;
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }

  .instructions ol,
  .instructions ul {
    padding-left: 1.5rem;
  }

  .instructions li {
    margin-bottom: 0.5rem;
    line-height: 1.6;
  }

  .instructions p {
    margin: 1rem 0;
  }

  .actions {
    display: flex;
    gap: 1rem;
  }

  button {
    padding: 1rem 2rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }

  .primary {
    background: #4ecca3;
    color: #1a1a2e;
  }

  .primary:hover {
    background: #5ef3b1;
    transform: translateY(-2px);
  }

  .secondary {
    background: #0f3460;
    color: #4ecca3;
    border: 2px solid #4ecca3;
  }

  .secondary:hover:not(:disabled) {
    background: #16213e;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
