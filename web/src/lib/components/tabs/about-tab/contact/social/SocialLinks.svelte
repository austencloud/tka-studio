<!-- SocialLinks.svelte - Social media links section -->
<script lang="ts">
  import { browser } from "$app/environment";
  import SocialIcons from "../icons/SocialIcons.svelte";

  const socialLinks = [
    {
      name: "GitHub",
      url: "https://github.com/yourusername",
      icon: "github" as const,
      description: "Source code and project repositories",
    },
    {
      name: "YouTube",
      url: "https://youtube.com/@yourchannel",
      icon: "youtube" as const,
      description: "Tutorial videos and flow arts content",
    },
    {
      name: "Instagram",
      url: "https://instagram.com/yourusername",
      icon: "instagram" as const,
      description: "Visual content and community updates",
    },
    {
      name: "Discord",
      url: "https://discord.gg/yourinvite",
      icon: "discord" as const,
      description: "Join our flow arts community",
    },
    {
      name: "Reddit",
      url: "https://reddit.com/r/flowarts",
      icon: "reddit" as const,
      description: "Flow arts discussions and sharing",
    },
    {
      name: "Email",
      url: "mailto:contact@kineticalphabetproject.com",
      icon: "email" as const,
      description: "Direct contact for inquiries",
    },
  ];

  function openSocialLink(url: string) {
    if (browser) {
      window.open(url, "_blank", "noopener,noreferrer");
    }
  }
</script>

<div class="social-section">
  <div class="social-header">
    <h3>Connect & Follow</h3>
    <p>Join the community and stay updated with the latest developments</p>
  </div>

  <div class="social-row">
    {#each socialLinks as social}
      <button
        class="social-link"
        onclick={() => openSocialLink(social.url)}
        type="button"
        title={social.description}
      >
        <div class="social-icon">
          <SocialIcons icon={social.icon} />
        </div>
        <span class="social-name">{social.name}</span>
        <div class="social-tooltip">
          {social.description}
        </div>
      </button>
    {/each}
  </div>
</div>

<style>
  .social-section {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    text-align: center;
  }

  .social-header {
    margin-bottom: var(--spacing-xl);
  }

  .social-header h3 {
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: var(--spacing-sm);
  }

  .social-header p {
    color: var(--text-secondary);
    line-height: 1.5;
    margin: 0;
  }

  .social-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--spacing-lg);
    flex-wrap: wrap;
  }

  .social-link {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    min-width: 80px;
  }

  .social-link:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary-color);
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  }

  .social-link:hover .social-tooltip {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%);
  }

  .social-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(
      135deg,
      var(--primary-color),
      var(--secondary-color)
    );
    border-radius: var(--border-radius);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    transition: transform 0.3s ease;
  }

  .social-link:hover .social-icon {
    transform: rotate(5deg) scale(1.1);
  }

  .social-name {
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--text-color);
    margin: 0;
  }

  .social-tooltip {
    position: absolute;
    top: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius);
    font-size: var(--font-size-xs);
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
    pointer-events: none;
  }

  .social-tooltip::before {
    content: "";
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-bottom-color: rgba(0, 0, 0, 0.9);
  }

  @media (max-width: 768px) {
    .social-row {
      gap: var(--spacing-md);
    }

    .social-link {
      min-width: 70px;
      padding: var(--spacing-sm);
    }

    .social-link:hover {
      transform: translateY(-2px) scale(1.02);
    }

    .social-icon {
      width: 40px;
      height: 40px;
    }

    .social-name {
      font-size: var(--font-size-xs);
    }
  }

  @media (max-width: 480px) {
    .social-row {
      gap: var(--spacing-sm);
    }

    .social-link {
      min-width: 60px;
    }

    .social-icon {
      width: 36px;
      height: 36px;
    }
  }
</style>
