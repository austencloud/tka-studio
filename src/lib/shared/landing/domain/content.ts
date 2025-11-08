/**
 * Landing Domain Content
 *
 * Provides the static content and configuration used across the landing experience.
 */

import type {
  LandingTextContent,
  Resource,
  SocialLink,
  SupportOption,
} from "./types";

export const CONTACT_EMAIL = "tkaflowarts@gmail.com";

export const LANDING_TEXT: LandingTextContent = {
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
    subtitle: "Social links",
  },
  support: {
    title: "Support Development",
    subtitle: "Help keep this project alive",
    message:
      "TKA Studio is free during beta. Eventually there will be paid features, but a free version will always exist. Your support helps fund hosting and continued development.",
  },
  dev: {
    title: "For Developers",
    subtitle: "Open source & contributions",
    message:
      "TKA Studio is open source. Check out the code, report bugs, or contribute features.",
  },
  contact: {
    title: "Get in Touch",
    subtitle: "Questions, feedback, or collaborations",
  },
};

export const SOCIAL_LINKS: SocialLink[] = [
  {
    name: "Facebook",
    url: "https://facebook.com/thekineticalphabet",
    icon: "fab fa-facebook",
    color: "#1877F2",
  },
  {
    name: "Instagram",
    url: "https://instagram.com/thekineticalphabet",
    icon: "fab fa-instagram",
    color: "#E4405F",
  },
  {
    name: "Email",
    url: `mailto:${CONTACT_EMAIL}`,
    icon: "fas fa-envelope",
    color: "#667eea",
  },
];

export const RESOURCES: Resource[] = [
  {
    title: "Level 1 PDF Book",
    description:
      "Comprehensive introduction to The Kinetic Alphabet methodology",
    url: "https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link",
    icon: "/images/level_images/level_1.png",
    type: "download",
  },
];

export const SUPPORT_OPTIONS: SupportOption[] = [
  {
    name: "PayPal",
    url: "https://paypal.me/austencloud",
    icon: "fab fa-paypal",
    color: "#00457C",
  },
  {
    name: "Zelle",
    url: "mailto:austencloud@gmail.com?subject=Zelle%20Donation",
    icon: "fas fa-money-bill-wave",
    color: "#6D1ED4",
  },
];
