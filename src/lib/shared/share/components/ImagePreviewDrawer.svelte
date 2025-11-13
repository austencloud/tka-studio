<!-- ImagePreviewDrawer.svelte - Preview and Options Drawer -->
<script lang="ts">
  import { Drawer } from "$shared";
  import type { SequenceData } from "$shared";
  import type { createShareState } from "../state";

  let {
    isOpen = $bindable(false),
    currentSequence,
    shareState,
    onRetryPreview,
    onToggle,
  }: {
    isOpen?: boolean;
    currentSequence: SequenceData | null;
    shareState: ReturnType<typeof createShareState> | null;
    onRetryPreview?: () => void;
    onToggle?: (key: keyof NonNullable<typeof shareState>["options"]) => void;
  } = $props();

  function handleToggle(key: keyof NonNullable<typeof shareState>["options"]) {
    onToggle?.(key);
  }
</script>

<Drawer bind:isOpen placement="bottom" ariaLabel="Image Preview & Options">
  <div class="preview-drawer-content">
    <!-- Preview Section -->
    <div class="drawer-preview-section">
      {#if !currentSequence}
        <div class="preview-placeholder">
          <p>No sequence selected</p>
          <span>Create or select a sequence to see preview</span>
        </div>
      {:else if currentSequence.beats?.length === 0}
        <div class="preview-placeholder">
          <p>Empty sequence</p>
          <span>Add beats to generate preview</span>
        </div>
      {:else if shareState?.isGeneratingPreview}
        <div class="preview-loading">
          <div class="loading-spinner"></div>
          <p>Generating preview...</p>
        </div>
      {:else if shareState?.previewError}
        <div class="preview-error">
          <p>Preview failed</p>
          <span>{shareState.previewError}</span>
          <button class="retry-button" onclick={onRetryPreview}>Try Again</button>
        </div>
      {:else if shareState?.previewUrl}
        <img
          src={shareState.previewUrl}
          alt="Sequence preview"
          class="drawer-preview-image"
        />
      {:else}
        <div class="preview-placeholder">
          <p>Preview will appear here</p>
        </div>
      {/if}
    </div>

    <!-- Image Options -->
    {#if shareState?.options}
      <div class="drawer-options">
        <!-- Toggle Options -->
        <div class="options-group">
          <h4>Include in Image</h4>
          <div class="toggle-options">
            <label class="toggle-option">
              <input
                type="checkbox"
                checked={shareState.options.addWord}
                onchange={() => handleToggle("addWord")}
              />
              <span class="toggle-switch"></span>
              <span class="toggle-label">Word Label</span>
            </label>

            <label class="toggle-option">
              <input
                type="checkbox"
                checked={shareState.options.addBeatNumbers}
                onchange={() => handleToggle("addBeatNumbers")}
              />
              <span class="toggle-switch"></span>
              <span class="toggle-label">Beat Numbers</span>
            </label>

            <label class="toggle-option">
              <input
                type="checkbox"
                checked={shareState.options.addDifficultyLevel}
                onchange={() => handleToggle("addDifficultyLevel")}
              />
              <span class="toggle-switch"></span>
              <span class="toggle-label">Difficulty Level</span>
            </label>

            <label class="toggle-option">
              <input
                type="checkbox"
                checked={shareState.options.includeStartPosition}
                onchange={() => handleToggle("includeStartPosition")}
              />
              <span class="toggle-switch"></span>
              <span class="toggle-label">Start Position</span>
            </label>

            <label class="toggle-option">
              <input
                type="checkbox"
                checked={shareState.options.addUserInfo}
                onchange={() => handleToggle("addUserInfo")}
              />
              <span class="toggle-switch"></span>
              <span class="toggle-label">User Info</span>
            </label>
          </div>
        </div>

        <!-- Format Selection -->
        <div class="options-group">
          <h4>Image Format</h4>
          <div class="format-buttons">
            <button
              class="format-btn"
              class:active={shareState.options.format === "PNG"}
              onclick={() => shareState?.updateOptions({ format: "PNG" })}
            >
              PNG
            </button>
            <button
              class="format-btn"
              class:active={shareState.options.format === "JPEG"}
              onclick={() => shareState?.updateOptions({ format: "JPEG" })}
            >
              JPEG
            </button>
            <button
              class="format-btn"
              class:active={shareState.options.format === "WebP"}
              onclick={() => shareState?.updateOptions({ format: "WebP" })}
            >
              WebP
            </button>
          </div>
        </div>

        <!-- Quality Slider (for JPEG/WebP) -->
        {#if shareState.options.format !== "PNG"}
          <div class="options-group">
            <h4>
              Quality
              <span class="quality-value"
                >{Math.round(shareState.options.quality * 100)}%</span
              >
            </h4>
            <input
              type="range"
              min="0.5"
              max="1"
              step="0.05"
              value={shareState.options.quality}
              oninput={(e) =>
                shareState?.updateOptions({
                  quality: parseFloat(e.currentTarget.value),
                })}
              class="quality-slider"
            />
          </div>
        {/if}
      </div>
    {/if}
  </div>
</Drawer>

<style>
  /* Drawer Content */
  .preview-drawer-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding: 20px;
  }

  .drawer-preview-section {
    width: 100%;
    min-height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 20px;
  }

  .drawer-preview-image {
    max-width: 100%;
    max-height: 400px;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  }

  .drawer-options {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .preview-placeholder,
  .preview-loading,
  .preview-error {
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: center;
  }

  .preview-placeholder p,
  .preview-loading p,
  .preview-error p {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
  }

  .preview-placeholder span,
  .preview-error span {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid rgba(59, 130, 246, 0.8);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .retry-button {
    margin-top: 8px;
    padding: 10px 20px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .retry-button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
  }

  /* Options Groups */
  .options-group {
    margin-bottom: 24px;
  }

  .options-group:last-child {
    margin-bottom: 0;
  }

  .options-group h4 {
    margin: 0 0 14px 0;
    font-size: 13px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .quality-value {
    font-size: 12px;
    color: rgba(59, 130, 246, 0.9);
    font-weight: 700;
    background: linear-gradient(
      135deg,
      rgba(59, 130, 246, 0.15),
      rgba(59, 130, 246, 0.08)
    );
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid rgba(59, 130, 246, 0.25);
  }

  /* Toggle Options */
  .toggle-options {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .toggle-option {
    display: flex;
    align-items: center;
    gap: 14px;
    cursor: pointer;
    padding: 12px 16px;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.03),
      rgba(255, 255, 255, 0.01)
    );
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    transition: all 0.2s ease;
  }

  .toggle-option:hover {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.06),
      rgba(255, 255, 255, 0.03)
    );
    border-color: rgba(255, 255, 255, 0.12);
  }

  .toggle-option input[type="checkbox"] {
    position: absolute;
    opacity: 0;
    pointer-events: none;
  }

  /* iOS-style Toggle Switch */
  .toggle-switch {
    position: relative;
    width: 48px;
    height: 28px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    flex-shrink: 0;
  }

  .toggle-switch::before {
    content: "";
    position: absolute;
    top: 2px;
    left: 2px;
    width: 22px;
    height: 22px;
    background: white;
    border-radius: 50%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow:
      0 2px 4px rgba(0, 0, 0, 0.2),
      0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .toggle-option input[type="checkbox"]:checked + .toggle-switch {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    border-color: #3b82f6;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.4);
  }

  .toggle-option input[type="checkbox"]:checked + .toggle-switch::before {
    transform: translateX(20px);
  }

  .toggle-label {
    font-size: 14px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
  }

  /* Format Buttons */
  .format-buttons {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }

  .format-btn {
    padding: 12px 20px;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08),
      rgba(255, 255, 255, 0.04)
    );
    border: 1.5px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.8);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .format-btn:hover {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.12),
      rgba(255, 255, 255, 0.06)
    );
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-1px);
  }

  .format-btn.active {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    border-color: #3b82f6;
    color: white;
    box-shadow:
      0 4px 12px rgba(59, 130, 246, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .format-btn.active:hover {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    transform: translateY(-2px);
    box-shadow:
      0 6px 16px rgba(59, 130, 246, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.25);
  }

  /* Quality Slider */
  .quality-slider {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
    outline: none;
    -webkit-appearance: none;
    appearance: none;
    cursor: pointer;
  }

  .quality-slider::-webkit-slider-track {
    width: 100%;
    height: 6px;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.12),
      rgba(255, 255, 255, 0.08)
    );
    border-radius: 3px;
    border: 1px solid rgba(255, 255, 255, 0.15);
  }

  .quality-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    border-radius: 50%;
    cursor: pointer;
    box-shadow:
      0 2px 8px rgba(59, 130, 246, 0.4),
      0 0 12px rgba(59, 130, 246, 0.3);
    border: 2px solid white;
    transition: all 0.2s ease;
  }

  .quality-slider::-webkit-slider-thumb:hover {
    transform: scale(1.15);
    box-shadow:
      0 4px 12px rgba(59, 130, 246, 0.5),
      0 0 16px rgba(59, 130, 246, 0.4);
  }

  .quality-slider::-moz-range-track {
    width: 100%;
    height: 6px;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.12),
      rgba(255, 255, 255, 0.08)
    );
    border-radius: 3px;
    border: 1px solid rgba(255, 255, 255, 0.15);
  }

  .quality-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    border-radius: 50%;
    cursor: pointer;
    box-shadow:
      0 2px 8px rgba(59, 130, 246, 0.4),
      0 0 12px rgba(59, 130, 246, 0.3);
    border: 2px solid white;
    transition: all 0.2s ease;
  }

  .quality-slider::-moz-range-thumb:hover {
    transform: scale(1.15);
    box-shadow:
      0 4px 12px rgba(59, 130, 246, 0.5),
      0 0 16px rgba(59, 130, 246, 0.4);
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .drawer-preview-section {
      min-height: 200px;
      padding: 16px;
    }

    .drawer-preview-image {
      max-height: 300px;
    }
  }
</style>
