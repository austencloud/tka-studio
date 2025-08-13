import { describe, expect, it } from "vitest";

describe("Letter Type Detection", () => {
  // Test the letter type detection logic used in OptionPickerScroll
  function detectLetterType(letter: string): string {
    if (!letter) return "Type1"; // Handle null/undefined/empty

    let pictographType = "Type1"; // Default fallback

    // Check longer patterns first to avoid partial matches
    if (letter.match(/^[WXYZ]-$|^[ΣΔθΩ]-$/)) pictographType = "Type3";
    else if (letter.match(/^[ΦΨΛ]-$/)) pictographType = "Type5";
    else if (letter.match(/^[A-V]$/)) pictographType = "Type1";
    else if (letter.match(/^[WXYZ]$|^[ΣΔθΩ]$/)) pictographType = "Type2";
    else if (letter.match(/^[ΦΨΛ]$/)) pictographType = "Type4";
    else if (letter.match(/^[αβΓ]$/)) pictographType = "Type6";

    return pictographType;
  }

  describe("Type1 Letters (A-V)", () => {
    const type1Letters = [
      "A",
      "B",
      "C",
      "D",
      "E",
      "F",
      "G",
      "H",
      "I",
      "J",
      "K",
      "L",
      "M",
      "N",
      "O",
      "P",
      "Q",
      "R",
      "S",
      "T",
      "U",
      "V",
    ];

    type1Letters.forEach((letter) => {
      it(`should classify ${letter} as Type1`, () => {
        expect(detectLetterType(letter)).toBe("Type1");
      });
    });
  });

  describe("Type2 Letters (W, X, Y, Z, Σ, Δ, θ, Ω)", () => {
    const type2Letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"];

    type2Letters.forEach((letter) => {
      it(`should classify ${letter} as Type2`, () => {
        expect(detectLetterType(letter)).toBe("Type2");
      });
    });
  });

  describe("Type3 Letters (W-, X-, Y-, Z-, Σ-, Δ-, θ-, Ω-)", () => {
    const type3Letters = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"];

    type3Letters.forEach((letter) => {
      it(`should classify ${letter} as Type3`, () => {
        expect(detectLetterType(letter)).toBe("Type3");
      });
    });
  });

  describe("Type4 Letters (Φ, Ψ, Λ)", () => {
    const type4Letters = ["Φ", "Ψ", "Λ"];

    type4Letters.forEach((letter) => {
      it(`should classify ${letter} as Type4`, () => {
        expect(detectLetterType(letter)).toBe("Type4");
      });
    });
  });

  describe("Type5 Letters (Φ-, Ψ-, Λ-)", () => {
    const type5Letters = ["Φ-", "Ψ-", "Λ-"];

    type5Letters.forEach((letter) => {
      it(`should classify ${letter} as Type5`, () => {
        expect(detectLetterType(letter)).toBe("Type5");
      });
    });
  });

  describe("Type6 Letters (α, β, Γ)", () => {
    const type6Letters = ["α", "β", "Γ"];

    type6Letters.forEach((letter) => {
      it(`should classify ${letter} as Type6`, () => {
        expect(detectLetterType(letter)).toBe("Type6");
      });
    });
  });

  describe("Edge Cases", () => {
    it("should handle empty string", () => {
      expect(detectLetterType("")).toBe("Type1");
    });

    it("should handle null/undefined", () => {
      expect(detectLetterType(null as any)).toBe("Type1");
    });

    it("should handle unknown letters", () => {
      expect(detectLetterType("Unknown")).toBe("Type1");
    });
  });

  describe("Integration Test", () => {
    it("should correctly organize a mixed set of letters", () => {
      const testLetters = [
        "A",
        "B",
        "W",
        "X",
        "W-",
        "X-",
        "Φ",
        "Ψ",
        "Φ-",
        "Ψ-",
        "α",
        "β",
      ];
      const organized = {
        Type1: [] as string[],
        Type2: [] as string[],
        Type3: [] as string[],
        Type4: [] as string[],
        Type5: [] as string[],
        Type6: [] as string[],
      };

      testLetters.forEach((letter) => {
        const type = detectLetterType(letter);
        organized[type as keyof typeof organized].push(letter);
      });

      expect(organized.Type1).toEqual(["A", "B"]);
      expect(organized.Type2).toEqual(["W", "X"]);
      expect(organized.Type3).toEqual(["W-", "X-"]);
      expect(organized.Type4).toEqual(["Φ", "Ψ"]);
      expect(organized.Type5).toEqual(["Φ-", "Ψ-"]);
      expect(organized.Type6).toEqual(["α", "β"]);
    });
  });
});
