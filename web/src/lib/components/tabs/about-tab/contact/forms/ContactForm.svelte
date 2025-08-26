<!-- ContactForm.svelte - Contact form with validation and submission -->
<script lang="ts">
  import SpinnerIcon from "../icons/SpinnerIcon.svelte";
  import CheckIcon from "../icons/CheckIcon.svelte";
  import ErrorIcon from "../icons/ErrorIcon.svelte";

  let formData = $state({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  let isSubmitting = $state(false);
  let submitStatus = $state<"idle" | "success" | "error">("idle");

  function validateEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();

    if (
      !formData.name.trim() ||
      !formData.email.trim() ||
      !formData.message.trim()
    ) {
      submitStatus = "error";
      return;
    }

    if (!validateEmail(formData.email)) {
      submitStatus = "error";
      return;
    }

    isSubmitting = true;
    submitStatus = "idle";

    try {
      // Simulate form submission (replace with actual API call)
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Reset form on success
      formData = { name: "", email: "", subject: "", message: "" };
      submitStatus = "success";
    } catch (error) {
      submitStatus = "error";
    } finally {
      isSubmitting = false;
    }
  }
</script>

<div class="contact-form-container">
  <h2>Send a Message</h2>
  <p class="form-description">
    Fill out the form below and I'll get back to you as soon as possible.
  </p>

  <form onsubmit={handleSubmit} class="contact-form">
    <div class="form-row">
      <div class="form-group">
        <label for="name">Name *</label>
        <input
          type="text"
          id="name"
          bind:value={formData.name}
          required
          placeholder="Your name"
          class="form-input"
        />
      </div>

      <div class="form-group">
        <label for="email">Email *</label>
        <input
          type="email"
          id="email"
          bind:value={formData.email}
          required
          placeholder="your.email@example.com"
          class="form-input"
        />
      </div>
    </div>

    <div class="form-group">
      <label for="subject">Subject</label>
      <input
        type="text"
        id="subject"
        bind:value={formData.subject}
        placeholder="What's this about?"
        class="form-input"
      />
    </div>

    <div class="form-group">
      <label for="message">Message *</label>
      <textarea
        id="message"
        bind:value={formData.message}
        required
        placeholder="Tell me about your question, suggestion, or how you'd like to contribute..."
        rows="6"
        class="form-textarea"
      ></textarea>
    </div>

    <button
      type="submit"
      disabled={isSubmitting}
      class="submit-button"
      class:submitting={isSubmitting}
    >
      {#if isSubmitting}
        <SpinnerIcon />
        Sending...
      {:else}
        Send Message
      {/if}
    </button>

    {#if submitStatus === "success"}
      <div class="status-message success">
        <CheckIcon />
        Thank you! Your message has been sent successfully.
      </div>
    {:else if submitStatus === "error"}
      <div class="status-message error">
        <ErrorIcon />
        Please check your information and try again.
      </div>
    {/if}
  </form>
</div>

<style>
  .contact-form-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-2xl);
  }

  .contact-form-container h2 {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--spacing-sm);
  }

  .form-description {
    color: var(--text-secondary);
    margin-bottom: var(--spacing-xl);
    line-height: 1.5;
  }

  .contact-form {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-md);
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .form-group label {
    font-weight: 500;
    color: var(--text-color);
    font-size: var(--font-size-sm);
  }

  .form-input,
  .form-textarea {
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    color: var(--text-color);
    font-size: var(--font-size-base);
    transition: all 0.2s ease;
  }

  .form-input:focus,
  .form-textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }

  .form-textarea {
    resize: vertical;
    min-height: 120px;
    font-family: inherit;
  }

  .submit-button {
    padding: var(--spacing-md) var(--spacing-xl);
    background: linear-gradient(
      135deg,
      var(--primary-color),
      var(--secondary-color)
    );
    border: none;
    border-radius: var(--border-radius);
    color: white;
    font-weight: 600;
    font-size: var(--font-size-base);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
    align-self: flex-start;
  }

  .submit-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  .submit-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .status-message {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    border-radius: var(--border-radius);
    font-weight: 500;
  }

  .status-message.success {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: #22c55e;
  }

  .status-message.error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #ef4444;
  }

  @media (max-width: 768px) {
    .form-row {
      grid-template-columns: 1fr;
    }

    .contact-form-container {
      padding: var(--spacing-md);
    }

    .submit-button:hover {
      transform: none;
    }
  }
</style>
