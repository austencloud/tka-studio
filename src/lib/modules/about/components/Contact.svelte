<!-- Contact.svelte - Main orchestrator for contact page -->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ContactFormData } from "../domain/models/contact-models";
  import { createContactState } from "../state/contact-state.svelte";
  import ContactHero from "./contact/ContactHero.svelte";
  import ContactForm from "./contact/forms/ContactForm.svelte";
  import ContactInfo from "./contact/info/ContactInfo.svelte";

  // Initialize state management
  const state = createContactState();

  // Services
  let hapticService: IHapticFeedbackService | null = null;

  onMount(async () => {
    try {
      hapticService = resolve<IHapticFeedbackService>(
        TYPES.IHapticFeedbackService
      );
    } catch (error) {
      console.error("Failed to resolve haptic service:", error);
    }
  });

  // Wrap form submission with haptic feedback
  async function handleFormSubmit() {
    try {
      // Trigger success haptic feedback for form submission
      hapticService?.trigger("success");

      await state.submitForm();

      // Success haptic feedback is already handled in state if needed
    } catch (error) {
      // Trigger error haptic feedback for failed submission
      hapticService?.trigger("error");
      throw error;
    }
  }

  // Wrap field updates with haptic feedback
  function handleFieldUpdate(field: keyof ContactFormData, value: string) {
    // Trigger subtle selection haptic feedback for text input
    hapticService?.trigger("selection");

    state.updateField(field, value);
  }
</script>

<svelte:head>
  <title>Contact - TKA Studio</title>
  <meta
    name="description"
    content="Get in touch with the creator of TKA Studio. I'd love to hear from you about collaborations, questions, or feedback."
  />
</svelte:head>

<main class="contact-container">
  <!-- Hero Section -->
  <ContactHero />

  <!-- Contact Content -->
  <section class="contact-content">
    <div class="container">
      <div class="contact-grid">
        <!-- Contact Information -->
        <ContactInfo />

        <!-- Contact Form -->
        <div class="contact-form-wrapper">
          <ContactForm
            formData={state.formData}
            formErrors={state.formErrors}
            isFormValid={state.isFormValid}
            isSubmitting={state.isSubmitting}
            submitStatus={state.submitStatus}
            onFieldUpdate={handleFieldUpdate}
            onSubmit={handleFormSubmit}
          />
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

  /* Contact Content Section */
  .contact-content {
    padding: var(--spacing-2xl) 0;
    position: relative;
    z-index: 2;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
  }

  .contact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-2xl);
    align-items: start;
  }

  .contact-form-wrapper {
    position: sticky;
    top: var(--spacing-xl);
  }

  @media (max-width: 968px) {
    .contact-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-xl);
    }

    .contact-form-wrapper {
      position: static;
    }

    .contact-content {
      padding: var(--spacing-xl) 0;
    }
  }
</style>
