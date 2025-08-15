<!-- SEO-Optimized Browse Page with User Redirect -->
<script lang="ts">
  import { onMount } from "svelte";
  import { browser } from "$app/environment";
  import { switchTab } from "$lib/state/appState.svelte";
  import { getCanonicalURL } from "$lib/config/domains";
  import MainApplication from "$components/MainApplication.svelte";

  onMount(async () => {
    if (browser) {
      // Check if this is a user visit and redirect to main app
      setTimeout(() => {
        const referrer = document.referrer;
        const isFromSearchEngine =
          referrer.includes("google.") ||
          referrer.includes("bing.") ||
          referrer.includes("duckduckgo.") ||
          referrer === "";

        if (isFromSearchEngine) {
          // Redirect to main app with browse tab open
          window.location.href = "/?tab=browse";
        } else {
          // Direct navigation - show browse tab
          switchTab("browse");
        }
      }, 100);
    }
  });

  const canonicalURL = getCanonicalURL("browse");
</script>

<svelte:head>
  <title>Browse Animations - TKA Gallery | Kinetic Typography Examples</title>
  <meta
    name="description"
    content="Explore hundreds of kinetic typography animations in the TKA gallery. Browse by difficulty, length, style, and more. Find inspiration for your projects."
  />
  <meta property="og:title" content="Browse Animations - TKA Gallery" />
  <meta
    property="og:description"
    content="Explore hundreds of kinetic typography animations. Browse by difficulty, length, style and find inspiration."
  />
  <meta property="og:type" content="website" />
  <meta property="og:url" content={canonicalURL} />
  <link rel="canonical" href={canonicalURL} />

  <!-- Structured Data for Gallery -->
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "TKA Animation Gallery",
      "description": "Collection of kinetic typography animations created with TKA",
      "isPartOf": {
        "@type": "WebSite",
        "name": "TKA - The Kinetic Constructor"
      }
    }
  </script>
</svelte:head>

<MainApplication />
