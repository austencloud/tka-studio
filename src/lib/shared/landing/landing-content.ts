/**
 * Landing Page Content Configuration
 *
 * Defines all content for the landing page/modal including resources,
 * social links, and support options.
 */

// ============================================================================
// TYPES
// ============================================================================

export interface SocialLink {
  name: string;
  url: string;
  icon: string; // FontAwesome class
  color: string; // Brand color
}

export interface Resource {
  title: string;
  description: string;
  url: string;
  icon: string;
  type: "download" | "internal" | "external";
}

export interface SupportOption {
  name: string;
  url: string;
  icon: string;
  color: string;
}

// ============================================================================
// SOCIAL LINKS
// ============================================================================

export const SOCIAL_LINKS: SocialLink[] = [
  {
    name: "Facebook",
    url: "https://facebook.com/thekineticalphabet", // TODO: Replace with real URL
    icon: "fab fa-facebook",
    color: "#1877F2",
  },
  {
    name: "Instagram",
    url: "https://instagram.com/thekineticalphabet", // TODO: Replace with real URL
    icon: "fab fa-instagram",
    color: "#E4405F",
  },
  {
    name: "Email",
    url: "mailto:tkaflowarts@gmail.com",
    icon: "fas fa-envelope",
    color: "#667eea",
  },
];

// ============================================================================
// RESOURCES
// ============================================================================

export const RESOURCES: Resource[] = [
  {
    title: "Level 1 PDF Book",
    description: "Comprehensive introduction to The Kinetic Alphabet methodology",
    url: "https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link",
    icon: "/images/level_images/level_1.png",
    type: "download",
  },
];

// ============================================================================
// SUPPORT OPTIONS
// ============================================================================

export const SUPPORT_OPTIONS: SupportOption[] = [
  {
    name: "PayPal",
    url: "https://paypal.me/austencloud",
    icon: "fab fa-paypal",
    color: "#00457C",
  },
  {
    name: "Zelle",
    url: "mailto:austencloud@gmail.com?subject=Zelle%20Donation", // Opens email to request Zelle info
    icon: "fas fa-money-bill-wave",
    color: "#6D1ED4",
  },
];

// ============================================================================
// CONTACT INFO
// ============================================================================

export const CONTACT_EMAIL = "tkaflowarts@gmail.com";

// ============================================================================
// LANDING PAGE TEXT
// ============================================================================

export const LANDING_TEXT = {
  hero: {
    title: "The Kinetic Alphabet",
    subtitle: "Master flow arts with data-driven sequence creation",
    cta: "Enter Studio",
  },
  resources: {
    title: "Resources",
    subtitle: "Learning materials and documentation",
  },
  community: {
    title: "Community",
    subtitle: "Connect with us and the flow arts community",
  },
  support: {
    title: "Support Development",
    subtitle: "Help keep this project alive",
    message: "TKA Studio is free during beta. Eventually there will be paid features, but a free version will always exist. Your support helps fund hosting and continued development.",
  },
  dev: {
    title: "For Developers",
    subtitle: "Open source & contributions",
    message: "TKA Studio is open source. Check out the code, report bugs, or contribute features.",
  },
  contact: {
    title: "Get in Touch",
    subtitle: "Questions, feedback, or collaborations",
  },
};
