<!--
ModalActions.svelte - Premium modal action buttons
Provides consistent, beautiful button layouts for modal actions
-->
<script lang="ts">
  let {
    onCancel,
    onConfirm,
    cancelLabel = "Cancel",
    confirmLabel = "Confirm",
    confirmDisabled = false,
    confirmVariant = "primary" as "primary" | "success" | "danger",
  } = $props<{
    onCancel: () => void;
    onConfirm: () => void;
    cancelLabel?: string;
    confirmLabel?: string;
    confirmDisabled?: boolean;
    confirmVariant?: "primary" | "success" | "danger";
  }>();
</script>

<div class="modal-actions">
  <button class="action-button cancel-button" onclick={onCancel} type="button">
    {cancelLabel}
  </button>
  <button
    class="action-button confirm-button {confirmVariant}"
    onclick={onConfirm}
    disabled={confirmDisabled}
    type="button"
  >
    {confirmLabel}
  </button>
</div>

<style>
  .modal-actions {
    display: flex;
    gap: 12px;
    margin-top: 8px;
  }

  .action-button {
    flex: 1;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    border: none;
    position: relative;
    overflow: hidden;
    letter-spacing: 0.01em;
  }

  .action-button::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(
      circle at center,
      rgba(255, 255, 255, 0.2) 0%,
      transparent 70%
    );
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .action-button:hover::before {
    opacity: 1;
  }

  .cancel-button {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1),
      rgba(255, 255, 255, 0.05)
    );
    color: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .cancel-button:hover {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.15),
      rgba(255, 255, 255, 0.08)
    );
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .cancel-button:active {
    transform: translateY(0);
  }

  .confirm-button {
    color: white;
    font-weight: 700;
  }

  .confirm-button.primary {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  }

  .confirm-button.primary:hover:not(:disabled) {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    transform: translateY(-2px);
    box-shadow:
      0 6px 20px rgba(59, 130, 246, 0.4),
      0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  }

  .confirm-button.success {
    background: linear-gradient(135deg, #10b981, #059669);
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  }

  .confirm-button.success:hover:not(:disabled) {
    background: linear-gradient(135deg, #059669, #047857);
    transform: translateY(-2px);
    box-shadow:
      0 6px 20px rgba(16, 185, 129, 0.4),
      0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  }

  .confirm-button.danger {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
  }

  .confirm-button.danger:hover:not(:disabled) {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    transform: translateY(-2px);
    box-shadow:
      0 6px 20px rgba(239, 68, 68, 0.4),
      0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  }

  .confirm-button:active:not(:disabled) {
    transform: translateY(0);
  }

  .confirm-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    filter: saturate(0.5);
  }

  @media (max-width: 640px) {
    .action-button {
      padding: 11px 16px;
      font-size: 14px;
    }
  }
</style>
