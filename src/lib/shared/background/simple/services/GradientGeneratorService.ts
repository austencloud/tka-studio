/**
 * Gradient Generator Service
 *
 * Generates beautiful random gradients for simple backgrounds.
 * Uses color theory to create harmonious color combinations.
 */

export interface GradientConfig {
  colors: string[];
  direction: number; // Angle in degrees (0-360)
}

export class GradientGeneratorService {
  /**
   * Preset beautiful gradients
   */
  static readonly PRESET_GRADIENTS: GradientConfig[] = [
    {
      colors: ["#667eea", "#764ba2", "#f093fb"],
      direction: 135,
    },
    {
      colors: ["#4facfe", "#00f2fe", "#43e97b"],
      direction: 45,
    },
    {
      colors: ["#fa709a", "#fee140", "#30cfd0"],
      direction: 90,
    },
    {
      colors: ["#a8edea", "#fed6e3", "#fbc2eb"],
      direction: 180,
    },
  ];

  /**
   * Generate a random gradient with 2-4 colors
   */
  static generateRandomGradient(numColors: number = 3): GradientConfig {
    // Ensure numColors is between 2 and 4
    const colorCount = Math.max(2, Math.min(4, numColors));

    // Generate random hue as starting point
    const baseHue = Math.random() * 360;

    // Generate colors using different color harmony strategies
    const colors: string[] = [];
    const strategy = Math.floor(Math.random() * 3);

    switch (strategy) {
      case 0: // Analogous colors (close hues)
        for (let i = 0; i < colorCount; i++) {
          const hue = (baseHue + i * 30) % 360;
          const saturation = 70 + Math.random() * 20;
          const lightness = 50 + Math.random() * 20;
          colors.push(this.hslToHex(hue, saturation, lightness));
        }
        break;

      case 1: // Complementary colors (opposite hues)
        for (let i = 0; i < colorCount; i++) {
          const hue = (baseHue + i * (180 / (colorCount - 1))) % 360;
          const saturation = 70 + Math.random() * 20;
          const lightness = 50 + Math.random() * 20;
          colors.push(this.hslToHex(hue, saturation, lightness));
        }
        break;

      case 2: // Triadic colors (evenly spaced hues)
        for (let i = 0; i < colorCount; i++) {
          const hue = (baseHue + i * (360 / colorCount)) % 360;
          const saturation = 70 + Math.random() * 20;
          const lightness = 50 + Math.random() * 20;
          colors.push(this.hslToHex(hue, saturation, lightness));
        }
        break;
    }

    // Random direction
    const direction = Math.floor(Math.random() * 8) * 45; // 0, 45, 90, 135, 180, 225, 270, 315

    return { colors, direction };
  }

  /**
   * Convert HSL to HEX color
   */
  private static hslToHex(h: number, s: number, l: number): string {
    const hDecimal = h / 360;
    const sDecimal = s / 100;
    const lDecimal = l / 100;

    let r, g, b;

    if (sDecimal === 0) {
      r = g = b = lDecimal;
    } else {
      const hue2rgb = (p: number, q: number, t: number) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1 / 6) return p + (q - p) * 6 * t;
        if (t < 1 / 2) return q;
        if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
        return p;
      };

      const q =
        lDecimal < 0.5
          ? lDecimal * (1 + sDecimal)
          : lDecimal + sDecimal - lDecimal * sDecimal;
      const p = 2 * lDecimal - q;

      r = hue2rgb(p, q, hDecimal + 1 / 3);
      g = hue2rgb(p, q, hDecimal);
      b = hue2rgb(p, q, hDecimal - 1 / 3);
    }

    const toHex = (x: number) => {
      const hex = Math.round(x * 255).toString(16);
      return hex.length === 1 ? "0" + hex : hex;
    };

    return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
  }

  /**
   * Get a random preset gradient
   */
  static getRandomPreset(): GradientConfig {
    const index = Math.floor(Math.random() * this.PRESET_GRADIENTS.length);
    return this.PRESET_GRADIENTS[index];
  }

  /**
   * Validate gradient colors
   */
  static isValidGradient(colors: string[]): boolean {
    if (colors.length < 2 || colors.length > 4) {
      return false;
    }

    // Check if all colors are valid hex colors
    const hexRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
    return colors.every((color) => hexRegex.test(color));
  }
}
