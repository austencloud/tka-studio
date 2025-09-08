/**
 * SEO Utilities
 * 
 * Provides utility functions for SEO operations using the SEO service.
 */

import { resolve, TYPES } from "../../inversify";
import type { ISeoService } from "../services/contracts/ISeoService";

/**
 * Handle SEO redirect using the SEO service
 * This function maintains the same interface as the previous utility
 */
export function handleSEORedirect(targetTab: string, targetSection?: string): void {
  const seoService = resolve<ISeoService>(TYPES.ISeoService);
  seoService.handleSEORedirect(targetTab, targetSection);
}

/**
 * Create SEO link using the SEO service  
 */
export function createSEOLink(path: string, options?: { tab?: string; section?: string; seoMode?: boolean }): string {
  const seoService = resolve<ISeoService>(TYPES.ISeoService);
  return seoService.createSEOLink(path, options || {});
}
