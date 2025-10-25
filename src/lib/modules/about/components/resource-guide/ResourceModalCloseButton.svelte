<script lang="ts">
  interface Props {
    /** Callback when close button is clicked */
    onClose: () => void;
    /** Bind reference to the button element */
    buttonRef?: HTMLButtonElement;
  }

  let { onClose, buttonRef = $bindable() }: Props = $props();
</script>

<button
  bind:this={buttonRef}
  class="modal-close"
  onclick={onClose}
  aria-label="Close modal"
  type="button"
>
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M18 6L6 18M6 6L18 18"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</button>

<style>
  .modal-close {
    position: absolute;
    top: var(--spacing-md);
    right: var(--spacing-md);
    z-index: 10;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .modal-close:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: scale(1.1);
  }

  @media (prefers-reduced-motion: reduce) {
    .modal-close {
      transition: none;
    }

    .modal-close:hover {
      transform: none;
    }
  }
</style>
