<!-- SpinnerIcon.svelte - Loading spinner icon -->
<svg
  class="spinner"
  width="20"
  height="20"
  viewBox="0 0 24 24"
  {...$$restProps}
>
  <circle
    cx="12"
    cy="12"
    r="10"
    stroke="currentColor"
    stroke-width="2"
    fill="none"
    opacity="0.25"
  />
  <path
    d="M12 2a10 10 0 0 1 10 10"
    stroke="currentColor"
    stroke-width="2"
    fill="none"
  />
</svg>

<style>
  .spinner {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
