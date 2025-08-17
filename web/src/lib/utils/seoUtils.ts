/**
 * SEO Utilities
 *
 * Provides utilities for SEO handling and redirects.
 */

import { goto } from "$app/navigation";
import { browser } from "$app/environment";

export interface SEOMetadata {
  title?: string;
  description?: string;
  keywords?: string[];
  ogTitle?: string;
  ogDescription?: string;
  ogImage?: string;
  twitterCard?: "summary" | "summary_large_image";
  canonical?: string;
}

/**
 * Handle SEO redirects for pages
 */
export function handleSEORedirect(targetPath: string = "/"): void {
  if (browser) {
    // In browser, redirect to the target path
    goto(targetPath, { replaceState: true });
  }
}

/**
 * Set page metadata for SEO
 */
export function setPageMetadata(metadata: SEOMetadata): void {
  if (!browser) return;

  const document = globalThis.document;
  if (!document) return;

  // Set title
  if (metadata.title) {
    document.title = metadata.title;
  }

  // Set or update meta tags
  const metaTags = [
    { name: "description", content: metadata.description },
    { name: "keywords", content: metadata.keywords?.join(", ") },
    { property: "og:title", content: metadata.ogTitle || metadata.title },
    {
      property: "og:description",
      content: metadata.ogDescription || metadata.description,
    },
    { property: "og:image", content: metadata.ogImage },
    { name: "twitter:card", content: metadata.twitterCard || "summary" },
    { name: "twitter:title", content: metadata.ogTitle || metadata.title },
    {
      name: "twitter:description",
      content: metadata.ogDescription || metadata.description,
    },
    { name: "twitter:image", content: metadata.ogImage },
  ];

  metaTags.forEach(({ name, property, content }) => {
    if (!content) return;

    const selector = name
      ? `meta[name="${name}"]`
      : `meta[property="${property}"]`;
    let metaElement = document.querySelector(selector) as HTMLMetaElement;

    if (!metaElement) {
      metaElement = document.createElement("meta");
      if (name) metaElement.name = name;
      if (property) metaElement.setAttribute("property", property);
      document.head.appendChild(metaElement);
    }

    metaElement.content = content;
  });

  // Set canonical URL
  if (metadata.canonical) {
    let canonicalElement = document.querySelector(
      'link[rel="canonical"]'
    ) as HTMLLinkElement;
    if (!canonicalElement) {
      canonicalElement = document.createElement("link");
      canonicalElement.rel = "canonical";
      document.head.appendChild(canonicalElement);
    }
    canonicalElement.href = metadata.canonical;
  }
}

/**
 * Generate structured data for TKA sequences
 */
export function generateSequenceStructuredData(sequence: {
  name: string;
  description?: string;
  author?: string;
  difficulty?: string;
  beats?: number;
}): string {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    name: sequence.name,
    description: sequence.description || `TKA sequence: ${sequence.name}`,
    creator: sequence.author
      ? {
          "@type": "Person",
          name: sequence.author,
        }
      : undefined,
    genre: "Dance Notation",
    inLanguage: "en",
    about: "The Kinetic Alphabet (TKA) movement sequence",
    keywords: [
      "TKA",
      "The Kinetic Alphabet",
      "dance notation",
      "movement",
      "flow arts",
      sequence.difficulty,
      `${sequence.beats} beats`,
    ].filter(Boolean),
  };

  return JSON.stringify(structuredData, null, 2);
}

/**
 * Set structured data in the page head
 */
export function setStructuredData(structuredData: string): void {
  if (!browser) return;

  const document = globalThis.document;
  if (!document) return;

  // Remove existing structured data
  const existingScript = document.querySelector(
    'script[type="application/ld+json"]'
  );
  if (existingScript) {
    existingScript.remove();
  }

  // Add new structured data
  const script = document.createElement("script");
  script.type = "application/ld+json";
  script.textContent = structuredData;
  document.head.appendChild(script);
}

/**
 * Get default TKA metadata
 */
export function getDefaultTKAMetadata(): SEOMetadata {
  return {
    title: "TKA - The Kinetic Alphabet",
    description:
      "The Kinetic Alphabet (TKA) is a digital notation system for kinetic movement and flow arts. Create, learn, and share movement sequences with visual pictographs.",
    keywords: [
      "TKA",
      "The Kinetic Alphabet",
      "dance notation",
      "movement notation",
      "flow arts",
      "kinetic movement",
      "dance sequences",
      "movement visualization",
    ],
    ogTitle: "TKA - The Kinetic Alphabet",
    ogDescription: "Digital notation system for kinetic movement and flow arts",
    twitterCard: "summary_large_image",
  };
}

/**
 * Generate page-specific metadata
 */
export function generatePageMetadata(
  page: string,
  _data?: unknown
): SEOMetadata {
  const baseMetadata = getDefaultTKAMetadata();

  switch (page) {
    case "browse":
      return {
        ...baseMetadata,
        title: "Browse Sequences - TKA",
        description:
          "Browse and discover TKA movement sequences. Filter by difficulty, author, length, and more.",
        keywords: [
          ...(baseMetadata.keywords || []),
          "browse sequences",
          "sequence library",
        ],
      };

    case "construct":
      return {
        ...baseMetadata,
        title: "Construct Sequences - TKA",
        description:
          "Create and build new TKA movement sequences using our interactive constructor.",
        keywords: [
          ...(baseMetadata.keywords || []),
          "create sequences",
          "sequence builder",
          "constructor",
        ],
      };

    case "learn":
      return {
        ...baseMetadata,
        title: "Learn TKA - TKA",
        description:
          "Learn The Kinetic Alphabet notation system and improve your movement skills.",
        keywords: [
          ...(baseMetadata.keywords || []),
          "learn TKA",
          "tutorials",
          "education",
        ],
      };

    case "about":
      return {
        ...baseMetadata,
        title: "About TKA - The Kinetic Alphabet",
        description:
          "Learn about The Kinetic Alphabet (TKA) notation system and its applications in movement and flow arts.",
        keywords: [
          ...(baseMetadata.keywords || []),
          "about TKA",
          "notation system",
          "movement theory",
        ],
      };

    default:
      return baseMetadata;
  }
}
