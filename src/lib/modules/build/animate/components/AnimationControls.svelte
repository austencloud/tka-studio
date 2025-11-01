<!--
  AnimationControls.svelte

  Reusable animation controls component with speed slider and export button.
-->
<script lang="ts">
  // Props
  let {
    speed = 1,
    onSpeedChange = () => {},
    onExport = () => {},
  }: {
    speed?: number;
    onSpeedChange?: (event: Event) => void;
    onExport?: () => void;
  } = $props();
</script>

<div class="controls-container">
  <div class="speed-control">
    <label for="speed-slider" class="speed-label">Speed</label>
    <input
      id="speed-slider"
      type="range"
      min="0.25"
      max="2"
      step="0.25"
      value={speed}
      oninput={onSpeedChange}
      aria-label="Animation speed"
    />
    <span class="speed-value">{speed.toFixed(2)}x</span>
  </div>

  <button class="export-button" onclick={onExport} aria-label="Export as GIF">
    <i class="fas fa-download"></i>
    <span>Export GIF</span>
  </button>
</div>

<style>
  .controls-container {
    width: 100%;
    max-width: 500px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex-shrink: 0;
  }

  .speed-control {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    width: 100%;
  }

  .speed-label {
    font-size: 12px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }

  #speed-slider {
    flex: 1;
    height: 6px;
    -webkit-appearance: none;
    appearance: none;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
    outline: none;
    min-width: 80px;
  }

  #speed-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    transition: all 0.2s ease;
  }

  #speed-slider::-webkit-slider-thumb:hover {
    transform: scale(1.2);
    box-shadow: 0 3px 8px rgba(59, 130, 246, 0.5);
  }

  #speed-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    transition: all 0.2s ease;
  }

  #speed-slider::-moz-range-thumb:hover {
    transform: scale(1.2);
    box-shadow: 0 3px 8px rgba(59, 130, 246, 0.5);
  }

  .speed-value {
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
    min-width: 45px;
    text-align: right;
  }

  .export-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 20px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    border-radius: 12px;
    color: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  }

  .export-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }

  .export-button:active {
    transform: translateY(0);
  }

  .export-button i {
    font-size: 16px;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .speed-control {
      padding: 10px 14px;
      gap: 10px;
    }

    .speed-label {
      font-size: 11px;
    }

    .speed-value {
      font-size: 12px;
      min-width: 42px;
    }
  }

  @media (max-width: 480px) {
    .speed-control {
      padding: 8px 12px;
      gap: 8px;
    }

    .speed-label {
      font-size: 10px;
    }

    .speed-value {
      font-size: 11px;
      min-width: 40px;
    }

    #speed-slider {
      min-width: 60px;
    }
  }

  /* Very narrow viewports */
  @media (max-width: 400px) {
    .speed-control {
      padding: 6px 10px;
      gap: 6px;
    }

    .speed-label {
      display: none; /* Hide label to save space */
    }

    .speed-value {
      font-size: 10px;
      min-width: 35px;
    }

    #speed-slider {
      min-width: 50px;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    #speed-slider::-webkit-slider-thumb,
    #speed-slider::-moz-range-thumb {
      transition: none;
    }

    #speed-slider::-webkit-slider-thumb:hover,
    #speed-slider::-moz-range-thumb:hover {
      transform: none;
    }
  }
</style>
