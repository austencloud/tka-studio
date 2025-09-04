<!-- ContactInfo.svelte - Contact information and methods -->
<script lang="ts">
  import EmailIcon from "../icons/EmailIcon.svelte";
  import ResponseTimeIcon from "../icons/ResponseTimeIcon.svelte";
</script>

<div class="contact-info">
  <h2>Get in Touch</h2>
  <p class="contact-description">
    Have questions about The Kinetic Alphabet? Want to contribute to the project
    or share feedback? I'd love to hear from you!
  </p>

  <div class="contact-methods">
    <div class="contact-method">
      <div class="method-icon">
        <EmailIcon />
      </div>
      <div class="method-details">
        <h3>Email</h3>
        <p>contact@kineticalphabetproject.com</p>
        <span class="method-note"
          >Best for detailed inquiries and collaboration</span
        >
      </div>
    </div>

    <div class="contact-method">
      <div class="method-icon">
        <ResponseTimeIcon />
      </div>
      <div class="method-details">
        <h3>Response Time</h3>
        <p>24-48 hours typically</p>
        <span class="method-note"
          >I aim to respond to all messages promptly</span
        >
      </div>
    </div>
  </div>
</div>

<style>
  .contact-info h2 {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
  }

  .contact-description {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: var(--spacing-2xl);
  }

  .contact-methods {
    margin-bottom: var(--spacing-2xl);
  }

  .contact-method {
    display: flex;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
  }

  .method-icon {
    flex-shrink: 0;
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: var(--border-radius);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }

  .method-details h3 {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: var(--spacing-xs);
  }

  .method-details p {
    font-size: var(--font-size-base);
    color: var(--primary-color);
    margin-bottom: var(--spacing-xs);
    font-weight: 500;
  }

  .method-note {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }
</style>
