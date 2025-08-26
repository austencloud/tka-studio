<!-- ContactSection.svelte - Clean contact section coordinator -->
<script lang="ts">
  import ContactInfo from "../contact/info/ContactInfo.svelte";
  import SocialLinks from "../contact/social/SocialLinks.svelte";
  import ContactForm from "../contact/forms/ContactForm.svelte";
</script>

<section class="contact-section">
  <div class="container">
    <div class="contact-grid">
      <!-- Contact Info & Social -->
      <div class="info-column">
        <SocialLinks />
      </div>

      <!-- Contact Form -->
      <div class="form-column">
        <ContactForm />
      </div>
    </div>
  </div>
</section>

<style>
  .contact-section {
    padding: var(--spacing-3xl) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  .contact-grid {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-3xl);
    align-items: stretch;
  }

  .info-column {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-2xl);
  }

  .form-column {
    display: flex;
    flex-direction: column;
  }

  @media (max-width: 768px) {
    .contact-section {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    .contact-grid {
      gap: var(--spacing-2xl);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    * {
      transition: none !important;
      animation: none !important;
    }
  }
</style>
