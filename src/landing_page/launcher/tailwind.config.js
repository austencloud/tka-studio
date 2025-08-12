import { addVariablesForColors } from "@tailwindcss/postcss";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {
      colors: {
        // Command Center Electric Theme
        "electric-blue": "#00d4ff",
        "cyber-blue": "#0ea5e9",
        "deep-blue": "#0f172a",
        "neon-green": "#10b981",
        "neon-orange": "#f59e0b",
        "neon-purple": "#a855f7",

        // Legacy colors for compatibility
        primary: "oklch(0.6 0.2 250)",
        success: "oklch(0.7 0.15 140)",
        warning: "oklch(0.8 0.15 80)",
        error: "oklch(0.65 0.2 25)",

        // Glassmorphism surfaces
        "glass-white": "rgba(255, 255, 255, 0.1)",
        "glass-dark": "rgba(0, 0, 0, 0.2)",
        surface: "#1e293b",
        "surface-light": "#334155",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Inter Display", "Inter", "sans-serif"],
        mono: ["JetBrains Mono", "Consolas", "monospace"],
      },
      animation: {
        "glow-pulse": "glow-pulse 2s ease-in-out infinite alternate",
        float: "float 6s ease-in-out infinite",
        "grid-slide": "grid-slide 20s linear infinite",
        "pulse-ring": "pulse-ring 2s ease-in-out infinite",
        "slide-up": "slide-up 0.5s ease-out",
        "fade-in": "fade-in 0.3s ease-out",
        "scale-in": "scale-in 0.2s ease-out",
      },
      keyframes: {
        "glow-pulse": {
          "0%": { filter: "drop-shadow(0 0 5px rgba(0, 212, 255, 0.8))" },
          "100%": { filter: "drop-shadow(0 0 20px rgba(0, 212, 255, 0.8))" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px) rotate(0deg)" },
          "50%": { transform: "translateY(-20px) rotate(180deg)" },
        },
        "grid-slide": {
          "0%": { transform: "translate(0, 0)" },
          "100%": { transform: "translate(50px, 50px)" },
        },
        "pulse-ring": {
          "0%": { transform: "scale(0.33)", opacity: "1" },
          "80%, 100%": { transform: "scale(2.33)", opacity: "0" },
        },
        "slide-up": {
          "0%": { transform: "translateY(20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        "scale-in": {
          "0%": { transform: "scale(0.95)", opacity: "0" },
          "100%": { transform: "scale(1)", opacity: "1" },
        },
      },
      backdropBlur: {
        xs: "2px",
      },
      boxShadow: {
        neon: "0 0 20px rgba(0, 212, 255, 0.5)",
        "neon-lg": "0 0 40px rgba(0, 212, 255, 0.3)",
        glass: "0 8px 32px rgba(0, 0, 0, 0.3)",
        electric: "0 0 30px rgba(0, 212, 255, 0.4)",
      },
      borderColor: {
        glass: "rgba(255, 255, 255, 0.2)",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
