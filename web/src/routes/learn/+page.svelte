<!-- SEO-Optimized LEARN Page with Enhanced Meta Data -->
<script lang="ts">
  import { onMount } from "svelte";
  import { browser } from "$app/environment";
  import { handleSEORedirect } from "$lib/utils/seo-utils";
  import MainApplication from "$components/layout/MainApplication.svelte";
  import type { PageData } from "./$types";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  // Enhanced SEO redirect with analytics potential
  onMount(() => {
    if (browser) {
      handleSEORedirect("learn");
    }
  });

  // Structured data for enhanced SEO
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: "Learn Flow Arts - TKA Tutorials",
    description:
      "Comprehensive flow arts education with progressive tutorials for poi, fans, staff, and advanced kinetic patterns.",
    url: "https://thekineticalphabet.com/learn",
    isPartOf: {
      "@type": "WebSite",
      name: "TKA - The Kinetic Constructor",
      url: "https://thekineticalphabet.com",
    },
    creator: {
      "@type": "SoftwareApplication",
      name: "TKA - The Kinetic Constructor",
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
  <meta property="og:site_name" content="TKA - The Kinetic Constructor" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={data.meta.ogTitle} />
  <meta name="twitter:description" content={data.meta.ogDescription} />
  <link rel="canonical" href={data.meta.canonical} />

  <!-- Enhanced Structured Data -->
  {@html `<script type="application/ld+json">${JSON.stringify(structuredData)}</script>`}
</svelte:head>

<MainApplication />
