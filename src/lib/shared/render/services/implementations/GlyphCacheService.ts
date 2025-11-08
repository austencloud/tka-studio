/**
 * Glyph Cache Service
 *
 * Pre-loads and caches all letter SVG glyphs AND turn number SVGs to eliminate
 * network requests during sequence preview rendering. This dramatically improves
 * performance by converting external <image> references to inline data URLs.
 */

import { injectable } from "inversify";
import { getLetterImagePath } from "$shared/pictograph/tka-glyph/utils";
import { Letter } from "$shared";

// Turn number values that need to be cached
type TurnNumberValue = 0.5 | 1 | 1.5 | 2 | 2.5 | 3 | "float";

export interface IGlyphCacheService {
  /**
   * Initialize the cache by preloading all glyphs
   */
  initialize(): Promise<void>;

  /**
   * Get a cached glyph as a data URL
   * @param letter The letter to get
   * @returns Base64 data URL or null if not cached
   */
  getGlyphDataUrl(letter: string): string | null;

  /**
   * Check if the cache is ready
   */
  isReady(): boolean;

  /**
   * Get cache statistics
   */
  getStats(): { total: number; loaded: number; failed: number };
}

@injectable()
export class GlyphCacheService implements IGlyphCacheService {
  private cache = new Map<string, string>();
  private ready = false;
  private loadedCount = 0;
  private failedCount = 0;

  // All possible TKA letters across all types
  private readonly LETTERS_TO_CACHE: Letter[] = [
    // Type1: Latin letters A-V + lowercase gamma
    Letter.A,
    Letter.B,
    Letter.C,
    Letter.D,
    Letter.E,
    Letter.F,
    Letter.G,
    Letter.H,
    Letter.I,
    Letter.J,
    Letter.K,
    Letter.L,
    Letter.M,
    Letter.N,
    Letter.O,
    Letter.P,
    Letter.Q,
    Letter.R,
    Letter.S,
    Letter.T,
    Letter.U,
    Letter.V,
    Letter.GAMMA_LOWERCASE,
    // Type2: W-Z + Greek uppercase + μ, ν
    Letter.W,
    Letter.X,
    Letter.Y,
    Letter.Z,
    Letter.SIGMA,
    Letter.DELTA,
    Letter.THETA,
    Letter.OMEGA,
    Letter.MU,
    Letter.NU,
    // Type3: Cross-Shift variants
    Letter.W_DASH,
    Letter.X_DASH,
    Letter.Y_DASH,
    Letter.Z_DASH,
    Letter.SIGMA_DASH,
    Letter.DELTA_DASH,
    Letter.THETA_DASH,
    Letter.OMEGA_DASH,
    // Type4: Dash Greek letters
    Letter.PHI,
    Letter.PSI,
    Letter.LAMBDA,
    // Type5: Dual-Dash variants
    Letter.PHI_DASH,
    Letter.PSI_DASH,
    Letter.LAMBDA_DASH,
    // Type6: Static Greek letters (α, β, Γ, ζ, η, τ, ⊕)
    Letter.ALPHA,
    Letter.BETA,
    Letter.GAMMA,
    Letter.ZETA,
    Letter.ETA,
    Letter.TAU,
    Letter.TERRA,
  ];

  // All turn number values that need to be cached
  private readonly TURN_NUMBERS_TO_CACHE: TurnNumberValue[] = [
    0.5,
    1,
    1.5,
    2,
    2.5,
    3,
    "float",
  ];

  async initialize(): Promise<void> {
    if (this.ready) {
      console.log("✅ GlyphCache: Already initialized");
      return;
    }

    const totalItems =
      this.LETTERS_TO_CACHE.length + this.TURN_NUMBERS_TO_CACHE.length;
    const startTime = performance.now();

    // Load all glyphs in parallel (max 10 at a time to avoid overwhelming the browser)
    const BATCH_SIZE = 10;

    // Load letters
    for (let i = 0; i < this.LETTERS_TO_CACHE.length; i += BATCH_SIZE) {
      const batch = this.LETTERS_TO_CACHE.slice(i, i + BATCH_SIZE);
      await Promise.all(batch.map((letter) => this.loadGlyph(letter)));
    }

    // Load turn numbers
    for (let i = 0; i < this.TURN_NUMBERS_TO_CACHE.length; i += BATCH_SIZE) {
      const batch = this.TURN_NUMBERS_TO_CACHE.slice(i, i + BATCH_SIZE);
      await Promise.all(
        batch.map((turnNumber) => this.loadTurnNumber(turnNumber))
      );
    }

    this.ready = true;
    const duration = performance.now() - startTime;

    // GlyphCache initialized silently
    // Debug: ${duration.toFixed(0)}ms, ${this.loadedCount} loaded, ${this.failedCount} failed, ${this.cache.size} cache entries
  }

  private async loadGlyph(letter: Letter): Promise<void> {
    try {
      const path = getLetterImagePath(letter);
      const response = await fetch(path);

      if (!response.ok) {
        // Some letters might not exist in all types - that's OK
        this.failedCount++;
        return;
      }

      const svgContent = await response.text();

      // Convert to base64 data URL for inline embedding
      const dataUrl = `data:image/svg+xml;base64,${btoa(svgContent)}`;

      // Cache with multiple keys to handle different encoding scenarios:
      // 1. The letter enum value (e.g., "α")
      this.cache.set(letter, dataUrl);

      // 2. The raw path (e.g., "/images/letters_trimmed/Type6/α.svg")
      this.cache.set(path, dataUrl);

      // 3. URL-encoded version of the path (e.g., "/images/letters_trimmed/Type6/%CE%B1.svg")
      try {
        const encodedPath = path
          .split("/")
          .map((segment, i) =>
            i === path.split("/").length - 1
              ? encodeURIComponent(segment)
              : segment
          )
          .join("/");
        if (encodedPath !== path) {
          this.cache.set(encodedPath, dataUrl);
        }
      } catch {
        // Ignore encoding errors
      }

      this.loadedCount++;
    } catch (error) {
      console.warn(`Failed to load glyph "${letter}":`, error);
      this.failedCount++;
    }
  }

  private async loadTurnNumber(value: TurnNumberValue): Promise<void> {
    try {
      // Construct path based on turn number value
      const filename = value === "float" ? "float" : value.toString();
      const path = `/images/numbers/${filename}.svg`;

      const response = await fetch(path);

      if (!response.ok) {
        this.failedCount++;
        return;
      }

      const svgContent = await response.text();

      // Convert to base64 data URL for inline embedding
      const dataUrl = `data:image/svg+xml;base64,${btoa(svgContent)}`;

      // Cache with the path as the key
      this.cache.set(path, dataUrl);

      this.loadedCount++;
    } catch (error) {
      console.warn(`Failed to load turn number "${value}":`, error);
      this.failedCount++;
    }
  }

  getGlyphDataUrl(letter: string): string | null {
    // Try the direct lookup first
    let result = this.cache.get(letter);
    if (result) return result;

    // Try URL-decoded version (browser might encode Greek letters)
    try {
      const decoded = decodeURIComponent(letter);
      result = this.cache.get(decoded);
      if (result) return result;
    } catch {
      // Ignore decoding errors
    }

    // Try encoding the letter (in case cache has encoded but we got raw)
    try {
      const encoded = encodeURIComponent(letter);
      result = this.cache.get(encoded);
      if (result) return result;
    } catch {
      // Ignore encoding errors
    }

    return null;
  }

  isReady(): boolean {
    return this.ready;
  }

  getStats() {
    return {
      total: this.LETTERS_TO_CACHE.length + this.TURN_NUMBERS_TO_CACHE.length,
      loaded: this.loadedCount,
      failed: this.failedCount,
    };
  }
}
