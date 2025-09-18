<!-- SharePanel.svelte - Modern Share Interface -->
<script lang="ts">
  import { browser } from "$app/environment";
  import type { SequenceData } from "$shared";
  import { createServiceResolver, TYPES } from "$shared";
  import type { ShareOptions } from "../domain";
  import type { IShareService } from "../services/contracts";
  import { createShareState } from "../state";
  import SharePreview from "./SharePreview.svelte";

  // Device detection for responsive design
  let isMobile = $state(false);
  let showOptionsModal = $state(false);
  let showExportModal = $state(false);

  // Detect mobile on mount
  $effect(() => {
    if (browser) {
      const checkMobile = () => {
        isMobile = window.innerWidth < 768;
      };
      checkMobile();
      window.addEventListener('resize', checkMobile);
      return () => window.removeEventListener('resize', checkMobile);
    }
  });

  let {
    currentSequence = null,
  }: {
    currentSequence?: SequenceData | null;
  } = $props();

  // HMR-safe service resolution
  const shareServiceResolver = createServiceResolver<IShareService>(TYPES.IShareService);

  // Create share state reactively when service becomes available
  let shareState = $state<ReturnType<typeof createShareState> | null>(null);

  $effect(() => {
    if (shareServiceResolver.value) {
      shareState = createShareState(shareServiceResolver.value);
    } else {
      shareState = null;
    }
  });

  // Auto-generate preview when sequence or options change
  $effect(() => {
    if (shareState && currentSequence && currentSequence.beats?.length > 0) {
      shareState.generatePreview(currentSequence);
    }
  });

  // Removed unused sequenceInfo - was not being used anywhere in the component

  // Handle download
  async function handleDownload() {
    if (!shareState || !currentSequence) return;
    await shareState.downloadImage(currentSequence);
  }

  // Handle options change
  function handleOptionsChange(newOptions: Partial<ShareOptions>) {
    if (!shareState) return;
    shareState.updateOptions(newOptions);
  }

  // Handle checkbox changes with proper typing
  function handleCheckboxChange(key: keyof ShareOptions) {
    return (event: Event) => {
      const target = event.target as HTMLInputElement;
      handleOptionsChange({ [key]: target.checked });
    };
  }

  // Handle input changes with proper typing
  function handleInputChange(key: keyof ShareOptions) {
    return (event: Event) => {
      const target = event.target as HTMLInputElement;
      handleOptionsChange({ [key]: target.value });
    };
  }
</script>

<div class="share-panel">
  <!-- Header -->
  <div class="share-header">
    <h2 class="share-title">Share & Download</h2>
    
    {#if !browser}
      <p class="share-status">⚠️ Sharing requires JavaScript</p>
    {:else if !shareState}
      <p class="share-status">⚠️ Share service not available</p>
    {:else if shareState.isDownloading}
      <p class="share-status">📤 Downloading...</p>
    {:else if shareState.downloadError}
      <p class="share-status error">❌ {shareState.downloadError}</p>
    {:else if shareState.lastDownloadedFile}
      <p class="share-status success">✅ Downloaded: {shareState.lastDownloadedFile}</p>
    {/if}
  </div>

  <!-- Main content -->
  <div class="share-content">
    <!-- Options Button (All Devices) -->
    <div class="options-section">
      <button
        class="options-btn"
        onclick={() => showOptionsModal = true}
      >
        ⚙️ Customize
      </button>
    </div>

    <!-- Middle: Preview -->
    <div class="preview-section">
      <SharePreview
        {currentSequence}
        previewUrl={shareState?.previewUrl}
        isGenerating={shareState?.isGeneratingPreview || false}
        error={shareState?.previewError}
        onRetry={() => currentSequence && shareState?.generatePreview(currentSequence)}
      />
    </div>

    <!-- Bottom: Export Actions -->
    <div class="export-section">
      {#if isMobile}
        <!-- Mobile: Single Share Button -->
        <button class="share-btn" onclick={() => showExportModal = true}>
          📤 Share
        </button>
      {:else}
        <!-- Desktop: Individual Export Buttons -->
        <div class="export-buttons">
          <button class="export-btn download-btn" onclick={handleDownload}>
            💾 Download
          </button>
          <button class="export-btn instagram-btn" disabled>
            📷 Instagram
          </button>
          <button class="export-btn tiktok-btn" disabled>
            🎵 TikTok
          </button>
          <button class="export-btn share-link-btn" disabled>
            📤 Share Link
          </button>
        </div>
      {/if}
    </div>
  </div>

  <!-- Panel Options Overlay -->
  {#if showOptionsModal}
    <div
      class="panel-overlay"
      role="dialog"
      aria-modal="true"
      tabindex="-1"
      onclick={() => showOptionsModal = false}
      onkeydown={(e) => e.key === 'Escape' && (showOptionsModal = false)}
    >
      <div
        class="panel-modal-content"
        role="document"
      >
        <div class="modal-header">
          <h3>Customize Image Options</h3>
          <button class="modal-close" onclick={() => showOptionsModal = false}>✕</button>
        </div>

        <div class="modal-body">
          {#if shareState?.options}
            <div class="mobile-checkboxes">
              <label class="mobile-checkbox">
                <input
                  type="checkbox"
                  checked={shareState.options.addWord}
                  onchange={handleCheckboxChange('addWord')}
                />
                <span class="checkbox-label">Include word/title</span>
              </label>

              <label class="mobile-checkbox">
                <input
                  type="checkbox"
                  checked={shareState.options.addBeatNumbers}
                  onchange={handleCheckboxChange('addBeatNumbers')}
                />
                <span class="checkbox-label">Show beat numbers</span>
              </label>

              <label class="mobile-checkbox">
                <input
                  type="checkbox"
                  checked={shareState.options.includeStartPosition}
                  onchange={handleCheckboxChange('includeStartPosition')}
                />
                <span class="checkbox-label">Include start position</span>
              </label>

              <label class="mobile-checkbox">
                <input
                  type="checkbox"
                  checked={shareState.options.addUserInfo}
                  onchange={handleCheckboxChange('addUserInfo')}
                />
                <span class="checkbox-label">Include user info</span>
              </label>

              <label class="mobile-checkbox">
                <input
                  type="checkbox"
                  checked={shareState.options.addDifficultyLevel}
                  onchange={handleCheckboxChange('addDifficultyLevel')}
                />
                <span class="checkbox-label">Show difficulty level</span>
              </label>
            </div>

            <!-- User Info Fields (if enabled) -->
            {#if shareState.options.addUserInfo}
              <div class="mobile-user-info">
                <label class="mobile-input-label">
                  Name
                  <input
                    type="text"
                    class="mobile-text-input"
                    value={shareState.options.userName}
                    oninput={handleInputChange('userName')}
                    placeholder="Your name"
                  />
                </label>

                <label class="mobile-input-label">
                  Notes
                  <input
                    type="text"
                    class="mobile-text-input"
                    value={shareState.options.notes}
                    oninput={handleInputChange('notes')}
                    placeholder="Optional notes"
                  />
                </label>
              </div>
            {/if}
          {/if}
        </div>

        <div class="modal-footer">
          <button class="modal-done-btn" onclick={() => showOptionsModal = false}>
            Done
          </button>
        </div>
      </div>
    </div>
  {/if}

  <!-- Mobile Export Modal -->
  {#if isMobile && showExportModal}
    <div
      class="modal-overlay"
      role="dialog"
      aria-modal="true"
      tabindex="-1"
      onclick={() => showExportModal = false}
      onkeydown={(e) => e.key === 'Escape' && (showExportModal = false)}
    >
      <div class="modal-content" role="document">
        <div class="modal-header">
          <h3>Export Options</h3>
          <button class="modal-close" onclick={() => showExportModal = false}>✕</button>
        </div>

        <div class="modal-body">
          <div class="export-options">
            <button class="export-option-btn download-option" onclick={handleDownload}>
              <div class="option-icon">💾</div>
              <div class="option-text">
                <div class="option-title">Download Image</div>
                <div class="option-desc">Save to your device</div>
              </div>
            </button>

            <button class="export-option-btn instagram-option" disabled>
              <div class="option-icon">📷</div>
              <div class="option-text">
                <div class="option-title">Instagram</div>
                <div class="option-desc">Coming soon</div>
              </div>
            </button>

            <button class="export-option-btn tiktok-option" disabled>
              <div class="option-icon">🎵</div>
              <div class="option-text">
                <div class="option-title">TikTok</div>
                <div class="option-desc">Coming soon</div>
              </div>
            </button>

            <button class="export-option-btn share-link-option" disabled>
              <div class="option-icon">📤</div>
              <div class="option-text">
                <div class="option-title">Share Link</div>
                <div class="option-desc">Coming soon</div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .share-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 1rem;
    position: relative;
  }

  .share-header {
    flex-shrink: 0;
  }

  .share-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
  }



  .share-status {
    margin: 0;
    font-size: 0.85rem;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    background: var(--bg-secondary);
    color: var(--text-secondary);
  }

  .share-status.error {
    background: var(--error-bg);
    color: var(--error-text);
  }

  .share-status.success {
    background: var(--success-bg);
    color: var(--success-text);
  }

  .share-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    flex: 1;
    min-height: 0;
    height: 100%;
    overflow: hidden;
  }

  /* Options Section */
  .options-section {
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    padding: 0.5rem 0;
  }

  .options-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 1.5rem;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    transform: translateY(0);
  }

  .options-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
  }

  .options-btn:active {
    transform: translateY(0);
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
  }

  /* Export Section */
  .export-section {
    flex-shrink: 0;
    padding: 1rem 0;
  }

  .export-buttons {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .export-btn {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 0.6rem 1.2rem;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 3px 12px rgba(79, 172, 254, 0.3);
    transform: translateY(0);
    min-width: 100px;
  }

  .export-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 18px rgba(79, 172, 254, 0.4);
  }

  .export-btn:active:not(:disabled) {
    transform: translateY(0);
  }

  .export-btn:disabled {
    background: linear-gradient(135deg, #a0a0a0 0%, #808080 100%);
    cursor: not-allowed;
    opacity: 0.6;
    box-shadow: 0 2px 8px rgba(160, 160, 160, 0.2);
  }

  .download-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    box-shadow: 0 3px 12px rgba(102, 126, 234, 0.3);
  }

  .download-btn:hover {
    box-shadow: 0 5px 18px rgba(102, 126, 234, 0.4);
  }

  .share-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 1rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    transform: translateY(0);
    width: 100%;
    max-width: 200px;
    margin: 0 auto;
    display: block;
  }

  .share-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  /* Export Modal Styles */
  .export-options {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .export-option-btn {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
    border: 1px solid var(--border-color);
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: left;
    width: 100%;
  }

  .export-option-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(79, 172, 254, 0.3);
  }

  .export-option-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background: linear-gradient(135deg, #f0f0f0 0%, #e0e0e0 100%);
  }

  .option-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  .option-text {
    flex: 1;
  }

  .option-title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .option-desc {
    font-size: 0.85rem;
    opacity: 0.8;
  }

  /* Preview Section */
  .preview-section {
    flex: 1;
    min-height: 200px;
    display: flex;
    flex-direction: column;
  }

  /* Modal Styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
  }

  /* Panel-specific overlay for options modal */
  .panel-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: flex-start;
    justify-content: center;
    z-index: 100;
    padding: 1rem;
    border-radius: inherit;
  }

  .modal-content {
    background: var(--bg-primary);
    border-radius: 12px;
    width: 100%;
    max-width: 500px;
    max-height: 80vh;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
  }

  .panel-modal-content {
    background: var(--bg-primary);
    border-radius: 12px;
    width: 100%;
    max-width: 100%;
    max-height: calc(100% - 2rem);
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    margin-top: 1rem;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-secondary);
  }

  .modal-header h3 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    transition: all 0.2s ease;
  }

  .modal-close:hover {
    background: var(--bg-hover);
    color: var(--text-primary);
  }

  .modal-body {
    padding: 1.25rem;
    overflow-y: auto;
    flex: 1;
  }

  .mobile-checkboxes {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .mobile-checkbox {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
    border: 1px solid var(--border-color);
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    transform: translateY(0);
  }

  .mobile-checkbox:hover {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    border-color: transparent;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(79, 172, 254, 0.3);
  }

  .mobile-checkbox input[type="checkbox"] {
    margin: 0;
    width: 20px;
    height: 20px;
    accent-color: var(--accent-color);
  }

  .mobile-user-info {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .mobile-input-label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-primary);
  }

  .mobile-text-input {
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    background: var(--bg-primary);
    color: var(--text-primary);
    font-size: 1rem;
    transition: all 0.3s ease;
  }

  .mobile-text-input:focus {
    outline: none;
    border-color: #4facfe;
    box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.2);
    transform: translateY(-1px);
  }

  .modal-footer {
    padding: 1.25rem;
    border-top: 1px solid var(--border-color);
    background: var(--bg-secondary);
  }

  .modal-done-btn {
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 15px;
    padding: 0.75rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    transform: translateY(0);
  }

  .modal-done-btn:hover {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  /* Responsive Design */
  @media (max-width: 767px) {
    .share-panel {
      padding: 0.75rem;
    }

    .share-content {
      gap: 1rem;
    }
  }
</style>
