import type { Config } from "tailwindcss"

// Design tokens from PulseAI/code.html, corrected to the InfoBeans BrandOS palette
// (brand red #EA1B3D, not the mockup's #ba002a). See .claude/skills/infobeans-brand.
const config: Config = {
  content: ["./src/**/*.{ts,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        primary: "#EA1B3D", // Brand Red — accent only, one emphasis per view
        "desire-red": "#EB4C5E",
        "dark-red": "#AA142D",
        "deep-red": "#7C2235",
        tertiary: "#b11f38",
        background: "#FFF9ED", // Light Cream — dominant background
        surface: "#FFFFFF",
        "surface-container": "#f9f9ff",
        charcoal: "#373742", // Primary text
        "medium-gray": "#676775", // Secondary text
        "light-gray": "#E6E6ED", // Borders / backgrounds
        peach: "#FFD0D8", // Accent + drop shadows only
        "outline-variant": "#e6bcbb",
        // Semantic (health), separate from the accent
        good: "#2F674F",
        warn: "#B07A1E",
      },
      fontFamily: {
        sans: ["var(--font-lexend)", "Verdana", "sans-serif"],
      },
      borderRadius: {
        none: "0",
        sm: "0.125rem",
        DEFAULT: "0.125rem",
        md: "0.25rem",
        lg: "0.25rem",
        xl: "0.5rem",
        "2xl": "0.5rem",
        full: "0.75rem",
        pill: "9999px",
      },
      spacing: {
        "margin-desktop": "48px",
        gutter: "24px",
      },
      fontSize: {
        "display-lg": ["48px", { lineHeight: "56px", letterSpacing: "-0.02em", fontWeight: "300" }],
        "headline-lg": ["36px", { lineHeight: "44px", letterSpacing: "-0.01em", fontWeight: "300" }],
        "headline-md": ["28px", { lineHeight: "36px", fontWeight: "300" }],
        "body-lg": ["16px", { lineHeight: "24px", fontWeight: "300" }],
        "body-md": ["14px", { lineHeight: "20px", fontWeight: "300" }],
        "label-md": ["12px", { lineHeight: "16px", fontWeight: "400" }],
      },
      boxShadow: {
        premium: "0 4px 20px rgba(55, 55, 66, 0.03)",
      },
    },
  },
  plugins: [],
}

export default config
