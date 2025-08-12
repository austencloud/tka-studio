<script>
  let formData = {
    name: '',
    email: '',
    subject: '',
    message: ''
  };

  let isSubmitting = false;
  let submitMessage = '';

  function handleSubmit() {
    isSubmitting = true;
    // Simulate form submission
    setTimeout(() => {
      isSubmitting = false;
      submitMessage = 'Thank you for your message! We\'ll get back to you soon.';
      formData = { name: '', email: '', subject: '', message: '' };
    }, 1000);
  }
</script>

<svelte:head>
  <title>Contact - The Kinetic Alphabet</title>
  <meta name="description" content="Get in touch with The Kinetic Alphabet team. We'd love to hear from you!" />
</svelte:head>

<section class="contact-section">
  <h1>Contact Us</h1>
  <p class="intro">We'd love to hear from you! Reach out with questions, feedback, or collaboration ideas.</p>

  <div class="contact-grid">
    <div class="contact-form">
      <h2>Send us a message</h2>

      {#if submitMessage}
        <div class="success-message" role="alert">
          {submitMessage}
        </div>
      {/if}

      <form on:submit|preventDefault={handleSubmit}>
        <div class="form-group">
          <label for="name">Name *</label>
          <input
            type="text"
            id="name"
            bind:value={formData.name}
            required
            disabled={isSubmitting}
          />
        </div>

        <div class="form-group">
          <label for="email">Email *</label>
          <input
            type="email"
            id="email"
            bind:value={formData.email}
            required
            disabled={isSubmitting}
          />
        </div>

        <div class="form-group">
          <label for="subject">Subject</label>
          <input
            type="text"
            id="subject"
            bind:value={formData.subject}
            disabled={isSubmitting}
          />
        </div>

        <div class="form-group">
          <label for="message">Message *</label>
          <textarea
            id="message"
            bind:value={formData.message}
            rows="5"
            required
            disabled={isSubmitting}
          ></textarea>
        </div>

        <button type="submit" class="submit-btn" disabled={isSubmitting}>
          {isSubmitting ? 'Sending...' : 'Send Message'}
        </button>
      </form>
    </div>

    <div class="contact-info">
      <h2>Other ways to reach us</h2>

      <div class="contact-method">
        <h3>Social Media</h3>
        <p>Follow us for updates and community content:</p>
        <ul class="social-list">
          <li><a href="http://youtube.com/thekineticalphabet" target="_blank">YouTube</a></li>
          <li><a href="http://instagram.com/thekineticalphabet" target="_blank">Instagram</a></li>
          <li><a href="http://facebook.com/thekineticalphabet" target="_blank">Facebook</a></li>
          <li><a href="http://tiktok.com/thekineticalphabet" target="_blank">TikTok</a></li>
        </ul>
      </div>

      <div class="contact-method">
        <h3>Community</h3>
        <p>Join our community discussions and get support from fellow flow artists.</p>
      </div>

      <div class="contact-method">
        <h3>Response Time</h3>
        <p>We typically respond to messages within 24-48 hours during business days.</p>
      </div>
    </div>
  </div>
</section>

<style>
  .contact-section {
    width: 100%;
    max-width: var(--container-max-width-wide);
    margin: 0 auto;
    padding: var(--container-padding);
  }

  .intro {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-xl);
  }

  .contact-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: var(--spacing-3xl);
    margin-top: var(--spacing-xl);
  }

  .contact-form h2,
  .contact-info h2 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-lg);
  }

  .form-group {
    margin-bottom: var(--spacing-lg);
  }

  .form-group label {
    display: block;
    margin-bottom: var(--spacing-sm);
    font-weight: 600;
    color: var(--text-color);
  }

  .form-group input,
  .form-group textarea {
    width: 100%;
    padding: var(--spacing-md);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    font-family: inherit;
    font-size: var(--font-size-base);
    font-weight: 500;

    /* Glassmorphism styling */
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    color: var(--text-color);
    box-shadow: var(--shadow-glass);

    /* Enhanced transitions */
    transition: all var(--transition-normal);
    will-change: border-color, box-shadow, background;
  }

  .form-group input:focus,
  .form-group textarea:focus {
    outline: none;
    border: 2px solid var(--primary-color);
    background: var(--surface-hover);
    box-shadow:
      var(--shadow-glass-hover),
      0 0 0 3px rgba(99, 102, 241, 0.1);
    transform: translateY(-1px);
  }

  .form-group input:disabled,
  .form-group textarea:disabled {
    background: var(--surface-color);
    opacity: 0.6;
    cursor: not-allowed;
  }

  .submit-btn {
    /* Use global button styling from app.css */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-md) var(--spacing-xl);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    font-family: inherit;
    font-size: var(--font-size-base);
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    position: relative;
    overflow: hidden;

    /* Clean primary button glassmorphism styling */
    background: var(--primary-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    color: var(--text-inverse);
    box-shadow: var(--shadow-glass);

    /* Enhanced transitions */
    transition: all var(--transition-normal);
    will-change: transform, box-shadow, background;
  }

  .submit-btn:hover:not(:disabled) {
    background: var(--primary-light);
    transform: translateY(-2px);
    box-shadow: var(--shadow-glass-hover);
  }

  .submit-btn:disabled {
    background: var(--surface-color);
    color: var(--text-muted);
    cursor: not-allowed;
    transform: none;
    box-shadow: var(--shadow-glass);
  }

  .success-message {
    /* Glassmorphism success message */
    background: rgba(76, 175, 80, 0.15);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    color: #4caf50;
    border: 1px solid rgba(76, 175, 80, 0.3);
    box-shadow: 0 4px 16px rgba(76, 175, 80, 0.1);
    padding: var(--spacing-md);
    border-radius: var(--border-radius-lg);
    margin-bottom: var(--spacing-lg);
  }

  .contact-method {
    margin-bottom: var(--spacing-xl);
    padding: var(--spacing-lg);

    /* Glassmorphism styling for contact method cards */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-glass);
  }

  .contact-method h3 {
    color: var(--primary-color);
    margin-top: 0;
    margin-bottom: var(--spacing-md);
  }

  .social-list {
    list-style: none;
    padding: 0;
  }

  .social-list li {
    margin: var(--spacing-sm) 0;
  }

  .social-list a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
  }

  .social-list a:hover {
    text-decoration: underline;
  }

  /* Desktop optimization */
  @media (min-width: 1200px) {
    .contact-grid {
      gap: var(--spacing-3xl);
    }
  }

  @media (max-width: 768px) {
    .contact-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-xl);
    }

    .contact-section {
      padding: var(--container-padding);
    }
  }
</style>
