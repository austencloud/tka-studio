<!--
  Instagram Carousel Composer Component

  Complete UI for composing Instagram carousel posts.
  Features:
  - Video file selection
  - Media preview (video, image, GIF)
  - Drag-and-drop reordering
  - Caption editor with character count
  - Hashtag input
  - Post to Instagram button
-->
<script lang="ts">
  import { onMount } from "svelte";
  import { authStore } from "$shared/auth";
  import { resolve, TYPES } from "$shared";
  import type {
    IInstagramAuthService,
    IInstagramGraphApiService,
    IMediaBundlerService,
  } from "../services/contracts";
  import type {
    InstagramToken,
    InstagramMediaItem,
    InstagramCarouselPost,
    InstagramPostStatus,
  } from "../domain";
  import {
    INSTAGRAM_MEDIA_CONSTRAINTS,
    INSTAGRAM_PERMISSIONS,
  } from "../domain";
  import type { SequenceData, ShareOptions } from "$shared";
  import { InstagramPostProgress } from "./";

  let {
    currentSequence,
    shareOptions,
    onPostSuccess,
  }: {
    currentSequence: SequenceData | null;
    shareOptions: ShareOptions;
    onPostSuccess?: (postUrl: string) => void;
  } = $props();

  // Services
  let instagramAuthService: IInstagramAuthService;
  let instagramGraphApiService: IInstagramGraphApiService;
  let mediaBundlerService: IMediaBundlerService;

  // State
  let instagramToken = $state<InstagramToken | null>(null);
  let isLoadingToken = $state(true);
  let videoFile = $state<File | null>(null);
  let mediaItems = $state<InstagramMediaItem[]>([]);
  let caption = $state("");
  let hashtags = $state<string[]>([]);
  let hashtagInput = $state("");
  let isBundling = $state(false);
  let isPosting = $state(false);
  let postStatus = $state<InstagramPostStatus | null>(null);
  let draggedIndex = $state<number | null>(null);
  let layout = $state<"video-first" | "sequence-first">("video-first");

  // Video file input ref
  let videoInputRef: HTMLInputElement;

  onMount(async () => {
    try {
      // Resolve services
      instagramAuthService = resolve<IInstagramAuthService>(
        TYPES.IInstagramAuthService
      );
      instagramGraphApiService = resolve<IInstagramGraphApiService>(
        TYPES.IInstagramGraphApiService
      );
      mediaBundlerService = resolve<IMediaBundlerService>(
        TYPES.IMediaBundlerService
      );

      // Load Instagram token
      if (authStore.user) {
        instagramToken = await instagramAuthService.getToken(
          authStore.user.uid
        );
      }
    } catch (error) {
      console.error("Failed to initialize Instagram services:", error);
    } finally {
      isLoadingToken = false;
    }
  });

  // Computed states
  let isConnected = $derived(instagramToken !== null);
  let canPost = $derived(
    isConnected &&
      mediaItems.length >= 2 &&
      caption.length <= INSTAGRAM_MEDIA_CONSTRAINTS.CAPTION_MAX_LENGTH &&
      hashtags.length <= INSTAGRAM_MEDIA_CONSTRAINTS.HASHTAG_MAX_COUNT &&
      !isPosting
  );

  let captionCharCount = $derived(caption.length);
  let captionCharLimit = $derived(
    INSTAGRAM_MEDIA_CONSTRAINTS.CAPTION_MAX_LENGTH
  );

  // Handle video file selection
  async function handleVideoSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file) return;

    // Validate file type
    if (!file.type.startsWith("video/")) {
      alert("Please select a valid video file");
      return;
    }

    videoFile = file;
    await bundleMedia();
  }

  // Bundle media (video + sequence image + GIF)
  async function bundleMedia() {
    if (!currentSequence || !videoFile || !mediaBundlerService) return;

    isBundling = true;

    try {
      const bundle = await mediaBundlerService.createCarouselBundle(
        currentSequence,
        videoFile,
        shareOptions,
        layout
      );

      mediaItems = bundle;
    } catch (error: any) {
      console.error("Failed to bundle media:", error);
      alert(`Failed to create carousel: ${error.message}`);
    } finally {
      isBundling = false;
    }
  }

  // Handle drag start
  function handleDragStart(event: DragEvent, index: number) {
    draggedIndex = index;
    if (event.dataTransfer) {
      event.dataTransfer.effectAllowed = "move";
    }
  }

  // Handle drag over
  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = "move";
    }
  }

  // Handle drop
  function handleDrop(event: DragEvent, dropIndex: number) {
    event.preventDefault();

    if (draggedIndex === null || draggedIndex === dropIndex) {
      draggedIndex = null;
      return;
    }

    // Reorder items
    mediaItems = mediaBundlerService.reorderMediaItems(
      mediaItems,
      draggedIndex,
      dropIndex
    );

    draggedIndex = null;
  }

  // Remove media item
  function handleRemoveItem(index: number) {
    mediaItems = mediaBundlerService.removeMediaItem(mediaItems, index);

    // If we removed all items, reset video file
    if (mediaItems.length === 0) {
      videoFile = null;
      if (videoInputRef) {
        videoInputRef.value = "";
      }
    }
  }

  // Add hashtag
  function handleAddHashtag() {
    const tag = hashtagInput.trim().replace(/^#/, "");
    if (!tag) return;

    if (hashtags.length >= INSTAGRAM_MEDIA_CONSTRAINTS.HASHTAG_MAX_COUNT) {
      alert(
        `Maximum ${INSTAGRAM_MEDIA_CONSTRAINTS.HASHTAG_MAX_COUNT} hashtags allowed`
      );
      return;
    }

    if (!hashtags.includes(tag)) {
      hashtags = [...hashtags, tag];
    }

    hashtagInput = "";
  }

  // Remove hashtag
  function handleRemoveHashtag(tag: string) {
    hashtags = hashtags.filter((t) => t !== tag);
  }

  // Handle hashtag input keypress
  function handleHashtagKeypress(event: KeyboardEvent) {
    if (event.key === "Enter") {
      event.preventDefault();
      handleAddHashtag();
    }
  }

  // Post to Instagram
  async function handlePost() {
    if (!canPost || !currentSequence || !instagramToken) return;

    isPosting = true;

    try {
      // Create carousel post
      const carouselPost: InstagramCarouselPost = {
        items: mediaItems,
        caption: caption.trim(),
        hashtags,
        shareToFacebook: false,
        sequenceId: currentSequence.id,
      };

      // Post with progress tracking
      const result = await instagramGraphApiService.postCarousel(
        instagramToken,
        carouselPost,
        (status) => {
          postStatus = status;
        }
      );

      // Success!
      onPostSuccess?.(result.permalink);
    } catch (error: any) {
      console.error("Failed to post to Instagram:", error);
    } finally {
      isPosting = false;
    }
  }

  // Connect Instagram
  async function handleConnectInstagram() {
    try {
      await instagramAuthService.initiateOAuthFlow([
        INSTAGRAM_PERMISSIONS.CONTENT_PUBLISH,
      ]);
    } catch (error: any) {
      console.error("Failed to initiate Instagram OAuth:", error);
      alert(`Failed to connect Instagram: ${error.message}`);
    }
  }

  // Change layout
  function toggleLayout() {
    layout = layout === "video-first" ? "sequence-first" : "video-first";
    if (videoFile && currentSequence) {
      bundleMedia();
    }
  }
</script>

<div class="carousel-composer">
  {#if isLoadingToken}
    <!-- Loading state -->
    <div class="loading-state">
      <i class="fas fa-spinner fa-spin"></i>
      <p>Loading Instagram connection...</p>
    </div>
  {:else if !isConnected}
    <!-- Not connected state -->
    <div class="not-connected-state">
      <div class="instagram-logo">
        <i class="fab fa-instagram"></i>
      </div>
      <h3>Connect Instagram to Post</h3>
      <p>
        Connect your Instagram Business account to post carousels directly from
        the app.
      </p>
      <button class="connect-button" onclick={handleConnectInstagram}>
        <i class="fab fa-instagram"></i>
        Connect Instagram
      </button>
    </div>
  {:else if postStatus?.status === "completed" || postStatus?.status === "failed"}
    <!-- Post progress/result -->
    <InstagramPostProgress
      status={postStatus}
      onRetry={() => {
        postStatus = null;
        handlePost();
      }}
      onClose={() => (postStatus = null)}
    />
  {:else}
    <!-- Composer UI -->
    <div class="composer-content">
      <!-- Header -->
      <div class="composer-header">
        <div class="instagram-icon">
          <i class="fab fa-instagram"></i>
        </div>
        <div class="header-info">
          <h3>Post to Instagram</h3>
          <p>@{instagramToken.username}</p>
        </div>
      </div>

      <!-- Video Selection -->
      <div class="section">
        <h4 class="section-title">
          <i class="fas fa-video"></i>
          Select Video
        </h4>
        <input
          bind:this={videoInputRef}
          type="file"
          accept="video/*"
          onchange={handleVideoSelect}
          class="video-input"
          id="video-input"
        />
        <label for="video-input" class="video-select-button">
          {#if videoFile}
            <i class="fas fa-check-circle"></i>
            {videoFile.name}
          {:else}
            <i class="fas fa-cloud-upload-alt"></i>
            Choose Video from Device
          {/if}
        </label>
        {#if videoFile}
          <p class="file-info">
            {(videoFile.size / (1024 * 1024)).toFixed(2)} MB
          </p>
        {/if}
      </div>

      {#if isBundling}
        <!-- Bundling state -->
        <div class="bundling-state">
          <i class="fas fa-spinner fa-spin"></i>
          <p>Creating carousel...</p>
        </div>
      {:else if mediaItems.length > 0}
        <!-- Media Preview & Reorder -->
        <div class="section">
          <div class="section-header">
            <h4 class="section-title">
              <i class="fas fa-images"></i>
              Carousel Items ({mediaItems.length})
            </h4>
            <button class="layout-toggle" onclick={toggleLayout}>
              <i class="fas fa-random"></i>
              {layout === "video-first" ? "Video First" : "Sequence First"}
            </button>
          </div>

          <div class="media-grid">
            {#each mediaItems as item, index}
              <div
                class="media-item"
                draggable="true"
                ondragstart={(e) => handleDragStart(e, index)}
                ondragover={handleDragOver}
                ondrop={(e) => handleDrop(e, index)}
                class:dragging={draggedIndex === index}
              >
                <div class="item-number">{index + 1}</div>
                <div class="item-preview">
                  {#if item.type === "VIDEO"}
                    <video
                      src={item.previewUrl}
                      class="preview-media"
                      muted
                    ></video>
                    <div class="media-type-badge">
                      <i class="fas fa-video"></i>
                      Video
                    </div>
                  {:else}
                    <img
                      src={item.previewUrl}
                      alt="Media item {index + 1}"
                      class="preview-media"
                    />
                    <div class="media-type-badge">
                      <i class="fas fa-image"></i>
                      {item.mimeType.includes("gif") ? "GIF" : "Image"}
                    </div>
                  {/if}
                </div>
                <button
                  class="remove-item-button"
                  onclick={() => handleRemoveItem(index)}
                  title="Remove item"
                >
                  <i class="fas fa-times"></i>
                </button>
                <div class="drag-handle">
                  <i class="fas fa-grip-vertical"></i>
                </div>
              </div>
            {/each}
          </div>
          <p class="hint">
            <i class="fas fa-hand-rock"></i>
            Drag items to reorder
          </p>
        </div>

        <!-- Caption Editor -->
        <div class="section">
          <h4 class="section-title">
            <i class="fas fa-edit"></i>
            Caption
          </h4>
          <textarea
            bind:value={caption}
            placeholder="Write a caption for your post..."
            class="caption-textarea"
            maxlength={captionCharLimit}
            rows="4"
          ></textarea>
          <div class="caption-footer">
            <span
              class="char-count"
              class:warning={captionCharCount > captionCharLimit * 0.9}
              class:error={captionCharCount >= captionCharLimit}
            >
              {captionCharCount} / {captionCharLimit}
            </span>
          </div>
        </div>

        <!-- Hashtags -->
        <div class="section">
          <h4 class="section-title">
            <i class="fas fa-hashtag"></i>
            Hashtags ({hashtags.length}/{INSTAGRAM_MEDIA_CONSTRAINTS.HASHTAG_MAX_COUNT})
          </h4>
          <div class="hashtag-input-row">
            <input
              bind:value={hashtagInput}
              onkeypress={handleHashtagKeypress}
              placeholder="Add hashtag (without #)"
              class="hashtag-input"
            />
            <button class="add-hashtag-button" onclick={handleAddHashtag}>
              <i class="fas fa-plus"></i>
              Add
            </button>
          </div>
          {#if hashtags.length > 0}
            <div class="hashtag-list">
              {#each hashtags as tag}
                <div class="hashtag-chip">
                  <span>#{tag}</span>
                  <button
                    class="remove-hashtag"
                    onclick={() => handleRemoveHashtag(tag)}
                  >
                    <i class="fas fa-times"></i>
                  </button>
                </div>
              {/each}
            </div>
          {/if}
        </div>

        <!-- Post Button -->
        <div class="post-section">
          {#if isPosting && postStatus}
            <InstagramPostProgress status={postStatus} />
          {:else}
            <button
              class="post-button"
              disabled={!canPost}
              onclick={handlePost}
            >
              <i class="fab fa-instagram"></i>
              Post to Instagram
            </button>
            {#if !canPost && mediaItems.length >= 2}
              <p class="post-hint">
                {#if caption.length > captionCharLimit}
                  Caption is too long
                {:else if hashtags.length > INSTAGRAM_MEDIA_CONSTRAINTS.HASHTAG_MAX_COUNT}
                  Too many hashtags
                {:else}
                  Check your post details
                {/if}
              </p>
            {/if}
          {/if}
        </div>
      {:else if currentSequence}
        <!-- Waiting for video -->
        <div class="waiting-state">
          <i class="fas fa-video"></i>
          <p>Select a video to create your carousel</p>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .carousel-composer {
    width: 100%;
    height: 100%;
    overflow-y: auto;
  }

  /* Loading State */
  .loading-state,
  .bundling-state,
  .waiting-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 3rem 1.5rem;
    color: var(--text-secondary);
  }

  .loading-state i,
  .bundling-state i {
    font-size: 3rem;
    color: var(--accent-color);
  }

  .waiting-state i {
    font-size: 4rem;
    color: rgba(255, 255, 255, 0.2);
  }

  /* Not Connected State */
  .not-connected-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    padding: 3rem 1.5rem;
    text-align: center;
  }

  .instagram-logo {
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 20px;
    background: linear-gradient(
      45deg,
      rgba(240, 148, 51, 0.1) 0%,
      rgba(230, 104, 60, 0.1) 25%,
      rgba(220, 39, 67, 0.1) 50%,
      rgba(204, 35, 102, 0.1) 75%,
      rgba(188, 24, 136, 0.1) 100%
    );
    border: 2px solid rgba(240, 148, 51, 0.3);
  }

  .instagram-logo i {
    font-size: 40px;
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

  .not-connected-state h3 {
    margin: 0;
    font-size: 1.5rem;
    color: var(--text-primary);
  }

  .not-connected-state p {
    margin: 0;
    color: var(--text-secondary);
    max-width: 400px;
  }

  .connect-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: linear-gradient(
      45deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .connect-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(240, 148, 51, 0.4);
  }

  /* Composer Content */
  .composer-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem;
  }

  /* Header */
  .composer-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }

  .instagram-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: linear-gradient(
      45deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
  }

  .instagram-icon i {
    font-size: 24px;
    color: white;
  }

  .header-info h3 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text-primary);
  }

  .header-info p {
    margin: 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
  }

  /* Sections */
  .section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .section-title i {
    color: var(--accent-color);
  }

  /* Video Selection */
  .video-input {
    display: none;
  }

  .video-select-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 2px dashed rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: var(--text-primary);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .video-select-button:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .file-info {
    margin: 0;
    font-size: 0.85rem;
    color: var(--text-secondary);
    text-align: center;
  }

  /* Layout Toggle */
  .layout-toggle {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    color: var(--text-secondary);
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .layout-toggle:hover {
    background: rgba(255, 255, 255, 0.08);
    color: var(--text-primary);
  }

  /* Media Grid */
  .media-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }

  .media-item {
    position: relative;
    aspect-ratio: 1;
    border-radius: 8px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.03);
    border: 2px solid rgba(255, 255, 255, 0.1);
    cursor: grab;
    transition: all 0.2s ease;
  }

  .media-item:hover {
    border-color: rgba(255, 255, 255, 0.3);
    transform: scale(1.02);
  }

  .media-item.dragging {
    opacity: 0.5;
    cursor: grabbing;
  }

  .item-number {
    position: absolute;
    top: 8px;
    left: 8px;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    font-size: 0.85rem;
    font-weight: 700;
    border-radius: 50%;
    z-index: 2;
  }

  .item-preview {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .preview-media {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .media-type-badge {
    position: absolute;
    bottom: 8px;
    left: 8px;
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 4px;
    z-index: 2;
  }

  .remove-item-button {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(239, 68, 68, 0.9);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s ease;
    z-index: 3;
  }

  .media-item:hover .remove-item-button {
    opacity: 1;
  }

  .drag-handle {
    position: absolute;
    bottom: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.6);
    z-index: 2;
  }

  .hint {
    margin: 0;
    font-size: 0.85rem;
    color: var(--text-secondary);
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  /* Caption Editor */
  .caption-textarea {
    width: 100%;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 1rem;
    font-family: inherit;
    resize: vertical;
    min-height: 100px;
  }

  .caption-textarea:focus {
    outline: none;
    border-color: rgba(59, 130, 246, 0.5);
    background: rgba(255, 255, 255, 0.08);
  }

  .caption-footer {
    display: flex;
    justify-content: flex-end;
  }

  .char-count {
    font-size: 0.85rem;
    color: var(--text-secondary);
  }

  .char-count.warning {
    color: #f59e0b;
  }

  .char-count.error {
    color: #ef4444;
  }

  /* Hashtags */
  .hashtag-input-row {
    display: flex;
    gap: 0.5rem;
  }

  .hashtag-input {
    flex: 1;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 1rem;
  }

  .hashtag-input:focus {
    outline: none;
    border-color: rgba(59, 130, 246, 0.5);
  }

  .add-hashtag-button {
    padding: 0.75rem 1.5rem;
    background: rgba(59, 130, 246, 0.2);
    color: #3b82f6;
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .add-hashtag-button:hover {
    background: rgba(59, 130, 246, 0.3);
  }

  .hashtag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .hashtag-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: rgba(59, 130, 246, 0.1);
    color: #3b82f6;
    border-radius: 20px;
    font-size: 0.9rem;
  }

  .remove-hashtag {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 0.7rem;
  }

  /* Post Section */
  .post-section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
  }

  .post-button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1rem;
    background: linear-gradient(
      45deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .post-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(240, 148, 51, 0.4);
  }

  .post-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  .post-hint {
    margin: 0;
    font-size: 0.85rem;
    color: var(--text-secondary);
    text-align: center;
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .composer-content {
      padding: 1rem;
    }

    .media-grid {
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    }
  }
</style>
