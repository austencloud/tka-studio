<!--
VideoFeedPanel.svelte

Camera feed component for the Record tab.
Handles camera access using MediaDevices API with support for both mobile and desktop.
Features square aspect ratio for consistent layout and settings dialog for camera controls.
-->
<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import CameraSettingsDialog from "./CameraSettingsDialog.svelte";

  // Props
  const {
    onCameraReady = () => {},
    onCameraError = (error: Error) => {},
  }: {
    onCameraReady?: () => void;
    onCameraError?: (error: Error) => void;
  } = $props();

  // State
  let videoElement: HTMLVideoElement | null = $state(null);
  let stream: MediaStream | null = $state(null);
  let isLoading = $state(true);
  let error = $state<string | null>(null);
  let isCameraActive = $state(false);
  let availableCameras = $state<MediaDeviceInfo[]>([]);
  let selectedCameraId = $state<string | null>(null);
  let isMirrored = $state(true); // Default to mirrored for front-facing cameras
  let isSettingsOpen = $state(false); // Settings dialog state

  // Camera constraints - square aspect ratio for consistent layout
  function getCameraConstraints(deviceId?: string): MediaStreamConstraints {
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent
    );

    const videoConstraints: MediaTrackConstraints = {
      width: { ideal: 720 },  // Square aspect ratio
      height: { ideal: 720 }, // Square aspect ratio
      facingMode: isMobile ? "environment" : "user",
    };

    if (deviceId) {
      videoConstraints.deviceId = { exact: deviceId };
    }

    return {
      video: videoConstraints,
      audio: false,
    };
  }

  // Settings dialog handlers
  function openSettings() {
    isSettingsOpen = true;
  }

  function closeSettings() {
    isSettingsOpen = false;
  }

  function toggleMirror() {
    isMirrored = !isMirrored;
  }

  function handleCameraChange(deviceId: string) {
    switchCamera(deviceId);
  }

  async function getAvailableCameras() {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      availableCameras = devices.filter((device) => device.kind === "videoinput");
    } catch (err) {
      console.error("Failed to enumerate cameras:", err);
    }
  }

  async function startCamera(deviceId?: string) {
    try {
      console.log("📹 Starting camera...", { deviceId });
      isLoading = true;
      error = null;

      // Stop existing stream if any
      if (stream) {
        console.log("🛑 Stopping existing stream");
        stream.getTracks().forEach((track) => track.stop());
        stream = null;
      }

      // Request camera access
      const constraints = getCameraConstraints(deviceId);
      console.log("📹 Requesting camera with constraints:", constraints);
      stream = await navigator.mediaDevices.getUserMedia(constraints);
      console.log("✅ Got camera stream:", stream);

      // Attach stream to video element
      if (videoElement) {
        console.log("📹 Attaching stream to video element");
        videoElement.srcObject = stream;

        // Wait for video to be ready
        videoElement.onloadedmetadata = () => {
          console.log("✅ Video metadata loaded");
          videoElement?.play()
            .then(() => {
              console.log("✅ Video playing");
              isCameraActive = true;
              isLoading = false;
              onCameraReady();
            })
            .catch((playErr) => {
              console.error("❌ Failed to play video:", playErr);
              error = "Failed to play video: " + (playErr instanceof Error ? playErr.message : String(playErr));
              isLoading = false;
            });
        };
      } else {
        console.error("❌ No video element found");
        error = "Video element not ready";
        isLoading = false;
      }
    } catch (err) {
      console.error("❌ Failed to access camera:", err);
      const errorMessage =
        err instanceof Error
          ? err.message
          : "Failed to access camera. Please check permissions.";
      error = errorMessage;
      isLoading = false;
      onCameraError(
        err instanceof Error ? err : new Error(errorMessage)
      );
    }
  }

  async function switchCamera(deviceId: string) {
    selectedCameraId = deviceId;
    await startCamera(deviceId);
  }

  function stopCamera() {
    console.log("🛑 Stopping camera...");
    if (stream) {
      stream.getTracks().forEach((track) => {
        console.log("🛑 Stopping track:", track.label);
        track.stop();
      });
      stream = null;
    }

    if (videoElement) {
      videoElement.srcObject = null;
    }

    isCameraActive = false;
    console.log("✅ Camera stopped");
  }

  // Effect to attach stream when video element becomes available
  $effect(() => {
    if (videoElement && stream && !videoElement.srcObject) {
      console.log("📹 Attaching stream to newly mounted video element");
      videoElement.srcObject = stream;
      videoElement.play()
        .then(() => {
          console.log("✅ Video playing after effect attachment");
          isCameraActive = true;
        })
        .catch((err) => {
          console.error("❌ Failed to play video in effect:", err);
        });
    }
  });

  // Lifecycle
  onMount(async () => {
    console.log("📹 VideoFeedPanel mounted");
    // Check for camera support
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      error = "Camera access is not supported in this browser.";
      isLoading = false;
      return;
    }

    await getAvailableCameras();
    await startCamera();
  });

  onDestroy(() => {
    console.log("🗑️ VideoFeedPanel destroying");
    stopCamera();
  });
</script>

<div class="video-feed-panel">
  <div class="video-container">
    <!-- Video element - ALWAYS render so it's available for stream attachment -->
    <!-- svelte-ignore a11y_media_has_caption -->
    <video
      bind:this={videoElement}
      class="video-feed"
      class:active={isCameraActive}
      class:mirrored={isMirrored}
      autoplay
      playsinline
      muted
    ></video>

    <!-- Settings button - always visible when camera is active -->
    {#if isCameraActive}
      <button
        class="settings-button"
        onclick={openSettings}
        title="Camera settings"
      >
        <span class="settings-icon">⚙️</span>
      </button>
    {/if}

    <!-- Overlays for different states -->
    {#if isLoading}
      <div class="state-overlay loading-state">
        <div class="spinner"></div>
        <p>Accessing camera...</p>
      </div>
    {:else if error}
      <div class="state-overlay error-state">
        <div class="error-icon">📷</div>
        <p class="error-message">{error}</p>
        <button class="retry-button" onclick={() => startCamera()}>
          Try Again
        </button>
      </div>
    {:else if !isCameraActive}
      <div class="state-overlay inactive-overlay">
        <p>Camera initializing...</p>
      </div>
    {/if}
  </div>

  <!-- Camera Settings Dialog -->
  <CameraSettingsDialog
    isOpen={isSettingsOpen}
    {isMirrored}
    {availableCameras}
    {selectedCameraId}
    onClose={closeSettings}
    onMirrorToggle={toggleMirror}
    onCameraChange={handleCameraChange}
  />
</div>

<style>
  .video-feed-panel {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background: var(--surface-dark, #1a1a1a);
    border-radius: var(--border-radius-lg, 12px);
    overflow: hidden;
  }

  .video-container {
    position: relative;
    width: 100%;
    aspect-ratio: 1; /* Square aspect ratio for consistent layout */
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface-darker, #0a0a0a);
    border-radius: var(--border-radius-lg, 12px);
    overflow: hidden;
  }

  .video-feed {
    width: 100%;
    height: 100%;
    object-fit: cover; /* Cover to fill square container */
    background: #000;
    display: block;
    transition: transform 0.3s ease;
  }

  .video-feed.active {
    opacity: 1;
  }

  .video-feed.mirrored {
    transform: scaleX(-1);
  }

  .settings-button {
    position: absolute;
    top: var(--spacing-md, 16px);
    right: var(--spacing-md, 16px);
    width: 48px;
    height: 48px;
    background: var(--surface-glass, rgba(0, 0, 0, 0.6));
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-color, rgba(255, 255, 255, 0.2));
    border-radius: var(--border-radius-md, 8px);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    z-index: 10;
  }

  .settings-button:hover {
    background: var(--surface-glass-hover, rgba(0, 0, 0, 0.8));
    border-color: var(--primary, #3b82f6);
    transform: translateY(-2px);
  }

  .settings-button:active {
    transform: translateY(0);
  }

  .settings-icon {
    font-size: 24px;
  }

  .state-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    z-index: 1;
  }

  .state-overlay > * {
    pointer-events: auto;
  }

  .inactive-overlay {
    background: rgba(0, 0, 0, 0.7);
    color: white;
  }

  .loading-state,
  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-md, 16px);
    color: var(--foreground, #ffffff);
    padding: var(--spacing-xl, 32px);
    text-align: center;
  }

  .spinner {
    width: 48px;
    height: 48px;
    border: 4px solid var(--surface-light, #333);
    border-top-color: var(--primary, #3b82f6);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .error-icon {
    font-size: 64px;
    opacity: 0.5;
  }

  .error-message {
    max-width: 400px;
    line-height: 1.5;
    color: var(--error, #ef4444);
  }

  .retry-button {
    padding: var(--spacing-sm, 8px) var(--spacing-lg, 24px);
    background: var(--primary, #3b82f6);
    color: white;
    border: none;
    border-radius: var(--border-radius-md, 8px);
    cursor: pointer;
    font-size: var(--font-size-md, 16px);
    transition: all 0.2s ease;
  }

  .retry-button:hover {
    background: var(--primary-hover, #2563eb);
    transform: translateY(-2px);
  }

  .retry-button:active {
    transform: translateY(0);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .settings-button {
      width: 40px;
      height: 40px;
      top: var(--spacing-sm, 8px);
      right: var(--spacing-sm, 8px);
    }

    .settings-icon {
      font-size: 20px;
    }
  }
</style>
