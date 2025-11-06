<!--
  InstagramLinkSheet.svelte - Bottom Sheet for Adding/Editing Instagram Links
  
  Modern slide-up panel for linking Instagram videos to TKA sequences.
-->
<script lang="ts">
  import { Drawer, SheetDragHandle, resolve, TYPES } from "$shared";
  import type { IHapticFeedbackService } from "$shared";
  import type { IInstagramLinkService } from "../services/contracts";
  import type { InstagramLink } from "../domain";
  import { onMount } from "svelte";

  const {
    show = false,
    existingLink = null,
    onSave,
    onRemove,
    onClose,
  }: {
    show?: boolean;
    existingLink?: InstagramLink | null;
    onSave?: (link: InstagramLink) => void;
    onRemove?: () => void;
    onClose?: () => void;
  } = $props();

  // Services
  let instagramService: IInstagramLinkService;
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    instagramService = resolve(TYPES.IInstagramLinkService) as IInstagramLinkService;
    hapticService = resolve(TYPES.IHapticFeedbackService) as IHapticFeedbackService;
  });

  // Form state
  let url = $state("");
  let caption = $state("");
  let validationError = $state<string | null>(null);

  // Initialize form when existing link changes
  $effect(() => {
    if (existingLink) {
      url = existingLink.url;
      caption = existingLink.caption || "";
    } else {
      url = "";
      caption = "";
    }
    validationError = null;
  });

  // Real-time validation
  $effect(() => {
    if (url.trim() && instagramService) {
      const validation = instagramService.validateUrl(url);
      validationError = validation.error;
    } else {
      validationError = null;
    }
  });

  const isValid = $derived(() => {
    return url.trim() && !validationError;
  });

  function handleSave() {
    if (!instagramService) return;

    hapticService?.trigger("selection");

    const validation = instagramService.validateUrl(url);
    if (!validation.isValid) {
      validationError = validation.error;
      hapticService?.trigger("error");
      return;
    }

    const link = instagramService.createLink(url, {
      caption: caption.trim() || undefined,
    });

    onSave?.(link);
    handleClose();
  }

  function handleRemove() {
    hapticService?.trigger("warning");
    onRemove?.();
    handleClose();
  }

  function handleClose() {
    hapticService?.trigger("selection");
    onClose?.();
  }

  const isEditing = $derived(() => Boolean(existingLink));
</script>

<Drawer
  isOpen={show}
  labelledBy="instagram-link-title"
  onclose={handleClose}
  closeOnBackdrop={true}
  focusTrap={true}
  lockScroll={true}
  showHandle={true}
  placement="bottom"
  class="instagram-link-sheet"
  backdropClass="instagram-link-sheet__backdrop"
>
  <div class="instagram-sheet__container">
    <SheetDragHandle />

    <!-- Header -->
    <header class="instagram-sheet__header">
      <div class="header-content">
        <i class="fa-brands fa-instagram instagram-icon"></i>
        <h2 id="instagram-link-title">
          {isEditing() ? "Edit Instagram Link" : "Link Instagram Video"}
        </h2>
      </div>
      <button
        class="close-button"
        onclick={handleClose}
        aria-label="Close Instagram link sheet"
      >
        <i class="fas fa-times"></i>
      </button>
    </header>

    <!-- Content -->
    <div class="instagram-sheet__content">
      <!-- URL Input -->
      <div class="form-group">
        <label for="instagram-url">Instagram URL</label>
        <input
          id="instagram-url"
          type="url"
          bind:value={url}
          placeholder="https://www.instagram.com/p/..."
          class:error={validationError}
          autocomplete="off"
          autocapitalize="off"
        />
        {#if validationError}
          <p class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            {validationError}
          </p>
        {/if}
        <p class="help-text">
          Paste a link to an Instagram post, reel, or video
        </p>
      </div>

      <!-- Caption Input -->
      <div class="form-group">
        <label for="instagram-caption">Caption (Optional)</label>
        <textarea
          id="instagram-caption"
          bind:value={caption}
          placeholder="Add a note about this video..."
          rows="3"
          maxlength="200"
        ></textarea>
        <p class="help-text char-count">
          {caption.length}/200 characters
        </p>
      </div>

      <!-- Preview (if valid) -->
      {#if isValid() && instagramService}
        {@const validation = instagramService.validateUrl(url)}
        {#if validation.isValid}
          <div class="preview-card">
            <div class="preview-header">
              <i class="fa-brands fa-instagram"></i>
              <span>Preview</span>
            </div>
            <div class="preview-content">
              <p class="preview-url">{url}</p>
              {#if validation.username}
                <p class="preview-username">@{validation.username}</p>
              {/if}
              {#if caption.trim()}
                <p class="preview-caption">{caption}</p>
              {/if}
            </div>
          </div>
        {/if}
      {/if}
    </div>

    <!-- Footer Actions -->
    <footer class="instagram-sheet__footer">
      <div class="button-group">
        {#if isEditing()}
          <button class="btn btn-danger" onclick={handleRemove}>
            <i class="fas fa-trash"></i>
            Remove Link
          </button>
        {/if}
        <button
          class="btn btn-primary"
          onclick={handleSave}
          disabled={!isValid()}
        >
          <i class="fas fa-check"></i>
          {isEditing() ? "Update Link" : "Save Link"}
        </button>
      </div>
    </footer>
  </div>
</Drawer>

<style>
  /* Container */
  .instagram-sheet__container {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-height: 85vh;
    background: linear-gradient(
      135deg,
      rgba(20, 20, 30, 0.98) 0%,
      rgba(30, 30, 45, 0.98) 100%
    );
    border-radius: 24px 24px 0 0;
    overflow: hidden;
  }

  /* Header */
  .instagram-sheet__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.03);
  }

  .header-content {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .instagram-icon {
    font-size: 1.5rem;
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .instagram-sheet__header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .close-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border: none;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-primary);
  }

  /* Content */
  .instagram-sheet__content {
    flex: 1;
    padding: 1.5rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  /* Form Groups */
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .form-group label {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .form-group input,
  .form-group textarea {
    padding: 0.75rem 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 1rem;
    font-family: inherit;
    transition: all 0.2s ease;
  }

  .form-group input:focus,
  .form-group textarea:focus {
    outline: none;
    border-color: rgba(59, 130, 246, 0.5);
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .form-group input.error {
    border-color: rgba(239, 68, 68, 0.5);
  }

  .form-group textarea {
    resize: vertical;
    min-height: 80px;
  }

  .help-text {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin: 0;
  }

  .help-text.char-count {
    text-align: right;
  }

  .error-message {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #ef4444;
    margin: 0;
  }

  /* Preview Card */
  .preview-card {
    padding: 1rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
  }

  .preview-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .preview-content {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .preview-url {
    font-size: 0.85rem;
    color: #3b82f6;
    word-break: break-all;
    margin: 0;
  }

  .preview-username {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
  }

  .preview-caption {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-style: italic;
    margin: 0;
  }

  /* Footer */
  .instagram-sheet__footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.03);
  }

  .button-group {
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
  }

  .btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-primary {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }

  .btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-danger {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  .btn-danger:hover {
    background: rgba(239, 68, 68, 0.2);
    border-color: rgba(239, 68, 68, 0.5);
  }

  /* Responsive */
  @media (max-width: 640px) {
    .instagram-sheet__header {
      padding: 0.75rem 1rem;
    }

    .instagram-sheet__header h2 {
      font-size: 1.1rem;
    }

    .instagram-sheet__content {
      padding: 1rem;
    }

    .button-group {
      flex-direction: column-reverse;
    }

    .btn {
      width: 100%;
      justify-content: center;
    }
  }
</style>

