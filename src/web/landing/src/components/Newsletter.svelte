<script lang="ts">
  let email = "";
  let isSubmitting = false;
  let submitStatus: 'success' | 'error' | null = null;
  let errorMessage = "";

  function validateEmail(email: string): boolean {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  async function handleSubmit() {
    if (!validateEmail(email)) {
      submitStatus = 'error';
      errorMessage = 'Please enter a valid email address.';
      return;
    }

    isSubmitting = true;
    submitStatus = null;

    try {
      // Simulate API call - replace with actual newsletter service
      await new Promise(resolve => setTimeout(resolve, 1000));

      // For now, just show success message
      submitStatus = 'success';
      email = "";

      // Reset success message after 5 seconds
      setTimeout(() => {
        submitStatus = null;
      }, 5000);

    } catch (error) {
      submitStatus = 'error';
      errorMessage = 'Something went wrong. Please try again.';
    } finally {
      isSubmitting = false;
    }
  }

  function clearStatus() {
    submitStatus = null;
    errorMessage = "";
  }
</script>

<div class="newsletter-container">
  <form on:submit|preventDefault={handleSubmit} class="newsletter-form">
    <h3>Stay in the Loop</h3>
    <p>Get updates on new releases, tutorials, and community events.</p>

    <div class="input-group">
      <div class="input-wrapper">
        <input
          type="email"
          bind:value={email}
          placeholder="Enter your email address"
          required
          disabled={isSubmitting}
          on:input={clearStatus}
          class:error={submitStatus === 'error'}
          class:success={submitStatus === 'success'}
          aria-describedby={submitStatus === 'error' ? 'email-error' : null}
        />
        <div class="input-glass-overlay" aria-hidden="true"></div>
      </div>

      <button
        type="submit"
        disabled={isSubmitting || !email.trim()}
        class="subscribe-btn"
        class:loading={isSubmitting}
        aria-label="Subscribe to newsletter"
      >
        <span class="button-content">
          {#if isSubmitting}
            <span class="loading-spinner" aria-hidden="true"></span>
            <span class="loading-text">Subscribing...</span>
          {:else}
            <span class="button-text">Subscribe</span>
            <span class="button-icon" aria-hidden="true">✉</span>
          {/if}
        </span>
        <div class="button-glass-overlay" aria-hidden="true"></div>
      </button>
    </div>

    {#if submitStatus === 'success'}
      <div class="status-message success" role="alert">
        ✅ Thanks for subscribing! Check your email for confirmation.
      </div>
    {/if}

    {#if submitStatus === 'error'}
      <div class="status-message error" role="alert" id="email-error">
        ❌ {errorMessage}
      </div>
    {/if}
  </form>
</div>

<style>
  .newsletter-container {
    width: 100%;
  }

  .newsletter-form {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .newsletter-form h3 {
    color: var(--text-color);
    margin: 0 0 var(--spacing-xs) 0;
    font-size: var(--font-size-lg);
  }

  .newsletter-form p {
    color: var(--text-secondary);
    margin: 0 0 var(--spacing-md) 0;
    font-size: var(--font-size-sm);
    line-height: 1.4;
  }

  .input-group {
    display: flex;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
    align-items: stretch;
  }

  .input-wrapper {
    position: relative;
    flex: 1;
    min-width: 200px;
  }

  .input-group input {
    width: 100%;
    padding: var(--spacing-md);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: white;
    font-size: var(--font-size-base);
    transition: all var(--transition-normal);
    box-shadow:
      0 4px 16px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .input-group input::placeholder {
    color: rgba(255, 255, 255, 0.6);
    transition: color var(--transition-fast);
  }

  .input-group input:focus {
    outline: none;
    border-color: var(--primary-color);
    background: rgba(255, 255, 255, 0.15);
    box-shadow:
      0 0 0 3px rgba(168, 28, 237, 0.2),
      0 8px 24px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .input-group input:focus::placeholder {
    color: rgba(255, 255, 255, 0.8);
  }

  .input-glass-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.05) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    border-radius: var(--border-radius);
    opacity: 0;
    transition: opacity var(--transition-fast);
    pointer-events: none;
  }

  .input-wrapper:hover .input-glass-overlay {
    opacity: 1;
  }

  .input-group input.error {
    border-color: #ff6b6b;
    box-shadow:
      0 0 0 3px rgba(255, 107, 107, 0.2),
      0 4px 16px rgba(255, 107, 107, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .input-group input.success {
    border-color: #4caf50;
    box-shadow:
      0 0 0 3px rgba(76, 175, 80, 0.2),
      0 4px 16px rgba(76, 175, 80, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .input-group input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .subscribe-btn {
    position: relative;
    padding: var(--spacing-md) var(--spacing-lg);
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-normal);
    white-space: nowrap;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 140px;
    overflow: hidden;
    box-shadow:
      0 4px 16px rgba(168, 28, 237, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    will-change: transform, box-shadow;
  }

  .button-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    position: relative;
    z-index: 1;
    transition: transform var(--transition-fast);
  }

  .button-icon {
    font-size: 1.1em;
    transition: transform var(--transition-fast);
  }

  .loading-text {
    font-size: var(--font-size-sm);
  }

  .subscribe-btn:hover:not(:disabled) {
    transform: translateY(-2px) scale(1.02);
    box-shadow:
      0 8px 24px rgba(168, 28, 237, 0.3),
      0 4px 12px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .subscribe-btn:hover:not(:disabled) .button-icon {
    transform: scale(1.1);
  }

  .subscribe-btn:active:not(:disabled) {
    transform: translateY(-1px) scale(1.01);
  }

  .subscribe-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .subscribe-btn.loading {
    pointer-events: none;
  }

  .subscribe-btn.loading .button-content {
    transform: scale(0.95);
  }

  .button-glass-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.05) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    opacity: 0;
    transition: opacity var(--transition-fast);
  }

  .subscribe-btn:hover:not(:disabled) .button-glass-overlay {
    opacity: 1;
  }

  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .status-message {
    padding: var(--spacing-sm);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-sm);
    font-weight: 500;
    margin-top: var(--spacing-sm);
  }

  /* Enhanced status messages with glassmorphism */
  .status-message.success {
    background: rgba(76, 175, 80, 0.15);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    color: #4caf50;
    border: 1px solid rgba(76, 175, 80, 0.3);
    box-shadow: 0 4px 16px rgba(76, 175, 80, 0.1);
  }

  .status-message.error {
    background: rgba(244, 67, 54, 0.15);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    color: #f44336;
    border: 1px solid rgba(244, 67, 54, 0.3);
    box-shadow: 0 4px 16px rgba(244, 67, 54, 0.1);
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .input-group input,
    .input-wrapper,
    .input-glass-overlay,
    .subscribe-btn,
    .button-content,
    .button-icon,
    .button-glass-overlay {
      transition: none;
      animation: none;
    }

    .subscribe-btn:hover:not(:disabled) {
      transform: none;
    }

    .subscribe-btn:hover:not(:disabled) .button-icon {
      transform: none;
    }

    .loading-spinner {
      animation: none;
      border-top-color: rgba(255, 255, 255, 0.5);
    }
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .input-group {
      flex-direction: column;
      gap: var(--spacing-md);
    }

    .input-wrapper {
      min-width: 100%;
    }

    .input-group input {
      min-width: 100%;
      padding: var(--spacing-md) var(--spacing-sm);
      font-size: var(--font-size-sm);
    }

    .subscribe-btn {
      width: 100%;
      min-width: 100%;
      padding: var(--spacing-md);
      font-size: var(--font-size-sm);
    }

    .button-content {
      gap: var(--spacing-xs);
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .input-group input {
      border: 2px solid white;
      background: rgba(0, 0, 0, 0.8);
    }

    .subscribe-btn {
      border: 2px solid white;
      background: var(--primary-color);
    }

    .status-message.success {
      border: 2px solid #4caf50;
      background: rgba(76, 175, 80, 0.3);
    }

    .status-message.error {
      border: 2px solid #f44336;
      background: rgba(244, 67, 54, 0.3);
    }
  }
</style>