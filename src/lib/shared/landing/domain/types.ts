/**
 * Landing Domain Types
 *
 * Defines the core domain structures that power the landing experience.
 */

import type { Section } from "../../navigation/domain/types";

export type LandingTab = "resources" | "support" | "dev";

export interface LandingSection extends Section {
  color: string;
  gradient: string;
}

export interface SocialLink {
  name: string;
  url: string;
  icon: string;
  color: string;
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

export interface LandingHeroContent {
  title: string;
  subtitle: string;
  cta: string;
}

export interface LandingPanelContent {
  title: string;
  subtitle: string;
}

export interface LandingSupportContent extends LandingPanelContent {}

export interface LandingDevContent extends LandingPanelContent {
  message: string;
}

export interface LandingTextContent {
  hero: LandingHeroContent;
  resources: LandingPanelContent;
  support: LandingSupportContent;
  dev: LandingDevContent;
}
