<script lang="ts">
  import { onMount } from "svelte";

  let isVisible = $state(false);

  onMount(() => {
    isVisible = true;
  });

  // Contact form state
  let formData = $state({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  let isSubmitting = $state(false);
  let submitStatus = $state<"idle" | "success" | "error">("idle");

  // Form validation
  let formErrors = $derived.by(() => {
    const errors: Record<string, string> = {};

    if (!formData.name.trim()) {
      errors.name = "Name is required";
    }

    if (!formData.email.trim()) {
      errors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = "Please enter a valid email address";
    }

    if (!formData.subject.trim()) {
      errors.subject = "Subject is required";
    }

    if (!formData.message.trim()) {
      errors.message = "Message is required";
    }

    return errors;
  });

  let isFormValid = $derived(Object.keys(formErrors).length === 0);

  async function handleSubmit(event: Event) {
    event.preventDefault();

    if (!isFormValid || isSubmitting) return;

    isSubmitting = true;
    submitStatus = "idle";

    try {
      // Simulate form submission - replace with actual endpoint
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Reset form on success
      formData = {
        name: "",
        email: "",
        subject: "",
        message: "",
      };

      submitStatus = "success";
      console.log("📧 Contact form submitted:", formData);
    } catch (error) {
      console.error("Form submission error:", error);
      submitStatus = "error";
    } finally {
      isSubmitting = false;
    }
  }

  function updateField(field: keyof typeof formData, value: string) {
    formData[field] = value;
  }
</script>

<svelte:head>
  <title>Contact - The Kinetic Alphabet</title>
  <meta
    name="description"
    content="Get in touch with The Kinetic Alphabet team. We'd love to hear from you about collaborations, questions, or feedback."
  />
</svelte:head>

<main class="contact-container">
  <!-- Hero Section -->
  <section class="hero" class:visible={isVisible}>
    <div class="hero-content">
      <h1 class="hero-title">Get In Touch</h1>
      <p class="hero-subtitle">
        We'd love to hear from the flow arts community
      </p>
    </div>
  </section>

  <!-- Contact Content -->
  <section class="contact-content">
    <div class="container">
      <div class="contact-grid">
        <!-- Contact Information -->
        <div class="contact-info">
          <h2>Connect With Us</h2>

          <div class="info-card">
            <div class="info-icon">📧</div>
            <div class="info-content">
              <h3>Email</h3>
              <p>tkaflowarts@gmail.com</p>
              <a href="mailto:tkaflowarts@gmail.com" class="contact-link">
                Send us an email
              </a>
            </div>
          </div>

          <div class="info-card">
            <div class="info-icon">💬</div>
            <div class="info-content">
              <h3>Community</h3>
              <p>Join our growing community of flow artists</p>
              <a href="/links" class="contact-link"> Find community links </a>
            </div>
          </div>

          <div class="info-card">
            <div class="info-icon">🔧</div>
            <div class="info-content">
              <h3>Technical Support</h3>
              <p>Need help with the Constructor or other tools?</p>
              <a
                href="mailto:tkaflowarts@gmail.com?subject=Technical Support"
                class="contact-link"
              >
                Get technical help
              </a>
            </div>
          </div>

          <div class="info-card">
            <div class="info-icon">🤝</div>
            <div class="info-content">
              <h3>Collaborations</h3>
              <p>Interested in partnerships or contributing?</p>
              <a
                href="mailto:tkaflowarts@gmail.com?subject=Collaboration"
                class="contact-link"
              >
                Discuss collaboration
              </a>
            </div>
          </div>
        </div>

        <!-- Contact Form -->
        <div class="contact-form-section">
          <h2>Send Us a Message</h2>

          <form class="contact-form" onsubmit={handleSubmit}>
            <!-- Name Field -->
            <div class="form-group">
              <label for="name" class="form-label">Name *</label>
              <input
                type="text"
                id="name"
                class="form-input"
                class:error={formErrors.name}
                value={formData.name}
                oninput={(e) => updateField("name", e.currentTarget.value)}
                placeholder="Your name"
                required
              />
              {#if formErrors.name}
                <span class="error-message">{formErrors.name}</span>
              {/if}
            </div>

            <!-- Email Field -->
            <div class="form-group">
              <label for="email" class="form-label">Email *</label>
              <input
                type="email"
                id="email"
                class="form-input"
                class:error={formErrors.email}
                value={formData.email}
                oninput={(e) => updateField("email", e.currentTarget.value)}
                placeholder="your.email@example.com"
                required
              />
              {#if formErrors.email}
                <span class="error-message">{formErrors.email}</span>
              {/if}
            </div>

            <!-- Subject Field -->
            <div class="form-group">
              <label for="subject" class="form-label">Subject *</label>
              <input
                type="text"
                id="subject"
                class="form-input"
                class:error={formErrors.subject}
                value={formData.subject}
                oninput={(e) => updateField("subject", e.currentTarget.value)}
                placeholder="What's this about?"
                required
              />
              {#if formErrors.subject}
                <span class="error-message">{formErrors.subject}</span>
              {/if}
            </div>

            <!-- Message Field -->
            <div class="form-group">
              <label for="message" class="form-label">Message *</label>
              <textarea
                id="message"
                class="form-textarea"
                class:error={formErrors.message}
                value={formData.message}
                oninput={(e) => updateField("message", e.currentTarget.value)}
                placeholder="Tell us what's on your mind..."
                rows="6"
                required
              ></textarea>
              {#if formErrors.message}
                <span class="error-message">{formErrors.message}</span>
              {/if}
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              class="submit-button"
              disabled={!isFormValid || isSubmitting}
            >
              {#if isSubmitting}
                <span class="button-spinner">
                  <svg viewBox="0 0 24 24" width="16" height="16">
                    <circle
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="2"
                      fill="none"
                    />
                    <path
                      d="M12,2 A10,10 0 0,1 22,12"
                      stroke="currentColor"
                      stroke-width="2"
                      fill="none"
                    >
                      <animateTransform
                        attributeName="transform"
                        attributeType="XML"
                        type="rotate"
                        from="0 12 12"
                        to="360 12 12"
                        dur="1s"
                        repeatCount="indefinite"
                      />
                    </path>
                  </svg>
                </span>
                Sending...
              {:else}
                Send Message
              {/if}
            </button>

            <!-- Status Messages -->
            {#if submitStatus === "success"}
              <div class="status-message success">
                ✅ Message sent successfully! We'll get back to you soon.
              </div>
            {:else if submitStatus === "error"}
              <div class="status-message error">
                ❌ Failed to send message. Please try again or email us
                directly.
              </div>
            {/if}
          </form>
        </div>
      </div>
    </div>
  </section>
</main>

<style>
  .contact-container {
    min-height: 100vh;
    padding: 0;
  }

  /* Hero Section */
  .hero {
    position: relative;
    color: var(--text-color);
    padding: var(--spacing-2xl) 0;
    text-align: center;
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s ease;
    z-index: 1;
    min-height: 30vh;
    display: flex;
    align-items: center;

    /* Glassmorphism styling */
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 2rem;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    margin: var(--spacing-lg);
  }

  .hero.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .hero-content {
    max-width: 600px;
    margin: 0 auto;
    padding: 0 var(--spacing-xl);
  }

  .hero-title {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-subtitle {
    font-size: 1.25rem;
    opacity: 0.9;
    font-weight: 300;
  }

  /* Contact Content */
  .contact-content {
    padding: var(--spacing-3xl) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  .contact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-3xl);
    align-items: start;
  }

  /* Contact Info */
  .contact-info h2,
  .contact-form-section h2 {
    color: var(--text-color);
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: var(--spacing-xl);
  }

  .info-card {
    display: flex;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    margin-bottom: var(--spacing-lg);
    transition: all 0.3s ease;
  }

  .info-card:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-2px);
  }

  .info-icon {
    font-size: 2rem;
    flex-shrink: 0;
  }

  .info-content h3 {
    color: var(--text-color);
    font-weight: 600;
    margin-bottom: var(--spacing-sm);
  }

  .info-content p {
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: var(--spacing-sm);
    line-height: 1.5;
  }

  .contact-link {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s ease;
  }

  .contact-link:hover {
    color: #764ba2;
    text-decoration: underline;
  }

  /* Contact Form */
  .contact-form {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1.5rem;
    padding: var(--spacing-xl);
  }

  .form-group {
    margin-bottom: var(--spacing-lg);
  }

  .form-label {
    display: block;
    color: var(--text-color);
    font-weight: 600;
    margin-bottom: var(--spacing-sm);
  }

  .form-input,
  .form-textarea {
    width: 100%;
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    color: var(--text-color);
    font-size: var(--font-size-base);
    transition: all 0.2s ease;
    box-sizing: border-box;
  }

  .form-input::placeholder,
  .form-textarea::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }

  .form-input:focus,
  .form-textarea:focus {
    outline: none;
    border-color: #667eea;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
  }

  .form-input.error,
  .form-textarea.error {
    border-color: #ff6b6b;
    box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2);
  }

  .form-textarea {
    resize: vertical;
    min-height: 120px;
  }

  .error-message {
    display: block;
    color: #ff6b6b;
    font-size: var(--font-size-sm);
    margin-top: var(--spacing-xs);
  }

  .submit-button {
    width: 100%;
    padding: var(--spacing-md) var(--spacing-lg);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: var(--border-radius);
    font-size: var(--font-size-base);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
  }

  .submit-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }

  .submit-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .button-spinner {
    display: flex;
    align-items: center;
  }

  .status-message {
    margin-top: var(--spacing-md);
    padding: var(--spacing-md);
    border-radius: var(--border-radius);
    text-align: center;
    font-weight: 500;
  }

  .status-message.success {
    background: rgba(34, 197, 94, 0.2);
    color: #22c55e;
    border: 1px solid rgba(34, 197, 94, 0.3);
  }

  .status-message.error {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .hero {
      padding: var(--spacing-xl) 0;
      min-height: 25vh;
      margin: var(--spacing-md);
    }

    .hero-title {
      font-size: 2.5rem;
    }

    .contact-content {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    .contact-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-2xl);
    }

    .info-card {
      padding: var(--spacing-md);
    }

    .contact-form {
      padding: var(--spacing-lg);
    }

    .form-group {
      margin-bottom: var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .hero {
      transition: none;
      opacity: 1;
      transform: none;
    }

    .info-card,
    .submit-button {
      transition: none;
    }

    .info-card:hover,
    .submit-button:hover {
      transform: none;
    }
  }
</style>
