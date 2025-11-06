<!--
  Instagram Post Progress Component

  Shows real-time progress during Instagram carousel posting.
  Displays upload progress, status messages, and success/error states.
-->
<script lang="ts">
  import type { InstagramPostStatus } from "../domain";

  let {
    status,
    onCancel,
    onRetry,
    onClose,
  }: {
    status: InstagramPostStatus;
    onCancel?: () => void;
    onRetry?: () => void;
    onClose?: () => void;
  } = $props();

  // Derived display states
  let isProcessing = $derived(
    status.status === "uploading" ||
      status.status === "processing" ||
      status.status === "publishing"
  );
  let isComplete = $derived(status.status === "completed");
  let isFailed = $derived(status.status === "failed");

  // Status icon and color
  let statusIcon = $derived(() => {
    switch (status.status) {
      case "uploading":
        return "fa-cloud-upload-alt";
      case "processing":
        return "fa-cog fa-spin";
      case "publishing":
        return "fa-paper-plane";
      case "completed":
        return "fa-check-circle";
      case "failed":
        return "fa-exclamation-circle";
      default:
        return "fa-question-circle";
    }
  });

  let statusColor = $derived(() => {
    switch (status.status) {
      case "completed":
        return "#10b981";
      case "failed":
        return "#ef4444";
      default:
        return "#3b82f6";
    }
  });

  function handleViewPost() {
    if (status.postUrl) {
      window.open(status.postUrl, "_blank", "noopener,noreferrer");
    }
  }
</script>

<div class="progress-container" style="--status-color: {statusColor()}">
  <!-- Header -->
  <div class="progress-header">
    <div class="status-icon" class:spinning={isProcessing}>
      <i class="fas {statusIcon()}"></i>
    </div>
    <h3 class="status-title">
      {#if isProcessing}
        Posting to Instagram...
      {:else if isComplete}
        Successfully Posted!
      {:else if isFailed}
        Post Failed
      {/if}
    </h3>
  </div>

  <!-- Progress Bar -->
  {#if isProcessing}
    <div class="progress-bar-container">
      <div
        class="progress-bar-fill"
        style="width: {status.progress}%"
      ></div>
    </div>
    <p class="progress-percentage">{Math.round(status.progress)}%</p>
  {/if}

  <!-- Status Message -->
  <p class="status-message">{status.message}</p>

  <!-- Error Details -->
  {#if isFailed && status.error}
    <div class="error-details">
      <div class="error-header">
        <i class="fas fa-bug"></i>
        <span>Error Details</span>
      </div>
      <p class="error-code">{status.error.code}</p>
      <p class="error-message">{status.error.message}</p>
    </div>
  {/if}

  <!-- Success Actions -->
  {#if isComplete && status.postUrl}
    <div class="success-actions">
      <button class="view-post-button" onclick={handleViewPost}>
        <i class="fab fa-instagram"></i>
        View on Instagram
      </button>
      {#if onClose}
        <button class="close-button" onclick={onClose}>
          <i class="fas fa-times"></i>
          Close
        </button>
      {/if}
    </div>
  {/if}

  <!-- Error Actions */}
  {#if isFailed}
    <div class="error-actions">
      {#if onRetry}
        <button class="retry-button" onclick={onRetry}>
          <i class="fas fa-redo"></i>
          Try Again
        </button>
      {/if}
      {#if onClose}
        <button class="cancel-button" onclick={onClose}>
          <i class="fas fa-times"></i>
          Close
        </button>
      {/if}
    </div>
  {/if}

  <!-- Cancel Button (during processing) -->
  {#if isProcessing && onCancel}
    <div class="processing-actions">
      <button class="cancel-button" onclick={onCancel}>
        <i class="fas fa-stop"></i>
        Cancel
      </button>
    </div>
  {/if}
</div>

<style>
  .progress-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
  }

  /* Header */
  .progress-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .status-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--status-color, #3b82f6) 0%, transparent 70%);
    border: 3px solid var(--status-color, #3b82f6);
  }

  .status-icon i {
    font-size: 28px;
    color: var(--status-color, #3b82f6);
  }

  .status-icon.spinning {
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%,
    100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.8;
      transform: scale(1.05);
    }
  }

  .status-title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    text-align: center;
  }

  /* Progress Bar */
  .progress-bar-container {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
  }

  .progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--status-color, #3b82f6), var(--status-color, #2563eb));
    border-radius: 4px;
    transition: width 0.3s ease;
  }

  .progress-percentage {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--status-color, #3b82f6);
    text-align: center;
  }

  /* Status Message */
  .status-message {
    margin: 0;
    font-size: 1rem;
    color: var(--text-secondary);
    text-align: center;
    line-height: 1.5;
  }

  /* Error Details */
  .error-details {
    padding: 1rem;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
  }

  .error-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #ef4444;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .error-code {
    margin: 0 0 0.5rem 0;
    font-size: 0.85rem;
    font-weight: 600;
    font-family: monospace;
    color: rgba(255, 255, 255, 0.7);
  }

  .error-message {
    margin: 0;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.4;
  }

  /* Action Buttons */
  .success-actions,
  .error-actions,
  .processing-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .view-post-button {
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

  .view-post-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(240, 148, 51, 0.4);
  }

  .retry-button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
  }

  .retry-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
  }

  .close-button,
  .cancel-button {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-secondary);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .close-button:hover,
  .cancel-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
  }

  /* Mobile Responsive */
  @media (max-width: 640px) {
    .progress-container {
      padding: 1.5rem;
    }

    .status-title {
      font-size: 1.25rem;
    }

    .status-icon {
      width: 56px;
      height: 56px;
    }

    .status-icon i {
      font-size: 24px;
    }

    button {
      width: 100%;
      justify-content: center;
    }

    .success-actions,
    .error-actions,
    .processing-actions {
      flex-direction: column;
    }
  }

  /* Accessibility - Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .status-icon.spinning,
    .progress-bar-fill,
    button {
      animation: none;
      transition: none;
    }
  }
</style>
