import {
  simplifyAndTruncate,
  simplifyRepeatedWord,
} from "$lib/modules/build/workspace-panel/shared/utils/word-simplifier";
import { describe, expect, it } from "vitest";

describe("Word Simplifier", () => {
  describe("simplifyRepeatedWord", () => {
    it("should simplify repeated patterns", () => {
      expect(simplifyRepeatedWord("ABCABCABC")).toBe("ABC");
      expect(simplifyRepeatedWord("TESTTEST")).toBe("TEST");
      expect(simplifyRepeatedWord("AAAA")).toBe("A");
    });

    it("should return original word if no pattern", () => {
      expect(simplifyRepeatedWord("HELLO")).toBe("HELLO");
      expect(simplifyRepeatedWord("ABCDEF")).toBe("ABCDEF");
    });

    it("should handle empty strings", () => {
      expect(simplifyRepeatedWord("")).toBe("");
    });

    it("should handle words with dashes", () => {
      expect(simplifyRepeatedWord("W-X-W-X-")).toBe("W-X-");
      expect(simplifyRepeatedWord("Φ-Ψ-Φ-Ψ-")).toBe("Φ-Ψ-");
    });
  });

  describe("simplifyAndTruncate", () => {
    it("should treat letter+dash as one unit", () => {
      // "W-X-Y-Z-" = 4 letter units (W-, X-, Y-, Z-)
      expect(simplifyAndTruncate("W-X-Y-Z-", 8)).toBe("W-X-Y-Z-");

      // "A-B-C-D-E-F-G-H-I-" = 9 letter units, should truncate to 8 + "..."
      expect(simplifyAndTruncate("A-B-C-D-E-F-G-H-I-", 8)).toBe(
        "A-B-C-D-E-F-G-H-..."
      );
    });

    it("should handle mixed letters with and without dashes", () => {
      // "AW-BX-CY-" = 4 letter units (A, W-, B, X-, C, Y-)
      expect(simplifyAndTruncate("AW-BX-CY-", 8)).toBe("AW-BX-CY-");

      // "AW-BX-CY-DZ-E" = 9 letter units, should truncate
      expect(simplifyAndTruncate("AW-BX-CY-DZ-E", 8)).toBe("AW-BX-CY-DZ-...");
    });

    it("should truncate regular letters correctly", () => {
      // "ABCDEFGHIJK" = 11 letters, truncate to 8
      expect(simplifyAndTruncate("ABCDEFGHIJK", 8)).toBe("ABCDEFGH...");
    });

    it("should simplify before truncating", () => {
      // "ABCABCABCABCABC" simplifies to "ABC" (3 letters), no truncation
      expect(simplifyAndTruncate("ABCABCABCABCABC", 8)).toBe("ABC");

      // "ABCDEFGHABCDEFGH" simplifies to "ABCDEFGH" (8 letters), no truncation
      expect(simplifyAndTruncate("ABCDEFGHABCDEFGH", 8)).toBe("ABCDEFGH");

      // "ABCDEFGHI" * 2 simplifies to "ABCDEFGHI" (9 letters), truncates
      expect(simplifyAndTruncate("ABCDEFGHIABCDEFGHI", 8)).toBe("ABCDEFGH...");
    });

    it("should not truncate if within limit", () => {
      expect(simplifyAndTruncate("ABC", 8)).toBe("ABC");
      expect(simplifyAndTruncate("ABCDEFGH", 8)).toBe("ABCDEFGH");
    });

    it("should handle Greek letters with dashes", () => {
      // "Φ-Ψ-Ω-Δ-" = 4 letter units
      expect(simplifyAndTruncate("Φ-Ψ-Ω-Δ-", 8)).toBe("Φ-Ψ-Ω-Δ-");

      // 9 Greek letter units should truncate
      expect(simplifyAndTruncate("Φ-Ψ-Ω-Δ-Σ-Λ-Θ-Π-Ξ-", 8)).toBe(
        "Φ-Ψ-Ω-Δ-Σ-Λ-Θ-Π-..."
      );
    });

    it("should handle empty strings", () => {
      expect(simplifyAndTruncate("", 8)).toBe("");
    });
  });
});
