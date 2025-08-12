<script lang="ts">
  import { onMount } from 'svelte';
  import SocialIcon from './SocialIcon.svelte';

  // Type definitions
  interface SocialLink {
    name: string;
    href: string;
    icon: string;
    color: string;
  }



  const socialLinks: SocialLink[] = [
    {
      name: "YouTube",
      href: "https://youtube.com/@thekineticalphabet",
      icon: "youtube",
      color: "#FF0000"
    },
    {
      name: "Instagram",
      href: "https://instagram.com/thekineticalphabet",
      icon: "instagram",
      color: "#E4405F"
    },
    {
      name: "Facebook",
      href: "https://facebook.com/thekineticalphabet",
      icon: "facebook",
      color: "#1877F2"
    },
    {
      name: "TikTok",
      href: "https://tiktok.com/@thekineticalphabet",
      icon: "tiktok",
      color: "#000000"
    }
  ];

  let mounted = false;

  onMount(() => {
    mounted = true;
  });
</script>

<div class="social-links">
  {#each socialLinks as link, index}
    <div
      class="social-link-container"
      style="--animation-delay: {index * 0.1}s"
    >
      <!-- Main social link -->
      <a
        href={link.href}
        target="_blank"
        rel="noopener noreferrer"
        aria-label={`Visit The Kinetic Alphabet on ${link.name}`}
        class="social-link"
        style="--platform-color: {link.color}"
      >
        <span class="icon icon-{link.icon}" aria-hidden="true">
          <SocialIcon platform={link.icon} size={22} />
        </span>
        <span class="sr-only">{link.name}</span>

        <!-- Glassmorphism overlay -->
        <div class="glass-overlay" aria-hidden="true"></div>
      </a>


    </div>
  {/each}
</div>

<style>
  /*
   * Enhanced Social Links with Glassmorphism and Micro-interactions
   *
   * Features:
   * - Glassmorphism effects with backdrop-blur
   * - Platform-specific color theming
   * - Loading states and micro-interactions
   * - Accessibility-compliant tooltips
   * - Copy-to-clipboard functionality
   * - Reduced motion support
   */

  .social-links {
    display: flex;
    gap: var(--spacing-md);
    align-items: center;
    flex-wrap: wrap;
  }

  .social-link-container {
    position: relative;
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);

    /* Entrance animation with staggered delay */
    opacity: 0;
    transform: translateY(20px);
    animation: slideInUp 0.6s ease-out forwards;
    animation-delay: var(--animation-delay, 0s);
  }

  @keyframes slideInUp {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Main social link with glassmorphism */
  .social-link {
    position: relative;
    color: white;
    text-decoration: none;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    overflow: hidden;

    /* Glassmorphism base */
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);

    /* Smooth transitions */
    transition: all var(--transition-normal);
    will-change: transform, background-color, box-shadow;
  }

  .social-link:hover {
    transform: translateY(-3px) scale(1.05);
    background: rgba(255, 255, 255, 0.15);
    box-shadow:
      0 12px 40px rgba(0, 0, 0, 0.15),
      0 0 0 2px var(--platform-color, rgba(255, 255, 255, 0.3)),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .social-link:focus-visible {
    outline: 2px solid var(--platform-color, var(--primary-color));
    outline-offset: 3px;
  }

  .social-link:active {
    transform: translateY(-1px) scale(1.02);
  }



  /* Glassmorphism overlay for enhanced depth */
  .glass-overlay {
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

  .social-link:hover .glass-overlay {
    opacity: 1;
  }

  .icon {
    font-size: 1.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 1;
    transition: transform var(--transition-fast);
  }

  .social-link:hover .icon {
    transform: scale(1.1);
  }





  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .social-link-container {
      animation: none;
      opacity: 1;
      transform: none;
    }

    .social-link,
    .icon,
    .glass-overlay {
      transition: none;
      animation: none;
    }


  }

  /* Mobile responsive design */
  @media (max-width: 768px) {
    .social-links {
      gap: var(--spacing-sm);
      justify-content: center;
    }

    .social-link {
      width: 2.5rem;
      height: 2.5rem;
    }

    .icon {
      font-size: 1.2rem;
    }




  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .social-link {
      border: 2px solid white;
      background: rgba(0, 0, 0, 0.8);
    }


  }
</style>
