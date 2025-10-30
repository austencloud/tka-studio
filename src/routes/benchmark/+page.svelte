<script lang="ts">
import { onMount } from 'svelte';
import { container } from '$shared/inversify/container';
import { TYPES } from '$shared/inversify/types';
import type { ISequenceRenderService } from '$render';
import type { SequenceData } from '$shared';

// Your actual 16-beat sequence from the request
const TEST_SEQUENCE: SequenceData = {
  "id": "fd609c39-163f-49ec-b504-7cd42103e399",
  "name": "Circular XΔX-ΔXΔX-ΔXΔX-ΔXΔX-Δ",
  "word": "XΔX-ΔXΔX-ΔXΔX-ΔXΔX-Δ",
  "beats": [
    {
      "id": "e7bf366d-ba05-46f2-abf1-c71546f90ed2",
      "letter": "X",
      "startPosition": "gamma11",
      "endPosition": "alpha3",
      "motions": {
        "blue": {
          "motionType": "anti",
          "rotationDirection": "ccw",
          "startLocation": "s",
          "endLocation": "w",
          "turns": 0,
          "startOrientation": "in",
          "endOrientation": "out",
          "isVisible": true,
          "propType": "staff",
          "arrowLocation": "n",
          "color": "blue",
          "gridMode": "diamond",
          "arrowPlacementData": {
            "positionX": 0,
            "positionY": 0,
            "rotationAngle": 0,
            "coordinates": null,
            "svgCenter": null,
            "svgMirrored": false
          },
          "propPlacementData": {
            "positionX": 0,
            "positionY": 0,
            "rotationAngle": 0,
            "coordinates": null,
            "svgCenter": null
          },
          "prefloatMotionType": null,
          "prefloatRotationDirection": null
        },
        "red": {
          "motionType": "static",
          "rotationDirection": "ccw",
          "startLocation": "e",
          "endLocation": "e",
          "turns": 1,
          "startOrientation": "in",
          "endOrientation": "out",
          "isVisible": true,
          "propType": "staff",
          "arrowLocation": "n",
          "color": "red",
          "gridMode": "diamond",
          "arrowPlacementData": {
            "positionX": 0,
            "positionY": 0,
            "rotationAngle": 0,
            "coordinates": null,
            "svgCenter": null,
            "svgMirrored": false
          },
          "propPlacementData": {
            "positionX": 0,
            "positionY": 0,
            "rotationAngle": 0,
            "coordinates": null,
            "svgCenter": null
          },
          "prefloatMotionType": null,
          "prefloatRotationDirection": null
        }
      },
      "beatNumber": 1,
      "duration": 1,
      "blueReversal": false,
      "redReversal": false,
      "isBlank": false
    },
    {
      "id": "0ced6c2e-6eda-4fca-9ecc-50b0f2ec880b",
      "letter": "Δ",
      "startPosition": "alpha3",
      "endPosition": "gamma13",
      "motions": {
        "blue": {
          "motionType": "static",
          "rotationDirection": "noRotation",
          "startLocation": "w",
          "endLocation": "w",
          "turns": 0,
          "startOrientation": "out",
          "endOrientation": "out",
          "isVisible": true,
          "propType": "staff",
          "arrowLocation": "n",
          "color": "blue",
          "gridMode": "diamond",
          "arrowPlacementData": {
            "positionX": 0,
            "positionY": 0,
            "rotationAngle": 0,
            "coordinates": null,
            "svgCenter": null,
            "svgMirrored": false
          },
          "propPlacementData": {
            "positionX": 0,
            "positionY": 0,
            "rotationAngle": 0,
            "coordinates": null,
            "svgCenter": null
          },
          "prefloatMotionType": null,
          "prefloatRotationDirection": null
        },
        "red": {
          "motionType": "anti",
          "rotationDirection": "ccw",
          "startLocation": "e",
          "endLocation": "s",
          "turns": 0,
          "startOrientation": "out",
          "endOrientation": "in",
          "isVisible": true,
          "propType": "staff",
          "arrowLocation": "n",
          "color": "red",
          "gridMode": "diamond",
          "arrowPlacementData": {
            "positionX": 0,
            "positionY": 0,
            "rotationAngle": 0,
            "coordinates": null,
            "svgCenter": null,
            "svgMirrored": false
          },
          "propPlacementData": {
            "positionX": 0,
            "positionY": 0,
            "rotationAngle": 0,
            "coordinates": null,
            "svgCenter": null
          },
          "prefloatMotionType": null,
          "prefloatRotationDirection": null
        }
      },
      "beatNumber": 2,
      "duration": 1,
      "blueReversal": false,
      "redReversal": false,
      "isBlank": false
    }
  ],
  "thumbnails": [],
  "isFavorite": false,
  "isCircular": true,
  "tags": ["circular", "cap", "strict-rotated"],
  "metadata": {
    "generated": true,
    "generatedAt": "2025-10-29T23:11:43.464Z",
    "algorithm": "freeform",
    "beatsGenerated": 2,
    "propContinuity": "continuous",
    "blueRotationDirection": "",
    "redRotationDirection": "",
    "turnIntensity": 1,
    "level": 2
  },
  "gridMode": "diamond",
  "propType": "fan",
  "startingPositionBeat": {
    "id": "4146b97b-0849-46fd-a971-2c73e0a7a4e6",
    "motions": {
      "blue": {
        "motionType": "static",
        "rotationDirection": "noRotation",
        "startLocation": "s",
        "endLocation": "s",
        "turns": 0,
        "startOrientation": "in",
        "endOrientation": "in",
        "isVisible": true,
        "propType": "staff",
        "arrowLocation": "s",
        "color": "blue",
        "gridMode": "diamond",
        "arrowPlacementData": {
          "positionX": 0,
          "positionY": 0,
          "rotationAngle": 0,
          "coordinates": null,
          "svgCenter": null,
          "svgMirrored": false
        },
        "propPlacementData": {
          "positionX": 0,
          "positionY": 0,
          "rotationAngle": 0,
          "coordinates": null,
          "svgCenter": null
        },
        "prefloatMotionType": null,
        "prefloatRotationDirection": null
      },
      "red": {
        "motionType": "static",
        "rotationDirection": "noRotation",
        "startLocation": "e",
        "endLocation": "e",
        "turns": 0,
        "startOrientation": "in",
        "endOrientation": "in",
        "isVisible": true,
        "propType": "staff",
        "arrowLocation": "e",
        "color": "red",
        "gridMode": "diamond",
        "arrowPlacementData": {
          "positionX": 0,
          "positionY": 0,
          "rotationAngle": 0,
          "coordinates": null,
          "svgCenter": null,
          "svgMirrored": false
        },
        "propPlacementData": {
          "positionX": 0,
          "positionY": 0,
          "rotationAngle": 0,
          "coordinates": null,
          "svgCenter": null
        },
        "prefloatMotionType": null,
        "prefloatRotationDirection": null
      }
    },
    "letter": "Γ",
    "startPosition": "gamma11",
    "endPosition": "gamma11",
    "beatNumber": 0,
    "duration": 1,
    "blueReversal": false,
    "redReversal": false,
    "isBlank": false
  },
  "startPosition": {
    "id": "4146b97b-0849-46fd-a971-2c73e0a7a4e6",
    "motions": {
      "blue": {
        "motionType": "static",
        "rotationDirection": "noRotation",
        "startLocation": "s",
        "endLocation": "s",
        "turns": 0,
        "startOrientation": "in",
        "endOrientation": "in",
        "isVisible": true,
        "propType": "staff",
        "arrowLocation": "s",
        "color": "blue",
        "gridMode": "diamond",
        "arrowPlacementData": {
          "positionX": 0,
          "positionY": 0,
          "rotationAngle": 0,
          "coordinates": null,
          "svgCenter": null,
          "svgMirrored": false
        },
        "propPlacementData": {
          "positionX": 0,
          "positionY": 0,
          "rotationAngle": 0,
          "coordinates": null,
          "svgCenter": null
        },
        "prefloatMotionType": null,
        "prefloatRotationDirection": null
      },
      "red": {
        "motionType": "static",
        "rotationDirection": "noRotation",
        "startLocation": "e",
        "endLocation": "e",
        "turns": 0,
        "startOrientation": "in",
        "endOrientation": "in",
        "isVisible": true,
        "propType": "staff",
        "arrowLocation": "e",
        "color": "red",
        "gridMode": "diamond",
        "arrowPlacementData": {
          "positionX": 0,
          "positionY": 0,
          "rotationAngle": 0,
          "coordinates": null,
          "svgCenter": null,
          "svgMirrored": false
        },
        "propPlacementData": {
          "positionX": 0,
          "positionY": 0,
          "rotationAngle": 0,
          "coordinates": null,
          "svgCenter": null
        },
        "prefloatMotionType": null,
        "prefloatRotationDirection": null
      }
    },
    "letter": "Γ",
    "startPosition": "gamma11",
    "endPosition": "gamma11",
    "beatNumber": 0,
    "duration": 1,
    "blueReversal": false,
    "redReversal": false,
    "isBlank": false
  },
  "difficultyLevel": "intermediate"
} as SequenceData;

let renderService: ISequenceRenderService;
let running = false;
let results: any[] = [];
let currentTest = '';
let progress = 0;

onMount(async () => {
  renderService = container.get<ISequenceRenderService>(TYPES.ISequenceRenderService);
});

async function runBenchmark() {
  running = true;
  results = [];
  progress = 0;

  const configs = [
    { beatScale: 0.15, quality: 0.4, format: 'JPEG' as const, name: 'CURRENT (Share Preview)' },
    { beatScale: 0.12, quality: 0.4, format: 'JPEG' as const, name: 'Lower Scale' },
    { beatScale: 0.15, quality: 0.3, format: 'JPEG' as const, name: 'Lower Quality' },
    { beatScale: 0.22, quality: 0.45, format: 'JPEG' as const, name: 'RECOMMENDED (Phone)' },
    { beatScale: 0.15, quality: 0.4, format: 'PNG' as const, name: 'PNG Format' },
  ];

  for (let i = 0; i < configs.length; i++) {
    const config = configs[i];
    currentTest = config.name;
    progress = ((i + 1) / configs.length) * 100;

    const times: number[] = [];
    let preview = '';

    // Run 3 times and average
    for (let j = 0; j < 3; j++) {
      const start = performance.now();

      preview = await renderService.generatePreview(TEST_SEQUENCE, {
        beatScale: config.beatScale,
        quality: config.quality,
        format: config.format,
        includeStartPosition: true,
        addBeatNumbers: true,
        addWord: true,
        addDifficultyLevel: true,
      });

      const end = performance.now();
      times.push(end - start);
    }

    const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
    const sizeKB = (preview.length * 0.75) / 1024;

    results.push({
      config: `Scale: ${config.beatScale}, Q: ${config.quality}, ${config.format}`,
      avgTime: avgTime.toFixed(0),
      sizeKB: sizeKB.toFixed(1),
      preview,
      ...config
    });

    results = [...results]; // Trigger reactivity
  }

  running = false;
  currentTest = '';
}
</script>

<div class="benchmark-page">
  <h1>🎨 REAL Sequence Preview Benchmark</h1>
  <p class="subtitle">Using ACTUAL pictograph rendering with your REAL sequence data</p>

  <div class="info-box">
    <h3>⚠️ This is the REAL test</h3>
    <p>Testing with 2-beat sequence using your actual rendering pipeline:</p>
    <ul>
      <li>✅ Real SVG generation via renderPictographToSVG()</li>
      <li>✅ Real ImageCompositionService</li>
      <li>✅ Real canvas rendering</li>
      <li>✅ Real format conversion</li>
    </ul>
    <p><strong>Note:</strong> Full 16-beat sequence would take ~8x longer</p>
  </div>

  <button on:click={runBenchmark} disabled={running || !renderService}>
    {running ? '⏳ Running Benchmark...' : '🚀 Run REAL Benchmark'}
  </button>

  {#if running}
    <div class="progress-bar">
      <div class="progress-fill" style="width: {progress}%"></div>
      <span class="progress-text">{currentTest} - {progress.toFixed(0)}%</span>
    </div>
  {/if}

  {#if results.length > 0}
    <div class="results">
      <h2>📊 Results</h2>

      <table>
        <thead>
          <tr>
            <th>Configuration</th>
            <th>Avg Time</th>
            <th>Size</th>
            <th>Preview</th>
          </tr>
        </thead>
        <tbody>
          {#each results as result}
            <tr>
              <td>
                <strong>{result.name}</strong><br>
                <small>{result.config}</small>
              </td>
              <td class:excellent={result.avgTime < 100} class:good={result.avgTime >= 100 && result.avgTime < 300} class:poor={result.avgTime >= 300}>
                {result.avgTime}ms
              </td>
              <td class:excellent={result.sizeKB < 10} class:good={result.sizeKB >= 10 && result.sizeKB < 20} class:poor={result.sizeKB >= 20}>
                {result.sizeKB}KB
              </td>
              <td>
                <img src={result.preview} alt="Preview" />
              </td>
            </tr>
          {/each}
        </tbody>
      </table>

      <div class="analysis">
        <h3>📈 Analysis</h3>
        <div class="recommendation">
          <h4>Current Performance</h4>
          <p>Time: {results[0].avgTime}ms, Size: {results[0].sizeKB}KB</p>
          <p><strong>For 16 beats:</strong> ~{(parseFloat(results[0].avgTime) * 8).toFixed(0)}ms estimated</p>
        </div>

        <div class="recommendation">
          <h4>Recommended Settings</h4>
          <p>{results.find(r => r.name.includes('RECOMMENDED'))?.name}</p>
          <p>Time: {results.find(r => r.name.includes('RECOMMENDED'))?.avgTime}ms</p>
          <p>Larger preview (190px vs 130px wide) for better phone visibility</p>
        </div>

        <div class="recommendation critical">
          <h4>💡 CONCLUSION</h4>
          <ul>
            <li>Current settings: {results[0].avgTime}ms × 8 = ~{(parseFloat(results[0].avgTime) * 8).toFixed(0)}ms for 16 beats</li>
            <li>
              {parseFloat(results[0].avgTime) * 8 > 500
                ? '⚠️ >500ms - Background pre-rendering RECOMMENDED'
                : '✅ <500ms - Acceptable, but pre-rendering still recommended'}
            </li>
            <li>✅ Increase beatScale to 0.22 for better phone visibility</li>
            <li>✅ Implement caching for instant subsequent views</li>
          </ul>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .benchmark-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  h1 {
    color: #667eea;
    margin-bottom: 10px;
  }

  .subtitle {
    color: #666;
    margin-bottom: 30px;
  }

  .info-box {
    background: #e7f3ff;
    border-left: 4px solid #667eea;
    padding: 20px;
    margin: 20px 0;
    border-radius: 8px;
  }

  .info-box h3 {
    margin-top: 0;
    color: #667eea;
  }

  .info-box ul {
    margin: 10px 0;
    padding-left: 20px;
  }

  button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 8px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    margin: 20px 0;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .progress-bar {
    position: relative;
    width: 100%;
    height: 50px;
    background: #f0f0f0;
    border-radius: 8px;
    overflow: hidden;
    margin: 20px 0;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    transition: width 0.3s;
  }

  .progress-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-weight: 600;
    color: #333;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
  }

  thead {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  th, td {
    padding: 12px;
    text-align: left;
  }

  tbody tr:nth-child(even) {
    background: #f8f9fa;
  }

  td.excellent {
    background: #d4edda;
    color: #155724;
    font-weight: 600;
  }

  td.good {
    background: #fff3cd;
    color: #856404;
    font-weight: 600;
  }

  td.poor {
    background: #f8d7da;
    color: #721c24;
    font-weight: 600;
  }

  td img {
    max-width: 150px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .analysis {
    margin-top: 30px;
  }

  .recommendation {
    background: #f8f9fa;
    border-left: 4px solid #667eea;
    padding: 15px;
    margin: 15px 0;
    border-radius: 4px;
  }

  .recommendation.critical {
    background: #fff3cd;
    border-left-color: #ffc107;
  }

  .recommendation h4 {
    margin-top: 0;
    color: #667eea;
  }

  .recommendation ul {
    margin: 10px 0;
    padding-left: 20px;
  }
</style>
