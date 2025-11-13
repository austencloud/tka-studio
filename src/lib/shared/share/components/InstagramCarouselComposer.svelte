<!--
  Instagram Share Component

  Simple share flow for Instagram - works with ALL account types (personal, business, creator).
  Uses native mobile sharing - no OAuth, no API required.

  Flow:
  1. User selects performance video
  2. App bundles: video + notation image + animated sequence
  3. Opens Instagram with all files pre-loaded (mobile) or downloads zip (desktop)
  4. User taps share in Instagram
-->
<script lang="ts">
  import { onMount } from "svelte";
  import { resolve, TYPES } from "$shared";
  import type { IMediaBundlerService } from "../services/contracts";
  import type { SequenceData } from "$shared";
  import type { InstagramMediaItem, ShareOptions } from "../domain";

  let {
    currentSequence,
    shareOptions,
    onShareComplete,
  }: {
    currentSequence: SequenceData | null;
    shareOptions: ShareOptions;
    onShareComplete?: () => void;
  } = $props();

  // Services
  let mediaBundlerService: IMediaBundlerService;

  // State
  let videoFile = $state<File | null>(null);
  let mediaItems = $state<InstagramMediaItem[]>([]);
  let caption = $state("");
  let isBundling = $state(false);
  let isSharing = $state(false);
  let videoInputRef = $state<HTMLInputElement>();
  let hasNativeShare = $state(false);

  onMount(async () => {
    mediaBundlerService = resolve<IMediaBundlerService>(
      TYPES.IMediaBundlerService
    );
    // Check if Web Share API is available (mobile devices)
    hasNativeShare =
      navigator.share !== undefined && navigator.canShare !== undefined;
  });

  // Handle video file selection
  async function handleVideoSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file) return;

    if (!file.type.startsWith("video/")) {
      alert("Please select a valid video file");
      return;
    }

    videoFile = file;
    await bundleMedia();
  }

  // Bundle media (video + notation + animation)
  async function bundleMedia() {
    if (!currentSequence || !videoFile || !mediaBundlerService) return;

    isBundling = true;

    try {
      const bundle = await mediaBundlerService.createCarouselBundle(
        currentSequence,
        videoFile,
        shareOptions,
        "video-first"
      );

      mediaItems = bundle;

      // Generate suggested caption
      caption = `${currentSequence.word || currentSequence.name}\n\nCreated with The Kinetic Alphabet Studio\n#TKA #TheKineticAlphabet #Flow #Movement`;
    } catch (error: any) {
      console.error("Failed to bundle media:", error);
      alert(`Failed to create media bundle: ${error.message}`);
    } finally {
      isBundling = false;
    }
  }

  // Share to Instagram using native share
  async function handleShareToInstagram() {
    if (!mediaItems.length) return;

    isSharing = true;

    try {
      // Convert media items to File objects
      const files: File[] = [];

      for (const item of mediaItems) {
        const blob = item.blob;
        const filename =
          item.type === "VIDEO"
            ? "performance.mp4"
            : item.type === "IMAGE"
              ? "notation.png"
              : "animation.webp";

        files.push(new File([blob], filename, { type: blob.type }));
      }

      if (hasNativeShare && navigator.canShare({ files })) {
        // Mobile: Use native share to open Instagram directly
        await navigator.share({
          files,
          title: "TKA Sequence",
          text: caption,
        });

        onShareComplete?.();
      } else {
        // Desktop fallback: Download as zip
        await downloadAsZip(files);
      }
    } catch (error: any) {
      if (error.name !== "AbortError") {
        // User didn't cancel
        console.error("Failed to share:", error);
        alert(`Share failed: ${error.message}`);
      }
    } finally {
      isSharing = false;
    }
  }

  // Fallback: Download as zip for desktop
  async function downloadAsZip(files: File[]) {
    // Simple download of files
    // TODO: Implement JSZip if you want a proper zip file
    // For now, just download files individually or show instructions

    const instructions = `To post to Instagram:
1. Open Instagram app on your phone
2. Create new post → Select multiple
3. Choose the downloaded files in order
4. Add this caption:
${caption}
5. Share!`;

    alert(instructions);

    // Download files individually
    for (const file of files) {
      const url = URL.createObjectURL(file);
      const a = document.createElement("a");
      a.href = url;
      a.download = file.name;
      a.click();
      URL.revokeObjectURL(url);
    }
  }

  // Reset everything
  function handleReset() {
    videoFile = null;
    mediaItems = [];
    caption = "";
    if (videoInputRef) {
      videoInputRef.value = "";
    }
  }
</script>

<div class="instagram-share">
  {#if !videoFile || mediaItems.length === 0}
    <!-- Step 1: Upload video -->
    <div class="upload-section">
      <div class="instagram-icon">
        <i class="fab fa-instagram"></i>
      </div>
      <h3>Share to Instagram</h3>
      <p class="subtitle">
        Upload your performance video to create a shareable carousel
      </p>

      <input
        bind:this={videoInputRef}
        type="file"
        accept="video/*"
        onchange={handleVideoSelect}
        style="display: none;"
        aria-label="Select performance video"
      />

      <button
        class="upload-button"
        onclick={() => videoInputRef?.click()}
        disabled={isBundling}
      >
        {#if isBundling}
          <i class="fas fa-spinner fa-spin"></i>
          Preparing media...
        {:else}
          <i class="fas fa-upload"></i>
          Upload Performance Video
        {/if}
      </button>

      <div class="info-box">
        <i class="fas fa-info-circle"></i>
        <p>Works with ANY Instagram account - personal, business, or creator</p>
      </div>
    </div>
  {:else}
    <!-- Step 2: Preview and share -->
    <div class="preview-section">
      <div class="preview-header">
        <h3>Ready to Share</h3>
        <button
          class="reset-button"
          onclick={handleReset}
          aria-label="Start over"
        >
          <i class="fas fa-redo"></i>
        </button>
      </div>

      <!-- Media preview -->
      <div class="media-preview">
        {#each mediaItems as item, index}
          <div class="media-item">
            <div class="media-thumbnail">
              {#if item.type === "VIDEO"}
                <video src={URL.createObjectURL(item.blob)} controls>
                  <track kind="captions" />
                </video>
                <span class="media-label">Performance</span>
              {:else if item.type === "IMAGE"}
                <img src={URL.createObjectURL(item.blob)} alt="Notation" />
                <span class="media-label">Notation</span>
              {:else}
                <img src={URL.createObjectURL(item.blob)} alt="Animation" />
                <span class="media-label">Animation</span>
              {/if}
            </div>
          </div>
        {/each}
      </div>

      <!-- Caption editor -->
      <div class="caption-section">
        <label for="caption">Caption</label>
        <textarea
          id="caption"
          bind:value={caption}
          placeholder="Add a caption..."
          rows="4"
          maxlength="2200"
        ></textarea>
        <p class="char-count">{caption.length}/2200</p>
      </div>

      <!-- Share button -->
      <button
        class="share-button"
        onclick={handleShareToInstagram}
        disabled={isSharing}
      >
        {#if isSharing}
          <i class="fas fa-spinner fa-spin"></i>
          Sharing...
        {:else}
          <i class="fab fa-instagram"></i>
          {hasNativeShare ? "Open Instagram" : "Download Files"}
        {/if}
      </button>

      {#if !hasNativeShare}
        <p class="desktop-note">
          <i class="fas fa-desktop"></i>
          Desktop detected - files will download. Transfer to your phone to post!
        </p>
      {/if}
    </div>
  {/if}
</div>

<style>
  .instagram-share {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem;
  }

  .upload-section,
  .preview-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
  }

  .instagram-icon {
    font-size: 4rem;
    background: linear-gradient(
      45deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  h3 {
    margin: 0;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .subtitle {
    margin: 0;
    color: var(--text-secondary);
    text-align: center;
    max-width: 400px;
  }

  .upload-button,
  .share-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    min-width: 250px;
  }

  .upload-button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
  }

  .upload-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
  }

  .upload-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .share-button {
    background: linear-gradient(
      45deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
    color: white;
  }

  .share-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(220, 39, 67, 0.4);
  }

  .share-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .info-box {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 8px;
    color: #3b82f6;
    max-width: 400px;
    text-align: center;
  }

  .info-box p {
    margin: 0;
    font-size: 0.9rem;
  }

  .preview-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }

  .reset-button {
    padding: 0.5rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .reset-button:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-primary);
  }

  .media-preview {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    width: 100%;
  }

  .media-item {
    position: relative;
  }

  .media-thumbnail {
    position: relative;
    aspect-ratio: 1;
    border-radius: 8px;
    overflow: hidden;
    background: rgba(0, 0, 0, 0.2);
  }

  .media-thumbnail video,
  .media-thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .media-label {
    position: absolute;
    bottom: 0.5rem;
    left: 0.5rem;
    padding: 0.25rem 0.5rem;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 4px;
  }

  .caption-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
  }

  .caption-section label {
    font-weight: 600;
    color: var(--text-primary);
  }

  .caption-section textarea {
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text-primary);
    font-family: inherit;
    font-size: 1rem;
    resize: vertical;
  }

  .caption-section textarea:focus {
    outline: none;
    border-color: rgba(59, 130, 246, 0.5);
    background: rgba(255, 255, 255, 0.08);
  }

  .char-count {
    text-align: right;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin: 0;
  }

  .desktop-note {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-secondary);
    font-size: 0.9rem;
    text-align: center;
    margin: 0;
  }

  @media (max-width: 640px) {
    .instagram-share {
      padding: 1rem;
    }

    .media-preview {
      grid-template-columns: repeat(3, 1fr);
    }
  }
</style>
