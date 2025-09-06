<!-- SEO-Optimized About Page with User Redirect -->
<script lang="ts">
  import AboutTab from '$lib/modules/about/components/AboutTab.svelte';
  import { browser } from "$app/environment";
  import { handleSEORedirect } from "$shared/utils";
  import { onMount } from "svelte";
  import type { PageData } from "./$types";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  // Redirect users to main app while preserving SEO benefits
  onMount(() => {
    if (browser) {
      handleSEORedirect("about");
    }
  });

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "TKA - The Kinetic Constructor",
    description:
      "Revolutionary browser-based tool for creating kinetic typography animations",
    applicationCategory: "DesignApplication",
    operatingSystem: "Web Browser",
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "USD",
    },
  };
</script>

<svelte:head>
  <title>{data.meta.title}</title>
  <meta name="description" content={data.meta.description} />
  <meta property="og:title" content={data.meta.ogTitle} />
  <meta property="og:description" content={data.meta.ogDescription} />
  <meta property="og:type" content={data.meta.ogType} />
  <meta property="og:url" content={data.meta.ogUrl} />
  <link rel="canonical" href={data.meta.canonical} />

  <!-- Structured Data for SEO -->
  {@html `<script type="application/ld+json">${JSON.stringify(structuredData)}</script>`}
</svelte:head>

<AboutTab />
