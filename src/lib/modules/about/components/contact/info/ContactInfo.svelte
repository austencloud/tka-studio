<!-- ContactInfo.svelte - Contact information using reusable cards -->
<script lang="ts">
  import ContactInfoCard from "./ContactInfoCard.svelte";
</script>

<div class="contact-info">
  <h2>Connect With Us</h2>

  <div class="info-cards">
    <ContactInfoCard
      title="Email"
      description="tkaflowarts@gmail.com"
      linkText="Send us an email"
      linkHref="mailto:tkaflowarts@gmail.com"
    >
      {#snippet icon()}
        <div class="icon-wrapper">📧</div>
      {/snippet}
    </ContactInfoCard>

    <ContactInfoCard
      title="Community"
      description="Join our growing community of flow artists"
      linkText="Find community links"
      linkHref="/links"
    >
      {#snippet icon()}
        <div class="icon-wrapper">💬</div>
      {/snippet}
    </ContactInfoCard>

    <ContactInfoCard
      title="Technical Support"
      description="Need help with TKA Studio or other tools?"
      linkText="Get technical help"
      linkHref="mailto:tkaflowarts@gmail.com?subject=Technical Support"
    >
      {#snippet icon()}
        <div class="icon-wrapper">🔧</div>
      {/snippet}
    </ContactInfoCard>

    <ContactInfoCard
      title="Collaborations"
      description="Interested in partnerships or contributing?"
      linkText="Discuss collaboration"
      linkHref="mailto:tkaflowarts@gmail.com?subject=Collaboration"
    >
      {#snippet icon()}
        <div class="icon-wrapper">🤝</div>
      {/snippet}
    </ContactInfoCard>
  </div>
</div>

<style>
  .contact-info {
    margin-bottom: var(--spacing-2xl);
  }

  .contact-info h2 {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--spacing-xl);
  }

  .info-cards {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
  }

  .icon-wrapper {
    font-size: 2.5rem;
  }

  @media (max-width: 768px) {
    .contact-info h2 {
      font-size: 2rem;
    }
  }
</style>
