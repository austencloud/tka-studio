<!-- SEO-Optimized Getting Started Page with User Redirect -->
<script lang="ts">
  import { browser } from "$app/environment";
  import AboutTab from "$lib/modules/about/components/AboutTab.svelte";
  import { onMount } from "svelte";

  onMount(() => {
    if (browser) {
      setTimeout(() => {
        const referrer = document.referrer;
        const isFromSearchEngine =
          referrer.includes("google.") ||
          referrer.includes("bing.") ||
          referrer.includes("duckduckgo.") ||
          referrer === "";

        if (isFromSearchEngine) {
          // Redirect to main app with about tab open, scrolled to getting started
          window.location.href = "/?tab=about&section=getting-started";
        }
      }, 100);
    }
  });
</script>

<svelte:head>
  <title
    >Getting Started with TKA - Kinetic Typography Tutorial | Animation Guide</title
  >
  <meta
    name="description"
    content="Learn how to create your first kinetic typography animation with TKA. Step-by-step tutorial and guide for beginners."
  />
  <meta
    property="og:title"
    content="Getting Started with TKA - Animation Tutorial"
  />
  <meta
    property="og:description"
    content="Step-by-step guide to create your first kinetic typography animation with TKA's intuitive tools."
  />
  <meta property="og:type" content="article" />
  <meta
    property="og:url"
    content="https://thekineticalphabet.com/getting-started"
  />
  <link rel="canonical" href="https://thekineticalphabet.com/getting-started" />

  <!-- Structured Data for Tutorial -->
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "HowTo",
      "name": "How to Create Kinetic Typography with TKA",
      "description": "Learn to create kinetic typography animations using TKA's browser-based tools",
      "image": "https://your-domain.com/images/tutorial-preview.jpg",
      "step": [
        {
          "@type": "HowToStep",
          "name": "Open TKA Constructor",
          "text": "Navigate to the Constructor tab to begin creating your animation"
        },
        {
          "@type": "HowToStep",
          "name": "Design Your Sequence",
          "text": "Use the sequence editor to create your kinetic typography animation"
        },
        {
          "@type": "HowToStep",
          "name": "Preview and Export",
          "text": "Preview your animation and export in your preferred format"
        }
      ]
    }
  </script>
</svelte:head>

<AboutTab />
