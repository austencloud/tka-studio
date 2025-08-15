<!-- SEO-Optimized Features Page with User Redirect -->
<script lang="ts">
  import { onMount } from "svelte";
  import { browser } from "$app/environment";
  import AboutTab from "$lib/components/about/AboutTab.svelte";

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
          // Redirect to main app with about tab open, scrolled to features
          window.location.href = "/?tab=about&section=features";
        }
      }, 100);
    }
  });
</script>

<svelte:head>
  <title
    >TKA Features - Kinetic Typography Animation Tools | Advanced Sequence
    Editor</title
  >
  <meta
    name="description"
    content="Discover TKA's powerful features for creating kinetic typography animations. Advanced sequence editor, motion controls, export options, and more."
  />
  <meta property="og:title" content="TKA Features - Advanced Animation Tools" />
  <meta
    property="og:description"
    content="Powerful kinetic typography animation features including sequence editor, motion controls, and professional export options."
  />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://thekineticalphabet.com/features" />
  <link rel="canonical" href="https://thekineticalphabet.com/features" />

  <!-- Structured Data for Features -->
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "TKA - The Kinetic Constructor",
      "featureList": [
        "Advanced Sequence Editor",
        "Motion Controls",
        "Professional Export Options",
        "Browser-based Animation",
        "Kinetic Typography Tools"
      ],
      "applicationCategory": "DesignApplication",
      "operatingSystem": "Web Browser"
    }
  </script>
</svelte:head>

<!-- Show the features section of AboutTab -->
<AboutTab />
