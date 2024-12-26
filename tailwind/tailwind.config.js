/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../**/templates/**/*.html"],
  // darkMode: ['[data-theme="dark"]', "media", "selector"],
  theme: {
    extend: {
      colors: {
        "primary": "var(--primary)",
        "secondary": "var(--secondary)",
        "accent": "var(--accent)",
        "neutral": "var(--neutral)",
        "base-100": "var(--base-100)",
        "base-200": "var(--base-200)",
        "base-300": "var(--base-300)",
        backgroundColor: {

        }
      },
      typography: {
        DEFAULT: {
          css: {
            color: "#333",
            a: {
              color: "#1a73e8",
              "&:hover": {
                color: "#0c47a1",
              },
            },
            h1: {
              fontSize: "2.25rem", // 4xl
              fontWeight: "700", // bold
            },
            h2: {
              fontSize: "1.875rem", // 3xl
              fontWeight: "600", // semibold
            },
            h3: {
              fontSize: "1.5rem", // 2xl
              fontWeight: "600", // semibold
            },
            h4: {
              fontSize: "1.25rem", // xl
              fontWeight: "500", // medium
            },
            h5: {
              fontSize: "1.125rem", // lg
              fontWeight: "500", // medium
            },
            h6: {
              fontSize: "1rem", // base
              fontWeight: "500", // medium
            },
          },
        },
      },
    },
  },
  
  plugins: [
    require("daisyui"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
  ],
};
