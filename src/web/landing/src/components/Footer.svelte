<script>
  import Newsletter from "./Newsletter.svelte";
  import SocialLinks from "./SocialLinks.svelte";
</script>

<footer class="footer">
  <div class="container">
    <div class="footer-content">
      <!-- Brand Section -->
      <div class="footer-section">
        <h3 class="footer-brand">The Kinetic Alphabet</h3>
        <p class="footer-description">
          Revolutionizing flow arts through systematic choreography and digital innovation.
        </p>
        <div class="footer-social">
          <SocialLinks />
        </div>
      </div>

      <!-- Quick Links -->
      <div class="footer-section">
        <h4>Quick Links</h4>
        <nav class="footer-nav">
          <a href="/">Home</a>
          <a href="/about">About</a>
          <a href="/contact">Contact</a>
        </nav>
      </div>

      <!-- Resources -->
      <div class="footer-section">
        <h4>Resources</h4>
        <nav class="footer-nav">
          <a href="https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link" target="_blank" rel="noopener noreferrer">
            Level 1 PDF
          </a>
          <a href="https://github.com/austencloud/tka-sequence-constructor/releases/download/v0.1.2/TKA_Setup.exe" target="_blank" rel="noopener noreferrer">
            Kinetic Constructor
          </a>
        </nav>
      </div>

      <!-- Newsletter -->
      <div class="footer-section newsletter-section">
        <Newsletter />
      </div>
    </div>

    <!-- Copyright -->
    <div class="footer-bottom">
      <p>&copy; 2025 The Kinetic Alphabet. All rights reserved.</p>
      <div class="footer-legal">
        <a href="/privacy" class="footer-link">Privacy Policy</a>
        <a href="/terms" class="footer-link">Terms of Service</a>
      </div>
    </div>
  </div>
</footer>

<style>
  .footer {
    /* Clean glassmorphism footer styling */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border-top: var(--glass-border);
    color: var(--text-color);
    padding: var(--spacing-3xl) 0 var(--spacing-lg) 0;
    margin-top: auto;

    /* Enhanced glassmorphism shadows */
    box-shadow: var(--shadow-glass);
  }

  .footer-content {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1.5fr;
    gap: var(--spacing-2xl);
    margin-bottom: var(--spacing-2xl);
  }

  .footer-section h3,
  .footer-section h4 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-lg);
  }

  .footer-brand {
    font-family: var(--font-family-heading);
    font-size: var(--font-size-xl);
  }

  .footer-description {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: var(--spacing-lg);
  }

  .footer-social {
    margin-top: var(--spacing-md);
  }

  .footer-nav {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .footer-nav a {
    color: var(--text-secondary);
    text-decoration: none;
    transition: color var(--transition-fast);
    padding: var(--spacing-xs) 0;
  }

  .footer-nav a:hover {
    color: var(--primary-color);
  }

  .newsletter-section {
    background: rgba(255, 255, 255, 0.05);
    padding: var(--spacing-lg);
    border-radius: var(--border-radius);
  }

  .footer-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: var(--spacing-lg);
    border-top: var(--glass-border);
    color: var(--text-muted);
  }

  .footer-legal {
    display: flex;
    gap: var(--spacing-lg);
  }

  .footer-link {
    color: var(--text-muted);
    text-decoration: none;
    font-size: var(--font-size-sm);
    transition: color var(--transition-fast);
  }

  .footer-link:hover {
    color: var(--primary-color);
  }

  /* Responsive Design */
  @media (max-width: 1024px) {
    .footer-content {
      grid-template-columns: 1fr 1fr;
      gap: var(--spacing-xl);
    }

    .newsletter-section {
      grid-column: 1 / -1;
    }
  }

  @media (max-width: 768px) {
    .footer {
      padding: var(--spacing-2xl) 0 var(--spacing-lg) 0;
    }

    .footer-content {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }

    .footer-bottom {
      flex-direction: column;
      gap: var(--spacing-md);
      text-align: center;
    }

    .footer-legal {
      justify-content: center;
    }
  }
</style>
